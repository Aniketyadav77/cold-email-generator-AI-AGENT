# 🤖 Cold Email Generator AI Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)](https://python.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent AI-powered application that generates personalized cold emails by analyzing job postings and matching them with your portfolio. Built with LangChain, Streamlit, and powered by Groq's lightning-fast LLM inference.

## 🌟 Features

- **🔍 Smart Job Analysis**: Automatically scrapes and analyzes job postings from URLs
- **🎯 Personalized Matching**: Matches job requirements with your portfolio using vector similarity search
- **✍️ AI-Powered Writing**: Generates compelling, personalized cold emails using advanced LLMs
- **⚡ Lightning Fast**: Powered by Groq's ultra-fast inference engine
- **📊 Portfolio Management**: Dynamic portfolio loading and querying with ChromaDB
- **🎨 Modern UI**: Clean, intuitive Streamlit interface
- **🔒 Secure**: Environment-based API key management

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
