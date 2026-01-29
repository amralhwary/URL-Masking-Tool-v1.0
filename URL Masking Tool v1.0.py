import re
import requests
import sys
import os
from urllib.parse import urlparse

class DAGDLinkShortener:
    def __init__(self, language='en'):
        self.api_url = "https://da.gd/shorten"
        self.language = language
        
      
        self.texts = {
            'en': {
                'invalid_url': "❌ Invalid URL, try again. Example: https://example.com",
                'invalid_domain': "❌ Invalid domain, try again. Example: https://pentratiom.com",
                'invalid_keyword': "❌ Invalid keyword. Use only letters, numbers and dash",
                'enter_url': "Enter the URL (With http or https): ",
                'enter_domain': "Enter the domain name to mask URL (With http or https): ",
                'enter_keyword': "Enter keywords (use '-' instead of whitespace): ",
                'processing': "\n⏳ Processing...\n",
                'mask_another': "🔄 Mask another URL? (yes/no): ",
                'yes_no_error': "❌ Enter 'yes' or 'no'",
                'goodbye': "\n👋 Goodbye! - Created by NSR",
                'choose_option': "👉 Choose option: ",
                'error_invalid_target': "❌ Error: Invalid target URL",
                'error_invalid_mask': "❌ Error: Invalid mask domain",
                'error_invalid_keyword': "❌ Error: Invalid keyword. Use letters, numbers and dash only",
                'error_shorten': "❌ Error: Could not shorten URL",
                'success': "✅ Masked URL: ",
                'menu': "\nMain Menu:",
                'option1': "1. 🚀 Mask a URL (Interactive)",
                'option2': "2. ℹ️  Show usage example",
                'option3': "3. ❌ Exit",
                'invalid_option': "\n❌ Invalid option!",
                'creator': "\n💡 Original Idea & Development by: NSR",
                'follow': "\n🌟 Follow NSR on:",
                'youtube': "   📺 YouTube:    https://www.youtube.com/@NSR.17",
                'github': "   💻 GitHub:     https://github.com/amralhwary",
                'instagram': "   📸 Instagram:  https://www.instagram.com/its_nsr.17/",
                'thank_you': "\nThank you for using this tool!",
                'created_with': "Created with ❤️ by NSR",
                'url_saved': "📁 URL saved to 'masked_urls.txt'",
                'example_title': "\nExample Usage:",
                'example_inputs': "\nInputs:",
                'example_target': "  Target URL: https://youtube.com",
                'example_mask': "  Mask Domain: https://pentratiom.com",
                'example_keywords': "  Keywords: watch19-7",
                'example_process': "\nProcess:",
                'example_step1': "  1. Shorten https://youtube.com → https://da.gd/CGayj",
                'example_step2': "  2. Parse URL → netloc: 'da.gd', path: '/CGayj'",
                'example_step3': "  3. Clean mask domain → 'pentratiom.com'",
                'example_step4': "  4. Build: https://pentratiom.com-watch19-7@da.gd/CGayj",
                'example_final': "\nFinal Result: https://pentratiom-watch19-7@da.gd/CGayj",
                'tool_by': "\n💡 Tool by NSR - Follow on:",
                'created_by': "\n👨‍💻 Creator: NSR",
                'thanks': "\nTool by NSR - Thanks for using!"
            },
            'ar': {
                'invalid_url': "❌ رابط غير صحيح، حاول مرة أخرى. مثال: https://example.com",
                'invalid_domain': "❌ نطاق غير صحيح، حاول مرة أخرى. مثال: https://pentratiom.com",
                'invalid_keyword': "❌ كلمة مفتاحية غير صالحة. استخدم فقط الحروف والأرقام والشرطة",
                'enter_url': "أدخل الرابط (مع http أو https): ",
                'enter_domain': "أدخل اسم النطاق لإخفاء الرابط (مع http أو https): ",
                'enter_keyword': "أدخل الكلمات المفتاحية (استخدم '-' بدلاً من المسافة): ",
                'processing': "\n⏳ جاري المعالجة...\n",
                'mask_another': "🔄 إخفاء رابط آخر؟ (نعم/لا): ",
                'yes_no_error': "❌ أدخل 'نعم' أو 'لا'",
                'goodbye': "\n👋 وداعاً! - صنع بواسطة NSR",
                'choose_option': "👉 اختر الخيار: ",
                'error_invalid_target': "❌ خطأ: رابط الهدف غير صالح",
                'error_invalid_mask': "❌ خطأ: نطاق الإخفاء غير صالح",
                'error_invalid_keyword': "❌ خطأ: الكلمة المفتاحية غير صالحة. استخدم فقط الحروف والأرقام والشرطة",
                'error_shorten': "❌ خطأ: تعذر تقصير الرابط",
                'success': "✅ الرابط المخفي: ",
                'menu': "\nالقائمة الرئيسية:",
                'option1': "1. 🚀 إخفاء رابط (وضع تفاعلي)",
                'option2': "2. ℹ️  عرض مثال للاستخدام",
                'option3': "3. ❌ خروج",
                'invalid_option': "\n❌ خيار غير صحيح!",
                'creator': "\n💡 الفكرة والتطوير الأصلي بواسطة: NSR",
                'follow': "\n🌟 تابع NSR على:",
                'youtube': "   📺 يوتيوب:    https://www.youtube.com/@NSR.17",
                'github': "   💻 جيتهاب:     https://github.com/amralhwary",
                'instagram': "   📸 إنستجرام:  https://www.instagram.com/its_nsr.17/",
                'thank_you': "\nشكراً لاستخدامك هذه الأداة!",
                'created_with': "صنع ب ❤️ بواسطة NSR",
                'url_saved': "📁 تم حفظ الرابط في ملف 'masked_urls.txt'",
                'example_title': "\nمثال للاستخدام:",
                'example_inputs': "\nالمدخلات:",
                'example_target': "  الرابط المستهدف: https://youtube.com",
                'example_mask': "  نطاق الإخفاء: https://pentratiom.com",
                'example_keywords': "  الكلمات المفتاحية: watch19-7",
                'example_process': "\nالعملية:",
                'example_step1': "  1. تقصير https://youtube.com → https://da.gd/CGayj",
                'example_step2': "  2. تحليل الرابط → netloc: 'da.gd', path: '/CGayj'",
                'example_step3': "  3. تنظيف نطاق الإخفاء → 'pentratiom.com'",
                'example_step4': "  4. البناء: https://pentratiom.com-watch19-7@da.gd/CGayj",
                'example_final': "\nالنتيجة النهائية: https://pentratiom-watch19-7@da.gd/CGayj",
                'tool_by': "\n💡 أداة بواسطة NSR - تابع على:",
                'created_by': "\n👨‍💻 المطور: NSR",
                'thanks': "\nأداة بواسطة NSR - شكراً للاستخدام!"
            }
        }
    
    def t(self, key):
        """احصل على النص المترجم"""
        return self.texts.get(self.language, self.texts['en']).get(key, key)
    
    def validate_keyword(self, keyword):
        if not keyword:
            return True
        pattern = r'^[a-zA-Z0-9\-]+$'
        return bool(re.match(pattern, keyword))
    
    def validate_url(self, url):
        pattern = r'^https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}'
        return bool(re.match(pattern, url))
    
    def clean_domain(self, domain):
        if not domain:
            return None
        domain = domain.strip()
        domain = domain.replace('http://', '').replace('https://', '')
        domain = domain.rstrip('/')
        if '/' in domain:
            domain = domain.split('/')[0]
        domain = domain.replace('www.', '')
        return domain
    
    def shorten_url(self, big_url):
        try:
            response = requests.post(
                self.api_url, 
                data={'url': big_url}, 
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if response.status_code == 200:
                short_url = response.text.strip()
                short_url = short_url.replace('\n', '').replace('\r', '')
                return short_url
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None
    
    def mask_url(self, target_url, mask_domain, keyword):
        
        if not self.validate_url(target_url):
            return f"{self.t('error_invalid_target')}"
        
        if not self.validate_url(mask_domain):
            return f"{self.t('error_invalid_mask')}"
        
        if not self.validate_keyword(keyword):
            return f"{self.t('error_invalid_keyword')}"
        
        short_url = self.shorten_url(target_url)
        if not short_url:
            return f"{self.t('error_shorten')}"
        
        parsed = urlparse(short_url)
        
        clean_mask = self.clean_domain(mask_domain)
        
        masked_url = f"https://{clean_mask}-{keyword}@{parsed.netloc + parsed.path}"
        
        return f"{self.t('success')}{masked_url}"
    
    def interactive_mode(self):
        print()
        
        while True:
            target = input(self.t('enter_url')).strip()
            if self.validate_url(target):
                break
            print(self.t('invalid_url'))
        
        while True:
            mask = input(self.t('enter_domain')).strip()
            if self.validate_url(mask):
                break
            print(self.t('invalid_domain'))
        
        while True:
            keyword = input(self.t('enter_keyword')).strip()
            if self.validate_keyword(keyword):
                break
            print(self.t('invalid_keyword'))
        
        print(self.t('processing'))
        result = self.mask_url(target, mask, keyword)
        
        print(result)
        
        return result

def select_language():
    """وظيفة اختيار اللغة"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = r"""
  _____        __            .__  .__        __    
_/ ____\____  |  | __ ____   |  | |__| ____ |  | __
\   __\\__  \ |  |/ // __ \  |  | |  |/    \|  |/ /
 |  |   / __ \|    <\  ___/  |  |_|  |   |  \    < 
 |__|  (____  /__|_ \\___  > |____/__|___|  /__|_ \
            \/     \/    \/               \/     \/ 
    
    URL Masking Tool v1.0 - Created by NSR
    أداة إخفاء الروابط - صنع بواسطة NSR
"""
    print(f"\033[91m{banner}\033[00m")
    
    print("\n" + "="*50)
    print("🌍 اختر اللغة / Select Language:")
    print("="*50)
    print("1. English 🇺🇸")
    print("2. العربية 🇸🇦")
    print("="*50)
    
    while True:
        choice = input("\n👉 اختر رقم اللغة / Select language number (1/2): ").strip()
        if choice == '1':
            return 'en'
        elif choice == '2':
            return 'ar'
        else:
            print("❌ خيار غير صحيح! / Invalid choice!")

def main():
    language = select_language()
    shortener = DAGDLinkShortener(language)
    
    banner = r"""
  _____        __            .__  .__        __    
_/ ____\____  |  | __ ____   |  | |__| ____ |  | __
\   __\\__  \ |  |/ // __ \  |  | |  |/    \|  |/ /
 |  |   / __ \|    <\  ___/  |  |_|  |   |  \    < 
 |__|  (____  /__|_ \\___  > |____/__|___|  /__|_ \
            \/     \/    \/               \/     \/ 
    
        Created by NSR - URL Masking Tool v1.0
"""
    print(f"\033[91m{banner}\033[00m")
    
    print(shortener.t('creator'))
    print(shortener.t('follow'))
    print(shortener.t('youtube'))
    print(shortener.t('github'))
    print(shortener.t('instagram'))
    
    while True:
        print(shortener.t('menu'))
        print(shortener.t('option1'))
        print(shortener.t('option2'))
        print(shortener.t('option3'))
        
        choice = input(f"\n{shortener.t('choose_option')}").strip()
        
        if choice == '1':
            result = shortener.interactive_mode()
            
            if shortener.t('success') in result:
                url_only = result.split(shortener.t('success'))[1]
                print(f"\n\033[91m{url_only}\033[00m")
            
            while True:
                again = input(f"\n{shortener.t('mask_another')}").strip().lower()
                if again in ['yes', 'y', 'نعم', 'ن']:
                    break
                elif again in ['no', 'n', 'لا', 'ل']:
                    print(shortener.t('goodbye'))
                    sys.exit(0)
                else:
                    print(shortener.t('yes_no_error'))
                    
        elif choice == '2':
            print(shortener.t('example_title'))
            
            print(shortener.t('example_inputs'))
            print(shortener.t('example_target'))
            print(shortener.t('example_mask'))
            print(shortener.t('example_keywords'))
            
            print(shortener.t('example_process'))
            print(shortener.t('example_step1'))
            print(shortener.t('example_step2'))
            print(shortener.t('example_step3'))
            print(shortener.t('example_step4'))
            
            print(f"\n\033[91m{shortener.t('example_final')}\033[00m")
            
            print(shortener.t('tool_by'))
            print(shortener.t('youtube'))
            print(shortener.t('github'))
            print(shortener.t('instagram'))
            
        elif choice == '3':
            print(shortener.t('thank_you'))
            print(shortener.t('created_with'))
            print(f"\n{shortener.t('follow')}")
            print(shortener.t('youtube'))
            print(shortener.t('github'))
            print(shortener.t('instagram'))
            break
            
        else:
            print(shortener.t('invalid_option'))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="URL Masking Tool - Created by NSR",
        epilog="Follow NSR: YouTube(@NSR.17) | GitHub(amralhwary) | Instagram(its_nsr.17)"
    )
    
    parser.add_argument(
        "--target",
        type=str,
        help="Target URL to Mask (With http or https)",
    )
    parser.add_argument(
        "--mask",
        type=str,
        help="Mask URL (With http or https)",
    )
    parser.add_argument(
        "--keywords",
        type=str,
        help="Keywords (Use (-) instead of whitespace)",
    )
    parser.add_argument(
        "--lang",
        type=str,
        choices=['en', 'ar'],
        default='en',
        help="Language: 'en' for English, 'ar' for Arabic"
    )
    
    if len(sys.argv) == 1:
        main()
    else:
        args = parser.parse_args()
        
      
        language = args.lang if hasattr(args, 'lang') else 'en'
        
        if not all([args.target, args.mask, args.keywords]):
            print("❌ Error: All arguments (--target, --mask, --keywords) are required!")
            print("\n💡 Example:")
            print("   python url_masker.py --target https://google.com --mask https://mydomain.com --keywords search-tool --lang en")
            print("\n👨‍💻 Created by NSR:")
            print("   YouTube:   https://www.youtube.com/@NSR.17")
            print("   GitHub:    https://github.com/amralhwary")
            print("   Instagram: https://www.instagram.com/its_nsr.17/")
            sys.exit(1)
        
        shortener = DAGDLinkShortener(language)
        result = shortener.mask_url(args.target, args.mask, args.keywords)
        
        banner = r"""
  _____        __            .__  .__        __    
_/ ____\____  |  | __ ____   |  | |__| ____ |  | __
\   __\\__  \ |  |/ // __ \  |  | |  |/    \|  |/ /
 |  |   / __ \|    <\  ___/  |  |_|  |   |  \    < 
 |__|  (____  /__|_ \\___  > |____/__|___|  /__|_ \
            \/     \/    \/               \/     \/ 
    
        URL Masking Tool v1.0 - Created by NSR
"""
        print(f"\033[91m{banner}\033[00m")
        
        print(shortener.t('created_by'))
        print(shortener.t('youtube'))
        print(shortener.t('github'))
        print(shortener.t('instagram'))
        print()
        
        if shortener.t('success') in result:
            url_only = result.split(shortener.t('success'))[1]
            print(f"\033[91m{url_only}\033[00m")
            
            try:
                with open("masked_urls.txt", "a", encoding="utf-8") as f:
                    f.write(f"{url_only}\n")
                print(f"\n{shortener.t('url_saved')}")
            except:
                pass
        else:
            print(f"\n{result}")
        
        print(shortener.t('thanks'))
