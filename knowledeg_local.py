from langchain.chains import RetrievalQA
from langchain.prompts.prompt import PromptTemplate


    #获取大语言模型返回的答案（基于本地知识库查询）
def get_knowledeg_based_answer(self,query,
                                  history_len=5,
                                  temperature=0.1,
                                  top_p=0.9,
                                  top_k=4,
                                  chat_history=[]):
    #定义查询的提示模板格式：
    prompt_template = """
        基于以下已知信息，简洁和专业的来回答用户的问题。
        如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的相关信息"，不允许在答案中添加编造成分，答案请使用中文，答案请带有情感的回答。
        已知内容:
        {context}
        问题:
        {question}
    """
    prompt = PromptTemplate(template=prompt_template,
                        input_variables=["context", "question"])
    self.llm_service.history = chat_history[-history_len:] if history_len>0 else []
    self.llm_service.temperature = temperature
    self.llm_service.top_p = top_p
    
    #利用预先存在的语言模型、检索器来创建并初始化BaseRetrievalQA类的实例
    knowledge_chain = RetrievalQA.from_llm(
    llm = self.llm_service,
    #基于本地知识库构建一个检索器，并仅返回top_k的结果
    retriever = self.knowledge_service.knowledge_base.as_retriever(
    search_kwargs={"k":top_k}),
    prompt = prompt)
    #combine_documents_chain的作用是将查询返回的文档内容（page_content）合并到一起作为prompt中context的值
    #将combine_documents_chain的合并文档内容改为{page_content}
    
    knowledge_chain.combine_documents_chain.document_prompt = PromptTemplate(
    input_variables=["page_content"],template="{page_content}")
    
    #返回结果中是否包含源文档
    knowledge_chain.return_source_documents = True
    
    #传入问题内容进行查询
    result = knowledge_chain({"query":query})
    return result
    
    #获取大语言模型返回的答案（未基于本地知识库查询）
def get_llm_answer(self,query):
    result = self.llm_service._call(query)
    return result