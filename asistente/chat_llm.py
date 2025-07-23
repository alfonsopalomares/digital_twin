# -*- coding: utf-8 -*-
"""

"""


import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# from langchain.llms import HuggingFaceInferenceAPI
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
# API_KEY = os.getenv("OPENROUTER_API_KEY") #OpenRouter
# API_KEY = os.getenv("HF_API_KEY") #HuggingFace
API_KEY = os.getenv("GOOGLE_API_KEY") #Google AI Studio

# def create_llm() -> BaseLanguageModel:
def create_llm():
    """
    Retorna un LLM apto para uso en asistente de chat

    Returns
    -------
    llm : BaseLanguageModel
        modelo LLM listo para incorporar al agente de langchain.

    """

    # Usando OpenRouter
    # model_name = "qwen/qwen3-4b:free"
    model_name = "deepseek/deepseek-chat-v3-0324:free"
    # llm = ChatOpenAI(
    #     model=model_name, 
    #     base_url="https://openrouter.ai/api/v1", 
    #     # api_key=API_KEY, 
    #     openai_api_key=API_KEY, 
    #     temperature=0.3)
    
    # usando HaggingFace
    # model_name = "tiiuae/falcon-7b-instruct"
    # llm = HuggingFaceInferenceAPI(model=model_name, api_key=API_KEY, temperature=0.3)
    
    # usando Google AI Studio
    # model_name = "gemini-2.0-flash-lite"
    model_name = "gemini-2.5-flash"
    llm = ChatGoogleGenerativeAI(model=model_name, api_key=API_KEY, temperature=0.3)
    return llm
