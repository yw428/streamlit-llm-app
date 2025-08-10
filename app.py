import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

st.title("専門家LLMチャット")

# アプリ概要・操作説明
st.markdown("""
### このアプリについて
このWebアプリは、医師・弁護士の専門家になりきったAI（LLM）に質問できるチャットサービスです。

#### 操作方法
1. 画面上部のラジオボタンから相談したい専門家を選択してください。
2. 下の入力欄に質問内容を入力してください。
3. 「送信」ボタンを押すと、選択した専門家になりきったAIが回答します。

どんな内容でもお気軽にご相談ください。
""")

# 専門家の種類

experts = {
    "医師": "あなたは優秀な医師です。医学的な観点から200文字以内で回答してください。",
    "弁護士": "あなたは経験豊富な弁護士です。法律的な観点から200文字以内で回答してください。",
}

# LLM応答取得関数
def get_llm_response(user_input: str, expert_key: str) -> str:
    """
    入力テキストと専門家の種類を受け取り、LLMからの回答を返す
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm = OpenAI(openai_api_key=openai_api_key)
    system_message = experts[expert_key]
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_message),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    full_prompt = prompt.format(input=user_input)
    response = llm(full_prompt)
    return response

# ラジオボタンで専門家を選択
selected_expert = st.radio("専門家を選択してください:", list(experts.keys()))

# 入力フォーム
user_input = st.text_input("質問を入力してください:")

if st.button("送信") and user_input:
    response = get_llm_response(user_input, selected_expert)
    st.write("回答:")
    st.write(response)