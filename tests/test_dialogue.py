from processors.llm_processor import LLMProcessor
from config.config_manager import ConfigManager

# 加载配置
config_manager = ConfigManager()
config = config_manager.get_model_config()  # 获取模型配置

# 确保配置包含必要的name字段
if not config.get('name'):
    config['name'] = config_manager.config.get('model_name_or_path')

# 初始化LLM处理器
llm = LLMProcessor()
llm.initialize(config)

# 测试单轮对话
try:
    response = llm.process({"text": "你好", "system_message": ""})
    print(f"单轮对话响应: {response}")
except Exception as e:
    print(f"单轮对话测试失败: {str(e)}")

# 测试多轮对话
try:
    response1 = llm.process({"text": "今天天气怎么样？", "system_message": ""})
    print(f"第一轮响应: {response1}")
    
    response2 = llm.process({"text": "我应该穿什么衣服？", "system_message": ""})
    print(f"第二轮响应: {response2}")
except Exception as e:
    print(f"多轮对话测试失败: {str(e)}")

# 清理资源
llm.cleanup()