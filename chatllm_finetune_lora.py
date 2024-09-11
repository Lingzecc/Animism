from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, DataCollatorForSeq2Seq, Trainer, AutoConfig
from datasets import Dataset
from peft import get_peft_model, LoraConfig, TaskType
from load_config import Load_Config
import torch
import pandas as pd
import os
import logger
# 初始化参数
cfg = Load_Config()
config = cfg.get_config()
model_name_or_path = config['model_name_or_path']
model_cache_path = config['model_cache_path']
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
# fine_name:微调参数文件名
fine_name = "epoch_2"
fine_weight = config["finetune_weight_path"] + fine_name
template_path = config["template"]
data = pd.read_json("data\\test_data.json")
data = Dataset.from_pandas(data)

# 微调参数
num_train_epochs = 2
# output_dir:微调参数保存路径
output_dir = fine_weight
learning_rate = 1e-4
gradient_accumulation_steps = 2
weight_decay = 0.1


def get_template(template_path):
    with open(template_path, "r", encoding="UTF-8") as f:  # 打开文件
        system_template = f.read()
    return system_template

system_message = get_template(template_path)
config = AutoConfig.from_pretrained(model_name_or_path, trust_remote_code=True)
config.use_cache = False
peft_config = LoraConfig(
    inference_mode=False,
    task_type=TaskType.CAUSAL_LM, r=8, 
    lora_alpha=32, lora_dropout=0.1, target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, torch_dtype=torch.bfloat16, config=config, trust_remote_code=True)


model = get_peft_model(model, peft_config)
# model.print_trainable_parameters()
print(model)

training_args = TrainingArguments(output_dir=output_dir,
                                  num_train_epochs=num_train_epochs,
                                  learning_rate=learning_rate,
                                  gradient_accumulation_steps=gradient_accumulation_steps,
                                  weight_decay=weight_decay
                                  )


def process_func(example):
        MAX_LENGTH = 512
        input_ids, attention_mask, labels = [], [], []

        system_default = system_message
        system = example.get("system", system_default)
        user_input = example['input']
        ai_output = example['output']

        instruction = tokenizer(f"<unk>{system}reserved_0{user_input}reserved_1", add_special_tokens=False)
        response = tokenizer(f"{ai_output}", add_special_tokens=False)
        input_ids = instruction["input_ids"] + response["input_ids"] + [tokenizer.pad_token_id]
        attention_mask = instruction["attention_mask"] + response["attention_mask"] + [1]
        labels = [-100] * len(instruction["input_ids"]) + response["input_ids"] + [tokenizer.pad_token_id]  
        if len(input_ids) > MAX_LENGTH:
            input_ids = input_ids[:MAX_LENGTH]
            attention_mask = attention_mask[:MAX_LENGTH]
            labels = labels[:MAX_LENGTH]
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels
        }
WEIGHTS_NAME = "pytorch_model.bin"
TRAINING_ARGS_NAME = "training_args.bin"

class LoRATrainer(Trainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save_model(self, output_dir=None, _internal_call=False):
        output_dir = output_dir if output_dir is not None else self.args.output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Saving model checkpoint to {output_dir}")
        model_to_save = self.model
        state_dict = {k: v.to("cpu") for k, v in model_to_save.named_parameters() if v.requires_grad}
        # Using Hugging Face's save_pretrained instead of PyTorch's torch.save
        model_to_save.save_pretrained(output_dir, state_dict=state_dict, save_function=torch.save,safe_serialization=False)
        
        # Save tokenizer and training arguments as usual
        if self.tokenizer is not None:
            self.tokenizer.save_pretrained(output_dir)

        print(self.args)
        torch.save(self.args, os.path.join(output_dir, TRAINING_ARGS_NAME, ))


tokenizer.padding_side = 'right'
tokenizer.pad_token_id = tokenizer.eos_token_id
tokenizer.pad_token = '<|endoftext|>'
tokenized_id = data.map(process_func, remove_columns=data.column_names)
trainer = LoRATrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_id,
    data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer, padding=True),
)
trainer.train()
trainer.save_model()