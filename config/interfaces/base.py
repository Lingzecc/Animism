from abc import ABC, abstractmethod
from typing import Any, Dict
from pathlib import Path

class BaseProcessor(ABC):
    """基础处理器接口"""
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """初始化处理器"""
        pass

    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """处理输入数据"""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """清理资源"""
        pass

class AudioProcessor(BaseProcessor):
    """音频处理器接口"""
    @abstractmethod
    def load_audio(self, audio_path: Path) -> Any:
        """加载音频文件"""
        pass

    @abstractmethod
    def save_audio(self, audio_data: Any, save_path: Path) -> None:
        """保存音频文件"""
        pass

class TextProcessor(BaseProcessor):
    """文本处理器接口"""
    @abstractmethod
    def preprocess(self, text: str) -> str:
        """预处理文本"""
        pass

    @abstractmethod
    def postprocess(self, text: str) -> str:
        """后处理文本"""
        pass

class ModelProcessor(BaseProcessor):
    """模型处理器接口"""
    @abstractmethod
    def load_model(self, model_path: str) -> None:
        """加载模型"""
        pass

    @abstractmethod
    def generate(self, input_data: Any, **kwargs) -> Any:
        """生成输出"""
        pass

    @abstractmethod
    def save_model(self, save_path: str) -> None:
        """保存模型"""
        pass

class APIProcessor(BaseProcessor):
    """API处理器接口"""
    @abstractmethod
    def prepare_request(self, input_data: Any) -> Dict[str, Any]:
        """准备请求数据"""
        pass

    @abstractmethod
    def handle_response(self, response: Any) -> Any:
        """处理响应数据"""
        pass

    @abstractmethod
    def handle_error(self, error: Exception) -> None:
        """处理错误"""
        pass