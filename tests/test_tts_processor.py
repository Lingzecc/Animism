from processors.tts_processor import TTSProcessor
from pathlib import Path

# 初始化TTS处理器
processor = TTSProcessor()

# 测试TTS处理功能
def test_process():
    try:
        print("测试TTS处理功能开始...")
        # 测试文本转语音
        test_text = "这是一个测试文本，用于测试文本转语音功能。"
        print(f"测试文本: {test_text}")
        
        # 处理文本
        output_path = processor.process(test_text)
        
        # 保存音频文件（可选）
        # output_dir = Path("data/audio_processing/tts")
        # output_dir.mkdir(parents=True, exist_ok=True)
        # output_path = output_dir / "test_output.wav"
        # processor.save_audio(audio_data, output_path)
        
        print(f"TTS处理完成，输出文件: {output_path}")
        print("测试TTS处理功能完成")
    except Exception as e:
        print(f"测试TTS处理功能失败: {str(e)}")

if __name__ == '__main__':
    # 初始化处理器
    try:
        print("初始化TTS处理器...")
        processor.initialize({})
        print("TTS处理器初始化成功")
    except Exception as e:
        print(f"TTS处理器初始化失败: {str(e)}")
        exit(1)
    
    # 运行测试
    test_process()
    
    # 清理资源
    try:
        print("清理TTS处理器资源...")
        processor.cleanup()
        print("TTS处理器资源清理完成")
    except Exception as e:
        print(f"TTS处理器资源清理失败: {str(e)}")