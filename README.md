# 🗣️ Voice AI Agent - Cold Email Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)](https://python.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🎙️ **Voice-First AI Agent** that transforms spoken ideas into professional cold emails. Upload audio, speak your thoughts, or type your message - our AI analyzes job opportunities and generates personalized outreach emails that get responses.

## 🌟 Key Features

### 🎧 Voice-First Experience
- **🎙️ Audio Upload**: Support for WAV, MP3, M4A, OGG, FLAC, AAC files (up to 25MB)
- **📝 Auto Transcription**: Intelligent speech-to-text conversion (demo mode available)
- **🔴 Voice Recording**: Browser-based recording (experimental feature)
- **✍️ Manual Input**: Traditional text input and URL analysis

### 🧠 Intelligent Processing
- **🔍 Smart Job Analysis**: Automatically scrapes and analyzes job postings from URLs
- **🎯 Context-Aware Matching**: Matches spoken requirements with your portfolio using vector similarity
- **✨ AI-Powered Writing**: Generates compelling, personalized cold emails from voice or text input
- **⚡ Lightning Fast**: Powered by Groq's ultra-fast inference engine

### 🎨 Modern Interface
- **🌟 Apple iOS-Inspired Glass UI**: Stunning glass morphism design with 3D effects
- **📱 Voice-First Layout**: Intuitive tabs for audio/voice and traditional text input
- **🎭 Smooth Animations**: Fluid transitions and hover effects throughout
- **🔒 Secure**: Environment-based API key management with demo mode fallback

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com/keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aniketyadav77/cold-email-generator-AI-AGENT.git
   cd cold-email-generator-AI-AGENT
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file in the app directory
   echo "GROQ_API_KEY=your_groq_api_key_here" > app/.env
   ```

4. **Run the application**
   ```bash
   cd app
   streamlit run main.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
cold-email-generator-AI-AGENT/
├── app/
│   ├── .env                 # Environment variables
│   ├── main.py             # Main Streamlit application
│   ├── chains.py           # LangChain implementation
│   ├── portfolio.py        # Portfolio management
│   ├── utils.py            # Utility functions
│   ├── resource/
│   │   └── my_portfolio.csv # Portfolio data
│   └── vectorstore/        # ChromaDB vector storage
├── imgs/                   # Application screenshots
├── notebooks/
│   ├── email_generator.ipynb     # Email generation examples
│   ├── tutorial_chromadb.ipynb  # ChromaDB tutorial
│   └── tutorial_groq.ipynb      # Groq API tutorial
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🛠️ Technology Stack

- **Backend**: Python, LangChain, ChromaDB
- **Frontend**: Streamlit
- **LLM**: Groq (Llama models)
- **Vector Database**: ChromaDB
- **Web Scraping**: BeautifulSoup4, Requests
- **Data Processing**: Pandas

## 💼 How It Works

1. **Job Posting Analysis**: Input a job posting URL, and the AI scrapes and analyzes the content
2. **Portfolio Matching**: The system uses vector similarity search to find relevant portfolio projects
3. **Context Generation**: Combines job requirements with matching portfolio items
4. **Email Generation**: AI generates a personalized cold email highlighting relevant experience
5. **Output**: Receive a professionally crafted email ready to send

![img.png](imgs/img.png)

## Architecture Diagram
![img.png](imgs/architecture.png)

## 📊 Portfolio Configuration

Customize your portfolio by editing `app/resource/my_portfolio.csv`:

```csv
Techstack,Links
"React, Node.js, MongoDB","https://github.com/yourusername/project1"
"Python, Django, PostgreSQL","https://github.com/yourusername/project2"
"Machine Learning, TensorFlow","https://github.com/yourusername/ml-project"
```

## 🔧 Configuration

### Environment Variables

Create an `app/.env` file with:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## 🚀 Deployment

### Recommended Platforms:

#### 1. **Streamlit Community Cloud** (Free & Easy)
1. Visit [share.streamlit.io](https://share.streamlit.io/)
2. Connect GitHub and select this repository
3. Set main file path: `app/main.py`
4. Add `GROQ_API_KEY` in secrets
5. Deploy!

#### 2. **Railway** (Reliable)
1. Visit [railway.app](https://railway.app/)
2. Deploy from GitHub repo
3. Add environment variables
4. Automatic deployment with `railway.json`

#### 3. **Render** (Free Tier)
1. Connect GitHub repo at [render.com](https://render.com/)
2. Runtime: Python 3
3. Build: `pip install -r requirements.txt`
4. Start: `streamlit run app/main.py --server.port $PORT --server.headless true`

#### 4. **Docker Deployment**
```bash
docker build -t cold-email-ai .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key cold-email-ai
```

> ⚠️ **Note**: Avoid Vercel/Netlify for Streamlit apps. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://python.langchain.com/) for the powerful LLM framework
- [Groq](https://groq.com/) for ultra-fast LLM inference
- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [ChromaDB](https://www.trychroma.com/) for vector database capabilities

---

**Made with ❤️ by [Aniket Yadav](https://github.com/Aniketyadav77)**

⭐ Star this repository if you find it helpful!
