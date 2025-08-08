import os
import json
import sys

def setup_google_cloud():
    print("🛠️ إعداد Google Cloud Speech-to-Text")
    print("="*50)
    
    # 1. الحصول على بيانات الاعتماد
    print("\n1. سجل الدخول إلى Google Cloud Console:")
    print("   https://console.cloud.google.com/")
    print("2. أنشئ مشروع جديد أو اختر مشروع موجود")
    print("3. ابحث عن 'Cloud Speech-to-Text API' وقم بتفعيلها")
    print("4. اذهب إلى 'Service Accounts' وأنشئ حساب خدمي جديد")
    print("5. اختر دور 'Cloud Speech API User'")
    print("6. في قسم 'Keys'، أنشئ مفتاح جديد من نوع JSON")
    print("7. افتح ملف JSON الذي تم تنزيله وانسخ محتواه")
    
    # 2. قراءة بيانات الاعتماد من المستخدم
    print("\n" + "="*50)
    creds_data = input("\nالصق محتوى ملف الاعتماد JSON هنا: ")
    
    try:
        # 3. حفظ الاعتماد في ملف
        with open("google_credentials.json", "w") as f:
            f.write(creds_data)
        
        # 4. تعيين متغير البيئة
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("google_credentials.json")
        
        print("\n✅ تم الإعداد بنجاح!")
        print(f"تم حفظ الاعتماد في: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
        
        # 5. تعليمات للاستخدام الدائم
        print("\nلتعيين هذا المسار دائمًا، شغّل:")
        print(f'   Windows: setx GOOGLE_APPLICATION_CREDENTIALS "{os.environ["GOOGLE_APPLICATION_CREDENTIALS"]}"')
        print(f'   Linux/Mac: echo \'export GOOGLE_APPLICATION_CREDENTIALS="{os.environ["GOOGLE_APPLICATION_CREDENTIALS"]}"\' >> ~/.bashrc')
        
        return True
    except Exception as e:
        print(f"❌ خطأ في حفظ الاعتماد: {str(e)}")
        return False

if __name__ == "__main__":
    if setup_google_cloud():
        sys.exit(0)
    else:
        sys.exit(1)