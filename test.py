def seconds_to_time(s):  
    # 将秒转换为小时、分钟和秒  
    hours = s // 3600  
    minutes = (s % 3600) // 60  
    seconds = s % 60  
      
    # 格式化时间字符串  
    # 使用zfill确保时间部分至少为两位数（例如，将5转换为05）  
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"  
      
    return time_str  
  
# 假设输入是距离当日午夜的秒数  
s = 8000  # 例如，这个值表示10小时10分钟10秒  
  
# 调用函数并打印结果  
current_time = seconds_to_time(s)  
print(f"当前时间是: {current_time}")