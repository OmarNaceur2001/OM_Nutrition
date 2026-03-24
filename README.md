# 🏋️ Fitness AI Trainer — Real-Time Exercise Recognition & Counting

> An AI-powered fitness coach that uses Computer Vision and Deep Learning to track your workouts in real time.

---

## 🎯 What is this project?

This application uses your **webcam or uploaded videos** to automatically:
- **Detect which exercise you're doing** (squat, push-up, shoulder press, etc.)
- **Count your repetitions** accurately using pose estimation
- **Give you fitness advice** via an AI chatbot

Built as part of my engineering studies at **ESPRIT Tunisia**, applying state-of-the-art ML research to a real-world fitness problem.

---

## 🚀 Demo

[![Watch the demo](https://img.youtube.com/vi/GPmDPB1bSmc/hqdefault.jpg)](https://www.youtube.com/watch?v=GPmDPB1bSmc)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📹 Video Analysis | Upload a workout video → get rep counts |
| 🎥 Webcam Mode | Real-time rep counting via webcam |
| 🤖 Auto Classify | AI detects your exercise automatically |
| 💬 AI Chatbot | GPT-powered fitness coach for guidance |

---

## 🧠 How It Works

### Pose Estimation
Uses **MediaPipe** to extract 33 body landmarks (joints) from each video frame.

### Exercise Classification
A **BiLSTM (Bidirectional LSTM)** neural network analyzes sequences of 30 frames and classifies the exercise based on joint angles and movement patterns.

### Rep Counting
Tracks "up" and "down" movement phases using angle thresholds — counts a rep only when a full movement cycle is completed.

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.7+-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-ML-orange)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose-green)
![Streamlit](https://img.shields.io/badge/Streamlit-WebApp-red)
![OpenAI](https://img.shields.io/badge/OpenAI-Chatbot-purple)

- **Pose Estimation**: MediaPipe
- **Deep Learning**: LSTM / BiLSTM (TensorFlow/Keras)
- **Web Interface**: Streamlit
- **Chatbot**: OpenAI GPT-3.5-turbo + LangChain
- **Computer Vision**: OpenCV

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.7+
- Webcam (for live mode)
- OpenAI API Key (for chatbot)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/fitness-ai-trainer.git
cd fitness-ai-trainer

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate       # Mac/Linux
# venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run main.py
```

---

## 📁 Project Structure

```
fitness-ai-trainer/
│
├── main.py                          # Streamlit app entry point
├── ExerciseAiTrainer.py             # Exercise-specific pose logic
├── AiTrainer_utils.py               # Image processing utilities
├── PoseModule2.py                   # MediaPipe pose estimation
├── chatbot.py                       # OpenAI chatbot integration
├── extract_features.py              # Feature extraction from videos
├── create_sequence_of_features.py   # Dataset sequence generation
├── train_bidirectionallstm.py       # BiLSTM model training script
├── requirements.txt
└── shoulder_press_form.mp4          # Sample exercise video
```

---

## 📊 Model Performance

The BiLSTM model was trained on a combined dataset:
- **Kaggle Real Workout Videos** — real-world exercise data
- **InfiniteRep Dataset** — synthetic avatar videos
- **Custom collected data** — diverse exercise variations

Evaluated using: Accuracy, Precision, Recall, F1-Score

---

## 🔬 Research Base

This project implements concepts from:

> *"Real-Time Fitness Exercise Classification and Counting from Video Frames"*  
> [arxiv.org/abs/2411.11548](https://arxiv.org/abs/2411.11548)

---

## 👨‍💻 Author

**Omar** — AI & Data Science Engineering Student @ ESPRIT Tunisia 🇹🇳  
🌍 Open to opportunities abroad  
📧 Connect with me on [LinkedIn](https://www.linkedin.com/in/omar-naceur-b152612a9/)

---

⭐ **If this project helped you, give it a star!** It motivates me to keep building.
