import os
import json
import datetime
import urllib.request
import urllib.error
import random
import time

def generate_omniverse_data():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ 錯誤：GEMINI_API_KEY 未設定。")
    
    tz = datetime.timezone(datetime.timedelta(hours=8))
    today_str = datetime.datetime.now(tz).strftime('%Y-%m-%d')

    print(f"🌌 正在為 {today_str} 進行量子文學創世運算...")

    styles = [
        "奧斯卡·王爾德《快樂王子》的無私與唯美哀傷",
        "赫曼·赫塞《流浪者之歌》的東方求道與萬物圓融",
        "紀伯倫《先知》如散文詩般的通透人生智慧",
        "法國名著《小王子》的純真與人生哲理",
        "宮澤賢治《銀河鐵道之夜》的宇宙意象與生死觀",
        "芥川龍之介《蜘蛛之絲》的人性幽暗與一念慈悲",
        "泰戈爾《飛鳥集》的極簡自然意象與生命哲理",
        "王小棣導演《魔法阿媽》的台灣本土溫暖與人情味",
        "《海賊王》(One Piece) 追尋自由與夥伴羈絆的熱血視角",
        "《多啦A夢》在平凡日常中遇見奇蹟的童趣視角",
        "《七龍珠》不斷突破自我極限的戰鬥與修行哲學",
        "《咒術迴戰》在詛咒與絕望中尋找生存意義的視角",
        "《火影忍者》傳承火之意志與忍道堅持的視角",
        "《名偵探柯南》在微小細節中勘破真相的推理視角",
        "像皮克敏(Pikmin)般微小卻團結面對巨大世界的視角",
        "史努比(Snoopy)那種慵懶、幽默又帶點哲學的犬系視角",
        "台灣黑熊在深山林道中漫步的孤獨與堅韌",
        "獨自重裝攀登嘉明湖時，面對浩瀚大自然的敬畏與內心沉澱",
        "普契尼歌劇《公主徹夜未眠》那種在深夜裡堅持與盼望的壯麗",
        "如同一杯現煮的虹吸式咖啡，在緩慢萃取的等待中體悟的禪意",
        "現代都會社畜的『躺平無罪』與『人間清醒』幹話哲學"
    ]
    chosen_styles = random.sample(styles, 4)

    # 【修復 2：賦予靈魂語氣，徹底終結文字雷同】
    prompt = f"""
    你是「太極萬象日曆」的創世神。你的任務是生成 4 段極具「巴納姆效應」的生活散文。
    
    為了讓 4 個宇宙的文字擁有「極端不同的個性」，避免讀起來像同一個人寫的，請嚴格套用以下語氣：
    
    1. 宇宙一：【{chosen_styles[0]}】。語氣要求：👉「幽默、自嘲、帶點現代社畜的無奈與慵懶」。
    2. 宇宙二：【{chosen_styles[1]}】。語氣要求：👉「極度唯美、詩意、溫柔治癒，像一首散文詩」。
    3. 宇宙三：【{chosen_styles[2]}】。語氣要求：👉「磅礡、史詩感、充滿大自然或宇宙的敬畏與哲學思辨」。
    4. 宇宙四：【{chosen_styles[3]}】。語氣要求：👉「冷靜、極簡、充滿東方禪意、一針見血的留白」。
    
    【極度重要：嚴格 JSON 格式】：
    - 絕對不要輸出任何解釋、思考過程或 Markdown 標記以外的文字。
    - 必須輸出為純 JSON 陣列，包含精準的 4 個物件，每個物件必須有以下 7 個 Key：
    [
      {{
        "theme": "自訂風格標籤(如: 躺平美學 / 唯美哀傷)",
        "article": "40~60字的情境散文，必須強烈展現該宇宙要求的『語氣』！",
        "quote": "15~25字的一擊必殺金句。",
        "hashtag": "兩個字標籤",
        "do_action": "兩個字的宜行動",
        "dont_action": "兩個字的忌禁忌",
        "image_subject": "一句簡短的英文，描述與這段文字意境相符的畫面主體（如：A lonely swordsman under a red moon.）。純描述畫面，不要加相機參數。"
      }}
    ]
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.95 
        }
    }
    data = json.dumps(payload).encode('utf-8')
    
    candidate_endpoints = [
        "v1beta/models/gemini-3.8-flash",
        "v1beta/models/gemini-3.6-flash"
    ]
    
    # API 連線與重試機制：【保證絕對原樣，一字未改】
    for endpoint in candidate_endpoints:
        url = f"https://generativelanguage.googleapis.com/{endpoint}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        print(f"📡 鎖定現役端點: {endpoint}，準備叩關...")
        
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    raw_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                    
                    if raw_text.startswith("```json"): raw_text = raw_text[7:]
                    elif raw_text.startswith("```"): raw_text = raw_text[3:]
                    if raw_text.endswith("```"): raw_text = raw_text[:-3]
                    raw_text = raw_text.strip()
                    
                    try:
                        quotes_data = json.loads(raw_text)
                        if isinstance(quotes_data, list) and len(quotes_data) == 4 and "image_subject" in quotes_data[0]:
                            print(f"✅ 叩關成功！{endpoint} 輸出完美 JSON 格式。")
                            return quotes_data, today_str
                        else:
                            print(f"⚠️ {endpoint} 輸出結構錯誤，捨棄並重試 (第 {attempt+1}/4 次)...")
                            time.sleep(2)
                            continue
                    except json.JSONDecodeError:
                        print(f"⚠️ {endpoint} 未遵守 JSON 格式規定，捨棄並重試 (第 {attempt+1}/4 次)...")
                        time.sleep(2)
                        continue
                        
            except urllib.error.HTTPError as e:
                if e.code in [503, 500, 429]:
                    print(f"⚠️ 伺服器大塞車 ({e.code})，深呼吸冷靜 5 秒後重新敲門 (第 {attempt+1}/4 次)...")
                    time.sleep(5)
                    continue 
                elif e.code in [404, 403]:
                    print(f"⚠️ {endpoint} 權限不足或不存在 ({e.code})，放棄此端點，切換下一組。")
                    break 
                else:
                    print(f"⚠️ {endpoint} 未知錯誤 ({e.code})，跳過此端點。")
                    break
    
    raise ValueError("❌ 慘烈失敗：現役 Gemini 模型皆因伺服器嚴重過載或權限問題，無法順利生成。")

def main():
    print("🚀 Taiji Genesis Engine: 啟動無盡萬象宇宙版...")
    
    try:
        quotes_data, today_str = generate_omniverse_data()
        quotes_js_string = json.dumps(quotes_data, ensure_ascii=False)
        print("✅ 嚴格檢驗通過，準備寫入皮囊！")
    except Exception as e:
        raise SystemExit(f"💀 大腦創世失敗，停止注入。錯誤原因: {e}")

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
