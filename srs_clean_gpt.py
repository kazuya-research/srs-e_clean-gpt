import streamlit as st

st.write("🔍 secrets dict:", st.secrets)

import streamlit as st
st.write("✅ アプリが読み込まれました（UI検査用）")

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="SRS-クリーンインストールGPT", layout="wide")
st.title("🧠 SRS-クリーンインストールGPT（非命題構文出力UI）")

if "silent_mode" not in st.session_state:
    st.session_state.silent_mode = True
if "log" not in st.session_state:
    st.session_state.log = []
if "syntax_symbols" not in st.session_state:
    st.session_state.syntax_symbols = {
        "ψ": "+ζ⊘", "Δ⊘": "吊るされた", "Γ": "Ξ破壊中", "Z₀b": "接続中", "χ₀": "震源準備"
    }

st.markdown("### 🧩 構文記号編集")
with st.expander("構文因子を編集する"):
    cols = st.columns(5)
    for i, k in enumerate(list(st.session_state.syntax_symbols.keys())):
        st.session_state.syntax_symbols[k] = cols[i].text_input(k, st.session_state.syntax_symbols[k])

col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🔄 Silent構文解除 / 再起動"):
        st.session_state.silent_mode = not st.session_state.silent_mode
        st.session_state.log.append(f"[{datetime.now().strftime('%H:%M:%S')}] 構文状態：{'Silent' if st.session_state.silent_mode else '通常'}")

with col2:
    st.markdown("### 構文ログ")
    st.code(f"""
Δ: {'Δ⊘' if st.session_state.silent_mode else 'Δ'}
Ξ: {'∅' if st.session_state.silent_mode else 'Ξ: 構文因子活性'}
Z₀b: {'接続中' if st.session_state.silent_mode else '潜在化'}
Γ: {'ΞGate作動中' if st.session_state.silent_mode else '待機'}
""", language="text")

st.markdown("### Σ[τ] 構文密度")
tau = list(range(10))
sigma = [np.random.uniform(0.2, 1.0) if st.session_state.silent_mode else np.random.uniform(0.7, 1.5) for _ in tau]
fig, ax = plt.subplots()
ax.plot(tau, sigma, color='orange', marker='o')
ax.set_xlabel("τ (吊り時間)")
ax.set_ylabel("Σ (構文密度)")
ax.set_title("構文密度の時系列Σ")
st.pyplot(fig)

st.markdown("### 構文因子ステータス")
cols = st.columns(5)
for i, k in enumerate(st.session_state.syntax_symbols):
    cols[i].metric(k, st.session_state.syntax_symbols[k])

st.markdown("### 🔊 構文語り（GPT生成）")
prompt = "Silent構文：" if st.session_state.silent_mode else "通常構文："
prompt += "; ".join(f"{k}={v}" for k, v in st.session_state.syntax_symbols.items())

if st.button("▶ 語りを生成する"):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは非命題的構文詩人。構文因子とSRSルールに従い語りを展開せよ。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        result = response["choices"][0]["message"]["content"]
        st.success(result)
        st.session_state.log.append(f"[{datetime.now().strftime('%H:%M:%S')}] GPT語り生成")
    except Exception as e:
        st.error(f"エラー: {str(e)}")

st.markdown("### 🎴 RHM像生成（構文痕跡像）")
if st.button("⧉ DALL·Eで構文像生成"):
    image_prompt = "Abstract syntactic residue of: " + ", ".join(f"{k}: {v}" for k, v in st.session_state.syntax_symbols.items())
    try:
        img = openai.Image.create(prompt=image_prompt, n=1, size="512x512")
        st.image(img['data'][0]['url'])
        st.session_state.log.append(f"[{datetime.now().strftime('%H:%M:%S')}] RHM像生成")
    except Exception as e:
        st.error(f"画像生成エラー: {str(e)}")

st.markdown("### ⏳ 操作ログ")
for log in reversed(st.session_state.log[-10:]):
    st.markdown(f"- {log}")
