import json  
  
def get_config(config_path):  
    try:  
        with open(config_path, 'r', encoding="utf-8") as f:  
            config = json.load(f)  
    except json.JSONDecodeError:  
        # 如果文件不是有效的JSON，则创建一个新的空配置  
        config = {'data': []}  
    return config  
  
def add_data(input_data, output_data, config_path):  
    # 读取现有配置  
    data = get_config(config_path)  
      
    # 检查是否存在'data'键，如果不存在则初始化它  
    if 'data' not in data:  
        data['data'] = []  
      
    # 添加新的输入/输出对  
    data['data'].append({"input": input_data, "output": output_data})  
      
    # 写回更新后的配置  
    with open(config_path, 'w', encoding="utf-8") as f:  
        json.dump(data, f, ensure_ascii=False, indent=4)  
      
    print(f"已添加到{config_path}") 
    print(f"当前共{len(data['data'])}条数据")  
  
  
  
config_path = "liang.json"  
data_n = get_config(config_path)
while True:
    query = input("input:")  
    output = input("output:")  
    add_data(query, output, config_path)
