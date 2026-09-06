import os
import json
import datetime
from google import genai
from google.genai import types

def generate_omniverse_data():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ 錯誤：GEMINI_API_KEY 未設定，無法喚醒大腦。")
    
    # 建立新版 Gemini 客戶端
    client = genai.Client(api_key=api_key)

    tz = datetime.timezone(datetime.timedelta(hours=8))
    today_str = datetime.datetime.now(tz).strftime('%Y-%m-%d')

    print(f"🌌 正在為 {today_str} 進行 Gemini Spark 創世運算...")

    # 普世巴納姆 Prompt，將您的世界觀提煉為大眾共鳴
    prompt = """
    你是「太極萬象日曆」的創世神。你的任務是生成 4 段極具「巴納姆效應(Barnum Effect)」、能引發現代大眾強烈共鳴的生活散文。
    必須嚴格包含 4 個物件，對應現代人的四種情境：
    1. 都會生存：寫現代人的焦慮、進度條卡住、指標劇烈起伏，給予允許停滯的安慰。
    2. 慢活細節：寫耐心觀察事物成形、萃取等待的過程，傳達不急躁的禪意。
    3. 浩瀚自然：寫走在冷空氣步道、仰望無盡夜空的孤獨，對比人類渺小與放下執念。
    4. 溫暖羈絆：寫身邊在意的人露出的笑容、微小善意的陪伴，傳達純粹的治癒力量。
    
    寫作要領：使用「看似精準，實則模糊」的語句。例如不要寫特定對象或山名，而是寫「當生活中的指標劇烈起伏時」或「走在冷空氣中的孤獨步道」。
    
    必須輸出為 JSON 陣列，每個物件必須完全符合以下 Key 值，不要有任何 Markdown 或額外文字：
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

    # 呼叫 API 並強制限制輸出為 JSON 格式 (防呆機制)
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        )
    )
    
    raw_text = response.text.strip()
    
    try:
        data = json.loads(raw_text)
        if not isinstance(data, list) or len(data) != 4:
            raise ValueError(f"JSON 結構錯誤：必須是長度為 4 的陣列，收到長度 {len(data) if isinstance(data, list) else '非陣列'}")
        return data, today_str
    except Exception as e:
        print(f"❌ JSON 格式解析失敗！原始回應內容如下：\n{raw_text}")
        raise e

def main():
    print("🚀 Taiji Genesis Engine: 啟動新世代大腦...")
    
    try:
        quotes_data, today_str = generate_omniverse_data()
        quotes_js_string = json.dumps(quotes_data, ensure_ascii=False)
        print("✅ 大腦生成成功！請檢視以下 JSON 結構是否符合對照表：")
        print(json.dumps(quotes_data, ensure_ascii=False, indent=2))
    except Exception as e:
        raise SystemExit(f"💀 大腦創世失敗，停止注入。錯誤原因: {e}")

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
