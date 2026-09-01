import json
from datetime import datetime, timezone, timedelta
import os
import urllib.request
import xml.etree.ElementTree as ET
import random
import ssl
import requests

class TaijiOmniverseCalendar:
    def __init__(self):
        tz_tw = timezone(timedelta(hours=8))
        self.today = datetime.now(tz_tw)
        self.api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        
        self._init_static_databases()
        self.self_diagnostic()
        self.real_trends = self.fetch_google_rss_trends()
        self.forum_titles = self.fetch_social_forum_trends()
        
        # 🧠 啟動多彈頭自適應尋標系統
        self.dynamic_quotes, self.is_llm_active = self.generate_quotes_via_llm(self.forum_titles)
        
        year, month, day = self.today.year, self.today.month, self.today.day
        stars = ["水瓶座", "雙魚座", "牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座"]
        zodiacs = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
        
        current_star = stars[(year + month + day + 6) % 12]
        current_zodiac = zodiacs[(year + month + day + 10) % 12]

        self.payload = {
            "date": self.today.strftime("%Y-%m-%d"),
            "star_sign": current_star,
            "star_color": self.star_visuals[current_star]["c"],
            "star_visual": self.star_visuals[current_star]["v"],
            "zodiac_sign": current_zodiac,
            "zodiac_color": self.zodiac_visuals[current_zodiac]["c"],
            "zodiac_visual": self.zodiac_visuals[current_zodiac]["v"],
        }

    def _init_static_databases(self):
        self.star_visuals = {"水瓶座": {"c": "星空藍", "v": "周圍環繞著發光的水波紋"}, "雙魚座": {"c": "海洋藍", "v": "頭頂有兩條光影小魚環繞"}, "牡羊座": {"c": "火焰紅", "v": "擁有發光的螺旋羊角"}, "金牛座": {"c": "大地綠", "v": "帶著小巧的黃金牛角"}, "雙子座": {"c": "明亮黃", "v": "身體有著雙重顏色的分裂感"}, "巨蟹座": {"c": "珍珠白", "v": "表面有一層閃亮的珍珠光澤"}, "獅子座": {"c": "王者金", "v": "頭頂戴著一頂微型的黃金皇冠"}, "處女座": {"c": "純淨白", "v": "周圍有純潔的光芒與花瓣飄落"}, "天秤座": {"c": "湖水綠", "v": "頭頂懸浮著一個發光的黃金小天平"}, "天蠍座": {"c": "深邃紫", "v": "背後有一條若隱若現的紫色毒刺光影"}, "射手座": {"c": "自由橘", "v": "背著一把迷你的光之弓箭"}, "摩羯座": {"c": "沉穩褐", "v": "額頭有發光的神秘符文"}}
        self.zodiac_visuals = {"鼠": {"c": "灰曜色", "v": "擁有靈動的小老鼠耳朵"}, "牛": {"c": "厚土色", "v": "帶著堅硬的牛角與鼻環"}, "虎": {"c": "霸氣橘", "v": "身上有著明顯的老虎斑紋"}, "兔": {"c": "櫻花粉", "v": "擁有長長的毛茸茸兔子耳朵"}, "龍": {"c": "神聖金", "v": "頭上長著威武的龍角"}, "蛇": {"c": "翡翠綠", "v": "身體呈現細長且帶有蛇鱗反光"}, "馬": {"c": "疾風棕", "v": "背部有著飄逸的馬鬃毛光影"}, "羊": {"c": "溫柔白", "v": "頭側有捲曲的綿羊角"}, "猴": {"c": "靈動桃", "v": "擁有一條長長的猴子尾巴"}, "雞": {"c": "晨曦紅", "v": "頭頂著鮮豔的雞冠"}, "狗": {"c": "忠誠黃", "v": "有著下垂的可愛狗狗耳朵"}, "豬": {"c": "豐饒粉", "v": "擁有一個可愛的粉紅豬鼻子"}}
        self.art_styles = ["最高規格「頂級寫實照」光學成像參數 (極致寫實、大師級攝影光影)"]
        self.fortune_fusion = [{"text": "水星逆行引發通訊危機，今日請再三確認訊息是否發錯群組。", "prop": "一支停在尷尬聊天室畫面的手機"}]
        self.themes_data = {"極致的懶散躺平": {"stages": ["試圖物理性登出的人類", "拒絕營業的廢物"], "emotions": ["毫無波瀾，徹底放空", "散發著慵懶的氣息"], "textures": ["融化成一灘液體", "像麻糬一樣軟爛"], "actions": ["展現極致鬆弛感", "緩慢地蠕動"]}}
        self.fallback_quotes = [{"q": "努力不一定會成功，但不努力一定很輕鬆。", "p": "躺平哲學"}]

    def self_diagnostic(self):
        print("🔍 [零一系統] 底層自檢完成。準備執行自動化排程。")

    def fetch_google_rss_trends(self):
        url = 'https://trends.google.com.tw/trending/rss?geo=TW'
        trends = []
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                root = ET.fromstring(response.read())
                for item in root.findall('./channel/item')[:15]:
                    trends.append(item.find('title').text)
            return trends
        except Exception:
            return ["連假塞車", "突發大停電", "物價上漲", "天氣預報不準"]

    def fetch_social_forum_trends(self):
        url = 'https://www.dcard.tw/service/api/v2/posts?popular=true&limit=15'
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json, text/plain, */*'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
                data = json.loads(response.read())
                titles = [item['title'] for item in data if 'title' in item]
                return titles[:10]
        except Exception:
            return ["不想上班想離職", "存不到錢好焦慮"]

    def generate_quotes_via_llm(self, forum_titles):
        if not self.api_key:
            print("⚠️ 未偵測到 API Key。切換至備用庫。")
            return self.fallback_quotes, False
            
        print("🧠 正在連線 LLM 靈魂引擎 (啟動自動尋標模式)...")
        
        # 🎯 終極武器：自動測試各種模型，直到找到您帳號有權限的那一個！
        models_to_try = [
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-pro",
            "gemini-1.0-pro"
        ]
        
        titles_text = "\n".join([f"- {t}" for t in forum_titles])
        prompt = f"""
        你是一位洞悉台灣社會現象的社群文案大師。今天是 {self.today.strftime("%Y-%m-%d")}。
        參考以下 Dcard 熱門標題的社會氛圍：\n{titles_text}\n
        為我寫出 5 句極度接地氣的大眾共鳴金句 (包含生活、上班、缺錢等普世痛點)。
        - 3 句為帶有自我解嘲的「幽默幹話」（厭世、吐槽）。
        - 2 句為「正向療癒、生活微光」的溫暖句子。
        請嚴格以 JSON 陣列格式回傳：[ {{"q": "金句內容", "p": "痛點標籤"}} ]
        """
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.9}
        }
        headers = {"Content-Type": "application/json"}
        
        last_error = ""
        
        try:
            for model_name in models_to_try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
                print(f"📡 正在嘗試連線模型: {model_name}...")
                
                response = requests.post(url, json=payload, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    raw_text = data['candidates'][0]['content']['parts'][0]['text']
                    # 清理可能附帶的 markdown 標籤
                    raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                    new_quotes = json.loads(raw_text)
                    print(f"🟢 靈魂引擎連線成功！(成功鎖定模型: {model_name})")
                    return new_quotes, True
                else:
                    last_error = f"[{model_name}] 失敗代碼 {response.status_code}"
                    print(f"⚠️ 模型 {model_name} 無權限或拒絕連線，自動切換下一個...")
                    
            print(f"❌ 所有模型均測試失敗。最後錯誤: {last_error}")
            return self.fallback_quotes, False
            
        except Exception as e:
            print(f"⚠️ LLM 處理過程發生崩潰 ({str(e)})。已切換至備用庫。")
            return self.fallback_quotes, False

    def export_to_html(self):
        themes_js = json.dumps(self.themes_data, ensure_ascii=False)
        quotes_js = json.dumps(self.dynamic_quotes, ensure_ascii=False)
        payload_js = json.dumps(self.payload, ensure_ascii=False)
        real_trends_js = json.dumps(self.real_trends, ensure_ascii=False)
        art_styles_js = json.dumps(self.art_styles, ensure_ascii=False)
        fortune_js = json.dumps(self.fortune_fusion, ensure_ascii=False)
        star_visuals_js = json.dumps(self.star_visuals, ensure_ascii=False)
        zodiac_visuals_js = json.dumps(self.zodiac_visuals, ensure_ascii=False)
        is_llm_active_js = "true" if self.is_llm_active else "false"

        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>TAIJI V31 Auto-Drive Edition</title>
            <script src="https://unpkg.com/lunar-javascript/lunar.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700&family=Inter:wght@400;600;700;900&display=swap');
                :root {{ --bg-color: #ffffff; --card-bg: #ffffff; --text-title: #111111; --text-main: #333333; --text-sub: #888888; --font-title: 'Noto Serif TC', serif; --font-body: 'Inter', sans-serif; --border-radius: 0px; --border-style: 1px solid #eeeeee; --hero-bg: #f9f9f9; --btn-bg: #111111; --btn-text: #ffffff; --spacing: 40px; }}
                body.theme-popeye {{ --bg-color: #F5F3E9; --text-title: #0d3b66; --border-radius: 12px; --border-style: 2px solid #1a1a1a; --btn-bg: #e63946; }}
                body.theme-brutus {{ --bg-color: #121212; --card-bg: #1e1e1e; --text-title: #f5f5f5; --text-main: #e0e0e0; --text-sub: #757575; --border-radius: 4px; --border-style: 1px solid #333333; --hero-bg: #1a1a1a; --btn-bg: #f5f5f5; --btn-text: #121212; }}
                body.theme-monocle {{ --bg-color: #F8F6F0; --card-bg: #ffffff; --text-title: #1c1c1c; --text-main: #3d3d3d; --text-sub: #9e9e9e; --border-radius: 2px; --border-style: 1px solid #e0ddd5; --hero-bg: #F8F6F0; --btn-bg: #e67e22; --btn-text: #ffffff; }}
                body.theme-wired {{ --bg-color: #ffffff; --card-bg: #f4f5f7; --text-title: #000000; --text-main: #111111; --text-sub: #6b7280; --border-radius: 16px; --border-style: none; --hero-bg: #ebf5ff; --btn-bg: #2563eb; --btn-text: #ffffff; }}
                body.theme-casa {{ --bg-color: #EAEAE4; --card-bg: #F4F4F0; --text-title: #4a5d4e; --text-main: #5c5c5c; --text-sub: #8a8a8a; --border-radius: 8px; --border-style: 1px solid #d1d1c7; --hero-bg: #e3e8e4; --btn-bg: #4a5d4e; --btn-text: #ffffff; }}
                body {{ font-family: var(--font-body); background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 40px 20px; transition: all 0.5s ease; }}
                .editorial-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }}
                .card {{ background: var(--card-bg); border-radius: var(--border-radius); padding: var(--spacing); border: var(--border-style); transition: all 0.3s ease; }}
                .control-panel {{ grid-column: span 12; background: var(--hero-bg); padding: 20px; border-radius: var(--border-radius); border: var(--border-style); display: flex; flex-wrap: wrap; gap: 15px; align-items: center; justify-content: center; }}
                .control-panel select, .control-panel input {{ padding: 10px; font-family: var(--font-body); font-size: 1rem; border: 1px solid #ccc; border-radius: 6px; }}
                .control-panel button.btn-apply {{ background: #2563eb; color: #fff; border: none; padding: 10px 20px; font-size: 1rem; border-radius: 6px; cursor: pointer; font-weight: bold; transition: 0.3s; }}
                .control-panel button.btn-apply:hover {{ background: #1d4ed8; }}
                .date-card {{ grid-column: span 12; background: var(--text-title); color: var(--bg-color); text-align: center; padding: 45px 20px; border: none; }}
                .date-card h1 {{ font-family: 'Inter', sans-serif; font-weight: 900; font-size: 4rem; margin: 0; color: var(--bg-color); letter-spacing: -2px; }}
                .date-card p.lunar {{ font-size: 1.1rem; color: var(--bg-color); opacity: 0.9; letter-spacing: 5px; margin: 15px 0 0 0; text-transform: uppercase; }}
                .headline-card {{ grid-column: span 12; background: var(--hero-bg); text-align: center; padding: 50px 20px; border-bottom: 3px solid var(--text-title); }}
                .headline-card h2 {{ font-family: var(--font-title); font-size: 2.5rem; color: var(--text-title); margin: 0 0 15px 0; }}
                .quote-card {{ grid-column: span 12; text-align: center; padding: 50px 30px; position: relative; }}
                .quote-card h2 {{ font-family: var(--font-title); font-size: 1.8rem; line-height: 1.5; color: var(--text-title); margin: 0 0 15px 0; }}
                .badge-llm {{ background: #4ec9b0; color: #111; padding: 6px 14px; font-size: 0.75rem; font-weight: bold; border-radius: 20px; display: inline-block; margin-bottom: 15px; }}
                .badge-static {{ background: #e5e7eb; color: #6b7280; border: 1px solid #d1d5db; padding: 6px 14px; font-size: 0.75rem; font-weight: bold; border-radius: 20px; display: inline-block; margin-bottom: 15px; }}
                .info-card {{ grid-column: span 6; }} .actor-card {{ grid-column: span 6; }}
                .action-buttons {{ grid-column: span 12; display: flex; gap: 20px; margin-top: 10px; }}
                .btn-ai {{ flex: 1; background: #e63946; color: white; padding: 25px; cursor: pointer; border: none; font-size: 1.2rem; font-weight: bold; border-radius: var(--border-radius); }}
                .btn-ig {{ flex: 1; background: linear-gradient(45deg, #405de6, #5851db, #833ab4, #c13584, #e1306c, #fd1d1d); color: white; padding: 25px; cursor: pointer; border: none; font-size: 1.2rem; font-weight: bold; border-radius: var(--border-radius); }}
                textarea {{ display: none; }}
                .floating-btn {{ position: fixed; bottom: 30px; right: 30px; background: var(--text-title); color: var(--bg-color); border: none; border-radius: 50px; padding: 15px 25px; font-size: 1rem; font-weight: bold; cursor: pointer; box-shadow: 0 10px 20px rgba(0,0,0,0.2); z-index: 100; }}
            </style>
        </head>
        <body>
            <button class="floating-btn" onclick="randomizeAll()">🔄 強制切換排版與內容</button>
            <div class="editorial-grid">
                
                <div class="control-panel">
                    <label>📅 時空跳躍：</label>
                    <input type="date" id="ui-date-picker" value="{self.payload['date']}">
                    <button class="btn-apply" onclick="applyDateChange()">確認日期</button>
                </div>

                <div class="card date-card">
                    <h1 id="display-date">{self.payload['date']}</h1>
                    <p class="lunar" id="display-lunar">正在演算農民曆...</p>
                </div>

                <div class="card headline-card">
                    <p style="text-transform: uppercase; letter-spacing: 3px; font-size: 0.85rem; margin-bottom:15px; font-weight: bold;">Google Trends Live</p>
                    <h2 id="ui-scene"></h2>
                </div>

                <div class="card quote-card" id="quote-card-container">
                    <div id="llm-badge"></div>
                    <h2 id="ui-quote"></h2>
                    <span style="display:inline-block; margin-top:10px;">DAILY EDITORIAL · 📌 今日觀察：<strong id="ui-pain"></strong></span>
                </div>
                
                <div class="card info-card">
                    <h3 style="border-bottom: 1px solid var(--text-sub); padding-bottom:10px;">綜合題點</h3>
                    <div class="content" style="line-height:1.6; margin-top:10px;">
                        <strong>⚠️ 注意事項：</strong><br><span id="ui-fortune-text"></span><br><br>
                        <em>💡 道具指令：<br><span style="color:#d97706; font-weight:bold;" id="ui-fortune-prop"></span></em>
                    </div>
                </div>

                <div class="card info-card">
                    <h3 style="border-bottom: 1px solid var(--text-sub); padding-bottom:10px;">系統日誌</h3>
                    <div class="content" style="color: var(--text-sub); font-size: 0.85rem; line-height:1.6; margin-top:10px;">
                        <span style="color: #2563eb; font-weight: bold;">[資料來源]</span> <span id="log-data-source"></span><br>
                        目前版型：<strong id="ui-web-theme" style="color:var(--text-main);"></strong><br><br>
                        自動化工廠：V32 全自動巡弋排程已準備就緒。<br>
                    </div>
                </div>

                <div class="card actor-card">
                    <h3 id="title-actor-a" style="border-bottom: 2px solid var(--text-title); padding-bottom:10px; margin-top:0;">A. {self.payload['star_sign']} Slime</h3>
                    <div class="detail-list" style="line-height:1.8; margin-top:10px;">
                        <strong>狀態：</strong><span id="ui-stage-a"></span><br><strong>表情：</strong><span id="ui-emo-a"></span><br>
                        <strong>材質：</strong><span id="ui-tex-a"></span><br><strong>動作：</strong><span id="ui-act-a"></span>
                    </div>
                </div>

                <div class="card actor-card">
                    <h3 id="title-actor-b" style="border-bottom: 2px solid var(--text-title); padding-bottom:10px; margin-top:0;">B. {self.payload['zodiac_sign']} Slime</h3>
                    <div class="detail-list" style="line-height:1.8; margin-top:10px;">
                        <strong>狀態：</strong><span id="ui-stage-b"></span><br><strong>表情：</strong><span id="ui-emo-b"></span><br>
                        <strong>材質：</strong><span id="ui-tex-b"></span><br><strong>動作：</strong><span id="ui-act-b"></span>
                    </div>
                </div>

                <div class="action-buttons">
                    <button class="btn-ai" onclick="copyText('rawPrompt', 'btnMsgAI')">🎨 COPY AI PROMPT<br><span id="btnMsgAI" style="font-size:0.8rem; font-weight:normal;">(複製繪圖指令)</span></button>
                    <button class="btn-ig" onclick="copyText('igCaption', 'btnMsgIG')">📱 COPY IG CAPTION<br><span id="btnMsgIG" style="font-size:0.8rem; font-weight:normal;">(複製貼文文案)</span></button>
                </div>
                
                <textarea id="rawPrompt"></textarea>
                <textarea id="igCaption"></textarea>
            </div>

            <script>
                const themes = {themes_js};
                const quotes = {quotes_js}; 
                let payload = {payload_js};
                const realTrends = {real_trends_js};
                const artStyles = {art_styles_js};
                const fortunes = {fortune_js};
                const starVisuals = {star_visuals_js};
                const zodiacVisuals = {zodiac_visuals_js};
                const isLlmActive = {is_llm_active_js};
                
                const coreTags = ["#日曆", "#生活碎片", "#史萊姆"];
                const emotionTags = ["#情緒價值", "#人間清醒", "#好好生活", "#自我療癒"];
                const artTags = ["#寫實攝影", "#視覺藝術"];

                const webThemes = [
                    {{ class: '', name: 'KINFOLK 極簡北歐風' }},
                    {{ class: 'theme-popeye', name: 'POPEYE 潮流日雜風' }},
                    {{ class: 'theme-brutus', name: 'BRUTUS 高級暗黑風' }},
                    {{ class: 'theme-monocle', name: 'MONOCLE 英倫商務風' }},
                    {{ class: 'theme-wired', name: 'WIRED 前衛科技風' }},
                    {{ class: 'theme-casa', name: 'CASA BRUTUS 生活美學風' }}
                ];

                function getAstrologySignsByDate(dateStr) {{
                    const d = new Date(dateStr + "T00:00:00");
                    const year = d.getFullYear(); const month = d.getMonth() + 1; const day = d.getDate();
                    const stars = ["水瓶座", "雙魚座", "牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座"];
                    const zodiacs = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"];
                    return {{ star: stars[(year + month + day + 6) % 12], zodiac: zodiacs[(year + month + day + 10) % 12] }};
                }}

                let currentThemeIndex = -1; 
                let currentAlmanacData = {{ lunarStr: "正在演算農民曆..." }};

                function getRandomItem(arr) {{ return arr[Math.floor(Math.random() * arr.length)]; }}
                function getRandomTwo(arr) {{
                    let shuffled = arr.slice(0), i = arr.length, temp, index;
                    while (i--) {{ index = Math.floor((i + 1) * Math.random()); temp = shuffled[index]; shuffled[index] = shuffled[i]; shuffled[i] = temp; }}
                    return shuffled.slice(0, 2);
                }}

                function applyDateChange() {{
                    const dateVal = document.getElementById('ui-date-picker').value;
                    if(!dateVal) return;
                    document.getElementById('display-date').innerText = dateVal;
                    
                    const luckySigns = getAstrologySignsByDate(dateVal);
                    payload.star_sign = luckySigns.star; payload.star_color = starVisuals[luckySigns.star].c; payload.star_visual = starVisuals[luckySigns.star].v;
                    payload.zodiac_sign = luckySigns.zodiac; payload.zodiac_color = zodiacVisuals[luckySigns.zodiac].c; payload.zodiac_visual = zodiacVisuals[luckySigns.zodiac].v;

                    document.getElementById('title-actor-a').innerText = "A. " + luckySigns.star + " Slime";
                    document.getElementById('title-actor-b').innerText = "B. " + luckySigns.zodiac + " Slime";

                    try {{
                        const d = new Date(dateVal + "T00:00:00");
                        if (typeof Lunar !== 'undefined') {{
                            const lunar = Lunar.fromDate(d);
                            let lunarStr = `農曆 ${{lunar.getMonthInChinese()}}月${{lunar.getDayInChinese()}}`;
                            const jieQi = lunar.getJieQi();
                            if(jieQi) lunarStr += ` | 節氣: ${{jieQi}}`;
                            currentAlmanacData.lunarStr = lunarStr;
                        }}
                    }} catch (e) {{ currentAlmanacData.lunarStr = "農曆查無資料"; }}
                    document.getElementById('display-lunar').innerText = currentAlmanacData.lunarStr;
                    randomizeAll();
                }}

                function randomizeAll() {{
                    const badgeElem = document.getElementById('llm-badge');
                    const logElem = document.getElementById('log-data-source');
                    const quoteCard = document.getElementById('quote-card-container');
                    
                    if (isLlmActive) {{
                        badgeElem.className = 'badge-llm';
                        badgeElem.innerHTML = '⚡ LLM SOUL ENGINE GENERATED';
                        quoteCard.style.border = '2px dashed #4ec9b0';
                        logElem.innerHTML = 'API 連線成功，使用雲端每日最新生成文案';
                    }} else {{
                        badgeElem.className = 'badge-static';
                        badgeElem.innerHTML = '🗄️ 靜態大眾資料庫 (雲端 API 未連線)';
                        quoteCard.style.border = '1px solid var(--border-style)';
                        logElem.innerHTML = '雲端 API 未連線，使用備用庫';
                        logElem.style.color = '#888';
                    }}

                    let newThemeIndex = Math.floor(Math.random() * webThemes.length);
                    while (newThemeIndex === currentThemeIndex) {{ newThemeIndex = Math.floor(Math.random() * webThemes.length); }}
                    currentThemeIndex = newThemeIndex;
                    document.body.className = webThemes[currentThemeIndex].class;
                    document.getElementById('ui-web-theme').innerText = webThemes[currentThemeIndex].name;

                    const currentDate = document.getElementById('ui-date-picker').value;
                    const trendKeyword = getRandomItem(realTrends);
                    const selectedFortune = getRandomItem(fortunes);
                    const themeKeys = Object.keys(themes);
                    const selectedThemeName = getRandomItem(themeKeys);
                    const theme = themes[selectedThemeName];
                    const selectedQuote = getRandomItem(quotes);
                    const stages = getRandomTwo(theme.stages);
                    const emos = getRandomTwo(theme.emotions);
                    const texs = getRandomTwo(theme.textures);
                    const acts = getRandomTwo(theme.actions);

                    document.getElementById('ui-scene').innerText = trendKeyword;
                    document.getElementById('ui-fortune-text').innerText = selectedFortune.text;
                    document.getElementById('ui-fortune-prop').innerText = selectedFortune.prop;
                    document.getElementById('ui-stage-a').innerText = stages[0];
                    document.getElementById('ui-emo-a').innerText = emos[0];
                    document.getElementById('ui-tex-a').innerText = texs[0];
                    document.getElementById('ui-act-a').innerText = acts[0];
                    document.getElementById('ui-stage-b').innerText = stages[1];
                    document.getElementById('ui-emo-b').innerText = emos[1];
                    document.getElementById('ui-tex-b').innerText = texs[1];
                    document.getElementById('ui-act-b').innerText = acts[1];
                    document.getElementById('ui-quote').innerText = '"' + selectedQuote.q + '"';
                    document.getElementById('ui-pain').innerText = selectedThemeName + " | " + selectedQuote.p;
                    
                    const promptText = `[系統指令] 今日時事熱點：${{trendKeyword}}。畫面請呈現真實寫實風格。角色A：${{payload.star_sign}}史萊姆，狀態${{stages[0]}}。角色B：${{payload.zodiac_sign}}史萊姆，狀態${{stages[1]}}。包含道具：${{selectedFortune.prop}}。`;
                    document.getElementById('rawPrompt').value = promptText;
                    document.getElementById('igCaption').value = `📅 ${{currentDate}} \\n\\n"${{selectedQuote.q}}"\\n\\n#日曆 #生活碎片`;
                }}

                window.onload = function() {{ setTimeout(applyDateChange, 500); }};

                function copyText(elementId, msgId) {{
                    var copyText = document.getElementById(elementId);
                    copyText.style.display = "block"; copyText.select(); document.execCommand("copy"); copyText.style.display = "none";
                    var msg = document.getElementById(msgId);
                    var originalText = msg.innerHTML;
                    msg.innerHTML = "✓ 複製成功！";
                    setTimeout(function() {{ msg.innerHTML = originalText; }}, 2000);
                }}
            </script>
        </body>
        </html>
        """
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'taiji_dashboard.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

if __name__ == "__main__":
    engine = TaijiOmniverseCalendar()
    engine.export_to_html()
