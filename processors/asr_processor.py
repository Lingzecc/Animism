# -*- coding: utf-8 -*-
"""
ASRProcessor 语音识别处理器模块
作者: 万物有灵团队
日期: 2025-05-20

本模块实现了基于FunASR的语音识别处理器，支持音频加载、分块识别、资源管理等功能。
"""
import os
from pathlib import Path
from typing import Any, Dict
import soundfile
from funasr import AutoModel

from config.interfaces.base import AudioProcessor
from logger import asr_logger, log_function_call, log_error


class ASRProcessor(AudioProcessor):
    """ASRProcessor 语音识别处理器，负责音频识别流程的实现"""
    def __init__(self):
        """
        初始化ASRProcessor实例。
        初始化成员变量，包括模型对象、配置、初始化状态。
        """
        self.model = None
        self.config = None
        self.initialized = False

    @log_function_call(asr_logger)
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        初始化ASR处理器。
        参数:
            config (Dict[str, Any]): 配置字典，包含模型名称、版本、分块参数等。
        """
        try:
            # 设置模型下载路径到项目下的models文件夹
            models_dir = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models"))
            models_dir.mkdir(exist_ok=True)  # 确保models文件夹存在
            os.environ["MODELSCOPE_CACHE"] = str(models_dir)
            asr_logger.info(f"设置模型下载路径为: {models_dir}")
            
            self.config = config
            self.model = AutoModel(
                model=config.get('model', 'paraformer-zh-streaming'),
                model_revision=config.get('model_revision', 'v2.0.4'),
                disable_update=True
            )
            self.chunk_size = config.get('chunk_size', [0, 10, 5])
            self.encoder_chunk_look_back = config.get('encoder_chunk_look_back', 4)
            self.decoder_chunk_look_back = config.get('decoder_chunk_look_back', 1)
            self.initialized = True
            asr_logger.info("ASR processor initialized successfully")
        except Exception as e:
            asr_logger.error(f"Failed to initialize ASR processor: {str(e)}")
            raise

    @log_function_call(asr_logger)
    def load_audio(self, audio_path: Path) -> Any:
        """
        加载音频文件。
        参数:
            audio_path (Path): 音频文件路径。
        返回:
            Tuple: (音频数据, 采样率)
        """
        try:
            speech, sample_rate = soundfile.read(str(audio_path))
            asr_logger.debug(f"Loaded audio file: {audio_path}, sample rate: {sample_rate}")
            return speech, sample_rate
        except Exception as e:
            asr_logger.error(f"Failed to load audio file {audio_path}: {str(e)}")
            raise

    @log_function_call(asr_logger)
    def save_audio(self, audio_data: Any, save_path: Path) -> None:
        """
        保存音频文件（当前ASR处理器不需要实现此方法）。
        参数:
            audio_data (Any): 音频数据。
            save_path (Path): 保存路径。
        """
        pass

    @log_error(asr_logger)
    def _process_chunk(self, speech_chunk: Any, is_final: bool, cache: Dict) -> str:
        """
        处理音频块，调用模型进行识别。
        参数:
            speech_chunk (Any): 音频块数据。
            is_final (bool): 是否为最后一块。
            cache (Dict): 缓存字典。
        返回:
            str: 识别结果。
        """
        return self.model.generate(
            input=speech_chunk,
            cache=cache,
            is_final=is_final,
            chunk_size=self.chunk_size,
            encoder_chunk_look_back=self.encoder_chunk_look_back,
            decoder_chunk_look_back=self.decoder_chunk_look_back
        )

    @log_function_call(asr_logger)
    def process(self, input_data: Any) -> str:
        """
        处理音频数据，分块识别并拼接结果。
        参数:
            input_data (Any): (音频数据, 采样率)元组。
        返回:
            str: 识别文本结果。
        """
        if not self.initialized:
            raise RuntimeError("ASR processor not initialized")

        try:
            speech, _ = input_data
            chunk_stride = self.chunk_size[1] * 960
            cache = {}
            total_chunk_num = int(len(speech) / chunk_stride)
            result = ""

            for i in range(total_chunk_num):
                speech_chunk = speech[i * chunk_stride:(i + 1) * chunk_stride]
                is_final = i == total_chunk_num - 1
                chunk_result = self._process_chunk(speech_chunk, is_final, cache)
                result = chunk_result

            asr_logger.info("Audio processing completed successfully")
            return str(result)

        except Exception as e:
            asr_logger.error(f"Error processing audio: {str(e)}")
            raise

    @log_function_call(asr_logger)
    def cleanup(self) -> None:
        """
        清理资源，释放模型。
        """
        try:
            if self.model:
                del self.model
                self.model = None
            self.initialized = False
            asr_logger.info("ASR processor cleaned up successfully")
        except Exception as e:
            asr_logger.error(f"Error during cleanup: {str(e)}")
            raise