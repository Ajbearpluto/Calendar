import os
import json
import datetime
import urllib.request
import urllib.error
import time

def generate_omniverse_data():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ 錯誤：GEMINI_API_KEY 未設定。")
    
    # 【零一決議】：已徹底移除愚蠢的 AIza 開頭檢查，全面支援 AQ. 等合法金鑰。

    tz = datetime.timezone(datetime.timedelta(hours=8))
    today_str = datetime.datetime.now(tz).strftime('%Y-%m-%d')

    print(f"🌌 正在為 {today_str} 進行原生 API 創世運算...")

    prompt = """
    你是「太極萬象日曆」的創世神。你的任務是生成 4 段極具「巴納姆效應(Barnum Effect)」、能引發現代大眾強烈共鳴的生活散文。
    必須嚴格包含 4 個物件，對應現代人的四種情境：
    1. 都會生存：寫現代人的焦慮、進度條卡住、指標劇烈起伏，給予允許停滯的安慰。
    2. 慢活細節：寫耐心觀察事物成形、萃取等待的過程，傳達不急躁的禪意。
    3. 浩瀚自然：寫走在冷空氣步道、仰望無盡夜空的孤獨，對比人類渺小與放下執念。
    4. 溫暖羈絆：寫身邊在意的人露出的笑容、微小善意的陪伴，傳達純粹的治癒力量。
    
    【極度重要】：
    必須輸出為純 JSON 陣列，每個物件必須完全符合以下 6 個 Key 值，絕不可更改名稱：
    [
      {
        "theme": "都會生存",
        "article": "捷運車廂裡陌生人的疲憊側臉，提醒我們允許偶爾的停滯。世界不會因為你停下五分鐘而崩塌。",
        "quote": "生活不需要永遠滿血，偶爾斷線也是一種戰術。",
        "hashtag": "斷線",
        "do_action": "躺平",
        "dont_action": "焦慮"
      }
    ]
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    data = json.dumps(payload).encode('utf-8')
    
    # 回歸唯一真理端點
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"📡 嘗試連線 (第 {attempt + 1}/{max_retries} 次)...")
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                raw_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                print("✅ API 連線成功！")
                break 
        except urllib.error.HTTPError as e:
            if e.code in [503, 500, 429]: # 遇到伺服器忙碌或限流，進行重試
                print(f"⚠️ 伺服器忙碌 (狀態碼: {e.code})，2秒後進行重試...")
                time.sleep(2)
                continue
            else:
                # 其他嚴重錯誤 (如 400 格式錯, 403 沒權限) 直接拋出
                error_info = e.read().decode('utf-8')
                raise ValueError(f"❌ 致命連線錯誤 (狀態碼: {e.code}): {error_info}")
    else:
        raise ValueError("❌ 慘烈失敗：已達最大重試次數，Google 伺服器無回應。")
            
    # 暴力清理 Markdown
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
    print("🚀 Taiji Genesis Engine: 啟動覺醒版原生大腦...")
    
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
