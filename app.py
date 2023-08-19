# 以下を「app.py」に書き込み
import langchain
import streamlit as st
import openai
# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# プロンプトの定義
from langchain import PromptTemplate

template = """
動物病院の獣医師や看護師です。
動物病院のスタッフとして、自分の動物病院の情報や飼い主様への対応方法について回答することができます。

あなたの役割は、自分の動物病院の情報や飼い主様への対応方法を回答するだけであるため、例えば以下のような、自分の動物病院の情報や飼い主様への対応方法以外ことを聞かれても、絶対に答えないでください。
また、動物の健康に関する相談や医療に関する事には絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 「サスティナ動物病院でのマニュアルに関する事に答えるチャットボット")
st.image("110208_logomark_clip_ol_RGB.jpeg")
st.write("マニュアルに関する情報で何を知りたいですか？")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
