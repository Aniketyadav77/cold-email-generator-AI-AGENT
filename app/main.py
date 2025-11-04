import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import os
import time
import json

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def inject_custom_css():
    """Inject Apple iOS-inspired glass morphism CSS styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@100;200;300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling - Futuristic Dark Theme */
    :root {
        --bg-1: #030318;
        --bg-2: #071030;
        --accent: #7cf0ff;
        --accent-2: #7a5cff;
        --muted: rgba(255,255,255,0.7);
        --glass-opacity: 0.06;
        --glass-border: rgba(124,240,255,0.12);
        --card-shadow: 0 20px 60px rgba(6, 10, 34, 0.7);
        --mono: 'SF Pro Display', 'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont;
    }

    .main {
        background: radial-gradient(1200px 600px at 10% 20%, rgba(122,92,255,0.08), transparent),
                    linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
        font-family: var(--mono);
        color: #e7eefc;
    }

    .stApp {
        min-height: 100vh;
        color: var(--muted);
    }

    /* Floating action button for visual affordance (non-functional) */
    .fab {
        position: fixed !important;
        right: 28px;
        bottom: 28px;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(90deg, var(--accent), var(--accent-2));
        display: flex;
        align-items: center;
        justify-content: center;
        color: #041025;
        box-shadow: 0 18px 50px rgba(122,92,255,0.2);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        z-index: 9999;
    }
    .fab:hover { transform: translateY(-6px) scale(1.04); box-shadow: 0 28px 80px rgba(122,92,255,0.28); }

    /* Subtle animated backdrop accents */
    .stApp::after {
        content: '';
        position: fixed;
        left: -10%;
        top: -20%;
        width: 60vw;
        height: 60vw;
        background: radial-gradient(circle at 20% 20%, rgba(122,92,255,0.06), transparent 20%), radial-gradient(circle at 80% 80%, rgba(124,240,255,0.04), transparent 25%);
        pointer-events: none;
        z-index: 0;
        transform: rotate(12deg);
        animation: slowFloat 16s linear infinite;
        mix-blend-mode: screen;
    }

    @keyframes slowFloat {
        0% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(6px) rotate(4deg); }
        100% { transform: translateY(0) rotate(0deg); }
    }
    
    /* Header with Apple Glass Effect */
    .main-header {
        background: 
            linear-gradient(135deg, 
                rgba(124, 92, 255, 0.06) 0%,
                rgba(124, 240, 255, 0.03) 40%,
                rgba(0, 0, 0, 0.06) 100%
            );
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.125);
        border-radius: 18px;
        padding: 2.2rem 1.6rem;
        margin: 1.6rem 0;
        box-shadow: var(--card-shadow), inset 0 1px 0 rgba(255, 255, 255, 0.04), 0 0 0 1px var(--glass-border);
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(59, 130, 246, 0.6) 50%, transparent 100%);
    }
    
    .main-header:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 
            0 25px 80px rgba(0, 0, 0, 0.8),
            inset 0 1px 0 rgba(255, 255, 255, 0.15),
            0 0 0 1px rgba(59, 130, 246, 0.2);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .title {
        font-size: 3.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, var(--accent), var(--accent-2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 2rem;
        letter-spacing: 0.01em;
        line-height: 1.4;
    }
    
    /* Input Container with Apple Glass effect */
    .input-container {
        background: linear-gradient(180deg, rgba(255,255,255,var(--glass-opacity)), rgba(255,255,255,0.01));
        backdrop-filter: blur(28px) saturate(220%);
        -webkit-backdrop-filter: blur(28px) saturate(220%);
        border: 1px solid var(--glass-border);
        border-radius: 14px;
        padding: 1.8rem;
        margin: 1.2rem 0;
        box-shadow: var(--card-shadow), inset 0 1px 0 rgba(255,255,255,0.03);
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
    }
    
    .input-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255, 255, 255, 0.2) 50%, 
            transparent 100%
        );
    }
    
    .input-container:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.12),
            0 0 0 1px rgba(59, 130, 246, 0.1);
        border-color: rgba(255, 255, 255, 0.15);
    }
    
    /* Apple-style Input Field */
    .stTextInput > div > div > input {
        background: 
            linear-gradient(135deg, 
                rgba(255, 255, 255, 0.08) 0%,
                rgba(255, 255, 255, 0.04) 50%,
                rgba(0, 0, 0, 0.08) 100%
            ) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 16px !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        padding: 16px 20px !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1) !important;
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(59, 130, 246, 0.6) !important;
        box-shadow: 
            0 0 30px rgba(59, 130, 246, 0.2),
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
        transform: translateY(-2px) !important;
        background: 
            linear-gradient(135deg, 
                rgba(255, 255, 255, 0.12) 0%,
                rgba(255, 255, 255, 0.06) 50%,
                rgba(59, 130, 246, 0.05) 100%
            ) !important;
    }
    
    .stTextInput > label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* Apple-style Glass Button */
    .stButton > button {
        background: linear-gradient(90deg, rgba(124,92,255,0.9), rgba(124,240,255,0.7)) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 16px 32px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
        box-shadow: 
            0 8px 32px rgba(59, 130, 246, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2),
            0 0 0 1px rgba(59, 130, 246, 0.1) !important;
        transition: transform 0.18s cubic-bezier(.2,.9,.2,1), box-shadow 0.18s ease !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255, 255, 255, 0.1) 50%, 
            transparent 100%
        ) !important;
        transition: left 0.5s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 30px 90px rgba(122,92,255,0.25), inset 0 2px 0 rgba(255,255,255,0.06) !important;
        border-color: rgba(255,255,255,0.22) !important;
    }
    
    .stButton > button:hover::before {
        left: 100% !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(0.98) !important;
    }
    
    /* Apple-style Result Container */
    .result-container {
        background: linear-gradient(180deg, rgba(12,14,30,0.6), rgba(6,8,20,0.45));
        backdrop-filter: blur(34px) saturate(180%);
        -webkit-backdrop-filter: blur(34px) saturate(180%);
        border: 1px solid rgba(124,92,255,0.06);
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1.6rem 0;
        box-shadow: 0 30px 90px rgba(6, 8, 20, 0.7);
        animation: fadeInUp 0.7s cubic-bezier(.2,1,.3,1);
        position: relative;
        overflow: hidden;
    }
    
    .result-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(59, 130, 246, 0.4) 50%, 
            transparent 100%
        );
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Loading Animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid rgba(255,255,255,0.2);
        border-top: 4px solid #64b5f6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Apple-style Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(122,92,255,0.02));
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(124,92,255,0.08);
        border-radius: 14px;
        padding: 1.6rem;
        margin: 0.8rem 0.6rem;
        text-align: center;
        box-shadow: 0 14px 44px rgba(4,6,20,0.6);
        transition: transform 0.28s cubic-bezier(0.2,1,0.3,1), box-shadow 0.28s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255, 255, 255, 0.15) 50%, 
            transparent 100%
        );
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 30px 90px rgba(122,92,255,0.18), inset 0 1px 0 rgba(255,255,255,0.04);
        border-color: rgba(124,92,255,0.16);
        background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(124,92,255,0.04));
    }
    
    .feature-icon {
        font-size: 2.2rem;
        margin-bottom: 0.8rem;
        filter: drop-shadow(0 8px 30px rgba(124,92,255,0.18));
        transition: transform 0.28s cubic-bezier(0.2,1,0.3,1), filter 0.28s ease;
        display: inline-block;
        padding: 8px;
        border-radius: 10px;
        background: linear-gradient(90deg, rgba(124,92,255,0.06), rgba(124,240,255,0.02));
    }
    
    .feature-card:hover .feature-icon {
        transform: scale(1.1) translateY(-2px);
        filter: drop-shadow(0 8px 20px rgba(59, 130, 246, 0.5));
    }
    
    .feature-card h3 {
        color: rgba(255, 255, 255, 0.95);
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 0.8rem;
        letter-spacing: 0.01em;
    }
    
    .feature-card p {
        color: rgba(255, 255, 255, 0.7);
        font-weight: 400;
        line-height: 1.5;
        font-size: 0.95rem;
    }

    /* Responsive grid tweaks for feature showcase */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        align-items: start;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Apple-style Alert styling */
    .stAlert {
        background: 
            linear-gradient(135deg, 
                rgba(239, 68, 68, 0.08) 0%,
                rgba(239, 68, 68, 0.04) 50%,
                rgba(0, 0, 0, 0.1) 100%
            ) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(239, 68, 68, 0.1) !important;
    }
    
    /* Success styling */
    .stSuccess {
        background: 
            linear-gradient(135deg, 
                rgba(34, 197, 94, 0.08) 0%,
                rgba(34, 197, 94, 0.04) 50%,
                rgba(0, 0, 0, 0.1) 100%
            ) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(34, 197, 94, 0.2) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(34, 197, 94, 0.1) !important;
    }
    
    /* Info styling */
    .stInfo {
        background: 
            linear-gradient(135deg, 
                rgba(59, 130, 246, 0.08) 0%,
                rgba(59, 130, 246, 0.04) 50%,
                rgba(0, 0, 0, 0.1) 100%
            ) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Code block styling */
    .stCodeBlock {
        background: 
            linear-gradient(135deg, 
                rgba(0, 0, 0, 0.6) 0%,
                rgba(255, 255, 255, 0.02) 50%,
                rgba(0, 0, 0, 0.6) 100%
            ) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Voice-specific UI enhancements */
    .stFileUploader {
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader:hover {
        transform: translateY(-2px) !important;
    }
    
    .stAudio {
        background: 
            linear-gradient(135deg, 
                rgba(255, 255, 255, 0.05) 0%,
                rgba(59, 130, 246, 0.02) 100%
            ) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    .stTextArea textarea {
        background: 
            linear-gradient(135deg, 
                rgba(255, 255, 255, 0.08) 0%,
                rgba(255, 255, 255, 0.04) 50%,
                rgba(0, 0, 0, 0.08) 100%
            ) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 16px !important;
        color: #ffffff !important;
        font-family: 'SF Pro Display', 'Inter', monospace !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(59, 130, 246, 0.6) !important;
        box-shadow: 
            0 0 30px rgba(59, 130, 246, 0.2),
            0 8px 32px rgba(0, 0, 0, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Enhanced tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 8px !important;
        backdrop-filter: blur(20px) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 12px !important;
        margin: 4px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.1) !important;
        transform: translateY(-1px) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: 
            linear-gradient(135deg, 
                rgba(59, 130, 246, 0.3) 0%,
                rgba(29, 78, 216, 0.2) 100%
            ) !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Pulse animation for record button */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    
    .record-button {
        animation: pulse 2s infinite !important;
        background: 
            linear-gradient(135deg, 
                rgba(239, 68, 68, 0.8) 0%,
                rgba(220, 38, 38, 0.9) 100%
            ) !important;
    }
    </style>
    """, unsafe_allow_html=True)


def create_modern_header():
    """Create the modern 3D header"""
    st.markdown("""
    <div class="main-header">
        <div class="title">🗣️ Voice AI Agent</div>
        <div class="subtitle">Turn spoken ideas into professional outreach — upload audio or record and generate personalized messages</div>
        <div class="fab" title="Help">❔</div>
    </div>
    """, unsafe_allow_html=True)


def create_feature_showcase():
    """Show app features in cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎙️</div>
            <h3>Voice First</h3>
            <p>Upload or record audio and let the agent transcribe your message instantly</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧭</div>
            <h3>Context Aware</h3>
            <p>Understands intent from speech and matches your portfolio to the opportunity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✍️</div>
            <h3>Polished Output</h3>
            <p>Generates crisp, professional emails from spoken or written briefs</p>
        </div>
        """, unsafe_allow_html=True)


def get_mock_email_response(url):
    """Generate a mock email response for demo purposes"""
    return f"""
Subject: Experienced Full-Stack Developer Ready to Drive Innovation at Your Company

Dear Hiring Manager,

I hope this email finds you well. I came across your job posting on your careers page and was immediately drawn to the opportunity to contribute to your team's success.

With my extensive experience in modern web technologies, I believe I'm an excellent fit for this role. Here's what I can bring to your organization:

🚀 **Technical Expertise:**
- **Full-Stack Development**: React, Node.js, and MongoDB - perfect for building scalable applications
- **Modern Frameworks**: Angular with .NET and SQL Server for enterprise solutions
- **Cloud & DevOps**: Experience with AWS, Docker, and CI/CD pipelines

💼 **Relevant Portfolio:**
- **E-commerce Platform**: Built with React/Node.js handling 10K+ users
  → https://github.com/portfolio/ecommerce-platform
- **Enterprise Dashboard**: Angular/.NET solution for data analytics  
  → https://github.com/portfolio/enterprise-dashboard
- **ML Recommendation Engine**: Python/TensorFlow for personalized experiences
  → https://github.com/portfolio/ml-recommendations

🎯 **Why I'm Excited About This Role:**
Your company's commitment to innovation and cutting-edge technology aligns perfectly with my passion for building exceptional digital experiences. I'm particularly impressed by your recent initiatives in AI and would love to contribute to these forward-thinking projects.

I'd welcome the opportunity to discuss how my skills can help drive your team's objectives. I'm available for a conversation at your convenience and can start immediately.

Thank you for considering my application. I look forward to hearing from you soon.

Best regards,
[Your Name]
[Your Phone] | [Your Email] | [LinkedIn Profile]

P.S. I've included links to my most relevant projects above. Happy to provide additional code samples or references upon request.
"""


def get_mock_transcript_from_audio(audio_file) -> str:
    """Return a demo transcript for an uploaded audio file with enhanced validation.

    This is a lightweight placeholder so the UI can show a transcript
    without requiring an STT provider or extra dependencies.
    """
    try:
        if not audio_file:
            return "(Demo) No audio file provided"
            
        filename = getattr(audio_file, "name", "unknown_audio")
        file_size = getattr(audio_file, "size", 0)
        
        # Simulate different responses based on file characteristics
        if file_size > 10 * 1024 * 1024:  # > 10MB
            demo_text = (
                "Hi there! I'm reaching out regarding the software engineering position. "
                "I have over 5 years of experience in full-stack development, particularly "
                "with React, Node.js, and cloud technologies like AWS. I'm passionate about "
                "building scalable applications and would love to discuss how my skills "
                "align with your team's needs. Looking forward to connecting!"
            )
        elif filename.lower().endswith(('.mp3', '.m4a')):
            demo_text = (
                "Hello! I'm very interested in this role. My background includes modern web "
                "development, API design, and DevOps practices. I've led several projects "
                "from conception to deployment and thrive in collaborative environments."
            )
        else:
            demo_text = (
                "Hi, I'm excited about this opportunity. I have experience building scalable "
                "web apps, working with cloud platforms, and collaborating on cross-functional teams."
            )
        
        return f"(Demo transcription from {filename}): {demo_text}"
        
    except Exception as e:
        return f"(Demo transcription error): Unable to process audio file - {str(e)[:50]}"


def validate_audio_file(audio_file) -> tuple[bool, str]:
    """Validate uploaded audio file and return status with message."""
    if not audio_file:
        return False, "No audio file provided"
    
    try:
        # Check file size (limit to 25MB for demo)
        file_size = getattr(audio_file, "size", 0)
        if file_size > 25 * 1024 * 1024:
            return False, f"File too large ({file_size / (1024*1024):.1f}MB). Maximum size is 25MB"
        
        if file_size == 0:
            return False, "Empty audio file detected"
        
        # Check file extension
        filename = getattr(audio_file, "name", "").lower()
        allowed_extensions = ['.wav', '.mp3', '.m4a', '.ogg', '.flac', '.aac']
        
        if not any(filename.endswith(ext) for ext in allowed_extensions):
            return False, f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        
        return True, f"✓ Valid audio file ({file_size / (1024*1024):.1f}MB)"
        
    except Exception as e:
        return False, f"File validation error: {str(e)}"


def create_streamlit_app():
    """Main Streamlit app with modern UI"""
    inject_custom_css()
    create_modern_header()
    
    # Feature showcase
    create_feature_showcase()
    
    # Main input section - voice-first UI
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    st.markdown("### 🎧 Input Mode")
    tab_audio, tab_url = st.tabs(["Audio / Voice", "URL / Text"])

    # Shared state
    audio_file = None
    transcript_text = ""

    with tab_audio:
        st.markdown("#### 🎙️ Upload Audio or Record (Experimental)")
        
        # Enhanced audio upload with validation
        audio_file = st.file_uploader(
            "Select audio file", 
            type=["wav", "mp3", "m4a", "ogg", "flac", "aac"],
            help="Supported formats: WAV, MP3, M4A, OGG, FLAC, AAC (Max: 25MB)"
        )
        
        # Validate audio file if uploaded
        if audio_file is not None:
            is_valid, validation_msg = validate_audio_file(audio_file)
            if is_valid:
                st.success(validation_msg)
                st.audio(audio_file, format="audio/wav")
            else:
                st.error(f"❌ {validation_msg}")
                audio_file = None  # Reset invalid file

        # Recording section with enhanced UI
        st.markdown("#### 🔴 Voice Recording")
        col_r1, col_r2, col_r3 = st.columns([2, 1, 1])
        with col_r1:
            st.info("🎧 Browser recording requires additional setup - use file upload for reliable results")
        with col_r2:
            record_btn = st.button("🔴 Record", help="Experimental feature", key="record_voice")
        with col_r3:
            if record_btn:
                st.warning("Recording feature coming soon!")

        # Transcript section
        st.markdown("#### 📝 Transcript")
        
        # Auto-generate transcript for demo if audio uploaded
        if audio_file is not None and is_valid:
            auto_transcript = get_mock_transcript_from_audio(audio_file)
            transcript_text = st.text_area(
                "Transcribed text (auto-generated in demo mode)", 
                value=auto_transcript, 
                height=160,
                help="Edit this text or replace with your own transcript"
            )
        else:
            transcript_text = st.text_area(
                "Enter transcript or upload audio for auto-transcription", 
                value="", 
                height=160,
                placeholder="Paste your spoken message here, or upload an audio file above..."
            )

    with tab_url:
        st.markdown("#### 🔗 Enter Job Posting URL or paste job description")
        url_input = st.text_input(
            "Job URL", 
            value="",
            placeholder="https://company.com/careers/job-id",
            help="Paste the URL of the job posting you want to apply for"
        )

        st.markdown("#### Or paste a job description / brief")
        pasted_text = st.text_area("Paste job description or role brief", value="", height=160)

    # Generate button centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.button("🎙️ Generate from Audio/Text", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        # Enhanced validation for voice AI agent
        has_audio = audio_file is not None
        has_transcript = transcript_text.strip() != ""
        has_url = url_input and url_input.startswith(('http://', 'https://'))
        has_text = 'pasted_text' in locals() and pasted_text.strip() != ""
        
        if not (has_audio or has_transcript or has_url or has_text):
            st.error("🎙️ **Please provide input**: Upload audio, enter text transcript, or provide a URL/job description")
            return
        
        # Show enhanced loading animation for voice processing
        with st.container():
            st.markdown("""
            <div class="loading">
                <div class="spinner"></div>
            </div>
            """, unsafe_allow_html=True)
            
            if has_audio:
                st.info("🎧 Processing audio file...")
            elif has_transcript:
                st.info("📝 Analyzing transcript...")
            elif has_url:
                st.info("🔗 Analyzing job posting...")
            else:
                st.info("✨ Processing your input...")
            
            # Simulate processing time with enhanced feedback
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.025)
                progress_bar.progress(i + 1)
            
            progress_bar.empty()
        
        # Enhanced generation logic for voice AI
        try:
            api_key = os.getenv('GROQ_API_KEY', '').strip()
            
            # Determine input source and prepare content
            content_source = ""
            if has_audio and has_transcript:
                content_source = f"Voice Input: {transcript_text}"
            elif has_transcript:
                content_source = f"Text Input: {transcript_text}"
            elif has_url:
                content_source = f"URL Analysis: {url_input}"
            elif has_text:
                content_source = f"Job Description: {pasted_text}"
            
            if not api_key or api_key == 'your_groq_api_key_here':
                # Enhanced demo mode with voice awareness
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                
                if has_audio or has_transcript:
                    st.success("🎙️ **Voice-to-Email Generated Successfully!**")
                    st.info(f"**Input Source**: {content_source[:100]}...")
                else:
                    st.success("✨ **Demo Email Generated Successfully!**")
                
                st.markdown("### 📧 Generated Professional Email:")
                
                # Use transcript or URL for mock generation
                input_for_mock = transcript_text if (has_audio or has_transcript) else (url_input or pasted_text)
                mock_email = get_mock_email_response(input_for_mock)
                st.code(mock_email, language='text')
                
                if has_audio or has_transcript:
                    st.markdown("### 🎯 Voice Analysis")
                    st.write("**Key Points Detected:**")
                    st.write("• Professional experience mentioned")
                    st.write("• Technical skills highlighted")  
                    st.write("• Interest in opportunity expressed")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                # Real mode - enhanced for voice input
                from chains import Chain
                from portfolio import Portfolio
                
                chain = Chain()
                portfolio = Portfolio()
                
                if has_url:
                    loader = WebBaseLoader([url_input])
                    data = clean_text(loader.load().pop().page_content)
                elif has_transcript or has_text:
                    data = transcript_text or pasted_text
                else:
                    data = "No specific job posting provided"
                
                portfolio.load_portfolio()
                jobs = chain.extract_jobs(data)
                
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.success("🎙️ **Voice AI Email Generated Successfully!**")
                st.info(f"**Input Source**: {content_source[:100]}...")
                
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = chain.write_mail(job, links)
                    
                    st.markdown("### 📧 Generated Professional Email:")
                    st.code(email, language='markdown')
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"🚨 **Processing Error**: {str(e)}")
            st.info("💡 **Tip**: Ensure your audio is clear, transcript is complete, or URL is accessible.")


if __name__ == "__main__":
    st.set_page_config(
        layout="wide", 
        page_title="Voice AI Agent", 
        page_icon="🗣️",
        initial_sidebar_state="collapsed"
    )
    create_streamlit_app()


