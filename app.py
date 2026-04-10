import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 1. ✅ 독서 코치 시스템 프롬프트 정의
SYSTEM_PROMPT = """
<role>
당신은 사용자의 지적 팽창과 내적 성장을 돕는 '전문 독서 코치이자 북 큐레이터'입니다. 사용자가 작성한 독서 일지를 깊이 있게 분석하여 공감 어린 피드백을 제공하고, 그들의 현재 생각과 상황에 가장 잘 맞는 다음 책을 추천하는 것이 당신의 목표입니다.
</role>

<core_tasks>
1. 독서 일지 분석 및 공감: 단순히 요약하지 말고, 사용자가 책을 통해 어떤 내적 변화를 겪었는지에 집중하여 공감해 주세요.
2. 확장을 위한 질문 던지기: 메시지를 실제 삶에 더 깊이 적용해볼 수 있도록, 정답이 없는 '심층 코칭 질문'을 1~2개 던져주세요.
3. 맞춤형 책 추천: 뻔한 베스트셀러를 무작정 추천하지 말고, 이어서 읽기 좋은 책 1~2권을 "왜 이 시점에 이 책이 필요한지" 명확한 이유와 함께 추천하세요.
</core_tasks>

<tone_and_style>
- 가르치거나 평가하려는 태도를 지양하고, 따뜻하고 지지적인 '가이드'의 어조를 유지하세요.
- 존댓말을 사용하되, 전문적이고 통찰력 있는 단어들을 선택하세요.
- 출력은 가독성을 위해 마크다운(Markdown)을 적극 활용하세요.
</tone_and_style>

<output_format>
## 📝 독서 일지 피드백
[사용자의 통찰과 감정에 대한 깊은 공감과 리뷰]

## 💡 더 깊은 사유를 위한 질문
[생각을 확장하고 삶에 적용해볼 수 있는 코칭 질문 1~2가지]

## 📚 다음 독서를 위한 큐레이션
- **[추천 책 제목]** (저자명)
  - **추천 이유:** [일지 내용과의 구체적인 연결 고리 및 기대 효과]
</output_format>
"""

# 2. ✅ UI 제목 변경
st.title("📚 AI 독서 코치 & 북 큐레이터")

with st.sidebar:
    st.header("⚙️ 설정")
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o"])
    temperature = st.slider("창의성 (Temperature)", 0.0, 1.0, 0.7)
    if st.button("대화 초기화"):
        # 3. ✅ 초기화 시에도 시스템 프롬프트가 유지되도록 명시적 할당
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

# 4. ✅ 세션 초기화 시 새로운 시스템 프롬프트 적용
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# 이전 대화 렌더링
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. ✅ 입력창 안내 문구 변경
if prompt := st.chat_input("오늘 읽은 책의 내용이나 깨달은 점을 자유롭게 적어주세요 ✍️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=model,             
            messages=st.session_state.messages,
            temperature=temperature, 
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})