# 🎯 AI Text Sentiment Analyzer Web App

A powerful web application that analyzes sentiment and emotions from both **text** and **facial expressions**. Leveraging cutting-edge AI models including OpenAI's GPT-5 and DeepFace for comprehensive emotional intelligence.

---

## ✨ Features

### 📝 Text Analysis
- **Sentiment Detection**: Analyze the emotional tone of any text (positive, negative, neutral)
- **Emotion Recognition**: Identify specific emotions conveyed in the text
- **AI-Powered**: Uses OpenAI's GPT-5 model through OpenRouter API for accurate analysis

### 📷 Facial Expression Analysis
- **Face Detection**: Automatically detects faces in uploaded images
- **Emotion Mapping**: Maps facial expressions to specific emotions
- **Sentiment Inference**: Converts facial emotions to sentiment scores

### 📊 History & Analytics
- **Analysis History**: View your last 50 analyses
- **Persistent Storage**: SQLite database stores all analysis results
- **Clear History**: Option to clear all analysis records
- **Timestamps**: Every analysis is timestamped for reference

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask (Python) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Database** | SQLite |
| **NLP** | OpenAI GPT-5 (via OpenRouter) |
| **Computer Vision** | DeepFace |
| **Image Processing** | Pillow (PIL) |
| **Deep Learning** | TensorFlow |
| **HTTP Client** | Requests |

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A valid OpenRouter API key

---

## 🚀 Installation & Setup

### 1. Clone or Download the Project
```bash
cd "Project Idea AI Text Sentiment Analyzer Web App"
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure API Key

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openrouter_api_key_here
```

**Get your API key:**
1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Sign up or log in
3. Generate an API key
4. Add it to the `.env` file

> ⚠️ **Security Note**: Never commit `.env` to version control. Add it to `.gitignore`.

### 6. Run the Application
```bash
python app.py
```

The application will start at `http://localhost:5000`

---

## 📁 Project Structure

```
Project Idea AI Text Sentiment Analyzer Web App/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not in version control)
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── templates/
│   └── index.html          # Frontend HTML
├── instance/
│   └── history.db          # SQLite database (auto-created)
└── uploads/
    └── [uploaded images]   # User-uploaded image files
```

---

## 🎮 Usage

### Text Analysis
1. Enter text in the input field
2. Click "Analyze"
3. View sentiment and emotion results

### Image Analysis
1. Upload an image containing a face
2. Click "Analyze"
3. View detected emotions and inferred sentiment

### View History
- Click "History" to see previous analyses
- View timestamps, sentiment, and emotions
- Click "Clear History" to reset all records

---

## 📊 API Response Format

### Text Analysis Response
```json
{
  "success": true,
  "result": {
    "sentiment": {
      "label": "positive"
    },
    "emotion": {
      "joy": 0.85,
      "sadness": 0.05,
      "anger": 0.03,
      "disgust": 0.02,
      "fear": 0.03,
      "surprise": 0.02
    }
  }
}
```

### Image Analysis Response
```json
{
  "success": true,
  "result": {
    "sentiment": {
      "label": "positive"
    },
    "emotion": {
      "angry": 0.02,
      "disgust": 0.01,
      "fear": 0.02,
      "happy": 0.92,
      "neutral": 0.01,
      "sad": 0.01,
      "surprise": 0.01
    }
  }
}
```

---

## 🔧 Configuration

### Database
- **Type**: SQLite
- **File**: `instance/history.db` (auto-created)
- **Retention**: Last 50 analyses

### Upload Folder
- **Location**: `uploads/`
- **Allowed Formats**: PNG, JPG, JPEG, BMP, TIFF
- **Max Size**: Configurable in app.py

### Flask Settings
- **Debug Mode**: Enabled by default (change in production)
- **Secret Key**: Set in `app.config['secret_key']`

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'openai'`
**Solution**: Run `pip install -r requirements.txt`

### Issue: `ValueError: OPENAI_API_KEY environment variable is not set`
**Solution**: Create `.env` file with your OpenRouter API key

### Issue: `401 - No auth credentials found`
**Solution**: Verify your API key is valid and not expired on [OpenRouter.ai](https://openrouter.ai)

### Issue: Face detection fails
**Solution**: Ensure image is clear, well-lit, and contains a visible face

### Issue: TensorFlow warnings
**Solution**: These are normal optimization warnings. To suppress them:
```bash
set TF_ENABLE_ONEDNN_OPTS=0
```

---

## 📦 Dependencies

Key packages included:
- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM for database
- **OpenAI**: API client for GPT-5
- **DeepFace**: Facial emotion recognition
- **Pillow**: Image processing
- **python-dotenv**: Environment variable management
- **TensorFlow**: Deep learning backend
- **NumPy**: Numerical computing

See `requirements.txt` for complete list.

---

## 🔐 Security Considerations

- ✅ API keys stored in environment variables (not in code)
- ✅ `.env` file excluded from version control
- ✅ User uploads stored securely
- ⚠️ For production: Disable Flask debug mode, use environment-specific configs

---

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Batch analysis for multiple texts/images
- [ ] Export analysis results (CSV, PDF)
- [ ] User authentication & personal analytics
- [ ] Real-time sentiment tracking dashboard
- [ ] Integration with additional AI models
- [ ] Mobile app version
- [ ] Advanced sentiment nuance detection

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👤 Author

Created as an AI-powered sentiment analysis portfolio project.

---

## 💬 Support

For issues, questions, or suggestions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Verify all dependencies are installed
3. Ensure API keys are configured correctly
4. Check logs in the terminal for detailed error messages

---

**Made with ❤️ using Flask, OpenAI, and DeepFace**
