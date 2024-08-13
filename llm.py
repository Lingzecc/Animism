from langchain.memory import ConversationBufferMemory
from Templates import *
from langchain.chains.llm import LLMChain
from langchain.llms.base import LLM
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
from typing import List, Optional
from peft import PeftModel
import torch
import json
import os
class Load_Config:
    def __init__(self,dir_path_or_name="",file_path_or_name="config.json"):
        # 基础配置
        self.dir_path_or_name = dir_path_or_name
        self.file_path_or_name = file_path_or_name
        self.config_path = os.path.join(self.dir_path_or_name, self.file_path_or_name) # json地址
        
        
    # 读取config.json文件
    def get_config(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config
    # 更新参数
    def set_config(self, **kwargs):
        data = self.get_config()
        for key, value in kwargs.items():
            data[key] = value
            with open(self.config_path, 'w') as f:
                json.dump(data, f)
                print(f"已添加到{self.config_path}\n内容：Key: {key}, Value: {value}")
    # 删除
    def del_config(self,key):
        data = self.get_config()
        del data[key]
        with open(self.config_path, 'w') as f:
                json.dump(data, f)
                print(f"从{self.config_path}处:\n内容:{key}已删除")
        
"""
继承langchain.LLM的自定义LLM模型类
"""
class ChatLLM(LLM):
    """
    继承langchain.LLM的自定义LLM模型类
    """
    max_token: int = 10000
    do_sample: bool = True
    temperature: float = 0.1
    top_p = 0.9
    tokenizer: object = None
    model: object = None
    history: List = []
    has_search: bool = False

    def __init__(self):
        super().__init__()

    def _llm_type(self) -> str:
        return "chatglm2-6b-int4"

    def load_model(self, model_name_or_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
        # self.model = AutoModel.from_pretrained(
        #     model_name_or_path, trust_remote_code=True, device_map="cpu",).float().eval()
        self.model = AutoModelForCausalLM.from_pretrained(model_name_or_path, torch_dtype=torch.bfloat16, trust_remote_code=True)
        
    def load_fine_model(self, model_name_or_path, fine_weight):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
        base_model = AutoModelForCausalLM.from_pretrained(model_name_or_path, torch_dtype=torch.bfloat16, trust_remote_code=True)
        lora_model = PeftModel.from_pretrained(base_model, fine_weight)
        self.model = lora_model.merge_and_unload()
        self.model = self.model.eval() # 开启评估模式
        


    def _call(self, prompt: str, history: List = [], stop: Optional[List[str]] = ["<|user|>"]):
        response, _ = self.model.chat(
            self.tokenizer,
            prompt,
            history=self.history,
            do_sample=self.do_sample,
            max_length=self.max_token,
            temperature=self.temperature,
        )
        return response
    
    

# 初始化参数
cfg = Load_Config()
config = cfg.get_config()
tokenizer_name_or_path = config['tokenizer_name_or_path']
model_name_or_path = config['model_name_or_path']
model_cache_path = config['model_cache_path']
device = config['device']
fine_weight = config["finetune_weight_path"] + "epoch_2"


llm = ChatLLM()
# llm.load_fine_model(model_name_or_path,fine_weight)
llm.load_model(model_name_or_path)
prompt = Templates()
memory = ConversationBufferMemory(memory_key="context")
# chain = LLMChain(llm=llm, prompt=prompt.nekomusume_prompt(),verbose=True,memory=memory)
chain = LLMChain(llm=llm, prompt=prompt(),verbose=True,memory=memory)
response = chain.invoke("你好(摸摸头)")
print(response.content)