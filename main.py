from langchain.chains.llm import LLMChain
# from langchain.agents import AgentExecutor, create_structured_chat_agent, load_tools
# from langchain_core.messages import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from Templates import *
from ChatChat import ChatChat
# from tools.Calculator import Calculator
# from tools.Weather import Weather
# from tools.DistanceConversion import DistanceConverter
from config import get_config
# 初始化
config = get_config()
tokenizer_name_or_path = config['tokenizer_name_or_path']
model_name_or_path = config['model_name_or_path']
model_cache_path = config['model_cache_path']
device = config['device']

prompt_template = Templates()
prompt = PromptTemplate(input_variables=["chat_history","human_input"], template=prompt_template)
if __name__ == "__main__":
    llm = ChatChat()
    llm.load_model(model_name_or_path)
    memory = ConversationBufferMemory(memory_key="chat_history")
    chain = LLMChain(llm=llm, prompt=prompt,verbose=True,memory=memory)
    chain.predict(human_input="你好")
