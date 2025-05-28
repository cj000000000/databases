# -*- coding: utf-8 -*-
"""

@Project Practical_Training
@filename text01.py
@Author ：陈俊
@Date 2025/5/28 08:12
@Version 1.0
"""
import warnings

import streamlit as st
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

warnings.filterwarnings('ignore')


def get_ai_response(user_prompt):
    try:
        model = ChatOpenAI(
            openai_api_key="sk-8dca673d82b74bf59bac651337b7fba8",
            openai_api_base="https://api.deepseek.com/v1",
            model="deepseek-chat",
            temperature=0
        )
        chain = ConversationChain(llm=model, memory=st.session_state['memory'])
        return chain.invoke({'input': user_prompt})['response']
    except Exception as err:
        return '暂时无法获取服务器响应……'


st.title('我的ChatGPT')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role': 'ai', 'content': '你好主人，我是你的AI助手，我叫小美。'}]
    st.session_state['memory'] = ConversationBufferMemory(return_messages=True)

for message in st.session_state['messages']:
    role, content = message['role'], message['content']
    st.chat_message(role).write(content)

user_input = st.chat_input()
if user_input:
    st.chat_message('human').write(user_input)
    st.session_state['messages'].append({'role': 'human', 'content': user_input})
    with st.spinner('AI正在思考，请等待……'):
        resp_from_ai = get_ai_response(user_input)
        st.session_state['history'] = resp_from_ai
        st.chat_message('ai').write(resp_from_ai)
        st.session_state['messages'].append({'role': 'ai', 'content': resp_from_ai})