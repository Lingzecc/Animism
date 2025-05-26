# -*- coding: utf-8 -*-
"""
LLMProcessor 大语言模型处理器模块
作者: 万物有灵团队
日期: 2025-05-20

本模块实现基于HuggingFace Transformers的大语言模型处理功能，支持模型加载、文本生成、资源管理等。
"""
import torch
from typing import Any, Dict
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

from config.interfaces.base import ModelProcessor
from logger import llm_logger, log_function_call, log_error


class LLMProcessor(ModelProcessor):
    """
    大语言模型处理器，负责文本生成流程
    
    特性:
    - 支持HuggingFace模型加载
    - 提供对话模板初始化
    - 支持生成参数配置
    - 完善的资源管理
    """
    def __init__(self):
        """初始化LLM处理器实例，自动检测设备"""
        self.model = None
        self.tokenizer = None
        self.generator = None
        self.config = None
        self.initialized = False
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    @log_function_call(llm_logger)
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        初始化LLM处理器配置
        
        参数:
            config (Dict[str, Any]): 包含模型路径和生成参数的配置字典
        """
        try:
            self.config = config
            self.load_model(config['name'])
            self.generate_config = config.get('generate_config', {})
            self.initialized = True
            llm_logger.info("LLM processor initialized successfully")
        except Exception as e:
            llm_logger.error(f"Failed to initialize LLM processor: {str(e)}")
            raise

    @log_function_call(llm_logger)
    def load_model(self, model_path: str) -> None:
        """
        加载预训练模型和分词器
        
        参数:
            model_path (str): 模型本地路径或HuggingFace模型ID
        """
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.bfloat16,
                trust_remote_code=True,
                device_map=self.device
            )
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                trust_remote_code=True
            )
            llm_logger.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            llm_logger.error(f"Failed to load model from {model_path}: {str(e)}")
            raise

    @log_function_call(llm_logger)
    def save_model(self, save_path: str) -> None:
        """
        保存模型到指定路径
        
        参数:
            save_path (str): 模型保存路径
        """
        try:
            if self.model and self.tokenizer:
                self.model.save_pretrained(save_path)
                self.tokenizer.save_pretrained(save_path)
                llm_logger.info(f"Model saved successfully to {save_path}")
            else:
                raise RuntimeError("Model or tokenizer not initialized")
        except Exception as e:
            llm_logger.error(f"Failed to save model to {save_path}: {str(e)}")
            raise

    def _init_chat_template(self) -> tuple:
        """
        (内部方法)初始化对话模板
        
        返回:
            tuple: 包含系统、用户、机器人起始token的元组
        """
        sys_token_id = self.generate_config.get('sys_token_id', 0)
        user_token_id = self.generate_config.get('user_token_id', 3)
        bot_token_id = self.generate_config.get('bot_token_id', 4)

        system_start_ids = torch.tensor([[sys_token_id]], dtype=torch.int64, device=self.device)
        user_start_ids = torch.tensor([[user_token_id]], dtype=torch.int64, device=self.device)
        bot_start_ids = torch.tensor([[bot_token_id]], dtype=torch.int64, device=self.device)

        return system_start_ids, user_start_ids, bot_start_ids

    @log_error(llm_logger)
    def _prepare_system_ids(self, system_message: str, system_start_ids: torch.Tensor) -> torch.Tensor:
        """准备系统消息ID"""
        system_ids = self.tokenizer.encode(system_message, return_tensors="pt").to(self.device)
        if len(system_ids) == 0 or system_ids.shape[-1] == 0:
            llm_logger.warning("System message is empty")
            return torch.tensor([[]], dtype=torch.int64).to(self.device)
        return torch.concat([system_start_ids, system_ids], dim=-1).long()

    @log_function_call(llm_logger)
    def generate(self, input_data: Dict[str, Any], **kwargs) -> str:
        """
        生成文本回复
        
        参数:
            input_data (Dict[str, Any]): 包含系统消息和用户查询的字典
            **kwargs: 可覆盖默认生成参数
        返回:
            str: 生成的文本回复
        """
        try:
            system_message = input_data.get('system_message', '')
            query = input_data.get('query', '')
            
            system_start_ids, user_start_ids, bot_start_ids = self._init_chat_template()
            system_ids = self._prepare_system_ids(system_message, system_start_ids)
            
            inputs = self.tokenizer.encode(query, return_tensors="pt").to(self.device)
            inputs = torch.concat([system_ids, user_start_ids, inputs, bot_start_ids], dim=-1).long()

            generate_kwargs = {
                'max_new_tokens': self.generate_config.get('max_new', 300),
                'top_k': self.generate_config.get('top_k', 5),
                'top_p': self.generate_config.get('top_p', 0.8),
                'temperature': self.generate_config.get('temperature', 0.65),
                'repetition_penalty': self.generate_config.get('repetition_penalty', 1.1),
                'do_sample': self.generate_config.get('do_sample', True)
            }

            history_outputs = self.model.generate(inputs, **generate_kwargs)
            
            if history_outputs[0][-1] == 2:  # Remove </s> token
                history_outputs = history_outputs[:, :-1]
            
            outputs = self.tokenizer.decode(history_outputs[0][len(inputs[0]):])
            llm_logger.debug(f"Generated response: {outputs}")
            return outputs

        except Exception as e:
            llm_logger.error(f"Error generating response: {str(e)}")
            raise

    @log_function_call(llm_logger)
    def process(self, input_data: Any) -> str:
        """处理输入数据"""
        if not self.initialized:
            raise RuntimeError("LLM processor not initialized")
        return self.generate(input_data)

    @log_function_call(llm_logger)
    def cleanup(self) -> None:
        """清理资源"""
        try:
            if self.model:
                del self.model
            if self.tokenizer:
                del self.tokenizer
            if self.generator:
                del self.generator
            self.model = None
            self.tokenizer = None
            self.generator = None
            self.initialized = False
            torch.cuda.empty_cache()
            llm_logger.info("LLM processor cleaned up successfully")
        except Exception as e:
            llm_logger.error(f"Error during cleanup: {str(e)}")
            raise