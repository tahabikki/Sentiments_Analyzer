import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to sys.path so subfolders can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
from datetime import datetime
import json
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from deepface import DeepFace

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tiff"}

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database model
class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.Text)  # JSON string
    emotion = db.Column(db.Text)    # JSON string
    date = db.Column(db.DateTime, default=datetime.utcnow)

# OpenRouter GPT-5 client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY
)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

def convert_numpy_to_python(obj):
    """
    Recursively convert all numpy types (float32, int64, etc.) to Python native types.
    """
    if isinstance(obj, dict):
        return {k: convert_numpy_to_python(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_to_python(i) for i in obj]
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    return obj

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("text", "").strip()
    file = request.files.get("image")
    result = {}

    if file and allowed_file(file.filename):
        # Save image
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Analyze emotions from face
        try:
            face_analysis = DeepFace.analyze(img_path=filepath, actions=['emotion'])

            # DeepFace may return a list if multiple faces are detected
            if isinstance(face_analysis, list):
                face_analysis = face_analysis[0]  # take first face

            face_analysis = convert_numpy_to_python(face_analysis)  # convert floats
            result["emotion"] = face_analysis["emotion"]

            # Map dominant emotion to sentiment
            dominant_emotion = face_analysis["dominant_emotion"]
            if dominant_emotion in ["happy", "surprise"]:
                result["sentiment"] = {"label": "positive"}
            elif dominant_emotion == "neutral":
                result["sentiment"] = {"label": "neutral"}
            else:
                result["sentiment"] = {"label": "negative"}

            text = f"Face Image ({dominant_emotion})"

        except Exception as e:
            return jsonify({"error": f"Face emotion detection failed: {e}"}), 500

    elif text:
        # Analyze text using GPT-5
        try:
            response = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Analyze sentiment and emotion of this text: '{text}'. Return JSON with sentiment and emotion."
                        }
                    ]
                }]
            )
            content = response.choices[0].message.content
            result = json.loads(content)
            result = convert_numpy_to_python(result)  # just in case
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No text or image provided"}), 400

    # Save to database
    try:
        analysis = Analysis(
            text=text,
            sentiment=json.dumps(result.get("sentiment", {})),
            emotion=json.dumps(result.get("emotion", {}))
        )
        db.session.add(analysis)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"success": True, "result": result})

@app.route("/history")
def history():
    entries = Analysis.query.order_by(Analysis.date.desc()).limit(50).all()
    data = []
    for e in entries:
        data.append({
            "text": e.text,
            "date": e.date.strftime("%Y-%m-%d %H:%M:%S"),
            "sentiment": json.loads(e.sentiment),
            "emotion": json.loads(e.emotion)
        })
    return jsonify(data)

@app.route("/clear_history", methods=["POST"])
def clear_history():
    try:
        db.session.query(Analysis).delete()
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
