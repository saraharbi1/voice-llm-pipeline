# مشروع تحويل الصوت إلى نص واستخدام LLM وتحويل الناتج إلى صوت

## 📁 هيكل المشروع
```
voice-llm-pipeline/
├── .env                  # لحفظ مفاتيح API  
├── requirements.txt      # المكاتب المطلوبة  
├── app.py                # البرنامج الرئيسي  
├── audio_input.wav       # مثال لملف صوتي مدخل  
├── audio_output.mp3      # مثال لملف صوتي مخرج  
└── README.md             # شرح تفصيلي للخطوات
```

## ⚙️ المتطلبات الأساسية
1. حساب Cohere API: https://dashboard.cohere.com/
2. حساب Google Cloud: https://console.cloud.google.com/
3. Python 3.8+

## 🔧 خطوات التشغيل
```bash
git clone https://github.com/username/voice-llm-pipeline.git
cd voice-llm-pipeline
pip install -r requirements.txt
python app.py
```

## 💡 ملاحظات
- الملف الصوتي يجب أن يكون WAV أحادي 16000Hz
- يمكن استبدال Google بـ SpeechRecognition
- يمكن استخدام pyttsx3 بدل gTTS للعمل أوفلاين
