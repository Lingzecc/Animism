from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains.llm import LLMChain
from langchain.llms.base import LLM
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel, pipeline
from transformers.generation.utils import GenerationMixin
from typing import List, Optional
from peft import PeftModel
import torch
from load_config import Load_Config
from optimum.intel import OVModelForCausalLM
import re
# 初始化参数
cfg = Load_Config()
config = cfg.get_config()
model_name_or_path = config['model_name_or_path']
model_cache_path = config['model_cache_path']
device = config['device']
fine_weight = config["finetune_weight_path"] + "epoch_2"
template_path = config["template"]

"""
继承langchain.LLM的自定义LLM模型类
"""
class ChatLLM(LLM):
    """
    继承langchain.LLM的自定义LLM模型类
    """
    tokenizer: object = None
    model: object = None

    def __init__(self):
        super().__init__()

    def _llm_type(self) -> str:
        return "chatglm2-6b-int4"

    def load_model(self, model_name_or_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
        # self.model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True, cache_dir='./cache').to(device).float().eval()
        # self.model = OVModelForCausalLM.from_pretrained(model_name_or_path, torch_dtype=torch.bfloat16, trust_remote_code=True, export=True, cache_dir='./cache').to(device).eval()
        self.model = AutoModelForCausalLM.from_pretrained(model_name_or_path, torch_dtype=torch.bfloat16, trust_remote_code=True, cache_dir='./cache').to(device).eval()
        
    def load_fine_model(self, model_name_or_path, fine_weight):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
        base_model = AutoModelForCausalLM.from_pretrained(model_name_or_path, torch_dtype=torch.bfloat16, trust_remote_code=True, cache_dir='./cache')
        lora_model = PeftModel.from_pretrained(base_model, fine_weight)
        self.model = lora_model.merge_and_unload()
        self.model = self.model.eval() # 开启评估模式

    def _call(self, prompt: str, history: List = [], stop: Optional[List[str]] = ["<|user|>"]):
        max_token: int = 8192
        do_sample: bool = True
        temperature: float = 0.9 # 用于调整随机程度的数字，小了模型输出结果尽可能一致，高了则更随机。
        top_p = 0.8 # 模型不断生成回复时，它有许多可选字词。top-p低了候选就多，高了候选就少。
        history: List = []
        has_search: bool = False
        
        # pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, max_length=max_token, temperature=temperature, top_p=top_p)
        # response = pipe(prompt)
        
        response, _ = self.model.chat(
            self.tokenizer,
            prompt,
            history=history,
            do_sample=do_sample,
            max_length=max_token,
            temperature=temperature,
        )
        return response


def get_template(template_path):
    with open(template_path, "r", encoding="UTF-8") as f:  # 打开文件
        system_template = f.read()
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)
    return prompt


llm = ChatLLM()
# llm.load_fine_model(model_name_or_path,fine_weight)
llm.load_model(model_name_or_path)
prompt = get_template(template_path)
memory = ConversationBufferMemory(memory_key="context")
# chain = LLMChain(llm=llm, prompt=prompt.nekomusume_prompt(),verbose=True,memory=memory)
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

# 对话测试
# for i in range(10):
#     ipt = input("我:")
#     response = chain.invoke(ipt)
#     question, context, text = response["question"], response["context"], response["text"]
#     print(text)

response = chain.invoke()
response_text = response["text"]