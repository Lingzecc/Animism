## 文件结构:

**models**----模型存储地址

- **chatGLM**----ChatGLM_6B             //已移除
- **ChatGLM2**----ChatGLM2_6B-int4 //已移除
- **mini**----MiniCPM_2B                     //已移除
- **mini_int4**----MiniCPM_2B-int4     //已移除
- **Qwen1.5-0.5B**----千问1.5_0.5B     //已移除

**config**----配置文件

- config.json----基本参数

config.py----加载config参数
**cache**----临时缓存地址
**help**----帮助
ChatChat.py----langchain自定义LLM文件
**embeddings**----编码器地址
**data**----数据存储地址
**output**----存储输出的模型
Templates.py----模型模板存储类
main.py----主接口
cli_demo.py----终端窗口交互
webui.py----网页窗口交互
LICENSE----开源协议2.0
requirements.txt----相关包      //可以使用---安装--> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple <--安装
README----这是什么？你说这是什么？你正在看什么？

---
