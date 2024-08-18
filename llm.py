from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from load_config import Load_Config
import torch
# 初始化参数
cfg = Load_Config()
config = cfg.get_config()
model_name_or_path = config['model_name_or_path']
model_cache_path = config['model_cache_path']
device = config['device']
fine_weight = config["finetune_weight_path"] + "epoch_2"
template_path = config["template"]

def get_template(template_path):
    with open(template_path, "r", encoding="UTF-8") as f:  # 打开文件
        system_template = f.read()
    return system_template
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

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, 
                                             torch_dtype=torch.bfloat16, 
                                             trust_remote_code=True, 
                                             device_map=device)
generator = pipeline("text-generation",
                    model=model,
                    tokenizer=tokenizer, 
                    trust_remote_code=True)


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



model_input = [{"role": "system", "content": system_message}]

print("=====预设生成参数:", generate_config)
while True:
    query = input("我：")
    model_input.append({"role": "user", "content": query})
    system_start_ids, user_start_ids, bot_start_ids, system_ids = init_chat_template(generate_config)
    model_output = generator(model_input, max_new_tokens=300, top_k=5, top_p=0.8, temperature=0.3, repetition_penalty=1.1, do_sample=True)

    print('Model:', system_ids)