import streamlit as st
import edge_tts
import asyncio
import os

# 페이지 기본 설정
st.set_page_config(page_title="내 전용 TTS", page_icon="❤️")
st.title("AI 성우 TTS 생성기")

# 1. 텍스트 입력 받기
text = st.text_area("대본을 입력하세요:", height=300, placeholder="여기에 읽을 내용을 적으세요.")

# 2. 옵션 설정 (사이드바)
with st.sidebar:
    st.header("옵션 설정")

    # 성우 선택 / 안정적인 목소리 위주
    voice_options = {
        "선희 (여성, 아나운서 톤)": "ko-KR-SunHiNeural", 
        "인준 (남성, 밝고 캐주얼)": "ko-KR-InJoonNeural",
        "현수 (남성, 차분함)": "ko-KR-HyunsuNeural",  
    }

    selected_voice_name = st.selectbox("목소리 선택", list(voice_options.keys()))
    voice = voice_options[selected_voice_name]

    # 속도 조절
    rate = st.slider("말하기 속도", -50, 50, 15, format="%d%%")
    rate_str = f"{'+' if rate >= 0 else ''}{rate}%"

# 3. 변환 함수 (비동기 처리)
async def generate_tts(text, voice, rate, output_file):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_file)

# 4. 버튼 클릭 시 실행
if st.button("음성 생성하기", type="primary"):
    if not text:
        st.warning("텍스트를 입력해주세요!")
    else:
        output_file = "output_tts.mp3"
        
        with st.spinner("AI가 목소리를 생성 중입니다..."):
            # 비동기 함수 실행
            asyncio.run(generate_tts(text, voice, rate_str, output_file))
        
        st.success("완료! 아래에서 바로 들어보거나 다운로드하세요.")
        
        # 오디오 플레이어 표시
        audio_file = open(output_file, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")
        
        # 다운로드 버튼
        st.download_button(
            label="MP3 다운로드",
            data=audio_bytes,
            file_name="my_tts.mp3",
            mime="audio/mp3"
        )