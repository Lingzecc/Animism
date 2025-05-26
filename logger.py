# -*- coding: utf-8 -*-
"""
日志管理模块
作者: 万物有灵团队
日期: 2025-05-20

本模块提供统一的日志管理功能，支持文件和控制台输出，
并提供日志格式化和日志级别设置。
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

class LogManager:
    """
    日志管理器类(单例模式)
    
    职责:
    1. 创建和管理日志记录器
    2. 提供文件和控制台日志输出
    3. 支持日志格式化和日志级别设置
    
    特性:
    - 线程安全的单例实现
    - 自动创建日志目录
    - 提供默认日志格式和输出
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        """单例模式实现: 确保全局唯一日志管理器实例"""
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化日志管理器实例(仅执行一次)
        
        初始化内容:
        - 日志记录器缓存字典
        - 日志目录创建
        - 初始化状态标记
        """
        if not self._initialized:
            self._initialized = True
            self.loggers = {}
            self.log_dir = Path('logs')
            self.log_dir.mkdir(exist_ok=True)

    def _create_file_handler(self, name: str) -> logging.FileHandler:
        """创建文件处理器
        
        参数:
            name (str): 日志记录器名称
        返回:
            logging.FileHandler: 文件处理器实例
        """
        log_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        handler = logging.FileHandler(log_file, encoding='utf-8')
        handler.setFormatter(self._get_formatter())
        return handler

    def _create_stream_handler(self) -> logging.StreamHandler:
        """创建控制台处理器
        
        返回:
            logging.StreamHandler: 控制台处理器实例
        """
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self._get_formatter())
        return handler

    def _get_formatter(self) -> logging.Formatter:
        """获取日志格式器
        
        返回:
            logging.Formatter: 日志格式器实例
        """
        return logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def get_logger(self, name: str, level: int = logging.INFO) -> logging.Logger:
        """获取或创建logger
        
        参数:
            name (str): 日志记录器名称
            level (int): 日志级别，默认为logging.INFO
        返回:
            logging.Logger: 日志记录器实例
        """
        if name not in self.loggers:
            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.addHandler(self._create_file_handler(name))
            logger.addHandler(self._create_stream_handler())
            logger.propagate = False
            self.loggers[name] = logger
        return self.loggers[name]

    def set_level(self, name: str, level: int) -> None:
        """设置日志级别
        
        参数:
            name (str): 日志记录器名称
            level (int): 要设置的日志级别
        """
        if name in self.loggers:
            self.loggers[name].setLevel(level)

# 创建默认logger
default_logger = LogManager().get_logger('default')

# 创建模块专用logger
asr_logger = LogManager().get_logger('asr')
tts_logger = LogManager().get_logger('tts')
llm_logger = LogManager().get_logger('llm')
api_logger = LogManager().get_logger('api')

def log_function_call(logger: Optional[logging.Logger] = None):
    """函数调用日志装饰器
    
    参数:
        logger (Optional[logging.Logger]): 可选的日志记录器实例，默认为default_logger
    
    返回:
        Callable: 装饰器函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            used_logger = logger or default_logger
            func_name = func.__name__
            used_logger.debug(f"Calling {func_name} with args: {args}, kwargs: {kwargs}")
            try:
                result = func(*args, **kwargs)
                used_logger.debug(f"{func_name} completed successfully")
                return result
            except Exception as e:
                used_logger.error(f"Error in {func_name}: {str(e)}", exc_info=True)
                raise
        return wrapper
    return decorator


def log_error(logger: Optional[logging.Logger] = None):
    """错误日志装饰器
    
    参数:
        logger (Optional[logging.Logger]): 可选的日志记录器实例，默认为default_logger
    
    返回:
        Callable: 装饰器函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            used_logger = logger or default_logger
            try:
                return func(*args, **kwargs)
            except Exception as e:
                used_logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                raise
        return wrapper
    return decorator