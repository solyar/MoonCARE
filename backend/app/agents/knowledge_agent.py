import json
import math
import os
from app.services.embedding_service import EmbeddingService
from app.agents.llm_service import LLMService


class KnowledgeAgent:
    def __init__(self):
        # __file__ = app/agents/knowledge_agent.py
        # dirname once = app/agents, dirname twice = app
        base_dir = os.path.dirname(os.path.dirname(__file__))
        index_path = os.path.join(base_dir, "data", "knowledge_embeddings.json")

        self.embedder = EmbeddingService()
        self.llm = LLMService()
        self._embedding_available = False

        try:
            with open(index_path, "r", encoding="utf-8") as f:
                self.knowledge = json.load(f)
            print(f"[KnowledgeAgent] 已加载向量知识库，共 {len(self.knowledge)} 条")
            # Test if embedding works
            try:
                self.embedder.embed("测试")
                self._embedding_available = True
                print("[KnowledgeAgent] 向量模型可用")
            except Exception as e:
                print(f"[KnowledgeAgent] 向量模型不可用，将使用关键词匹配: {e}")
        except Exception as e:
            print(f"[KnowledgeAgent] 加载向量知识库失败: {e}")
            self.knowledge = []

    def _keyword_match(self, message: str, top_k: int = 3):
        """关键词匹配作为embedding的降级方案"""
        scored = []
        message_lower = message.lower()

        for item in self.knowledge:
            score = 0.0
            # 关键词匹配得分
            for kw in item.get("keywords", []):
                if kw.lower() in message_lower:
                    score += 1.0
            # 标题/问题匹配
            if item.get("question", "").lower() in message_lower:
                score += 2.0
            if scored:
                scored.append((score, item))
            else:
                scored = [(score, item)]

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]

    def _cosine_similarity(self, a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot / (norm_a * norm_b)

    def _keyword_bonus(self, message, item):
        score = 0.0
        for kw in item.get("keywords", []):
            if kw.lower() in message.lower():
                score += 0.08
        return score

    def _retrieve_top_k(self, message: str, k: int = 3):
        if self._embedding_available:
            try:
                query_vector = self.embedder.embed(message)

                scored = []
                for item in self.knowledge:
                    sim = self._cosine_similarity(query_vector, item["embedding"])
                    sim += self._keyword_bonus(message, item)
                    scored.append((sim, item))

                scored.sort(key=lambda x: x[0], reverse=True)
                return scored[:k]
            except Exception as e:
                print(f"[KnowledgeAgent] Embedding失败，使用关键词匹配: {e}")

        # 降级：使用关键词匹配
        return self._keyword_match(message, k)

    def _answer_from_knowledge(self, top_k, message):
        """基于检索到的知识回答"""
        references = []
        for idx, (_, item) in enumerate(top_k, start=1):
            references.append(
                f"参考资料{idx}：\n问题：{item['question']}\n答案：{item['answer']}"
            )

        reference_text = "\n\n".join(references)

        system_prompt = """
你是"她语 MoonCARE"的经期知识科普助手。
请基于给定的参考资料回答用户问题。

要求：
1. 回答自然、温柔、可信，不要机械照搬原文。
2. 优先基于参考资料，不要胡乱扩展。
3. 不要做明确医疗诊断。
4. 尽量控制在180字以内。
5. 如果问题和参考资料关系不大，就温和地给一个通用解释。
"""

        user_prompt = f"""
用户问题：
{message}

参考资料：
{reference_text}
"""

        return self.llm.generate_reply(user_prompt, {"mode": "knowledge_rag", "raw_system_prompt": system_prompt})

    def _answer_from_llm(self, message):
        """知识库不可用时，直接用模型能力回答"""
        system_prompt = """
你是"她语 MoonCARE"的经期知识科普助手。
你可以温柔地回答用户关于经期、PMS（经前综合征）、月经周期等相关问题。

要求：
1. 回答自然、温柔、可信，像朋友聊天一样。
2. 尽量控制在150字以内。
3. 不要做明确医疗诊断。
4. 如果不确定，建议用户咨询医生。
"""

        user_prompt = f"用户问题：{message}"

        try:
            return self.llm.generate_reply(user_prompt, {"mode": "knowledge_fallback", "raw_system_prompt": system_prompt})
        except Exception as e:
            print(f"[KnowledgeAgent] LLM回答失败: {e}")
            return "我现在有点状况，可能需要稍后再试~"

    def respond(self, message: str, state: dict = None) -> str:
        # 知识库完全没加载成功
        if not self.knowledge:
            return self._answer_from_llm(message)

        top_k = self._retrieve_top_k(message, k=3)

        # 知识库检索有效且有结果
        if top_k and top_k[0][0] > 0:
            best_score = top_k[0][0]
            threshold = 0.4 if self._embedding_available else 0.5
            if best_score >= threshold:
                try:
                    return self._answer_from_knowledge(top_k, message)
                except Exception:
                    pass

        # 知识库检索失败或分数低，直接用模型能力回答
        return self._answer_from_llm(message)