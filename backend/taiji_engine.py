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

    # 文學宗師的無限資料庫：加入西方哲理與東方靈性，並保留生活微觀
    styles = [
        "奧斯卡·王爾德《快樂王子》極致唯美卻又無比哀傷，探討愛與無私犧牲的視角",
        "赫曼·赫塞《流浪者之歌》歷經世俗誘惑，最終在萬物圓融中體悟內在平靜的東方求道視角",
        "紀伯倫《先知》如散文詩般優雅，蘊含通透人生智慧的智者視角",
        "宮澤賢治《銀河鐵道之夜》充滿宇宙意象，探討孤獨、生死與真正幸福的星際視角",
        "芥川龍之介《蜘蛛之絲》在極短篇幅內刻畫人性幽暗、貪婪與一念慈悲的佛教寓言視角",
        "泰戈爾《飛鳥集》用極簡自然意象捕捉深邃東方宇宙觀與生命哲理的詩意視角",
        "法國名著《小王子》的純真與人生哲理",
        "王小棣導演《魔法阿媽》那種台灣本土的溫暖、遺憾與人情味",
        "獨自重裝攀登高海拔百岳（如嘉明湖）時，面對浩瀚大自然的敬畏與內心沉澱",
        "像皮克敏(Pikmin)或史努比(Snoopy)那樣，以幽默可愛的微觀視角看待大人的煩惱",
        "日系雜誌般清新、通透且注重生活微小細節的慢活視角",
        "如同一杯現煮的虹吸式咖啡，在緩慢萃取的等待中體悟時間的禪意"
    ]
    # 隨機抽取 4 種不同風格
    chosen_styles = random.sample(styles, 4)

    prompt = f"""
    你是「太極萬象日曆」的創世神。你的任務是生成 4 段極具「巴納姆效應(Barnum Effect)」的生活散文。
    
    情境與風格分配：
    1. 宇宙一 (都會生存)：請以【{chosen_styles[0]}】的風格來撰寫。
    2. 宇宙二 (慢活細節)：請以【{chosen_styles[1]}】的風格來撰寫。
    3. 宇宙三 (浩瀚自然)：請以【{chosen_styles[2]}】的風格來撰寫。
    4. 宇宙四 (溫暖羈絆)：請以【{chosen_styles[3]}】的風格來撰寫。
    
    【極度重要：嚴格 JSON 格式】：
    - 內容必須緊扣分配的風格，讓文字有哲理、幽默、或是高山的沉澱感。
    - 絕對不要輸出任何解釋、思考過程或 Markdown 標記以外的文字。
    - 必須輸出為純 JSON 陣列，包含精準的 4 個物件，每個物件 6 個 Key：
    [
      {{
        "theme": "自訂風格標籤(例如: 星際求道)",
        "article": "40~60字的情境散文，完美融入指定風格。",
        "quote": "15~25字的一擊必殺金句。",
        "hashtag": "兩個字標籤",
        "do_action": "兩個字的宜行動(如: 仰望)",
        "dont_action": "兩個字的忌禁忌(如: 執著)"
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
    
    # 程式宗師的改良：雙層耐心迴圈 (先挑模型，再給予多次深呼吸重試的機會)
    for endpoint in candidate_endpoints:
        url = f"https://generativelanguage.googleapis.com/{endpoint}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        print(f"📡 鎖定現役端點: {endpoint}，準備叩關...")
        
        # 內層迴圈：每個模型最多忍受 4 次 503 伺服器忙碌
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    raw_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                    
                    # 暴力清理 Markdown
                    if raw_text.startswith("```json"): raw_text = raw_text[7:]
                    elif raw_text.startswith("```"): raw_text = raw_text[3:]
                    if raw_text.endswith("```"): raw_text = raw_text[:-3]
                    raw_text = raw_text.strip()
                    
                    # 內容防彈驗證
                    try:
                        quotes_data = json.loads(raw_text)
                        if isinstance(quotes_data, list) and len(quotes_data) == 4 and "theme" in quotes_data[0]:
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
                    continue # 繼續當前模型的下一次嘗試
                elif e.code in [404, 403]:
                    print(f"⚠️ {endpoint} 權限不足或不存在 ({e.code})，放棄此端點，切換下一組。")
                    break # 跳出內層重試迴圈，直接換下一個模型
                else:
                    print(f"⚠️ {endpoint} 未知錯誤 ({e.code})，跳過此端點。")
                    break
    
    raise ValueError("❌ 慘烈失敗：現役 Gemini 模型皆因伺服器嚴重過載或權限問題，無法順利生成。")

def main():
    print("🚀 Taiji Genesis Engine: 啟動深邃文學與自癒耐心版...")
    
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
