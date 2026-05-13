import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="오픈소스 고인물 판독기", page_icon="💻", layout="wide")

st.markdown("###  20222204043 채민성")
st.divider()

@st.cache_data
def load_quiz_data():
    print(">> [서버 로그] 퀴즈 데이터를 불러옵니다...")
    time.sleep(3)
    return [
        {"q": "1. 수정한 파일을 다음 버전에 반영할 파일 후보(Stage)로 올리는 Git 명령어는?", "options": ["git init", "git add", "git commit", "git push"], "answer": "git add"},
        {"q": "2. Markdown에서 가장 큰 제목(Heading 1)을 만들 때 사용하는 기호는?", "options": ["#", "##", "###", "**"], "answer": "#"},
        {"q": "3. Streamlit에서 데이터를 캐싱하여 앱 속도를 높일 때 사용하는 데코레이터는?", "options": ["@st.save", "@st.cache_data", "@st.memory", "@st.fast"], "answer": "@st.cache_data"},
        {"q": "4. 원격 저장소(github)의 변경 사항을 로컬로 가져와 병합하는 명령어는?", "options": ["git push", "git clone", "git pull", "git status"], "answer": "git pull"},
        {"q": "5. Streamlit에서 화면을 좌우 단으로 나눌 때 사용하는 함수는?", "options": ["st.split()", "st.columns()", "st.sidebar()", "st.container()"], "answer": "st.columns()"}
    ]

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'quiz_submitted' not in st.session_state:
    st.session_state['quiz_submitted'] = False
if 'score' not in st.session_state:
    st.session_state['score'] = 0

if not st.session_state['logged_in']:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.title(" 오픈소스 실습 시스템")
        st.info("테스트 계정으로 로그인해주세요. (ID: admin / PW: 1234)")
        
        with st.form("login_form"):
            user_id = st.text_input("아이디")
            user_pw = st.text_input("비밀번호", type="password")
            submit_btn = st.form_submit_button("로그인")
            
            if submit_btn:
                print(f">> [서버 로그] 누군가 로그인 시도 중... 입력 ID: {user_id}")
                if user_id == "admin" and user_pw == "1234":
                    st.session_state['logged_in'] = True
                    print(">> [서버 로그] 관리자 로그인 성공!")
                    st.success("로그인 성공!")
                    time.sleep(0.5) 
                    st.rerun()
                else:
                    print(">> [서버 로그] 로그인 실패: 정보 불일치")
                    st.error("아이디 또는 비밀번호가 틀렸습니다.")

else:
    with st.sidebar:
        st.header("👤 내 프로필")
        st.write("**이름:** 채민성")
        st.write("**학번:** 2022204043")
        st.write("**상태:** 접속됨 🟢")
        st.divider()
        if st.button("로그아웃", use_container_width=True):
            print(">> [서버 로그] 사용자가 로그아웃 버튼을 클릭했습니다.")
            st.session_state.clear() 
            st.rerun()

    st.title(" 오픈소스 실습 고인물 판독기")
    
    with st.spinner("퀴즈 데이터를 불러오는 중입니다... (최초 1회만 로딩)"):
        quiz_data = load_quiz_data()
    
    if not st.session_state['quiz_submitted']:
        st.success("데이터 로딩 완료! (캐싱 적용됨)")
        st.write("아래 5문제를 풀고 점수를 확인해보세요.")
        
        st.progress(50, text="진행 중...")
        
        with st.form("quiz_form"):
            user_answers = []
            for idx, item in enumerate(quiz_data):
                st.subheader(item["q"])
                answer = st.radio("정답 선택:", item["options"], key=f"q_{idx}")
                user_answers.append(answer)
                st.write("---")
                
            submit_quiz = st.form_submit_button("제출하기")
            
            if submit_quiz:
                current_score = 0
                for i in range(len(quiz_data)):
                    if user_answers[i] == quiz_data[i]["answer"]:
                        current_score += 1
                
                print(f">> [서버 로그] 사용자가 퀴즈를 제출했습니다. 획득 점수: {current_score}점")
                st.session_state['score'] = current_score
                st.session_state['quiz_submitted'] = True
                st.rerun()
                
    else: 
        score = st.session_state['score']
        total = len(quiz_data)
        
        st.header(" 결과 확인")
        
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.metric(label="내 점수", value=f"{score} / {total} 점")
            if score == total:
                st.balloons()
                st.success("🎉 만점입니다! 수업을 정말 열심히 들으셨네요!")
            elif score >= 3:
                st.warning("🙂 훌륭합니다. 복습만 조금 더 하면 완벽하겠어요.")
            else:
                st.error("😭 수업 자료를 다시 한번 확인해 보시는 게 좋겠습니다.")
                
            if st.button("다시 풀기"):
                print(">> [서버 로그] 사용자가 '다시 풀기' 버튼을 클릭했습니다.")
                st.session_state['quiz_submitted'] = False
                st.rerun()
                
        with res_col2:
            st.write("**[ 내 점수 vs 전체 평균 ]**")
            chart_data = pd.DataFrame({
                "점수": [score, 2.5], 
                "비교": ["내 점수", "수강생 평균(가정)"]
            }).set_index("비교")
            st.bar_chart(chart_data)
