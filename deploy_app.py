import openai
import streamlit as st
import configparser
import tiktoken

# config.iniからAPIキーを取得
# config = configparser.ConfigParser()
# config.read('config.ini')
# api_key = config['OpenAI']['API_KEY']
openai.api_key = st.secrets.OpenAI.API_KEY

st.title("ChatGPT風 AIチャットアプリ")

# openai.api_key = api_key ←ここを消せていなかった…

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.inquiry_messages = []  # 問い合わせ用の履歴

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  # エンコーディングの設定

# 表示
for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.inquiry_messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        role = "assistant"

        # ヒストリーのトークン数を管理
        total_tokens = 0
        for m in st.session_state.inquiry_messages:
            total_tokens += len(encoding.encode(m['content']))

        while total_tokens > 1000:
            removed_message = st.session_state.inquiry_messages.pop(0)
            total_tokens -= len(encoding.encode(removed_message['content']))

        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.inquiry_messages,
            stream=True,
            temperature=0.1,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
            if "role" in response.choices[0].delta:
                role = response.choices[0].delta["role"]
        st.session_state.messages.append({"role": role, "content": full_response})
        st.session_state.inquiry_messages.append({"role": role, "content": full_response})

        # Debug用: 問い合わせ履歴とそのトークン数
        print("Inquiry Messages: ", st.session_state.inquiry_messages)
        print("Total Tokens: ", total_tokens)
