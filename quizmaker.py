import streamlit as st
from openai import OpenAI
import os

MODEL = "gpt-4o"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY","sk-proj-H1uWG7XOFeK3GdjgvMiWT3BlbkFJGnyS6bHmduTtQoUNobFA"))

def generate_questions(question_type, num_questions, difficulty, word_list=None):
    if word_list:
        word_list_str = ", ".join(word_list)
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "あなたは経験豊富な英語教師です。生徒に渡すための問題を作成してください。生徒のレベルに合わせた分かりやすい言葉で問題文を作成してください。問題を生成したら最後に答えをつけてください。"},
                {"role": "user", "content": f"{question_type}の形式で、{difficulty}レベルの生徒向けの英単語問題を{num_questions}問作成してください。\問題は、以下の単語リストから出題してください:\n{word_list_str}"}
            ]
        )
    else:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "あなたは経験豊富な英語教師です。生徒に渡すための問題を作成してください。生徒のレベルに合わせた分かりやすい言葉で問題文を作成してください。問題を生成したら最後に答えをつけてください。"},
                {"role": "user", "content": f"{question_type}の形式で、{difficulty}レベルの生徒向けの英単語問題を{num_questions}問作成してください。"}
            ]
        )
    return completion.choices[0].message.content

st.title("英単語問題ジェネレーター")

# 問題形式の選択
question_type = st.selectbox(
    "問題形式を選択してください:",
    ["4択問題", "長文", "穴埋め"]
)

# 問題数の入力
num_questions = st.number_input("問題数を入力してください:", min_value=1, value=10)

# 難易度の選択
difficulty = st.selectbox(
    "難易度を選択してください:",
    ["簡単", "普通", "難しい"]
)

# 単語リストの入力
word_list_str = st.text_area("単語リストを入力してください（カンマ区切り）:", "")
word_list = [word.strip() for word in word_list_str.split(",") if word.strip()]

if st.button("問題生成"):
    if question_type and num_questions and difficulty:
        response = generate_questions(question_type, num_questions, difficulty, word_list)
        st.text_area("アシスタント:", value=response, height=400)
