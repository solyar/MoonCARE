# HealthAI - 智能情绪管理平台

基于PRD文档第4部分"功能需求详述"生成的核心模块源代码。

## 技术栈

- **前端**: Vue 3 + Vite + Pinia + Vue Router + TailwindCSS
- **后端**: Python FastAPI + SQLAlchemy + PostgreSQL

## 项目结构

```
healthAI/
├── backend/                    # Python FastAPI 后端
│   ├── app/
│   │   ├── main.py            # FastAPI 应用入口
│   │   ├── config.py          # 配置管理
│   │   ├── database.py         # 数据库连接
│   │   ├── models/            # SQLAlchemy 模型
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── api/v1/            # API 路由
│   │   └── services/          # 业务逻辑服务
│   ├── requirements.txt
│   └── run.py
├── frontend/                   # Vue 3 前端
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   ├── stores/            # Pinia 状态管理
│   │   ├── api/               # API 调用
│   │   └── router/            # 路由配置
│   ├── package.json
│   └── vite.config.js
└── SPEC.md
```

## 核心功能模块

### 数据输入层

| 功能 | 描述 |
|------|------|
| F-002 | 用户主动输入 - 月经记录、症状录入、情绪日记 |
| F-003 | AI对话筛查 - 语音转文字 + NLP情绪分析 |

### 核心处理层

| 功能 | 描述 |
|------|------|
| F-004 | 情绪分析引擎 - 综合分析 + PMS风险预测 |

### 服务输出层

| 功能 | 描述 |
|------|------|
| F-005 | 陪伴Agent - 聊天共情AI |
| F-008 | 呼吸引导 - 呼吸训练引导 |
| F-009 | 情绪日记 - 语音日记 + 趋势展示 |
| F-012/F-013 | 经期记录 + 预测 |

## API 端点

### 生理数据
- `POST /api/v1/biometric/upload` - 上传生理数据
- `GET /api/v1/biometric/query` - 查询生理数据

### 情绪分析
- `GET /api/v1/emotion/predict` - 获取情绪预测
- `GET /api/v1/emotion/phase` - 获取当前周期阶段
- `GET /api/v1/emotion/intervention/recommend` - 获取干预建议

### 月经周期
- `POST /api/v1/menstrual/record` - 记录月经
- `GET /api/v1/menstrual/records` - 获取记录历史
- `GET /api/v1/menstrual/predict` - 周期预测

### 情绪日记
- `POST /api/v1/diary` - 创建日记
- `GET /api/v1/diary` - 获取日记列表
- `PUT /api/v1/diary/{id}` - 更新日记

### AI对话
- `WebSocket /api/v1/chat/ws/{user_id}` - 实时对话
- `GET /api/v1/chat/history/{session_id}` - 获取对话历史

## 启动方式

### 后端
```bash
cd backend
pip install -r requirements.txt
python run.py
# 访问 http://localhost:8000/docs 查看API文档
```

### 前端
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:3000
```

## 关键算法

### PMS风险计算 (F-004)
- 输入: HRV均值、皮肤温度变化斜率、情绪关键词密度、对话负向情绪占比
- 输出: 风险值 0.0-1.0，≥0.7 为高风险

### 周期预测 (F-013)
- 方法: 加权移动平均法，近期周期权重更高
- 要求: 至少2个历史周期记录
- 误差范围: ±2天

## 数据库模型

- `User` - 用户信息
- `BiometricData` - 生理数据 (心率、HRV、皮肤温度)
- `MenstrualRecord` - 月经记录
- `MoodDiary` - 情绪日记
- `Conversation` - AI对话记录
