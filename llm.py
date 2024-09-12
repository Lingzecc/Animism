from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from load_config import Load_Config
import torch

# 初始化参数
cfg = Load_Config()
config = cfg.get_config()
model_name_or_path = config['model_name_or_path'] # 模型地址
model_cache_path = config['model_cache_path'] # 模型缓存地址
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # 判断是否能使用gpu
print(device)
fine_weight = config["finetune_weight_path"] + "epoch_2" # 微调保存地址
template_path = config["template"] # 模板地址
# 读取模板内容
def get_template(template_path):
    with open(template_path, "r", encoding="UTF-8") as f:  # 打开文件
        system_template = f.read()
    return system_template
# 获取模板
system_message = get_template(template_path)

# 生成器参数
generate_config = {
        "max_new":300,
        "do_sample":True,
        "top_p":0.8,
        "top_k":5,
        "temperature": 0.3,
        "repetition_penalty":1.1,
        "system_message": system_message,
        "sys_token_id": 0,
        "user_token_id": 3,
        "bot_token_id": 4
    }
# 加载模型（地址里模型是空的，需要自己下载）
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, 
                                             torch_dtype=torch.bfloat16, 
                                             trust_remote_code=True, 
                                             device_map=device)
generator = pipeline("text-generation",
                    model=model,
                    tokenizer=tokenizer, 
                    trust_remote_code=True)

# 内容初始化
def init_chat_template(generate_config):
    # Special Token 编号
    sys_token_id = generate_config['sys_token_id'] 
    user_token_id = generate_config['user_token_id']
    bot_token_id = generate_config['bot_token_id']

    system_start_ids = torch.tensor([[sys_token_id]], dtype=torch.int64, device=model.device)
    user_start_ids = torch.tensor([[user_token_id]], dtype=torch.int64, device=model.device)
    bot_start_ids = torch.tensor([[bot_token_id]], dtype=torch.int64, device=model.device)

    # System Message
    system = generate_config['system_message']
    system_ids = tokenizer.encode(system, return_tensors="pt").to(model.device)
    if len(system_ids) == 0 or system_ids.shape[-1] == 0:
        print('system_message is empty')
        system_ids = torch.tensor([[]], dtype=torch.int64).to(model.device)
    else:
        system_ids = torch.concat([system_start_ids,system_ids], dim=-1).long()
    return system_start_ids, user_start_ids, bot_start_ids, system_ids


# 模板
template = [{"role": "system", "content": system_message}]
# 模型封装成函数
def chat(query, template=template):
    system_start_ids, user_start_ids, bot_start_ids, system_ids = init_chat_template(generate_config)
    history_outputs = system_ids
    print("=====预设生成参数:", generate_config)
    model_input : list = template
    # 输入
    query : str = query
    model_input.append({"role": "user", "content": query})
    inputs = tokenizer.encode(query, return_tensors="pt").to(model.device)
    inputs = torch.concat([history_outputs, user_start_ids, inputs, bot_start_ids], dim=-1).long()
    history_outputs = model.generate(inputs, 
                    max_new_tokens=generate_config['max_new'], 
                    top_k=generate_config['top_k'], 
                    top_p=generate_config['top_p'], 
                    temperature=generate_config['temperature'], 
                    repetition_penalty=generate_config['repetition_penalty'], 
                    do_sample=generate_config['do_sample'])
    # 删除</s>
    if history_outputs[0][-1] == 2:
        history_outputs = history_outputs[:, :-1]
    # 模型输出
    outputs = tokenizer.decode(history_outputs[0][len(inputs[0]):])
    return outputs

# while True:
#     t = input("说：")
#     print(chat(t))