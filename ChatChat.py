import json
from langchain.llms.base import LLM
from transformers import AutoTokenizer, AutoModel, AutoConfig, AutoModelForCausalLM
from typing import List, Optional
from langchain.prompts import ChatPromptTemplate
"""
继承langchain.LLM的自定义LLM模型类
"""
class ChatChat(LLM):
    """
    继承langchain.LLM的自定义LLM模型类
    """
    max_token: int = 10000
    do_sample: bool = True
    temperature: float = 0.1
    top_p = 0.8
    tokenizer: object = None
    model: object = None
    history: List = []
    has_search: bool = False

    def __init__(self):
        super().__init__()

    def _llm_type(self) -> str:
        return "MiniCPM-2B"

    def load_model(self, model_name_or_path=None):
        model_config = AutoConfig.from_pretrained(
            model_name_or_path,
            trust_remote_code=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name_or_path,
            trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path, config=model_config, trust_remote_code=True, device_map="cpu").eval().float()


    def _call(self, prompt: str, history: List = [], stop: Optional[List[str]] = ["<|user|>"]):
        response, _ = self.model.chat(
            self.tokenizer,
            prompt,
            history=self.history,
            do_sample=self.do_sample,
            max_length=self.max_token,
            temperature=self.temperature,
        )
        print('='*(len(response)+3)*2)
        print(f"回答：{response}")
        print('='*(len(response)+3)*2)
    