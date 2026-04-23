from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from datetime import datetime, timedelta
from pydantic import BaseModel
import random
import json

from app.database import get_db
from app.models.biometric import BiometricData
from app.schemas.biometric import BiometricUpload, BiometricResponse, BiometricDataPoint
from app.services.emotion_engine import EmotionEngine

router = APIRouter(prefix="/biometric", tags=["生理数据"])


class RawBiometricUpload(BaseModel):
    """原始硬件数据格式 - 允许部分字段缺失"""
    temp: Optional[float] = None
    bpm: Optional[float] = None
    motion: Optional[str] = None
    wearing: Optional[bool] = None


@router.post("/upload", response_model=BiometricResponse)
async def upload_biometric_data(
    data: BiometricUpload,
    db: Session = Depends(get_db)
):
    """
    上传生理数据（温度、心率、运动状态）
    触发条件：耳挂设备采集到数据后上传
    前置条件：蓝牙连接成功
    注意：只有 confidence == "HIGH" 时才写入数据库
    """
    try:
        # Check confidence - if LOW, skip writing to database
        confidence = (data.confidence or "HIGH").upper()
        if confidence == "LOW":
            return BiometricResponse(
                status="skipped",
                msg="Confidence LOW, not stored",
                data_id=None
            )

        # Use current time if timestamp not provided by hardware
        timestamp = data.timestamp or datetime.now()

        # Create biometric record
        # Note: In production, user_id should come from authentication
        biometric = BiometricData(
            user_id=1,  # TODO: Get from auth context
            device_id=data.device_id,
            timestamp=timestamp,
            hrv=data.bpm,  # hardware bpm -> stored as hrv
            skin_temperature=data.temp,
            motion=data.motion,
            is_valid=1
        )

        db.add(biometric)
        db.commit()
        db.refresh(biometric)

        return BiometricResponse(
            status="success",
            msg="Data received",
            data_id=biometric.id
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/query", response_model=List[BiometricDataPoint])
async def query_biometric_data(
    user_id: int,
    start_date: datetime = None,
    end_date: datetime = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """查询用户的生理数据历史"""
    query = db.query(BiometricData).filter(BiometricData.user_id == user_id)

    if start_date:
        query = query.filter(BiometricData.timestamp >= start_date)
    if end_date:
        query = query.filter(BiometricData.timestamp <= end_date)

    query = query.order_by(BiometricData.timestamp.desc()).limit(limit)

    return query.all()


@router.get("/latest")
async def get_latest_biometric(
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取最新一条生理数据"""
    latest = db.query(BiometricData).filter(
        BiometricData.user_id == user_id
    ).order_by(BiometricData.timestamp.desc()).first()

    if not latest:
        return None

    return {
        "timestamp": latest.timestamp,
        "hrv": latest.hrv,
        "skin_temperature": latest.skin_temperature,
        "motion": latest.motion
    }


@router.post("/seed")
async def seed_mock_data(
    user_id: int = 1,
    count: int = 50,
    db: Session = Depends(get_db)
):
    """
    生成模拟生理数据用于测试
    生成指定数量的模拟数据点，时间间隔均匀分布
    """
    now = datetime.now()
    motions = ["LOW", "MEDIUM", "HIGH"]

    for i in range(count):
        # 模拟数据，略带随机波动
        biometric = BiometricData(
            user_id=user_id,
            device_id="MOCK_DEVICE",
            timestamp=now - timedelta(seconds=count - i),
            hrv=random.uniform(60, 90),  # 心率 60-90 BPM
            skin_temperature=random.uniform(35.5, 37.0),  # 体温 35.5-37.0°C
            motion=random.choice(motions),
            is_valid=1
        )
        db.add(biometric)

    db.commit()

    return {
        "status": "success",
        "msg": f"已生成 {count} 条模拟数据",
        "count": count
    }


@router.post("/raw")
async def upload_raw_biometric_data(
    data: RawBiometricUpload,
    user_id: int = 1,
    device_id: str = "DEVICE_001",
    db: Session = Depends(get_db)
):
    """
    接收原始硬件数据（通过USB/蓝牙网关转发）
    硬件数据格式: {"temp":24.2,"bpm":94.5,"motion":"LOW","wearing":false}
    """
    try:
        biometric = BiometricData(
            user_id=user_id,
            device_id=device_id,
            timestamp=datetime.now(),
            hrv=data.bpm,
            skin_temperature=data.temp,
            motion=data.motion,
            is_valid=1
        )

        db.add(biometric)
        db.commit()
        db.refresh(biometric)

        return {
            "status": "success",
            "data_id": biometric.id
        }
    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "msg": str(e)
        }
