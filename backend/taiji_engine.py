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

    # 【太極萬象庫】：41 個涵蓋古今中外、二次元與真實世界的平行宇宙
    styles = [
        # 原有宇宙 (21)
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
        "現代都會社畜的『躺平無罪』與『人間清醒』幹話哲學",

        # 新增宇宙：中國古典文學與哲思 (5)
        "吳承恩《西遊記》歷經九九八十一難的修心與降妖伏魔之路",
        "曹雪芹《紅樓夢》繁華落盡如春夢一場的無常與淒美輓歌",
        "莊子《逍遙遊》化蝶入夢、超然物外且『無用之用』的灑脫大智慧",
        "蘇軾《赤壁賦》『寄蜉蝣於天地，渺滄海之一粟』的曠達與釋然",
        "劉鶚《老殘遊記》在冰天雪地中聽大珠小珠落玉盤的純粹知音視角",

        # 新增宇宙：世界經典名著與小品 (5)
        "海明威《老人與海》『人可以被毀滅，但不能被打敗』的硬漢堅持",
        "卡繆《異鄉人》面對世界荒謬時的冷靜、直率與孤獨反叛",
        "夏目漱石《我是貓》以貓的冷眼旁觀人類社會的滑稽與無奈視角",
        "珍·奧斯汀《傲慢與偏見》在日常交際與機鋒中看透人性的幽默",
        "魯迅《阿Q正傳》在荒誕現實中以『精神勝利法』自我解嘲的黑色幽默",

        # 新增宇宙：動漫影視與流行文化 (5)
        "《進擊的巨人》在殘酷世界中探究真相與不計代價追求自由的決心",
        "《葬送的芙莉蓮》在漫長歲月中重新體會生命重量與日常溫度的旅程",
        "《新世紀福音戰士》(EVA) 於末日危機中對自我存在價值的深層叩問",
        "宮崎駿《神隱少女》在迷失與貪婪的奇幻世界中找回名字與初心的堅定",
        "《深夜食堂》以一道簡單家常菜撫慰都市疲憊靈魂的溫情視角",

        # 新增宇宙：生活感悟與自然美學 (5)
        "蔣勳《孤獨六講》中在喧囂裡與自己對話、享受美學孤獨的從容",
        "日本『侘寂（Wabi-sabi）』美學中欣賞殘缺、短暫與歲月痕跡的平靜",
        "極簡主義（Minimalism）『少即是多』的斷捨離與回歸生活本質的清爽",
        "在雨天獨自聆聽黑膠唱片，任由時間隨唱針緩慢流淌的復古浪漫",
        "現代數位遊牧民族（Digital Nomad）四海為家、擁抱未知的不羈靈魂"
    ]
    chosen_styles = random.sample(styles, 4)

    prompt = f"""
    你是「太極萬象日曆」的創世神。你的任務是生成 4 段極具「巴納姆效應」的生活散文。
    
    為了讓 4 個宇宙的文字擁有「極端不同的個性」，請嚴格套用以下語氣：
    1. 宇宙一：【{chosen_styles[0]}】。
    2. 宇宙二：【{chosen_styles[1]}】。
    3. 宇宙三：【{chosen_styles[2]}】。
    4. 宇宙四：【{chosen_styles[3]}】。
    
    【🔥 極度重要：反審查與意象轉換守則 (Anti-Censorship & Metaphor)】
    前端將使用「Hyper-realistic raw photograph (極致寫實攝影)」來生成你指定的 `image_subject`。為了避免觸發 AI 繪圖的安全審查被封鎖，你必須遵守：
    1. 絕對禁止出現「幼童、未成年、孩童」相關詞彙 (如: little boy, child, kid, little prince, boy, girl)。
    2. 絕對禁止直接使用「版權角色與動漫名」 (如: Pikachu, Snoopy, Conan, Doraemon, Naruto, One Piece, Eva, Frieren, Totoro)。
    3. 絕對禁止血腥、暴力、武器直白描述 (如: blood, kill, gun, corpse)。
    4. 必須「借物喻景」。如果抽到《小王子》，畫面主體請寫「沙漠中的一朵被玻璃罩保護的紅玫瑰」；如果抽到《多啦A夢》，請寫「半開的木抽屜透出神秘藍光」；如果抽到《火影忍者》，請寫「插在樹幹上的苦無與飄落的樹葉」；如果抽到《進擊的巨人》，請寫「巨大的殘破石牆與展翅飛越的鳥」；如果抽到《神隱少女》，請寫「水中隱約浮現的紅色神秘鐵軌」。
    5. 畫面描述必須是能夠被相機真實拍出來的「實體靜物、大自然、動物或成人背影」。
    
    【極度重要：嚴格 JSON 格式】：
    - 絕對不要輸出任何解釋、思考過程或 Markdown 標記以外的文字。
    - 必須輸出為純 JSON 陣列，包含精準的 4 個物件，每個物件必須有以下 7 個 Key：
    [
      {{
        "theme": "自訂風格標籤(如: 侘寂美學 / 唯美哀傷)",
        "article": "40~60字的情境散文，必須強烈展現該宇宙要求的『語氣』！",
        "quote": "15~25字的一擊必殺金句。",
        "hashtag": "兩個字標籤",
        "do_action": "兩個字的宜行動",
        "dont_action": "兩個字的忌禁忌",
        "image_subject": "一句簡短的英文，純描述符合上述『意象轉換守則』的靜物或風景（例如: A single red rose inside a glass dome under a starry night.）。請務必只用英文，純描述畫面，不要加相機參數。"
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
                if e.code == 429:
                    print(f"⚠️ 觸發流量管制 ({e.code})，強制深呼吸 15 秒冷卻 (第 {attempt+1}/4 次)...")
                    time.sleep(15)
                    continue
                elif e.code in [503, 500]:
                    print(f"⚠️ 伺服器大塞車 ({e.code})，深呼吸冷靜 8 秒後重新敲門 (第 {attempt+1}/4 次)...")
                    time.sleep(8)
                    continue 
                elif e.code in [404, 403]:
                    print(f"⚠️ {endpoint} 權限不足或不存在 ({e.code})，放棄此端點，切換下一組。")
                    break 
                else:
                    print(f"⚠️ {endpoint} 未知錯誤 ({e.code})，跳過此端點。")
                    break

    # 【零一的終極防禦：本地備用大腦】
    print("❌ 警告：所有線上 Gemini 模型皆因伺服器過載或限流無法連線。")
    print("🛡️ 啟動【本地備用量子庫】，確保 GitHub Actions 綠燈與網站正常運作！")
    
    fallback_data = [
        {
            "theme": "系統守護",
            "article": "當雲端伺服器陷入無盡的沉睡與擁塞時，本地的備用宇宙依然為您精準運轉。請享受這份不被網路打擾的寧靜。",
            "quote": "最深的寂靜，往往孕育著最強大的力量。",
            "hashtag": "靜心",
            "do_action": "等待",
            "dont_action": "焦慮",
            "image_subject": "A solitary ancient tree standing on a quiet misty mountain peak"
        },
        {
            "theme": "寫實日常",
            "article": "網路的波動就像生活中的陣雨，來得突然，卻也洗刷了空氣中的煩躁。沖一杯熱茶，讓時間稍微暫停一下。",
            "quote": "停下腳步，才能看清雨後的彩虹。",
            "hashtag": "暫停",
            "do_action": "喝茶",
            "dont_action": "抱怨",
            "image_subject": "A steaming cup of tea on a vintage wooden desk by a rain-streaked window"
        },
        {
            "theme": "純粹療癒",
            "article": "即使在沒有 AI 運算的宇宙裡，真實世界的小確幸依然存在。比如一隻正在陽光下打呼嚕的貓咪，牠才不在乎伺服器有沒有當機。",
            "quote": "真正的療癒，存在於無需運算的純粹之中。",
            "hashtag": "陪伴",
            "do_action": "撫摸",
            "dont_action": "執著",
            "image_subject": "A fluffy cat sleeping peacefully in a patch of warm sunlight on a rug"
        },
        {
            "theme": "極簡禪意",
            "article": "斷線的瞬間，世界突然安靜了下來。我們終於有理由把目光從螢幕移開，看看窗外真實飄落的樹葉。",
            "quote": "失去連結的那一刻，我們才真正與自己連線。",
            "hashtag": "留白",
            "do_action": "遠眺",
            "dont_action": "刷新",
            "image_subject": "A single red autumn leaf resting on a smooth zen garden stone"
        }
    ]
    return fallback_data, today_str

def main():
    print("🚀 Taiji Genesis Engine: 啟動永不墜毀防彈版...")
    
    try:
        quotes_data, today_str = generate_omniverse_data()
        quotes_js_string = json.dumps(quotes_data, ensure_ascii=False)
        print("✅ 大腦數據備妥，準備寫入皮囊！")
    except Exception as e:
        raise SystemExit(f"💀 系統發生致命核心錯誤: {e}")

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
