# Allium AI助手

## 项目简介

Allium是一个基于大语言模型的AI助手系统，集成了语音识别(ASR)、语音合成(TTS)和对话生成等功能，可以实现自然的语音交互体验。

## 系统架构

### 核心模块

1. **语音识别(ASR)**
   - 使用FunASR框架
   - 支持实时语音识别
   - 高准确度的中文识别

2. **语音合成(TTS)**
   - 基于Fish-Speech引擎
   - 自然流畅的语音输出
   - 可配置的语音参数

3. **对话生成(LLM)**
   - 使用先进的语言模型
   - 支持上下文理解
   - 个性化的对话风格

4. **前端交互**
   - Live2D模型展示
   - 实时语音交互
   - 响应式界面设计

## 安装说明

### 环境要求

- Python 3.10+
- CUDA 11.7+ (GPU加速，可选)
- FFmpeg (音频处理)

### 安装步骤

1. 克隆项目
```bash
git clone [项目地址]
cd Allium
```

2. 创建虚拟环境
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置设置
- 复制`config.yaml.example`为`config.yaml`
- 根据需要修改配置参数

## 使用说明

### 启动服务

1. 启动主程序
```bash
python main.py
```

2. 访问Web界面
- 打开浏览器访问`http://localhost:5000`

### 功能说明

1. **语音对话**
   - 点击录音按钮开始对话
   - 自动语音识别和响应
   - 实时语音合成

2. **文本对话**
   - 支持文本输入
   - 即时响应
   - 语音播放

## 开发指南

### 项目结构
```
Allium/
├── config/             # 配置文件
├── processors/         # 核心处理器
├── interfaces/         # 接口定义
├── utils/             # 工具函数
├── assets/            # 静态资源
├── templates/         # 模板文件
└── main.py           # 主程序入口
```

### 开发流程

1. **环境配置**
   - 设置开发环境
   - 安装开发依赖

2. **代码规范**
   - 遵循PEP 8规范
   - 使用类型注解
   - 编写单元测试

3. **提交规范**
   - 清晰的提交信息
   - 代码审查
   - 测试验证

## 常见问题

1. **安装问题**
   - 检查Python版本
   - 确认CUDA版本匹配
   - 验证依赖完整性

2. **运行问题**
   - 检查配置文件
   - 确认模型下载完整
   - 验证端口占用

## 更新日志

### v1.0.0
- 初始版本发布
- 基础功能实现

## 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。

## 贡献指南

欢迎提交Issue和Pull Request。在贡献代码前，请先阅读贡献指南。
