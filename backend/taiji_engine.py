import os
import json
import datetime
import google.generativeai as genai

def generate_omniverse_data():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ 錯誤：GEMINI_API_KEY 未設定，無法喚醒大腦。")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    tz = datetime.timezone(datetime.timedelta(hours=8))
    today_str = datetime.datetime.now(tz).strftime('%Y-%m-%d')

    print(f"🌌 正在為 {today_str} 進行 AI 創世運算...")

    prompt = f"""
    你是「太極萬象日曆」的創世神。請生成 4 段極具「巴納姆效應(Barnum Effect)」、能引發現代大眾強烈共鳴的生活散文。
    
    【重要規定】：
    1. 必須輸出「純 JSON 陣列」，嚴禁使用 Markdown 標記 (如 ```json)、嚴禁任何開場白或解釋文字。
    2. 必須嚴格包含 4 個物件，對應現代人的四種情境：都會焦慮、微小慢活、大自然敬畏、人際溫暖。
    3. 所有的 Key 必須完全依照下列格式，不能多也不能少：
    
    [
      {{
        "theme": "都會生存",
        "article": "捷運車廂裡陌生人的疲憊側臉，提醒我們允許偶爾的停滯。世界不會因為你停下五分鐘而崩塌。",
        "quote": "生活不需要永遠滿血，偶爾斷線也是一種戰術。",
        "hashtag": "斷線",
        "do_action": "躺平",
        "dont_action": "焦慮"
      }},
      ... (其餘 3 個物件)
    ]
    """

    response = model.generate_content(prompt)
    raw_text = response.text.strip()
    
    # 嚴格清理任何可能破壞 JSON 解析的 Markdown 符號
    if raw_text.startswith("```"):
        lines = raw_text.split('\n')
        if lines[0].startswith("```"): lines = lines[1:]
        if lines[-1].startswith("```"): lines = lines[:-1]
        raw_text = '\n'.join(lines).strip()
        
    try:
        data = json.loads(raw_text)
        if not isinstance(data, list) or len(data) != 4:
            raise ValueError("JSON 結構錯誤：不是長度為 4 的陣列")
        return data, today_str
    except Exception as e:
        print(f"❌ JSON 格式解析失敗！Gemini 原始回應內容如下：\n{raw_text}")
        raise e

def main():
    print("🚀 Taiji Genesis Engine: 啟動大腦...")
    
    try:
        quotes_data, today_str = generate_omniverse_data()
        quotes_js_string = json.dumps(quotes_data, ensure_ascii=False)
        print("✅ 成功生成並驗證 JSON 陣列！範例如下：")
        print(json.dumps(quotes_data, ensure_ascii=False, indent=2))
    except Exception as e:
        # 如果大腦當機，直接報錯中止，絕對不拿假陣列去污染 HTML
        raise SystemExit(f"💀 大腦創世失敗，停止注入皮囊。錯誤原因: {e}")

    template_path = os.path.join('frontend', 'template.html')
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"找不到皮囊檔案：{template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 精準寫入皮囊
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
        
    print("🎉 大腦意識已成功注入皮囊並封存！")

if __name__ == "__main__":
    main()
