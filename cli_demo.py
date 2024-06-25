import os
import platform
import signal
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
import json
from config import Config
# 初始化参数
cfg = Config()
config = cfg.get_config()
tokenizer_name_or_path = config['tokenizer_name_or_path']
model_name_or_path = config['model_name_or_path']
model_cache_path = config['model_cache_path']
device = config['device']

tokenizer = AutoTokenizer.from_pretrained(tokenizer_name_or_path, trust_remote_code=True, cache_dir=model_cache_path)
model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True).float().to(device)
model = model.eval() # 开启评估模式

os_name = platform.system()
clear_command = 'cls' if os_name == 'Windows' else 'clear'
stop_stream = False


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

def build_prompt(history):
    prompt = "输入内容即可进行对话，clear 清空对话历史，stop 终止程序"
    for query, response in history:
        prompt += f"\n\n用户：{query}"
        prompt += f"\n\nAI：{response}"
    return prompt


def signal_handler(signal, frame):
    global stop_stream
    stop_stream = True


def main():
    history = []
    global stop_stream
    print("输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
    while True:
        query = input("\n用户：")
        if query.strip() == "stop":
            break
        if query.strip() == "clear":
            history = []
            os.system(clear_command)
            print("输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
            continue
        count = 0
        for response, history in model.stream_chat(tokenizer, query, history=history):
            if stop_stream:
                stop_stream = False
                break
            else:
                count += 1
                if count % 8 == 0:
                    os.system(clear_command)
                    print(build_prompt(history), flush=True)
                    signal.signal(signal.SIGINT, signal_handler)
        os.system(clear_command)
        print(build_prompt(history), flush=True)


if __name__ == "__main__":
    main()