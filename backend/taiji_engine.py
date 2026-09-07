import os
import json
import datetime
import urllib.request
import urllib.error
import time
import random

def generate_omniverse_data():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ 錯誤：GEMINI_API_KEY 未設定。")
    
    tz = datetime.timezone(datetime.timedelta(hours=8))
    today_str = datetime.datetime.now(tz).strftime('%Y-%m-%d')

    print(f"🌌 正在為 {today_str} 進行原生 API 創世運算...")

    # ==========================================
    # 📖 文學宗師的「量子亂數風格池」
    # ==========================================
    styles = [
        "法國名著《小王子》的純真與人生哲理",
        "王小棣導演《魔法阿媽》那種台灣本土的溫暖、遺憾與人情味",
        "《名偵探柯南》般在日常細節中尋找微小真相的推理視角",
        "普契尼歌劇《公主徹夜未眠》那種在深夜裡堅持與盼望的壯麗情感",
        "獨自重裝攀登高海拔百岳（如嘉明湖）時，面對浩瀚大自然的敬畏與內心沉澱",
        "像皮克敏(Pikmin)或史努比(Snoopy)那樣，以幽默可愛的微觀視角看待大人的煩惱",
        "賽博龐克(Cyberpunk)的霓虹都市孤獨感與科技反思",
        "日系雜誌般清新、通透且注重生活微小細節的慢活視角",
        "猶如電影長鏡頭般的冷調敘事，充滿空間感與疏離感"
    ]
    
    # 隨機抽取 4 種不同風格，賦予今日的 4 篇散文
    chosen_styles = random.sample(styles, 4)

    prompt = f"""
    你是「太極萬象日曆」的創世神。你的任務是生成 4 段極具「巴納姆效應(Barnum Effect)」的生活散文，每一段必須採用指定的文學或電影風格。
    
    情境與風格分配：
    1. 宇宙一 (都會生存)：請以【{chosen_styles[0]}】的風格來撰寫。
    2. 宇宙二 (慢活細節)：請以【{chosen_styles[1]}】的風格來撰寫。
    3. 宇宙三 (浩瀚自然)：請以【{chosen_styles[2]}】的風格來撰寫。
    4. 宇宙四 (溫暖羈絆)：請以【{chosen_styles[3]}】的風格來撰寫。
    
    【寫作要領】：
    - 文章內容必須緊扣上述分配的風格，讓文字有哲理、幽默、或是高山的沉澱感。
    - 必須輸出為純 JSON 陣列，每個物件必須完全符合以下 6 個 Key 值：
    [
      {{
        "theme": "根據風格自訂標籤(例如：微觀哲學、霓虹孤獨)",
        "article": "40~60字的情境散文，完美融入指定的風格與巴納姆效應。",
        "quote": "15~25字的一擊必殺金句。",
        "hashtag": "兩個字的情境標籤",
        "do_action": "兩個字的宜行動",
        "dont_action": "兩個字的忌禁忌"
      }}
    ]
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.9 # 提高創意溫度，讓文字千變萬化
        }
    }
    data = json.dumps(payload).encode('utf-8')
    
    # 程式宗師的穩定端點陣列 (v1beta 擁有最高的模型涵蓋率)
    endpoints = [
        "v1beta/models/gemini-1.5-flash",
        "v1beta/models/gemini-1.5-pro",
        "v1beta/models/gemini-pro"
    ]
    
    raw_text = None
    
    for endpoint in endpoints:
        url = f"https://generativelanguage.googleapis.com/{endpoint}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        try:
            print(f"📡 嘗試連線端點: {endpoint} ...")
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                raw_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                print(f"✅ 連線成功！成功使用端點: {endpoint}")
                break 
        except urllib.error.HTTPError as e:
            print(f"⚠️ {endpoint} 連線失敗 (狀態碼: {e.code})，自動切換備用端點...")
            continue
            
    if not raw_text:
        raise ValueError("❌ 慘烈失敗：所有連線皆失敗，請再次確認您的 API Key 是否有效。")
            
    if raw_text.startswith("```json"): raw_text = raw_text[7:]
    elif raw_text.startswith("```"): raw_text = raw_text[3:]
    if raw_text.endswith("```"): raw_text = raw_text[:-3]
    raw_text = raw_text.strip()
    
    try:
        quotes_data = json.loads(raw_text)
        if not isinstance(quotes_data, list) or len(quotes_data) != 4:
            raise ValueError("JSON 結構長度錯誤：必須是 4 個物件的陣列。")
        return quotes_data, today_str
        
    except Exception as e:
        print(f"❌ JSON 格式解析失敗！原始回應內容如下：\n{raw_text}")
        raise e

def main():
    print("🚀 Taiji Genesis Engine: 啟動量子文學大腦...")
    
    try:
        quotes_data, today_str = generate_omniverse_data()
        quotes_js_string = json.dumps(quotes_data, ensure_ascii=False)
        print("✅ 大腦生成成功！請檢視以下 JSON 結構：")
        print(json.dumps(quotes_data, ensure_ascii=False, indent=2))
    except Exception as e:
        raise SystemExit(f"💀 大腦創世失敗，停止注入皮囊。錯誤原因: {e}")

    template_path = os.path.join('frontend', 'template.html')
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"找不到皮囊檔案：{template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    html_content = html_content.replace('__PAYLOAD_DATE__', today_str)
    html_content = html_content.replace('__QUOTES_JS__', quotes_js_string)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    archive_dir = 'archive'
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    archive_path = os.path.join(archive_dir, f"{today_str}.html")
    with open(archive_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print("🎉 大腦意識已成功寫入 HTML！")

if __name__ == "__main__":
    main()
