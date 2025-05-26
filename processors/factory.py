# -*- coding: utf-8 -*-
"""
Factory处理器工厂模块
作者: 万物有灵团队
日期: 2025-05-20
功能: 实现处理器工厂模式，统一管理ASR/TTS/LLM处理器的创建和生命周期
"""

from typing import Dict, Any

from config.config_manager import ConfigManager
from processors.asr_processor import ASRProcessor
from processors.tts_processor import TTSProcessor
from processors.llm_processor import LLMProcessor
from processors.silicon_flow_processor import SiliconFlowProcessor
from logger import default_logger, log_function_call

class ProcessorFactory:
    """
    处理器工厂类(单例模式)
    
    职责:
    1. 统一创建和管理ASR/TTS/LLM处理器实例
    2. 确保处理器配置正确初始化
    3. 提供处理器实例的全局访问点
    4. 管理处理器的生命周期和资源清理
    
    特性:
    - 线程安全的单例实现
    - 延迟初始化处理器实例
    - 自动注入配置管理器
    - 集成日志记录功能
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        """单例模式实现: 确保全局唯一工厂实例"""
        if cls._instance is None:
            cls._instance = super(ProcessorFactory, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化工厂实例(仅执行一次)
        
        初始化内容:
        - 配置管理器实例
        - 处理器实例缓存字典
        - 初始化状态标记
        """
        if not self._initialized:
            self._initialized = True
            self.config_manager = ConfigManager()  # 配置管理依赖注入
            self.processors: Dict[str, Any] = {}   # 处理器实例缓存
            default_logger.info("ProcessorFactory initialized")

    @log_function_call(default_logger)
    def get_asr_processor(self) -> ASRProcessor:
        """获取ASR语音识别处理器实例
        
        返回:
            ASRProcessor: 初始化的ASR处理器实例
            
        注意:
        - 如果实例不存在会自动创建并初始化
        - 使用配置管理器的get_asr_config获取配置
        """
        if 'asr' not in self.processors:
            processor = ASRProcessor()
            processor.initialize(self.config_manager.get_asr_config())
            self.processors['asr'] = processor
            default_logger.info("Created new ASR processor")
        return self.processors['asr']

    @log_function_call(default_logger)
    def get_tts_processor(self) -> TTSProcessor:
        """获取TTS语音合成处理器实例
        
        返回:
            TTSProcessor: 初始化的TTS处理器实例
            
        注意:
        - 如果实例不存在会自动创建并初始化
        - 使用配置管理器的get_tts_config获取配置
        """
        if 'tts' not in self.processors:
            processor = TTSProcessor()
            processor.initialize(self.config_manager.get_tts_config())
            self.processors['tts'] = processor
            default_logger.info("Created new TTS processor")
        return self.processors['tts']

    @log_function_call(default_logger)
    def get_llm_processor(self) -> LLMProcessor:
        """获取LLM大语言模型处理器实例
        
        返回:
            LLMProcessor: 初始化的LLM处理器实例
            
        注意:
        - 如果实例不存在会自动创建并初始化
        - 使用配置管理器的get_model_config获取配置
        """
        if 'llm' not in self.processors:
            processor = LLMProcessor()
            processor.initialize(self.config_manager.get_model_config())
            self.processors['llm'] = processor
            default_logger.info("Created new LLM processor")
        return self.processors['llm']

    @log_function_call(default_logger)
    def cleanup_processor(self, processor_type: str) -> None:
        """清理指定类型的处理器资源
        
        参数:
            processor_type (str): 处理器类型('asr'/'tts'/'llm')
            
        异常:
            Exception: 清理过程中出现的任何错误都会记录并重新抛出
        """
        if processor_type in self.processors:
            try:
                self.processors[processor_type].cleanup()
                del self.processors[processor_type]
                default_logger.info(f"Cleaned up {processor_type} processor")
            except Exception as e:
                default_logger.error(f"Error cleaning up {processor_type} processor: {str(e)}")
                raise

    @log_function_call(default_logger)
    def get_silicon_flow_processor(self) -> SiliconFlowProcessor:
        """获取硅基流动大模型处理器实例
        
        返回:
            SiliconFlowProcessor: 初始化的硅基流动处理器实例
            
        注意:
        - 如果实例不存在会自动创建并初始化
        - 使用配置管理器的get_silicon_flow_config获取配置
        """
        if 'silicon_flow' not in self.processors:
            processor = SiliconFlowProcessor()
            processor.initialize(self.config_manager.get_silicon_flow_config())
            self.processors['silicon_flow'] = processor
            default_logger.info("Created new Silicon Flow processor")
        return self.processors['silicon_flow']

    @log_function_call(default_logger)
    def cleanup_all(self) -> None:
        """清理所有处理器资源
        
        注意:
        - 会依次调用各处理器的cleanup方法
        - 清理顺序不保证
        - 任何处理器清理失败不会中断其他处理器清理
        """
        for processor_type in list(self.processors.keys()):
            self.cleanup_processor(processor_type)
        default_logger.info("All processors cleaned up")

# 全局处理器工厂实例(单例)
processor_factory = ProcessorFactory()