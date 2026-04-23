"""
Agent服务 - 委托给新的 Agent 系统
"""
import traceback
from typing import Dict, List
from datetime import datetime
from app.config import settings

from app.agents.router import Router
from app.agents.perception_agent import PerceptionAgent


class AgentService:
    """
    Agent 服务 - 使用新的多 Agent 系统
    """

    def __init__(self):
        self.context_window = settings.CONTEXT_WINDOW_SIZE  # 10轮对话
        self.conversation_histories: Dict[str, List[Dict]] = {}
        self.router = None  # Lazy init
        self.perception = None  # Lazy init

    def _get_router(self):
        if self.router is None:
            self.router = Router()
        return self.router

    def _get_perception(self):
        if self.perception is None:
            self.perception = PerceptionAgent()
        return self.perception

    async def get_response(
        self,
        user_id: int,
        session_id: str,
        user_message: str,
        context: Dict
    ) -> Dict:
        """
        获取AI响应
        使用新的 Agent 路由系统
        """
        try:
            cycle_phase = context.get("cycle_phase")
            sensor_data = context.get("sensor_data", {})

            # 1. PerceptionAgent 分析风险等级
            perception = self._get_perception()
            state = perception.analyze(
                message=user_message,
                cycle_phase=cycle_phase,
                sensor_data=sensor_data
            )

            # 2. Router 路由到对应 Agent
            router = self._get_router()
            reply, agent_name = router.route(user_message, state)

        except Exception as e:
            print(f"[AgentService] Error in routing: {e}")
            traceback.print_exc()
            # 后备回复
            reply = "我现在有点状况，可能需要稍后再试~"
            agent_name = "error"
            state = {"risk_level": "low", "cycle_phase": "未知"}

        # 保存对话历史
        if session_id not in self.conversation_histories:
            self.conversation_histories[session_id] = []

        self.conversation_histories[session_id].append({
            "role": "user",
            "content": user_message,
            "emotion": state.get("risk_level", "low"),
            "timestamp": datetime.now().isoformat()
        })

        self.conversation_histories[session_id].append({
            "role": "assistant",
            "content": reply,
            "agent": agent_name,
            "timestamp": datetime.now().isoformat()
        })

        # 保留最近的上下文
        if len(self.conversation_histories[session_id]) > self.context_window * 2:
            self.conversation_histories[session_id] = \
                self.conversation_histories[session_id][-self.context_window * 2:]

        return {
            "message": reply,
            "intent": agent_name,
            "emotion_detected": state.get("risk_level", "low"),
            "suggestions": [],
            "state": state
        }

    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """获取对话历史"""
        return self.conversation_histories.get(session_id, [])

    def clear_history(self, session_id: str):
        """清除对话历史"""
        if session_id in self.conversation_histories:
            del self.conversation_histories[session_id]