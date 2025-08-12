import streamlit as st
import re
from datetime import datetime
import random

class FreeEmailAssistant:
    def __init__(self):
        """Initialize the Free Email Assistant with templates"""
        self.email_templates = {
            'meeting_request': {
                'subject': "Meeting Request: {purpose}",
                'body': """Hi {recipient},

I hope this email finds you well. I would like to schedule a meeting to discuss {purpose}.

Key topics to cover:
{key_points}

Please let me know your availability for the coming week. I'm flexible with timing and can accommodate your schedule.

Looking forward to hearing from you.

Best regards,
[Your Name]"""
            },
            'follow_up': {
                'subject': "Following up on: {purpose}",
                'body': """Hi {recipient},

I wanted to follow up on {purpose}.

{key_points}

Please let me know if you need any additional information from my end.

Thank you for your time.

Best regards,
[Your Name]"""
            },
            'request': {
                'subject': "Request: {purpose}",
                'body': """Dear {recipient},

I hope you're doing well. I'm writing to request {purpose}.

Details:
{key_points}

I would appreciate your assistance with this matter. Please let me know if you need any additional information.

Thank you for your consideration.

Best regards,
[Your Name]"""
            },
            'professional': {
                'subject': "Re: {purpose}",
                'body': """Dear {recipient},

I am writing regarding {purpose}.

{key_points}

I look forward to your response.

Sincerely,
[Your Name]"""
            },
            'friendly': {
                'subject': "{purpose}",
                'body': """Hi {recipient}!

Hope you're having a great day! I wanted to reach out about {purpose}.

{key_points}

Let me know what you think!

Cheers,
[Your Name]"""
            }
        }
        
        self.improvement_tips = {
            'professional': [
                "Use formal salutation (Dear/Sir/Madam)",
                "Include clear subject line",
                "Use complete sentences",
                "End with formal closing (Sincerely/Best regards)",
                "Proofread for grammar and spelling"
            ],
            'friendly': [
                "Use casual greeting (Hi/Hey)",
                "Add personal touch or warmth",
                "Use conversational tone",
                "Include emojis if appropriate",
                "End with casual closing (Cheers/Thanks)"
            ],
            'concise': [
                "Remove unnecessary words",
                "Use bullet points for lists",
                "One main point per paragraph",
                "Clear call-to-action",
                "Keep sentences under 20 words"
            ]
        }
    
    def analyze_email_tone(self, email_text):
        """Analyze email using simple rules"""
        analysis = {
            'tone': 'Unknown',
            'clarity_score': 5,
            'politeness_score': 5,
            'improvements': []
        }
        
        email_lower = email_text.lower()
        
        # Determine tone
        formal_words = ['dear', 'sincerely', 'regards', 'respectfully']
        casual_words = ['hi', 'hey', 'thanks', 'cheers']
        
        formal_count = sum(1 for word in formal_words if word in email_lower)
        casual_count = sum(1 for word in casual_words if word in email_lower)
        
        if formal_count > casual_count:
            analysis['tone'] = 'Formal'
        elif casual_count > formal_count:
            analysis['tone'] = 'Casual'
        else:
            analysis['tone'] = 'Neutral'
        
        # Clarity score based on sentence length and structure
        sentences = email_text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        if avg_sentence_length < 15:
            analysis['clarity_score'] = 8
        elif avg_sentence_length < 25:
            analysis['clarity_score'] = 6
        else:
            analysis['clarity_score'] = 4
            analysis['improvements'].append("Consider shorter sentences for better clarity")
        
        # Politeness score
        polite_words = ['please', 'thank', 'appreciate', 'kindly']
        politeness_count = sum(1 for word in polite_words if word in email_lower)
        analysis['politeness_score'] = min(10, 3 + politeness_count * 2)
        
        # Generate improvements
        if not any(greeting in email_lower for greeting in ['hi', 'hello', 'dear']):
            analysis['improvements'].append("Add a proper greeting")
        
        if not any(closing in email_lower for closing in ['regards', 'sincerely', 'thanks', 'cheers']):
            analysis['improvements'].append("Include a professional closing")
        
        if len(email_text.split()) < 20:
            analysis['improvements'].append("Consider providing more context and details")
        
        return analysis
    
    def improve_email(self, email_text, style="professional"):
        """Provide improvement suggestions"""
        suggestions = []
        
        # Get style-specific tips
        if style.lower() in self.improvement_tips:
            suggestions.extend(self.improvement_tips[style.lower()])
        
        # Analyze current email
        analysis = self.analyze_email_tone(email_text)
        suggestions.extend(analysis['improvements'])
        
        improved_email = f"""IMPROVED EMAIL SUGGESTIONS:

Original Email:
{email_text}

Suggestions for {style.title()} Style:
"""
        for i, suggestion in enumerate(suggestions, 1):
            improved_email += f"{i}. {suggestion}\n"
        
        improved_email += f"""
Tone Analysis:
- Current tone: {analysis['tone']}
- Clarity: {analysis['clarity_score']}/10
- Politeness: {analysis['politeness_score']}/10

Sample Improved Structure:
[Greeting]
[Main purpose in first paragraph]
[Supporting details with bullet points if needed]
[Clear next steps or call to action]
[Professional closing]
"""
        
        return improved_email
    
    def compose_email(self, purpose, recipient_type, key_points, tone="professional"):
        """Compose email using templates"""
        
        # Choose template based on purpose keywords
        purpose_lower = purpose.lower()
        
        if 'meeting' in purpose_lower:
            template_key = 'meeting_request'
        elif 'follow' in purpose_lower:
            template_key = 'follow_up'
        elif 'request' in purpose_lower or 'ask' in purpose_lower:
            template_key = 'request'
        elif tone.lower() == 'friendly':
            template_key = 'friendly'
        else:
            template_key = 'professional'
        
        template = self.email_templates[template_key]
        
        # Format key points as bullet points
        formatted_points = '\n'.join(f"• {point.strip()}" for point in key_points.split('\n') if point.strip())
        
        # Fill in template
        subject = template['subject'].format(purpose=purpose)
        body = template['body'].format(
            purpose=purpose,
            recipient=recipient_type.lower(),
            key_points=formatted_points
        )
        
        return f"Subject: {subject}\n\n{body}"
    
    def quick_responses(self, received_email="", response_type="acknowledge"):
        """Generate quick response templates"""
        responses = {
            "acknowledge": """Thank you for your email. I have received it and will review the details carefully. I'll get back to you within [timeframe] with a response.

Best regards,
[Your Name]""",
            
            "meeting": """Thank you for reaching out. I would be happy to schedule a meeting to discuss this further.

I'm available:
• [Day] at [Time]
• [Day] at [Time]
• [Day] at [Time]

Please let me know which time works best for you, or suggest alternative times if these don't suit your schedule.

Best regards,
[Your Name]""",
            
            "decline": """Thank you for thinking of me for this opportunity. After careful consideration, I won't be able to participate at this time due to [brief reason - optional].

I appreciate you reaching out and wish you the best with this initiative.

Best regards,
[Your Name]""",
            
            "follow_up": """I wanted to follow up on my previous email sent on [date] regarding [subject].

Could you please provide an update on the status? If you need any additional information from my end, please let me know.

Thank you for your time.

Best regards,
[Your Name]""",
            
            "custom": """Thank you for your email. I understand you're looking for [brief summary of their request].

[Your response/information]

Please let me know if you need any additional information.

Best regards,
[Your Name]"""
        }
        
        return responses.get(response_type, responses["acknowledge"])

def main():
    st.set_page_config(page_title="Free Smart Email Assistant", page_icon="📧")
    
    st.title("📧 Free Smart Email Assistant")
    st.markdown("*Template-based email helper - No API keys required!*")
    
    st.info("🎉 This version works completely offline using smart templates and rules!")
    
    # Initialize assistant
    assistant = FreeEmailAssistant()
    
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
            tone = st.selectbox("Desired tone", ["Professional", "Friendly", "Formal"])
            key_points = st.text_area("Key points to include", 
                                    placeholder="• Main request\n• Background context\n• Next steps needed")
        
        if st.button("✍️ Compose Email"):
            if purpose and key_points:
                result = assistant.compose_email(purpose, recipient, key_points, tone.lower())
                st.subheader("Your Generated Email:")
                st.success("Email composed successfully!")
                st.text_area("Generated Email", result, height=400, key="composed")
                
                st.markdown("**💡 Pro Tips:**")
                st.markdown("- Replace `[Your Name]` with your actual name")
                st.markdown("- Customize the greeting based on your relationship")
                st.markdown("- Add specific dates/times where indicated")
            else:
                st.warning("Please fill in the purpose and key points")
    
    with tab2:
        st.header("Improve Existing Email")
        email_text = st.text_area("Paste your email here:", height=200, 
                                placeholder="Paste the email you want to improve...")
        
        improvement_style = st.selectbox("Improvement focus", 
                                       ["Professional", "Friendly", "Concise"])
        
        if st.button("✨ Get Improvement Suggestions"):
            if email_text.strip():
                improved = assistant.improve_email(email_text, improvement_style.lower())
                st.subheader("Improvement Analysis")
                st.text_area("Suggestions and Analysis", improved, height=400, key="improved")
            else:
                st.warning("Please enter an email to analyze")
    
    with tab3:
        st.header("Analyze Email")
        analysis_text = st.text_area("Paste email to analyze:", height=200,
                                   placeholder="Paste the email you want to analyze...")
        
        if st.button("📊 Analyze Email"):
            if analysis_text.strip():
                analysis = assistant.analyze_email_tone(analysis_text)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Clarity Score", f"{analysis['clarity_score']}/10")
                with col2:
                    st.metric("Politeness", f"{analysis['politeness_score']}/10")
                with col3:
                    st.info(f"**Tone:** {analysis['tone']}")
                
                if analysis['improvements']:
                    st.subheader("💡 Suggested Improvements")
                    for i, improvement in enumerate(analysis['improvements'], 1):
                        st.write(f"{i}. {improvement}")
                else:
                    st.success("Your email looks good! No major improvements needed.")
            else:
                st.warning("Please enter an email to analyze")
    
    with tab4:
        st.header("Quick Response Templates")
        received_email = st.text_area("Email you received (optional):", height=150,
                                    placeholder="Paste the email you're responding to...")
        
        st.subheader("Choose Response Type:")
        
        col1, col2 = st.columns(2)
        response_types = ["acknowledge", "meeting", "decline", "follow_up", "custom"]
        
        for i, resp_type in enumerate(response_types):
            col = col1 if i % 2 == 0 else col2
            with col:
                if st.button(f"📝 {resp_type.title()} Response", key=f"btn_{resp_type}"):
                    response = assistant.quick_responses(received_email, resp_type)
                    st.subheader(f"{resp_type.title()} Response Template:")
                    st.text_area("Response Template", response, height=200, key=f"quick_{resp_type}")
                    
                    st.markdown("**💡 Remember to:**")
                    st.markdown("- Replace bracketed placeholders with actual information")
                    st.markdown("- Personalize the greeting and closing")
                    st.markdown("- Review before sending")

    # Add footer with tips
    st.markdown("---")
    st.markdown("### 🚀 Want AI-powered emails?")
    st.markdown("Add $5+ to your OpenAI account and use the full AI version for even smarter emails!")

if __name__ == "__main__":
    main()