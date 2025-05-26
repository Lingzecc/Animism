# -*- coding: utf-8 -*-
"""
硅基流动大模型示例脚本
作者: 万物有灵团队
日期: 2025-05-25

本脚本演示如何使用硅基流动大模型处理器进行文本生成。
"""

import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processors.factory import processor_factory
from config.config_manager import ConfigManager
from logger import default_logger


def load_template(template_path):
    """加载模板文件内容"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        default_logger.error(f"加载模板文件失败: {str(e)}")
        return "你是一个友好、专业的AI助手，擅长回答用户的各种问题。"


def main():
    # 初始化配置管理器
    config_manager = ConfigManager()
    
    # 获取模板配置
    template_config = config_manager.get_template_config()
    template_path = template_config.get('path', 'templates/allium.txt')
    system_message = load_template(template_path)
    
    # 获取硅基流动处理器实例
    try:
        processor = processor_factory.get_silicon_flow_processor()
        default_logger.info("成功初始化硅基流动处理器")
        
        # 准备输入数据
        input_data = {
            'system_message': system_message,
            'query': '请介绍一下硅基流动技术的发展历程和应用前景。'
        }
        
        # 生成回复
        default_logger.info("开始生成回复...")
        response = processor.process(input_data)
        
        # 打印结果
        print("\n===== 硅基流动大模型回复 =====")
        print(response)
        print("===========================\n")
        
        # 清理资源
        processor_factory.cleanup_processor('silicon_flow')
        default_logger.info("资源已清理")
        
    except Exception as e:
        default_logger.error(f"发生错误: {str(e)}")
        print(f"错误: {str(e)}")
        print("请确保已在config.yaml中正确配置硅基流动API密钥和模型信息")


if __name__ == "__main__":
    main()