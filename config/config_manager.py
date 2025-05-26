import yaml
import json
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    def __init__(self, yaml_path: str = 'config/config.yaml', json_path: str = 'config/config.json'):
        self.yaml_path = Path(yaml_path)
        self.json_path = Path(json_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件，优先使用YAML配置，同时保持对JSON配置的兼容"""
        config = {}
        
        # 加载YAML配置
        if self.yaml_path.exists():
            with open(self.yaml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        
        # 如果存在JSON配置，合并配置
        if self.json_path.exists():
            with open(self.json_path, 'r', encoding='utf-8') as f:
                json_config = json.load(f)
                # 保持向后兼容
                if not config.get('model'):
                    config['model'] = {
                        'name': json_config.get('model_name_or_path'),
                        'finetune_weight': json_config.get('finetune_weight_path')
                    }
                if not config.get('template'):
                    config['template'] = {
                        'path': json_config.get('template')
                    }
        
        return config
    
    def get_model_config(self) -> Dict[str, Any]:
        """获取模型相关配置"""
        return self.config.get('model', {})
    
    def get_api_config(self) -> Dict[str, Any]:
        """获取API相关配置"""
        return self.config.get('api', {})
    
    def get_asr_config(self) -> Dict[str, Any]:
        """获取语音识别相关配置"""
        return self.config.get('asr', {})
    
    def get_template_config(self) -> Dict[str, Any]:
        """获取模板相关配置"""
        return self.config.get('template', {})
    
    def get_generate_config(self) -> Dict[str, Any]:
        """获取生成相关配置"""
        return self.config.get('model', {}).get('generate_config', {})
    
    def get_tts_config(self) -> Dict[str, Any]:
        """获取TTS相关配置"""
        return self.config.get('api', {}).get('tts', {})
    
    def get_silicon_flow_config(self) -> Dict[str, Any]:
        """获取硅基流动相关配置"""
        return self.config.get('api', {}).get('silicon_flow', {})
    
    def save_config(self) -> None:
        """保存配置到YAML文件"""
        with open(self.yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """更新配置"""
        self.config.update(new_config)
        self.save_config()