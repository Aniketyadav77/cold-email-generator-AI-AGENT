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
    
    /* Global Styling - Apple Dark Theme */
    .main {
        background: linear-gradient(145deg, #000000 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #000000 100%);
        font-family: 'SF Pro Display', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: 
            radial-gradient(circle at 20% 80%, rgba(30, 58, 138, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
            linear-gradient(145deg, #000000 0%, #0a0a0a 25%, #1a1a2e 50%, #16213e 75%, #0f0f23 100%);
        color: #ffffff;
        min-height: 100vh;
    }
    
    /* Header with Apple Glass Effect */
    .main-header {
        background: 
            linear-gradient(135deg, 
                rgba(255, 255, 255, 0.08) 0%,
                rgba(255, 255, 255, 0.04) 50%,
                rgba(0, 0, 0, 0.1) 100%
            );
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.125);
        border-radius: 24px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 0 1px rgba(59, 130, 246, 0.1);
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
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, 
            #ffffff 0%, 
            #e0e7ff 25%,
            #3b82f6 50%,
            #1d4ed8 75%,
            #ffffff 100%
        );
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
        background: 
            linear-gradient(135deg, 
                rgba(255, 255, 255, 0.06) 0%,
                rgba(255, 255, 255, 0.02) 50%,
                rgba(0, 0, 0, 0.05) 100%
            );
        backdrop-filter: blur(30px) saturate(200%);
        -webkit-backdrop-filter: blur(30px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 
            0 8px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.08),
            0 0 0 1px rgba(59, 130, 246, 0.05);
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
        background: 
            linear-gradient(135deg, 
                rgba(59, 130, 246, 0.8) 0%,
                rgba(29, 78, 216, 0.9) 50%,
                rgba(30, 58, 138, 0.8) 100%
            ) !important;
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
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1) !important;
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
        transform: translateY(-4px) !important;
        box-shadow: 
            0 20px 60px rgba(59, 130, 246, 0.4),
            inset 0 2px 0 rgba(255, 255, 255, 0.3),
            0 0 0 1px rgba(59, 130, 246, 0.2) !important;
        background: 
            linear-gradient(135deg, 
                rgba(59, 130, 246, 0.9) 0%,
                rgba(29, 78, 216, 1) 50%,
                rgba(30, 58, 138, 0.9) 100%
            ) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    .stButton > button:hover::before {
        left: 100% !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(0.98) !important;
    }
    
    /* Apple-style Result Container */
    .result-container {
        background: 
            linear-gradient(135deg, 
                rgba(0, 0, 0, 0.4) 0%,
                rgba(255, 255, 255, 0.02) 50%,
                rgba(0, 0, 0, 0.4) 100%
            );
        backdrop-filter: blur(40px) saturate(200%);
        -webkit-backdrop-filter: blur(40px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 
            0 16px 64px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.05),
            0 0 0 1px rgba(59, 130, 246, 0.05);
        animation: slideInUp 0.8s cubic-bezier(0.23, 1, 0.320, 1);
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
            transform: translateY(30px);
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
        background: 
            linear-gradient(135deg, 
                rgba(255, 255, 255, 0.05) 0%,
                rgba(255, 255, 255, 0.02) 50%,
                rgba(0, 0, 0, 0.05) 100%
            );
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 2rem 1.5rem;
        margin: 1rem 0.5rem;
        text-align: center;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
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
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.08),
            0 0 0 1px rgba(59, 130, 246, 0.1);
        border-color: rgba(255, 255, 255, 0.15);
        background: 
            linear-gradient(135deg, 
                rgba(255, 255, 255, 0.08) 0%,
                rgba(255, 255, 255, 0.04) 50%,
                rgba(59, 130, 246, 0.02) 100%
            );
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1.2rem;
        filter: drop-shadow(0 4px 12px rgba(59, 130, 246, 0.3));
        transition: all 0.3s ease;
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
    </style>
    """, unsafe_allow_html=True)


def create_modern_header():
    """Create the modern 3D header"""
    st.markdown("""
    <div class="main-header">
        <div class="title">🤖 Cold Email AI Agent</div>
        <div class="subtitle">Generate personalized cold emails using AI-powered job analysis</div>
    </div>
    """, unsafe_allow_html=True)


def create_feature_showcase():
    """Show app features in cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3>Smart Analysis</h3>
            <p>AI analyzes job postings to extract key requirements and skills</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>Perfect Match</h3>
            <p>Matches your portfolio with job requirements using vector search</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✍️</div>
            <h3>AI Writing</h3>
            <p>Generates compelling, personalized cold emails that get responses</p>
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


def create_streamlit_app():
    """Main Streamlit app with modern UI"""
    inject_custom_css()
    create_modern_header()
    
    # Feature showcase
    create_feature_showcase()
    
    # Main input section
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # URL Input
    st.markdown("### 🔗 Enter Job Posting URL")
    url_input = st.text_input(
        "Job URL", 
        value="https://www.kfintech.com/career/",
        placeholder="https://company.com/careers/job-id",
        help="Paste the URL of the job posting you want to apply for"
    )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.button("🚀 Generate Cold Email", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        if not url_input or not url_input.startswith(('http://', 'https://')):
            st.error("⚠️ Please enter a valid URL starting with http:// or https://")
            return
        
        # Show loading animation
        with st.container():
            st.markdown("""
            <div class="loading">
                <div class="spinner"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Simulate processing time
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            progress_bar.empty()
        
        # Generate email
        try:
            api_key = os.getenv('GROQ_API_KEY', '').strip()
            
            if not api_key or api_key == 'your_groq_api_key_here':
                # Demo mode - show mock response
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.success("✨ **Demo Email Generated Successfully!**")
                st.markdown("### 📧 Generated Cold Email:")
                
                mock_email = get_mock_email_response(url_input)
                st.code(mock_email, language='text')
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                # Real mode - use actual API
                from chains import Chain
                from portfolio import Portfolio
                
                chain = Chain()
                portfolio = Portfolio()
                
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = chain.extract_jobs(data)
                
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.success("✨ **Email Generated Successfully!**")
                
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = chain.write_mail(job, links)
                    
                    st.markdown("### 📧 Generated Cold Email:")
                    st.code(email, language='markdown')
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"🚨 **Error**: {str(e)}")
            st.info("💡 **Tip**: Make sure the URL is accessible and contains job posting information.")


if __name__ == "__main__":
    st.set_page_config(
        layout="wide", 
        page_title="Cold Email AI Agent", 
        page_icon="🤖",
        initial_sidebar_state="collapsed"
    )
    create_streamlit_app()


