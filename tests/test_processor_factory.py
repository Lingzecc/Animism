from processors.factory import ProcessorFactory
from processors.asr_processor import ASRProcessor
from processors.llm_processor import LLMProcessor
from processors.tts_processor import TTSProcessor

# 初始化处理器工厂
factory = ProcessorFactory()

# 测试工厂创建各处理器
def test_create_processor():
    try:
        print("测试处理器工厂创建功能开始...")
        
        # 测试创建ASR处理器
        print("测试创建ASR处理器...")
        asr_processor = factory.create_processor('asr')
        if isinstance(asr_processor, ASRProcessor):
            print("ASR处理器创建成功")
        else:
            print(f"ASR处理器创建失败，返回类型: {type(asr_processor)}")
        
        # 测试创建LLM处理器
        print("测试创建LLM处理器...")
        llm_processor = factory.create_processor('llm')
        if isinstance(llm_processor, LLMProcessor):
            print("LLM处理器创建成功")
        else:
            print(f"LLM处理器创建失败，返回类型: {type(llm_processor)}")
        
        # 测试创建TTS处理器
        print("测试创建TTS处理器...")
        tts_processor = factory.create_processor('tts')
        if isinstance(tts_processor, TTSProcessor):
            print("TTS处理器创建成功")
        else:
            print(f"TTS处理器创建失败，返回类型: {type(tts_processor)}")
            
        print("测试处理器工厂创建功能完成")
    except Exception as e:
        print(f"测试处理器工厂创建功能失败: {str(e)}")

if __name__ == '__main__':
    # 运行测试
    test_create_processor()