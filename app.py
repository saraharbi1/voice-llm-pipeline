import os
import argparse
import sys
import cohere
from dotenv import load_dotenv
from google.cloud import speech
import pyttsx3  # استبدال gTTS بـ pyttsx3

load_dotenv()

def check_google_credentials():
    """التحقق من وجود بيانات اعتماد Google Cloud"""
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path or not os.path.exists(creds_path):
        print("❌ ملف اعتماد Google Cloud غير موجود")
        print("يرجى اتباع الخطوات التالية:")
        print("1. تشغيل ملف الإعداد: python setup_gcloud.py")
        print("2. تعيين متغير البيئة:")
        print('   setx GOOGLE_APPLICATION_CREDENTIALS "C:\\مسار\\المشروع\\google_credentials.json"')
        return False
    return True

def speech_to_text(audio_file):
    """تحويل الصوت إلى نص باستخدام Google Cloud Speech-to-Text"""
    try:
        client = speech.SpeechClient()
        with open(audio_file, "rb") as f:
            audio = speech.RecognitionAudio(content=f.read())
        
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="ar-SA",
            enable_automatic_punctuation=True
        )
        
        response = client.recognize(config=config, audio=audio)
        
        if not response.results:
            print("🔇 لم يتم التعرف على كلام في الملف الصوتي")
            return None
            
        return response.results[0].alternatives[0].transcript
        
    except Exception as e:
        print(f"❌ خطأ في تحويل الصوت إلى نص: {str(e)}")
        return None

def generate_response(prompt):
    """توليد رد باستخدام Cohere API"""
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        print("❌ مفتاح Cohere API غير موجود")
        return None
        
    try:
        co = cohere.Client(cohere_api_key)
        response = co.generate(
            model="command",
            prompt=f"أنت مساعد يتحدث العربية. جاوب باختصار على ما يلي:\n{prompt}",
            max_tokens=200,
            temperature=0.6,
        )
        return response.generations[0].text.strip()
        
    except Exception as e:
        print(f"❌ خطأ في توليد الرد: {str(e)}")
        return None

def text_to_speech(text, output_file):
    """تحويل النص إلى صوت باستخدام pyttsx3 (بدون إنترنت)"""
    if not text:
        print("❌ لا يوجد نص للتحويل")
        return False
        
    try:
        # تهيئة محرك pyttsx3
        engine = pyttsx3.init()
        
        # البحث عن صوت عربي متاح
        voices = engine.getProperty('voices')
        arabic_voice = None
        for voice in voices:
            if 'arabic' in voice.name.lower() or 'ar' in voice.id.lower():
                arabic_voice = voice.id
                break
        
        if arabic_voice:
            engine.setProperty('voice', arabic_voice)
            print("✅ تم العثور على صوت عربي واستخدامه")
        else:
            print("⚠️ لم يتم العثور على صوت عربي، سيتم استخدام الصوت الافتراضي")
        
        # ضبط خصائص الصوت
        engine.setProperty('rate', 150)  # سرعة الكلمات في الدقيقة
        engine.setProperty('volume', 1.0)  # مستوى الصوت (0.0 إلى 1.0)
        
        # حفظ الصوت في ملف
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        
        print(f"🔊 تم تحويل النص إلى صوت وحفظه في: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تحويل النص إلى صوت: {str(e)}")
        return False

if __name__ == "__main__":
    if not check_google_credentials():
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="نظام معالجة الصوت بالذكاء الاصطناعي")
    parser.add_argument("--input", default="audio_input.wav", help="ملف الصوت المدخل")
    parser.add_argument("--output", default="audio_output.mp3", help="ملف الصوت المخرج")
    args = parser.parse_args()

    print("🎤 بدء تحويل الصوت إلى نص...")
    text = speech_to_text(args.input)
    
    if not text:
        sys.exit(1)
        
    print(f"🎤 النص المقروء: {text}")

    print("🧠 توليد الرد باستخدام الذكاء الاصطناعي...")
    response = generate_response(text)
    
    if not response:
        sys.exit(1)
        
    print(f"🧠 الرد المولد: {response}")

    print(f"🔊 تحويل النص إلى صوت...")
    if text_to_speech(response, args.output):
        print(f"✅ تم بنجاح: يمكنك الاستماع إلى الملف الصوتي في {args.output}")