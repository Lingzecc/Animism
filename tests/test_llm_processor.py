from processors.llm_processor import LLMProcessor

# 初始化LLM处理器
llm = LLMProcessor()
llm.initialize()

# 测试单轮对话
response = llm.process("你好")
print(f"单轮对话响应: {response}")

# 测试多轮对话
response1 = llm.process("今天天气怎么样？")
print(f"第一轮响应: {response1}")
response2 = llm.process("我应该穿什么衣服？")
print(f"第二轮响应: {response2}")

# 清理资源
llm.cleanup()