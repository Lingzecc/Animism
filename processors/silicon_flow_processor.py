# -*- coding: utf-8 -*-
"""
SiliconFlowProcessor 硅基流动大模型处理器模块
作者: 万物有灵团队
日期: 2025-05-25

本模块实现基于硅基流动API的大语言模型处理功能，支持API调用、文本生成、资源管理等。
"""
import json
import requests
from typing import Any, Dict

from config.interfaces.base import ModelProcessor
from logger import llm_logger, log_function_call


class SiliconFlowProcessor(ModelProcessor):
    """
    硅基流动大模型处理器，负责API调用和文本生成流程
    
    特性:
    - 支持硅基流动API调用
    - 提供对话模板初始化
    - 支持生成参数配置
    - 完善的错误处理和重试机制
    """
    def __init__(self):
        """初始化硅基流动处理器实例"""
        self.api_url = None
        self.api_key = None
        self.model_name = None
        self.headers = None
        self.generate_config = None
        self.initialized = False

    @log_function_call(llm_logger)
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        初始化硅基流动处理器配置
        
        参数:
            config (Dict[str, Any]): 包含API配置和生成参数的配置字典
        """
        try:
            self.api_url = config.get('api_url')
            self.api_key = config.get('api_key')
            self.model_name = config.get('model_name')
            
            if not self.api_url or not self.api_key or not self.model_name:
                raise ValueError("API URL, API Key and Model Name must be provided")
            
            self.headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            self.generate_config = config.get('generate_config', {})
            self.initialized = True
            llm_logger.info("Silicon Flow processor initialized successfully")
        except Exception as e:
            llm_logger.error(f"Failed to initialize Silicon Flow processor: {str(e)}")
            raise

    @log_function_call(llm_logger)
    def load_model(self, model_path: str) -> None:
        """
        设置模型名称（API模式下不需要实际加载模型）
        
        参数:
            model_path (str): 模型名称或标识符
        """
        try:
            self.model_name = model_path
            llm_logger.info(f"Model set to {model_path}")
        except Exception as e:
            llm_logger.error(f"Failed to set model to {model_path}: {str(e)}")
            raise

    @log_function_call(llm_logger)
    def save_model(self, save_path: str) -> None:
        """
        保存模型配置（API模式下不需要实际保存模型）
        
        参数:
            save_path (str): 配置保存路径
        """
        try:
            # 在API模式下，我们只需保存配置信息
            config = {
                'model_name': self.model_name,
                'api_url': self.api_url,
                'generate_config': self.generate_config
            }
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
            llm_logger.info(f"Model configuration saved to {save_path}")
        except Exception as e:
            llm_logger.error(f"Failed to save model configuration to {save_path}: {str(e)}")
            raise

    @log_function_call(llm_logger)
    def generate(self, input_data: Dict[str, Any], **kwargs) -> str:
        """
        通过API生成文本回复
        
        参数:
            input_data (Dict[str, Any]): 包含系统消息和用户查询的字典
            **kwargs: 可覆盖默认生成参数
        返回:
            str: 生成的文本回复
        """
        try:
            system_message = input_data.get('system_message', '')
            query = input_data.get('query', '')
            
            # 准备请求数据
            payload = {
                'model': self.model_name,
                'messages': [
                    {'role': 'system', 'content': system_message},
                    {'role': 'user', 'content': query}
                ],
                'stream': False,
                'max_tokens': kwargs.get('max_tokens', self.generate_config.get('max_tokens', 512)),
                'enable_thinking': kwargs.get('enable_thinking', self.generate_config.get('enable_thinking', False)),
                'thinking_budget': kwargs.get('thinking_budget', self.generate_config.get('thinking_budget', 4096)),
                'min_p': kwargs.get('min_p', self.generate_config.get('min_p', 0.05)),
                'stop': None,
                'temperature': kwargs.get('temperature', self.generate_config.get('temperature', 0.7)),
                'top_p': kwargs.get('top_p', self.generate_config.get('top_p', 0.7)),
                'top_k': kwargs.get('top_k', self.generate_config.get('top_k', 50)),
                'frequency_penalty': kwargs.get('frequency_penalty', self.generate_config.get('frequency_penalty', 0.5)),
                'n': 1,
                'response_format': {"type": "text"}
            }
            
            # 发送API请求
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            if 'error' in result:
                raise ValueError(f"API Error: {result['error']}")
                
            output = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            llm_logger.debug(f"Generated response: {output}")
            return output
            
        except requests.exceptions.RequestException as e:
            llm_logger.error(f"API request error: {str(e)}")
            raise
        except Exception as e:
            llm_logger.error(f"Error generating response: {str(e)}")
            raise

    @log_function_call(llm_logger)
    def process(self, input_data: Any) -> str:
        """处理输入数据"""
        if not self.initialized:
            raise RuntimeError("Silicon Flow processor not initialized")
        return self.generate(input_data)

    @log_function_call(llm_logger)
    def cleanup(self) -> None:
        """清理资源"""
        try:
            # API模式下不需要特别的资源清理
            self.initialized = False
            llm_logger.info("Silicon Flow processor cleaned up successfully")
        except Exception as e:
            llm_logger.error(f"Error during cleanup: {str(e)}")
            raise