import streamlit as st

def create_chat_interface():

    st.markdown("### 💬 AI Resume Assistant")
    st.markdown("*Ask specific questions about your resume, get career advice, or request improvements*")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message-user">
                <strong>👤 You:</strong><br>{message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message-assistant">
                <strong>🤖 ResumeFit AI:</strong><br>{message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Ask me anything about your resume...",
            placeholder="e.g., How can I improve my resume for this role?"
        )
        send_button = st.form_submit_button("Send 📤")
    
    if send_button and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        
        with st.spinner("🤖 ResumeFit is thinking..."):
            from utils.llm_handler import LLMHandler
            llm_handler = LLMHandler()
            response = llm_handler.chat_response(
                user_input.strip(),
                st.session_state.resume_text,
                st.session_state.job_role,
                st.session_state.chat_history[:-1]
            )
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        st.rerun()
