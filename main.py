# -*- coding: utf-8 -*-
"""
Allium助手主模块
作者: 万物有灵团队
日期: 2025-05-22

本模块实现了Allium助手的核心功能，采用V型架构设计，分为数据层、业务逻辑层和表示层。
支持语音识别、文本生成和语音合成等功能，并提供Web服务接口。
"""
from pathlib import Path
import os
import traceback
from typing import Dict, List, Tuple

# 核心组件
from processors.factory import processor_factory
from logger import default_logger, log_function_call

# Web服务相关
from flask import Flask, send_from_directory, request, send_file, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# =====================================================================
# 数据层 (Data Layer)
# =====================================================================

class DataManager:
    """
    数据管理类，负责数据的存储和访问
    
    特性:
    - 管理对话历史记录
    - 提供模板缓存功能
    - 支持多会话管理
    """
    
    def __init__(self):
        """初始化数据管理器，创建会话历史和模板缓存"""
        self.conversation_history: Dict[str, List[Dict[str, str]]] = {}
        self.template_cache: Dict[str, str] = {}
        
    def get_template(self, template_name: str = "allium") -> str:
        """
        获取对话模板
        
        参数:
            template_name (str): 模板名称，默认为"allium"
            
        返回:
            str: 模板内容
        """
        if template_name in self.template_cache:
            return self.template_cache[template_name]
            
        template_path = Path(f'templates/{template_name}.txt')
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
                self.template_cache[template_name] = template
                return template
        except Exception as e:
            default_logger.error(f"加载模板失败: {str(e)}")
            raise
    
    def add_conversation(self, session_id: str, role: str, content: str) -> None:
        """
        添加对话历史
        
        参数:
            session_id (str): 会话ID
            role (str): 角色，"user"或"assistant"
            content (str): 对话内容
        """
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
            
        self.conversation_history[session_id].append({"role": role, "content": content})
        
        # 限制历史长度，防止过长
        if len(self.conversation_history[session_id]) > 20:  # 保留最近10轮对话
            self.conversation_history[session_id] = self.conversation_history[session_id][-20:]
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        获取对话历史
        
        参数:
            session_id (str): 会话ID
            
        返回:
            List[Dict[str, str]]: 对话历史列表
        """
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        return self.conversation_history[session_id]
    
    def clear_conversation_history(self, session_id: str) -> None:
        """
        清除对话历史
        
        参数:
            session_id (str): 会话ID
        """
        if session_id in self.conversation_history:
            self.conversation_history[session_id] = []

# =====================================================================
# 业务逻辑层 (Business Logic Layer)
# =====================================================================

class AlliumAssistant:
    """
    Allium助手主类，处理核心业务逻辑
    
    特性:
    - 集成语音识别、文本生成和语音合成功能
    - 支持多轮对话和会话历史管理
    - 提供完善的资源管理
    """
    
    def __init__(self):
        """初始化Allium助手，加载处理器和数据管理器"""
        try:
            # 初始化处理器
            self.asr_processor = processor_factory.get_asr_processor()
            self.tts_processor = processor_factory.get_tts_processor()
            self.llm_processor = processor_factory.get_llm_processor()
            
            # 初始化数据管理器
            self.data_manager = DataManager()
            
            # 加载默认模板
            self.template = self.data_manager.get_template()
            
            default_logger.info("Allium助手初始化成功")
        except Exception as e:
            default_logger.error(f"初始化Allium助手失败: {str(e)}")
            raise

    @log_function_call(default_logger)
    def process_voice(self, audio_path: Path) -> str:
        """
        处理语音输入，返回识别的文本
        
        参数:
            audio_path (Path): 音频文件路径
            
        返回:
            str: 识别的文本
        """
        try:
            # 语音识别
            audio_data = self.asr_processor.load_audio(audio_path)
            text = self.asr_processor.process(audio_data)
            default_logger.info(f"语音识别结果: {text}")
            return text
        except Exception as e:
            default_logger.error(f"处理语音失败: {str(e)}")
            raise

    @log_function_call(default_logger)
    def generate_response(self, text: str, session_id: str = "default") -> str:
        """
        生成回复，支持会话历史
        
        参数:
            text (str): 用户输入文本
            session_id (str): 会话ID，默认为"default"
            
        返回:
            str: 生成的回复文本
        """
        try:
            # 添加用户输入到历史
            self.data_manager.add_conversation(session_id, "user", text)
            
            # 获取历史对话
            history = self.data_manager.get_conversation_history(session_id)[:-1]  # 不包括当前输入
            
            # 准备输入数据
            input_data = {
                'system_message': self.template,
                'query': text,
                'history': history
            }
            
            # 生成回复
            response = self.llm_processor.process(input_data)
            
            # 添加助手回复到历史
            self.data_manager.add_conversation(session_id, "assistant", response)
            
            default_logger.info(f"生成回复: {response}")
            return response
        except Exception as e:
            default_logger.error(f"生成回复失败: {str(e)}")
            raise

    @log_function_call(default_logger)
    def synthesize_voice(self, text: str) -> Path:
        """
        合成语音
        
        参数:
            text (str): 需要合成的文本
            
        返回:
            Path: 合成的音频文件路径
        """
        try:
            audio_path = self.tts_processor.process(text)
            default_logger.info(f"语音合成完成: {audio_path}")
            return audio_path
        except Exception as e:
            default_logger.error(f"语音合成失败: {str(e)}")
            raise

    @log_function_call(default_logger)
    def process_text_input(self, text: str, session_id: str = "default") -> Tuple[str, Path]:
        """
        处理文本输入，返回回复文本和语音路径
        
        参数:
            text (str): 用户输入文本
            session_id (str): 会话ID，默认为"default"
            
        返回:
            Tuple[str, Path]: 回复文本和语音文件路径
        """
        try:
            # 生成回复
            response = self.generate_response(text, session_id)
            # 合成语音
            audio_path = self.synthesize_voice(response)
            return response, audio_path
        except Exception as e:
            default_logger.error(f"处理文本输入失败: {str(e)}")
            raise

    @log_function_call(default_logger)
    def process_voice_input(self, audio_path: Path, session_id: str = "default") -> Tuple[str, str, Path]:
        """
        处理语音输入，返回识别文本、回复文本和语音路径
        
        参数:
            audio_path (Path): 音频文件路径
            session_id (str): 会话ID，默认为"default"
            
        返回:
            Tuple[str, str, Path]: 识别文本、回复文本和语音文件路径
        """
        try:
            # 语音识别
            text = self.process_voice(audio_path)
            # 生成回复并合成语音
            response, response_audio = self.process_text_input(text, session_id)
            return text, response, response_audio
        except Exception as e:
            default_logger.error(f"处理语音输入失败: {str(e)}")
            raise
    
    def clear_conversation_history(self, session_id: str = "default") -> None:
        """
        清除会话历史
        
        参数:
            session_id (str): 会话ID，默认为"default"
        """
        try:
            self.data_manager.clear_conversation_history(session_id)
            default_logger.info(f"会话 {session_id} 的历史已清除")
        except Exception as e:
            default_logger.error(f"清除会话历史失败: {str(e)}")
            raise

    def cleanup(self):
        """
        清理资源，释放处理器占用的内存
        """
        try:
            processor_factory.cleanup_all()
            default_logger.info("Allium助手资源已清理")
        except Exception as e:
            default_logger.error(f"清理资源失败: {str(e)}")
            raise

# =====================================================================
# 表示层 (Presentation Layer)
# =====================================================================

# 配置常量
UPLOAD_FOLDER = 'data/audio_processing/recording/'
ALLOWED_EXTENSIONS = {'webm', 'mp3', 'wav', 'ogg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用跨域资源共享
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 创建全局助手实例
try:
    allium_assistant = AlliumAssistant()
    default_logger.info("Allium助手实例创建成功")
except Exception as e:
    default_logger.error(f"创建Allium助手实例失败: {str(e)}")
    raise

# 辅助函数
def allowed_file(filename):
    """
    检查文件扩展名是否允许
    
    参数:
        filename (str): 文件名
        
    返回:
        bool: 文件类型是否允许
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 错误处理
@app.errorhandler(413)
def request_entity_too_large(error):
    """
    处理请求实体过大错误
    
    参数:
        error: 错误对象
        
    返回:
        tuple: 包含错误信息的JSON响应和状态码
    """
    return jsonify({
        'error': '文件太大',
        'message': f'上传文件不能超过{MAX_CONTENT_LENGTH/(1024*1024)}MB'
    }), 413

@app.errorhandler(500)
def internal_server_error(error):
    """
    处理服务器内部错误
    
    参数:
        error: 错误对象
        
    返回:
        tuple: 包含错误信息的JSON响应和状态码
    """
    return jsonify({
        'error': '服务器内部错误',
        'message': '处理请求时发生错误，请稍后再试'
    }), 500

# 网页投射
@app.route('/')
def web():
    """提供Web界面"""
    return send_file('./web.html')

# 静态资源路由
@app.route('/assets/<path:path>')
def live2d(path):
    """提供Live2D资源"""
    return send_from_directory('./assets/', path)

@app.route('/js/<path:path>')
def js(path):
    """提供JavaScript资源"""
    return send_from_directory('./assets/js/', path)

@app.route('/css/<path:path>')
def css(path):
    """提供CSS资源"""
    return send_from_directory('./assets/css/', path)

@app.route('/img/<path:path>')
def img(path):
    """提供图片资源"""
    return send_from_directory('./assets/img/', path)

# API状态检查
@app.route('/api/status')
def api_status():
    """
    检查API状态
    
    返回:
        Response: 包含API状态信息的JSON响应
    """
    return jsonify({
        'status': 'online',
        'version': '1.0.0'
    })

# 获取前端音频保存到UPLOAD_FOLDER
@app.route('/upload/audio', methods=['POST'])
def record_audio2wav():
    """
    处理音频上传请求，将音频转换为WAV格式并生成回复
    
    返回:
        Response: 音频文件或错误信息
    """
    # 检查是否有文件
    if 'audioFile' not in request.files:
        return jsonify({
            'error': '没有文件部分',
            'message': '请求中未找到音频文件'
        }), 400
        
    file = request.files['audioFile']
    
    # 检查文件名
    if file.filename == '':
        return jsonify({
            'error': '没有选择文件',
            'message': '请选择一个音频文件'
        }), 400
        
    # 检查文件类型
    if not allowed_file(file.filename):
        return jsonify({
            'error': '文件类型不允许',
            'message': f'允许的文件类型: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    # 获取会话ID，如果没有则使用默认值
    session_id = request.form.get('session_id', 'default')
    
    try:
        # 安全地保存文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        towavfilepath = os.path.join(app.config['UPLOAD_FOLDER'], "recorded_audio.wav")
        file.save(filepath)
        
        # 转wav
        try:
            import moviepy.video.io.ffmpeg_tools
            moviepy.video.io.ffmpeg_tools.ffmpeg_extract_audio(filepath, towavfilepath)
            default_logger.info(f"音频已成功转换为WAV格式，并保存到{towavfilepath}")
        except Exception as e:
            default_logger.error(f"音频转换失败: {str(e)}")
            return jsonify({
                'error': '音频转换失败',
                'message': str(e)
            }), 500
        
        # 使用AlliumAssistant处理语音
        audio_path = Path(towavfilepath)
        text, response, response_audio = allium_assistant.process_voice_input(audio_path, session_id)
        default_logger.info(f"识别文本: {text}, 响应: {response}")
        
        return send_file(response_audio, mimetype='audio/wav')
    except Exception as e:
        default_logger.error(f"处理语音失败: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': '处理语音失败',
            'message': str(e)
        }), 500

@app.route('/upload/tts', methods=['POST'])
def text_to_speech():
    """
    处理文本转语音请求
    
    返回:
        Response: 音频文件或错误信息
    """
    try:
        # 检查是否有文本
        if 'text' not in request.form:
            return jsonify({
                'error': '没有文本',
                'message': '请求中未找到文本内容'
            }), 400
            
        text = request.form['text']
        
        # 检查文本长度
        if len(text) > 1000:  # 限制文本长度
            return jsonify({
                'error': '文本太长',
                'message': '文本长度不能超过1000个字符'
            }), 400
            
        # 获取会话ID，如果没有则使用默认值
        session_id = request.form.get('session_id', 'default')
        
        default_logger.info(f"接收到文本: {text}")
        response, audio_path = allium_assistant.process_text_input(text, session_id)
        default_logger.info(f"生成响应: {response}")
        
        return send_file(audio_path, mimetype='audio/wav')
    except Exception as e:
        default_logger.error(f"文本转语音失败: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': '文本转语音失败',
            'message': str(e)
        }), 500

# 清除会话历史
@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """
    清除会话历史
    
    返回:
        Response: 操作结果
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default') if data else 'default'
        
        allium_assistant.clear_conversation_history(session_id)
            
        return jsonify({
            'status': 'success',
            'message': f'会话 {session_id} 的历史已清除'
        })
    except Exception as e:
        default_logger.error(f"清除会话历史失败: {str(e)}")
        return jsonify({
            'error': '清除会话历史失败',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    try:
        default_logger.info("启动Allium助手服务，端口8080")
        app.run(port=8080, debug=True, host="0.0.0.0")
    except Exception as e:
        default_logger.error(f"启动服务失败: {str(e)}")
    finally:
        allium_assistant.cleanup()