from openai import OpenAI

class KnowledgeBase:
    def __init__(self, api_key: str, base_url: str = "https://api.chatanywhere.tech/v1"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
    
    def gpt_35_api(self, question):
        messages = [{'role': 'user','content': question}]
        completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        return completion.choices[0].message.content

    def get_answer(self, question: str) -> str:
        # 非流式获取答案
        return self.gpt_35_api(question)
