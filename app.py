import os
import argparse
import sys
import cohere
from dotenv import load_dotenv
from google.cloud import speech
from gtts import gTTS

load_dotenv()

def speech_to_text(audio_file):
    """تحويل الصوت إلى نص باستخدام Google Cloud Speech-to-Text"""
    client = speech.SpeechClient()
    try:
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
            prompt=prompt,
            max_tokens=300,
            temperature=0.7,
            stop_sequences=["\n\n"]
        )
        return response.generations[0].text.strip()
        
    except Exception as e:
        print(f"❌ خطأ في توليد الرد: {str(e)}")
        return None

def text_to_speech(text, output_file):
    """تحويل النص إلى صوت باستخدام gTTS"""
    if not text:
        print("❌ لا يوجد نص للتحويل")
        return False
        
    try:
        tts = gTTS(text=text, lang="ar", slow=False)
        tts.save(output_file)
        return True
    except Exception as e:
        print(f"❌ خطأ في تحويل النص إلى صوت: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="نظام معالجة الصوت باستخدام الذكاء الاصطناعي")
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
        print(f"✅ تم حفظ الصوت في: {args.output}")