# -*- coding: utf-8 -*-
"""
TTSProcessor 语音合成处理器模块
作者: 万物有灵团队
日期: 2025-05-20

本模块实现基于API的语音合成功能，支持请求准备、响应处理、音频保存等完整工作流。
"""
import requests
from pathlib import Path
from typing import Any, Dict

from config.interfaces.base import APIProcessor
from logger import tts_logger, log_function_call, log_error

class TTSProcessor(APIProcessor):
    """
    语音合成处理器，负责文本到语音的转换流程
    
    特性:
    - 支持自定义API配置
    - 自动处理请求/响应格式
    - 异常处理与日志记录
    """
    def __init__(self):
        """初始化TTS处理器实例，创建输出目录"""
        self.config = None
        self.initialized = False
        self.output_dir = Path('data/audio_processing/tts')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @log_function_call(tts_logger)
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        初始化TTS API配置
        
        参数:
            config (Dict[str, Any]): 包含API端点、请求头、默认参数的配置字典
        """
        try:
            self.config = config
            self.url = config['url']
            self.headers = config.get('headers', {})
            self.default_params = config.get('params', {})
            self.initialized = True
            tts_logger.info("TTS processor initialized successfully")
        except Exception as e:
            tts_logger.error(f"Failed to initialize TTS processor: {str(e)}")
            raise

    @log_function_call(tts_logger)
    def prepare_request(self, input_data: str) -> Dict[str, Any]:
        """
        构建API请求数据
        
        参数:
            input_data (str): 待合成的文本内容
        返回:
            Dict[str, Any]: 包含完整请求参数的字典
        """
        try:
            request_data = self.default_params.copy()
            request_data.update({'text': input_data})
            return request_data
        except Exception as e:
            tts_logger.error(f"Error preparing request data: {str(e)}")
            raise

    @log_error(tts_logger)
    def _save_audio_content(self, content: bytes, filename: str = 'tmp.wav') -> Path:
        """
        (内部方法)保存音频文件到指定目录
        
        参数:
            content (bytes): 音频二进制数据
            filename (str): 保存文件名，默认为tmp.wav
        返回:
            Path: 保存文件的绝对路径
        """
        output_path = self.output_dir / filename
        with open(output_path, 'wb') as f:
            f.write(content)
        tts_logger.debug(f"Audio saved to {output_path}")
        return output_path

    @log_function_call(tts_logger)
    def handle_response(self, response: requests.Response) -> Path:
        """
        处理API响应，保存有效音频数据
        
        参数:
            response (requests.Response): API响应对象
        返回:
            Path: 保存的音频文件路径
        异常:
            RuntimeError: 当API返回非200状态码时抛出
        """
        try:
            if response.status_code == 200:
                return self._save_audio_content(response.content)
            else:
                error_msg = f"API request failed with status code {response.status_code}"
                tts_logger.error(error_msg)
                try:
                    error_detail = response.json()
                    tts_logger.error(f"Error details: {error_detail}")
                except:
                    pass
                raise RuntimeError(error_msg)
        except Exception as e:
            tts_logger.error(f"Error handling API response: {str(e)}")
            raise

    @log_function_call(tts_logger)
    def handle_error(self, error: Exception) -> None:
        """处理错误"""
        try:
            tts_logger.error(f"TTS processing error: {str(error)}", exc_info=True)
            raise error
        except Exception as e:
            tts_logger.error(f"Error in handle_error: {str(e)}")
            raise

    @log_function_call(tts_logger)
    def process(self, input_text: str) -> Path:
        """
        完整文本转语音处理流程
        
        参数:
            input_text (str): 输入文本内容
        返回:
            Path: 生成的音频文件路径
        异常:
            RuntimeError: 处理器未初始化时抛出
            requests.RequestException: API请求失败时抛出
        """
        if not self.initialized:
            raise RuntimeError("TTS processor not initialized")

        try:
            request_data = self.prepare_request(input_text)
            tts_logger.debug(f"Sending request to TTS API: {self.url}")
            response = requests.post(self.url, json=request_data, headers=self.headers)
            return self.handle_response(response)

        except requests.RequestException as e:
            tts_logger.error(f"API request failed: {str(e)}")
            self.handle_error(e)
        except Exception as e:
            tts_logger.error(f"Unexpected error: {str(e)}")
            self.handle_error(e)

    @log_function_call(tts_logger)
    def cleanup(self) -> None:
        """清理资源"""
        try:
            # 清理临时文件等资源
            self.initialized = False
            tts_logger.info("TTS processor cleaned up successfully")
        except Exception as e:
            tts_logger.error(f"Error during cleanup: {str(e)}")
            raise