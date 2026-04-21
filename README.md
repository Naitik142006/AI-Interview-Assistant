# 🤖 AI Interview Assistant

AI Interview Assistant is a powerful, Flask-based web application that leverages the **Groq Cloud API** to provide users with a realistic and interactive mock interview experience. Whether you're preparing for technical roles or general behavioral interviews, this tool provides real-time feedback and detailed performance analytics.

---

## ✨ Features

- **AI-Powered Question Generation**: Dynamically creates interview questions tailored to specific topics and experience levels.
- **Real-Time Analysis**: Analyzes your responses instantly, providing scores for:
    - **Knowledge**: Accuracy and depth of your answer.
    - **Clarity**: How well you articulated your thoughts.
    - **Confidence**: The tone and conviction of your delivery.
- **Dynamic Follow-Up**: Generates intelligent follow-up questions based on your previous answers to dive deeper into topics.
- **Comprehensive Summary**: After the interview, receive a detailed report with:
    - Overall performance score.
    - Topic-wise breakdown.
    - Model answers for every question asked.
- **Responsive UI**: A sleek, user-friendly interface designed for a seamless interview flow.

---

## 🛠️ Tech Stack

- **Backend**: Python, [Flask](https://flask.palletsprojects.com/)
- **AI Engine**: [Groq SDK](https://github.com/groq/groq-python) (using Llama 3 or similar models)
- **Environment Management**: `python-dotenv`
- **Frontend**: HTML5, CSS3, Jinja2 Templates

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- A Groq API Key (Get one at [Groq Console](https://console.groq.com/))

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ai-interview-assistant.git
   cd ai-interview-assistant
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   SECRET_KEY=your_secret_key_here
   FLASK_ENV=development
   ```

### Running the Application

Start the Flask server:
```bash
python app.py
```

Open your browser and navigate to `http://localhost:5000`.

---

## 📂 Project Structure

```text
AI Interview Assistant/
├── app.py              # Main application entry point
├── config.py           # Configuration handler
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (API keys)
├── static/             # CSS, JS, and image assets
├── templates/          # HTML templates (Jinja2)
├── utils/              # AI logic and helper functions
│   └── ai_interview.py # AI Interviewer class logic
└── test_groq.py        # Utility script to test API connectivity
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have ideas for new features or improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using Groq and Flask.**
