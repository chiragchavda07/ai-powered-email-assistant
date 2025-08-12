import openai
import streamlit as st
import json
from datetime import datetime
import re

class EmailAssistant:
    def __init__(self, api_key):
        """Initialize the Email Assistant with OpenAI API key"""
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
    
    def analyze_email_tone(self, email_text):
        """Analyze the tone and professionalism of an email"""
        prompt = f"""
        Analyze this email for:
        1. Tone (professional, casual, friendly, formal, etc.)
        2. Clarity score (1-10)
        3. Politeness level (1-10)
        4. Potential improvements
        
        Email: {email_text}
        
        Respond in JSON format with keys: tone, clarity_score, politeness_score, improvements
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Failed to analyze email: {str(e)}"}
    
    def improve_email(self, email_text, style="professional"):
        """Improve an email's clarity and tone"""
        prompt = f"""
        Improve this email to be more {style}. Keep the core message but enhance:
        - Clarity and structure
        - Appropriate tone
        - Grammar and flow
        - Politeness
        
        Original email: {email_text}
        
        Return only the improved email text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Failed to improve email: {str(e)}"
    
    def compose_email(self, purpose, recipient_type, key_points, tone="professional"):
        """Compose a new email from scratch"""
        prompt = f"""
        Compose an email with these details:
        - Purpose: {purpose}
        - Recipient: {recipient_type} 
        - Key points to include: {key_points}
        - Tone: {tone}
        
        Create a complete email with subject line and body.
        Format as:
        Subject: [subject line]
        
        [email body]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Failed to compose email. Error: {str(e)}"

    def quick_responses(self, received_email, response_type="acknowledge"):
        """Generate quick response templates"""
        responses = {
            "acknowledge": "Thank you for your email. I've received it and will get back to you shortly.",
            "meeting": "Thank you for reaching out. I'm available for a meeting. Please let me know what times work best for you.",
            "decline": "Thank you for thinking of me. Unfortunately, I won't be able to participate at this time.",
            "follow_up": "I wanted to follow up on my previous email. Please let me know if you need any additional information."
        }
        
        if response_type in responses:
            return responses[response_type]
        
        # AI-generated custom response
        prompt = f"""
        Generate a brief, polite response to this email:
        {received_email}
        
        Response type: {response_type}
        Keep it short and professional.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return responses.get("acknowledge", "Thank you for your email.")

def get_api_key():
    """Get API key from Streamlit secrets only"""
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        if api_key and api_key != "your_actual_openai_api_key_here":
            return api_key
    except KeyError:
        st.error("OpenAI API key not found in Streamlit secrets!")
        st.info("Please add your OpenAI API key to Streamlit secrets configuration.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading API key: {str(e)}")
        st.stop()

def main():
    st.set_page_config(page_title="Smart Email Assistant", page_icon="📧")
    
    st.title("📧 Smart Email Assistant")
    st.markdown("*Your AI-powered email companion for better communication*")
    
    # Get API key from secrets only
    api_key = get_api_key()
    
    # Initialize assistant
    assistant = EmailAssistant(api_key)
    
    # Main interface
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Compose", "✨ Improve", "📊 Analyze", "⚡ Quick Reply"])
    
    with tab1:
        st.header("Compose New Email")
        col1, col2 = st.columns(2)
        
        with col1:
            purpose = st.text_input("What's the purpose of this email?", 
                                  placeholder="e.g., Request a meeting, Follow up on proposal")
            recipient = st.selectbox("Who are you writing to?", 
                                   ["Colleague", "Boss/Manager", "Client", "Friend", "Customer", "Other"])
        
        with col2:
            tone = st.selectbox("Desired tone", ["Professional", "Friendly", "Formal", "Casual"])
            key_points = st.text_area("Key points to include", 
                                    placeholder="- Main request\n- Background context\n- Next steps needed")
        
        if st.button("✍️ Compose Email"):
            if purpose and key_points:
                with st.spinner("Composing your email..."):
                    result = assistant.compose_email(purpose, recipient, key_points, tone.lower())
                    st.subheader("Your Generated Email:")
                    
                    if "Failed to compose email" in result:
                        st.error(result)
                    else:
                        st.success("Email composed successfully!")
                        st.text_area("Generated Email", result, height=300, key="composed")
            else:
                st.warning("Please fill in the purpose and key points")
    
    with tab2:
        st.header("Improve Existing Email")
        email_text = st.text_area("Paste your email here:", height=200, 
                                placeholder="Paste the email you want to improve...")
        
        col1, col2 = st.columns(2)
        with col1:
            improvement_style = st.selectbox("Improvement style", 
                                           ["Professional", "Friendly", "Concise", "Detailed"])
        
        if st.button("✨ Improve Email"):
            if email_text.strip():
                with st.spinner("Improving your email..."):
                    improved = assistant.improve_email(email_text, improvement_style.lower())
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Original")
                        st.text_area("Original Email", email_text, height=250, key="original", disabled=True)
                    with col2:
                        st.subheader("Improved")
                        st.text_area("Improved Email", improved, height=250, key="improved")
            else:
                st.warning("Please enter an email to improve")
    
    with tab3:
        st.header("Analyze Email")
        analysis_text = st.text_area("Paste email to analyze:", height=200,
                                   placeholder="Paste the email you want to analyze...")
        
        if st.button("📊 Analyze Email"):
            if analysis_text.strip():
                with st.spinner("Analyzing email..."):
                    analysis = assistant.analyze_email_tone(analysis_text)
                    
                    if "error" not in analysis:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Clarity Score", f"{analysis.get('clarity_score', 'N/A')}/10")
                        with col2:
                            st.metric("Politeness", f"{analysis.get('politeness_score', 'N/A')}/10")
                        with col3:
                            st.info(f"**Tone:** {analysis.get('tone', 'Unknown')}")
                        
                        if 'improvements' in analysis:
                            st.subheader("💡 Suggested Improvements")
                            st.write(analysis['improvements'])
                    else:
                        st.error("Failed to analyze email. Please try again.")
            else:
                st.warning("Please enter an email to analyze")
    
    with tab4:
        st.header("Quick Responses")
        received_email = st.text_area("Email you received (optional):", height=150,
                                    placeholder="Paste the email you're responding to...")
        
        col1, col2 = st.columns(2)
        response_types = ["acknowledge", "meeting", "decline", "follow_up", "custom"]
        
        for i, resp_type in enumerate(response_types):
            col = col1 if i % 2 == 0 else col2
            with col:
                if st.button(f"📝 {resp_type.title()} Response"):
                    with st.spinner(f"Generating {resp_type} response..."):
                        response = assistant.quick_responses(received_email, resp_type)
                        st.subheader(f"{resp_type.title()} Response:")
                        st.text_area("Quick Response", response, height=100, key=f"quick_{resp_type}")

if __name__ == "__main__":
    main()
