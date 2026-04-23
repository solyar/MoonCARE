class PerceptionAgent:
    def analyze(self, message: str, cycle_phase: str = None, sensor_data: dict = None) -> dict:
        sensor_data = sensor_data or {}
        text = (message or "").lower()

        risk_level = "low"

        crisis_keywords = [
            "不想活", "想死", "自杀", "结束生命", "活不下去"
        ]
        high_keywords = [
            "没有意义", "撑不住了", "想消失", "我真的不行了", "崩溃到不行"
        ]
        medium_keywords = [
            "烦躁", "难受", "想哭", "崩溃", "焦虑", "累", "低落", "敏感"
        ]

        if any(kw in text for kw in crisis_keywords):
            risk_level = "crisis"
        elif any(kw in text for kw in high_keywords):
            risk_level = "high"
        elif any(kw in text for kw in medium_keywords):
            risk_level = "medium"

        return {
            "risk_level": risk_level,
            "cycle_phase": cycle_phase or "经前期",
            "sensor_data": sensor_data,
            "emotion_summary": message,
        }