import streamlit as st
from groq import Groq

# 1. Page & Colorful Layout Style Customization
st.set_page_config(page_title="Universal Study Engine", page_icon="🧬", layout="centered")

# Inject Advanced CSS for multicolor layout and reading contrast overlays
st.markdown("""
    <style>
    /* Dynamic Soft Multicolor Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #E0F7FA 0%, #E8EAF6 40%, #F3E5F5 100%) !important;
    }
    div[data-testid="stWidgetLabel"] p {
        color: #2C3E50 !important;
        font-weight: bold !important;
        font-size: 1.05rem !important;
    }
    .header-box {
        background: linear-gradient(135deg, #FF4B4B, #4A90E2, #9B51E0);
        padding: 24px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.15);
    }
    .header-box h1 { color: white !important; margin: 0; font-size: 2.2rem; }
    .header-box p { color: #f0f2f6 !important; margin: 5px 0 0 0; font-size: 1rem; }
    div[data-baseweb="select"] {
        border: 2px solid #4A90E2 !important;
        border-radius: 8px !important;
        background-color: white !important;
    }
    input {
        border: 2px solid #9B51E0 !important;
        border-radius: 8px !important;
        background-color: white !important;
        color: #2C3E50 !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4A90E2, #9B51E0) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        box-shadow: 0px 4px 10px rgba(155, 81, 224, 0.3) !important;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0px 6px 15px rgba(155, 81, 224, 0.5) !important;
    }
    div[data-testid="stExpander"], div[data-testid="stTabs"] {
        background-color: white !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-box">
        <h1>🧬 Universal AI Study Material Architect</h1>
        <p>Complete Class 5 to Class 12 Educational Practice Sheet Planner</p>
    </div>
""", unsafe_allow_html=True)

# Initialize Secure Groq Cloud Connection utilizing Streamlit Secrets
# This ensures your password key stays completely hidden from the user!
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("🔒 Security Key Error: GROQ_API_KEY must be configured in settings.")
    st.stop()

# 2. Universal Master Curriculum Database Dictionary Map
CLASSES = [f"Class {i}" for i in range(5, 13)]
SUBJECTS = {
    "Primary (5-8)": ["Science", "Mathematics"],
    "Senior (9-12)": ["Physics", "Chemistry", "Biology"]
}

# 3. Selection Interfaces
selected_class = st.selectbox("Select Student Class:", CLASSES)
class_num = int(selected_class.split()[-1])

tier = "Primary (5-8)" if class_num <= 8 else "Senior (9-12)"
selected_subject = st.selectbox("Select Subject Focus:", SUBJECTS[tier])
selected_chapter = st.text_input("Enter Chapter Name:", "Complete Syllabus")

if "exam_ready" not in st.session_state:
    st.session_state.exam_ready = False
    st.session_state.clean_questions = ""
    st.session_state.clean_solutions = ""

if st.button("🚀 Build Tailored Study Material Package"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    all_questions, all_answers = [], []
    
    is_complete = (selected_chapter.lower() == "complete syllabus")
    total_loops = 5 if is_complete else 1
    questions_per_loop = 10 if is_complete else 15
    
    try:
        # ==========================================
        # 🤖 AGENT A: CLOUD BLUEPRINT ANALYSIS
        # ==========================================
        status_text.markdown("🎨 **Agent A:** Fetching competitive framework layouts from the cloud...")
        prompt_a = f"Study the curriculum framework guidelines for {selected_class} {selected_subject}. Output a crisp checklist of format directives for the topic: {selected_chapter}."
        
        completion_a = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt_a}]
        )
        directives = completion_a.choices[0].message.content
        
        # ==========================================
        # 🤖 GENERATION LOOP WAVES
        # ==========================================
        q_start = 1
        for i in range(1, total_loops + 1):
            q_end = q_start + (questions_per_loop - 1)
            status_text.markdown(f"✍️ **Wave 1/2:** Drafting Practice Problems **{q_start} to {q_end}**...")
            
            prompt_q = (
                f"Follow these structural rules:\n{directives}\n\n"
                f"Act as an educational textbook author. Generate exactly {questions_per_loop} tough multiple-choice review exercises for {selected_class} {selected_subject} on the topic '{selected_chapter}'. "
                f"Number them sequentially from {q_start} to {q_end}. Choices A, B, C, D on separate lines. Do not embed any answer lines."
            )
            completion_q = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt_q}]
            )
            all_questions.append(completion_q.choices[0].message.content.strip())
            
            q_start += questions_per_loop
            progress_bar.progress(int((i / total_loops) * 50))
            
        # ==========================================
        # 🧠 WAVE 2: SOLUTIONS ARCHITECT WAVES
        # ==========================================
        st.session_state.clean_questions = "\n\n---\n\n".join(all_questions)
        q_start = 1
        for i in range(1, total_loops + 1):
            q_end = q_start + (questions_per_loop - 1)
            status_text.markdown(f"🔑 **Wave 2/2:** Computing Explanations Manual for Problems **{q_start} to {q_end}**...")
            
            prompt_ans = (
                f"Look closely at these standard tutoring items:\n\n{all_questions[i-1]}\n\n"
                f"Task: Provide the teacher reference tutorial key manual for the review items listed above. "
                f"For each item number from {q_start} to {q_end}, state which option letter (A, B, C, or D) is accurate "
                f"and write a thorough 2-sentence instructional note explaining the concept path clearly."
            )
            completion_a = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt_ans}]
            )
            all_answers.append(completion_a.choices[0].message.content.strip())
            
            q_start += questions_per_loop
            progress_bar.progress(int(50 + ((i / total_loops) * 50)))
        
        status_text.empty()
        st.session_state.clean_solutions = "\n\n---\n\n".join(all_answers)
        st.session_state.exam_ready = True
        progress_bar.empty()
        
    except Exception as e:
        st.error(f"❌ Cloud Execution Slip: {str(e)}")

# 5. Display Layout Tabs Block
if st.session_state.exam_ready:
    st.balloons()
    st.success("✨ Custom Study Package Compiled Successfully!")
    
    tab1, tab2 = st.tabs(["📝 Section 1: Clean Practice Sheet", "🔑 Section 2: Teacher Reference Manual"])
    
    with tab1:
        st.markdown("<h3 style='color: #2C3E50;'>📋 Classroom Review Sheet Details</h3>", unsafe_allow_html=True)
        st.write(st.session_state.clean_questions)
        st.download_button(label="📥 Download Practice Sheet (.txt)", data=st.session_state.clean_questions, file_name=f"{selected_subject}_{selected_class}_Practice.txt", mime="text/plain")
    with tab2:
        st.markdown("<h3 style='color: #2C3E50;'>🔑 Detailed Concept Explanations Manual</h3>", unsafe_allow_html=True)
        st.write(st.session_state.clean_solutions)
        st.download_button(label="📥 Download Tutorial Key (.txt)", data=st.session_state.clean_solutions, file_name=f"{selected_subject}_{selected_class}_TutorialKey.txt", mime="text/plain")
