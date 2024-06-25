import json
import os
class Config:
    def __init__(self,dir_path_or_name="config",file_path_or_name="config.json"):
        # 基础配置
        self.dir_path_or_name = dir_path_or_name
        self.file_path_or_name = file_path_or_name
        self.config_path = os.path.join(self.dir_path_or_name, self.file_path_or_name) # json地址
        
        
    # 读取config.json文件
    def get_config(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config
    # 更新参数
    def set_config(self, **kwargs):
        data = self.get_config()
        for key, value in kwargs.items():
            data[key] = value
            with open(self.config_path, 'w') as f:
                json.dump(data, f)
                print(f"已添加到{self.config_path}\n内容：Key: {key}, Value: {value}")
    # 删除
    def del_config(self,key):
        data = self.get_config()
        del data[key]
        with open(self.config_path, 'w') as f:
                json.dump(data, f)
                print(f"从{self.config_path}处:\n内容:{key}已删除")
        
        