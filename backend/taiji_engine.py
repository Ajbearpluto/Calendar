import os
import json
import datetime
import google.generativeai as genai

def generate_omniverse_data():
    # 1. 初始化 Gemini 大腦
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("無法喚醒 Gemini，請確認 GitHub Secrets 是否已設定 GEMINI_API_KEY")
    
    genai.configure(api_key=api_key)
    # 使用超高速的 flash 模型
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 取得台灣今天日期
    tz = datetime.timezone(datetime.timedelta(hours=8))
    today_str = datetime.datetime.now(tz).strftime('%Y-%m-%d')

    print(f"🌌 正在為 {today_str} 進行 AI 創世運算...")

    # 2. 最高機密的「普世巴納姆」系統提示詞
    prompt = f"""
    你是「太極萬象日曆」的創世神。你的任務是生成 4 段極具「巴納姆效應(Barnum Effect)」、能引發大眾強烈共鳴的生活散文與格言。
    今天是 {today_str}。不要用任何模板，每一句話都要像真實人類寫出來的。
    
    這 4 段文字分別對應四種普世情境：
    1. 【人間/都會浮生】：寫現代人的焦慮、疲憊、進度條卡住、人際關係的疏離，並給予放下與允許停滯的安慰。
    2. 【細節/慢活哲學】：寫微小的事物(如咖啡、喝茶、白噪音、雨滴)，傳達放慢步調、靜心專注、不急躁的禪意。
    3. 【浩瀚/自然隱喻】：寫山脈、星空、沙漠、深海，對比人類的渺小，傳達放下執念、心胸開闊的壯闊感。
    4. 【萬物/溫暖羈絆】：寫動物、植物的生機，或是人與人之間微小卻溫暖的善意，傳達被治癒與陪伴的力量。
    
    請務必輸出為純 JSON 陣列格式(不要加 ```json 標籤，只要純陣列)，包含 4 個物件，每個物件必須有以下欄位：
    - "style": 主題標籤 (如：人間清醒, 慢活時光, 浩瀚視角, 溫暖微光)
    - "article": 一段 40~60 字的極致寫實散文。描述當下的細微情境(視覺/聽覺)與內心的體悟。必須充滿溫度。
    - "q": 一句 15~25 字的一擊必殺金句。必須能讓人截圖發 IG 限動。
    - "p": 兩個字的心境標籤 (如：日常, 沉澱, 仰望, 療癒)
    - "do": 兩個字的宜做事項 (如：放空, 喝茶)
    - "dont": 兩個字的忌做事項 (如：焦慮, 攀比)
    """

    # 3. 呼叫 Gemini 進行生成
    response = model.generate_content(prompt)
    
    # 清理回應，確保是乾淨的 JSON
    raw_text = response.text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
        
    quotes_data = json.loads(raw_text.strip())
    return quotes_data, today_str

def main():
    print("🚀 Taiji Genesis Engine: 啟動每日 AI 創世程序...")
    
    try:
        quotes_data, today_str = generate_omniverse_data()
        quotes_js_string = json.dumps(quotes_data, ensure_ascii=False)
        print("✅ Gemini 創世完成，獲得全新 4 個宇宙靈魂。")
    except Exception as e:
        print(f"❌ Gemini 創世失敗: {e}")
        print("降級使用本地緊急備用電源...")
        today_str = "Unknown"
        quotes_js_string = "[]" # 失敗時傳空陣列，讓前端接管

    # 4. 讀取前端皮囊
    template_path = os.path.join('frontend', 'template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 5. 靈魂注入皮囊
    html_content = html_content.replace('__PAYLOAD_DATE__', today_str)
    html_content = html_content.replace('__QUOTES_JS__', quotes_js_string)

    # 6. 覆寫今日首頁
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 7. 寫入永久歷史備份
    archive_dir = 'archive'
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    archive_path = os.path.join(archive_dir, f"{today_str}.html")
    with open(archive_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print("🎉 太極宇宙渲染完畢，歷史備份已安全封存！")

if __name__ == "__main__":
    main()
