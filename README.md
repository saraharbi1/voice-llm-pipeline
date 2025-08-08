# مشروع معالجة الصوت بالذكاء الاصطناعي

## ⚙️ المتطلبات
- Python 3.8+
- مفاتيح API من [Cohere](https://cohere.com/) و[Google Cloud](https://cloud.google.com/)

## 🚀 خطوات التشغيل
```bash
# 1. إنشاء بيئة افتراضية
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. إعداد مفاتيح API
# أ) إنشاء ملف .env وإضافة مفتاح Cohere:
echo "COHERE_API_KEY=your_cohere_key_here" > .env

# ب) إعداد Google Cloud:
python setup_gcloud.py

# 4. تحويل ملف صوتي إلى تنسيق 16kHz WAV
ffmpeg -i input.mp3 -ar 16000 -ac 1 audio_input.wav

# 5. تشغيل البرنامج
python app.py