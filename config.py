import json

# 读取config.json文件
def get_config(path='config/config.json'):
    with open(path, 'r') as f:
        config = json.load(f)
    return config