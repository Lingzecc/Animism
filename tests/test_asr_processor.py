from processors.asr_processor import ASRProcessor

# 初始化ASR处理器
processor = ASRProcessor()

# 测试ASR处理功能
def test_process():
    try:
        # 这里可以添加实际的测试代码
        print("测试ASR处理功能开始...")
        # 例如：加载音频文件并处理
        # audio_path = Path("path/to/test/audio.wav")
        # audio_data = processor.load_audio(audio_path)
        # result = processor.process(audio_data)
        # print(f"ASR处理结果: {result}")
        print("测试ASR处理功能完成")
    except Exception as e:
        print(f"测试ASR处理功能失败: {str(e)}")

if __name__ == '__main__':
    # 初始化处理器
    try:
        print("初始化ASR处理器...")
        processor.initialize({})
        print("ASR处理器初始化成功")
    except Exception as e:
        print(f"ASR处理器初始化失败: {str(e)}")
        exit(1)
    
    # 运行测试
    test_process()
    
    # 清理资源
    try:
        print("清理ASR处理器资源...")
        processor.cleanup()
        print("ASR处理器资源清理完成")
    except Exception as e:
        print(f"ASR处理器资源清理失败: {str(e)}")