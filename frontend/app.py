import streamlit as st
import requests

API = "http://127.0.0.1:8000/interview"

st.set_page_config(page_title="AI Interview Prep", layout="centered")
st.title("🤖 AI Interview Prep — Mock Interview")

if "session" not in st.session_state:
    st.session_state["session"] = None

with st.form("start_form"):
    name = st.text_input("Your name")
    role = st.selectbox("Role", ["Software Engineer","Product Manager","Data Analyst","Other"])
    domain = st.text_input("Domain (optional): e.g., backend, frontend, ml")
    experience = st.selectbox("Experience", ["0-1 years","1-3 years","3+ years"])
    mode = st.selectbox("Mode", ["technical","behavioral"])
    start = st.form_submit_button("Start Mock Interview")

if start:
    payload = {"name": name or "Anonymous", "role": role, "domain": domain, "experience": experience, "mode": mode}
    res = requests.post(f"{API}/start", json=payload)
    if res.status_code == 200:
        st.session_state["session"] = res.json()
        st.success("Session started! Scroll down for questions.")
    else:
        st.error("Failed to start session: " + res.text)

if st.session_state["session"]:
    session = st.session_state["session"]
    sid = session["session_id"]
    st.subheader("Questions")
    for q in session["questions"]:
        st.write(f"**Q{q['id']}.** {q['question']}")
        ans_key = f"ans_{q['id']}"
        if ans_key not in st.session_state:
            st.session_state[ans_key] = ""
        st.session_state[ans_key] = st.text_area(f"Your answer for Q{q['id']}", key=ans_key, height=120)
        cols = st.columns(3)
        if cols[0].button("Submit", key=f"submit_{q['id']}"):
            with st.spinner("Evaluating answer..."):
                payload = {"question_id": q['id'], "answer": st.session_state[ans_key]}
                resp = requests.post(f"{API}/session/{sid}/answer", json=payload)
                if resp.status_code == 200:
                    st.success("Received feedback:")
                    st.json(resp.json())
                else:
                    st.error("Evaluation failed: " + resp.text)
        if cols[1].button("Skip", key=f"skip_{q['id']}"):
            st.warning("Skipped question.")
        if cols[2].button("Retry", key=f"retry_{q['id']}"):
            st.info("Edit your answer above and press Submit again.")

    if st.button("Finish & Get Report"):
        with st.spinner("Generating final report..."):
            r = requests.post(f"{API}/session/{sid}/finalize")
            if r.status_code == 200:
                st.success("Final Report")
                st.json(r.json())
            else:
                st.error("Finalize failed: " + r.text)
