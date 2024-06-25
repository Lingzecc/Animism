from transformers import AutoModel, AutoTokenizer,AutoModelForCausalLM
import gradio as gr
import mdtex2html
import os
from ChatChat import ChatChat
import torch
from langchain.chains.llm import LLMChain
from config import Config
# 初始化参数
cfg = Config()
config = cfg.get_config()
tokenizer_name_or_path = config['tokenizer_name_or_path']
model_name_or_path = config['model_name_or_path']
model_cache_path = config['model_cache_path']
device = config['device']

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, 
                                          trust_remote_code=True, 
                                          cache_dir=os.path.join(model_cache_path, model_name_or_path))
model = AutoModel.from_pretrained(model_name_or_path, 
                                  trust_remote_code=True,
                                  cache_dir=os.path.join(model_cache_path, model_name_or_path)
                                  ).to(device).float()
model = model.eval()


def postprocess(self, y):
    if y is None:
        return []
    for i, (message, response) in enumerate(y):
        y[i] = (
            None if message is None else mdtex2html.convert((message)),
            None if response is None else mdtex2html.convert(response),
        )
    return y


gr.Chatbot.postprocess = postprocess


def parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>"+line
    text = "".join(lines)
    return text


def predict(input, chatbot, max_length, top_p, temperature, history):
    chatbot.append((parse_text(input), ""))
    for response, history in model.stream_chat(tokenizer, input, history, max_length=max_length, top_p=top_p,
                                               temperature=temperature):
        chatbot[-1] = (parse_text(input), parse_text(response))

        yield chatbot, history


def reset_user_input():
    return gr.update(value='')


def reset_state():
    return [], []


custom_html = """
<style>
  body {
    background-image: url("D:\光.png");
    background-size: cover; 
    background-repeat: no-repeat;
    background-color:#cccccc;
  }
</style>
"""
custom_js = ""

with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">聊天框</h1>""")
    
    chatbot = gr.Chatbot()
    with gr.Row():
        with gr.Column(scale=4):
            with gr.Column(scale=12):
                user_input = gr.Textbox(show_label=False, placeholder="请输入...", lines=10)
            with gr.Column(min_width=32, scale=1):
                submitBtn = gr.Button("发送", variant="primary")
        with gr.Column(scale=1):
            emptyBtn = gr.Button("清空")
            max_length = gr.Slider(0, 4096, value=2048, step=1.0, label="最大长度", interactive=True)# max_length
            top_p = gr.Slider(0, 1, value=0.7, step=0.01, label="随机度", interactive=True)# Top P
            temperature = gr.Slider(0, 1, value=0.95, step=0.01, label="发散思维", interactive=True)# Temperature

    history = gr.State([])

    submitBtn.click(predict, [user_input, chatbot, max_length, top_p, temperature, history], [chatbot, history],
                    show_progress=True)
    submitBtn.click(reset_user_input, [], [user_input])

    emptyBtn.click(reset_state, outputs=[chatbot, history], show_progress=True)


# gr.Interface(
#     fn=Test,
#     inputs='None',
#     outputs='None',
#     css=custom_html,
#     js=custom_js).launch(share=False, inbrowser=True)
demo.queue().launch(share=False, inbrowser=True)