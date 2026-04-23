try:
    from app.agents.support_agent import SupportAgent
    from app.agents.knowledge_agent import KnowledgeAgent
    from app.agents.intervention_agent import InterventionAgent
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    SupportAgent = None
    KnowledgeAgent = None
    InterventionAgent = None

class Router:
    def __init__(self):
        self._support = None
        self._knowledge = None
        self._intervention = None

    @property
    def support(self):
        if self._support is None:
            self._support = SupportAgent()
        return self._support

    @property
    def knowledge(self):
        if self._knowledge is None:
            try:
                self._knowledge = KnowledgeAgent()
            except Exception as e:
                print(f"[Router] Failed to initialize KnowledgeAgent: {e}")
                self._knowledge = None
        return self._knowledge

    @property
    def intervention(self):
        if self._intervention is None:
            try:
                self._intervention = InterventionAgent()
            except Exception as e:
                print(f"[Router] Failed to initialize InterventionAgent: {e}")
                self._intervention = None
        return self._intervention

    def route(self, message: str, state: dict):
        message = message or ""
        risk_level = state.get("risk_level", "low")

        # 1. 高风险 / 危机优先
        if risk_level in ["high", "crisis"]:
            if self.intervention is None:
                return "我现在有点状况，可能需要稍后再试~", "error"
            try:
                reply = self.intervention.respond(message, state)
                return reply, "intervention"
            except Exception as e:
                print(f"[Router] InterventionAgent error: {e}")
                return "我现在有点状况，可能需要稍后再试~", "error"

        # 2. 科普问题走 knowledge
        knowledge_keywords = [
            "什么是", "为什么", "正常吗", "是不是", "会不会",
            "PMS", "pms", "经前综合征", "月经前", "经期前"
        ]
        if any(k in message for k in knowledge_keywords):
            if self.knowledge is not None:
                try:
                    reply = self.knowledge.respond(message, state)
                    return reply, "knowledge"
                except Exception as e:
                    print(f"[Router] KnowledgeAgent error: {e}")

            # Knowledge agent not available or failed, fall back to support
            pass

        # 3. 默认走陪伴
        try:
            reply = self.support.respond(message, state)
            return reply, "support"
        except Exception as e:
            print(f"[Router] SupportAgent error: {e}")
            return "我现在有点状况，可能需要稍后再试~", "error"