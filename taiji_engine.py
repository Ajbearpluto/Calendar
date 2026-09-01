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
        self.real_trends = self.fetch_google_rss_trends()
        self.forum_titles = self.fetch_social_forum_trends()
        
        # 🧠 啟動終極顯影引擎
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
        self.art_styles = ["最高規格「頂級寫實照」光學成像參數"]
        self.fortune_fusion = [{"text": "系統正在進行深度除錯", "prop": "一把放大鏡"}]
        self.themes_data = {"極致的懶散躺平": {"stages": ["試圖物理性登出的人類", "拒絕營業的廢物"], "emotions": ["毫無波瀾", "放空"], "textures": ["融化", "軟爛"], "actions": ["躺平", "蠕動"]}}

    def fetch_google_rss_trends(self):
        return ["系統診斷中"]

    def fetch_social_forum_trends(self):
        return ["診斷中"]

    def generate_quotes_via_llm(self, forum_titles):
        if not self.api_key:
            return [{"q": "致命錯誤：在 GitHub 找不到金鑰，請確認 Secret 命名是否正確。", "p": "金鑰遺失"}], False
            
        print("🧠 正在連線 LLM 靈魂引擎 (啟動終極顯影模式)...")
        # 直接挑戰最新最強的 Gemini 2.0 模型
        models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash"]
        
        prompt = f"寫一句話：'連線成功！'。嚴格以 JSON 陣列回傳：[ {{\"q\": \"金句\", \"p\": \"標籤\"}} ]"
        payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.9}}
        headers = {"Content-Type": "application/json"}
        
        last_error_code = ""
        last_error_text = ""
        
        try:
            for model_name in models_to_try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
                response = requests.post(url, json=payload, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    raw_text = data['candidates'][0]['content']['parts'][0]['text']
                    raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                    return json.loads(raw_text), True
                else:
                    last_error_code = response.status_code
                    last_error_text = response.text
                    
            # 🚨 破釜沉舟：如果全部失敗，直接把 Google 的錯誤訊息變為「金句」印在網頁上！
            clean_error = last_error_text.replace('"', "'").replace('\n', ' ')
            diagnostic_msg = f"Google 拒絕連線 (代碼 {last_error_code})。真實原因：{clean_error}"
            diagnostic_msg = diagnostic_msg[:250] + ("..." if len(diagnostic_msg) > 250 else "")
            
            return [{"q": diagnostic_msg, "p": "⚠️ 終極錯誤診斷"}], False
            
        except Exception as e:
            return [{"q": f"系統發生崩潰：{str(e)}", "p": "系統異常"}], False

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
            <title>TAIJI V33 Diagnostic Edition</title>
            <script src="https://unpkg.com/lunar-javascript/lunar.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700&family=Inter:wght@400;600;700;900&display=swap');
                :root {{ --bg-color: #ffffff; --card-bg: #ffffff; --text-title: #111111; --text-main: #333333; --text-sub: #888888; --font-title: 'Noto Serif TC', serif; --font-body: 'Inter', sans-serif; --border-radius: 0px; --border-style: 1px solid #eeeeee; --hero-bg: #f9f9f9; --btn-bg: #111111; --btn-text: #ffffff; --spacing: 40px; }}
                body.theme-brutus {{ --bg-color: #121212; --card-bg: #1e1e1e; --text-title: #f5f5f5; --text-main: #e0e0e0; --text-sub: #757575; --border-radius: 4px; --border-style: 1px solid #333333; --hero-bg: #1a1a1a; --btn-bg: #f5f5f5; --btn-text: #121212; }}
                body {{ font-family: var(--font-body); background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 40px 20px; transition: all 0.5s ease; }}
                .editorial-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }}
                .card {{ background: var(--card-bg); border-radius: var(--border-radius); padding: var(--spacing); border: var(--border-style); transition: all 0.3s ease; }}
                .date-card {{ grid-column: span 12; background: var(--text-title); color: var(--bg-color); text-align: center; padding: 45px 20px; border: none; }}
                .date-card h1 {{ font-family: 'Inter', sans-serif; font-weight: 900; font-size: 4rem; margin: 0; color: var(--bg-color); letter-spacing: -2px; }}
                .quote-card {{ grid-column: span 12; text-align: center; padding: 50px 30px; position: relative; }}
                .quote-card h2 {{ font-family: var(--font-title); font-size: 1.8rem; line-height: 1.5; color: var(--text-title); margin: 0 0 15px 0; }}
                .badge-llm {{ background: #4ec9b0; color: #111; padding: 6px 14px; font-size: 0.75rem; font-weight: bold; border-radius: 20px; display: inline-block; margin-bottom: 15px; }}
                .badge-error {{ background: #ef4444; color: #fff; padding: 6px 14px; font-size: 0.75rem; font-weight: bold; border-radius: 20px; display: inline-block; margin-bottom: 15px; }}
            </style>
        </head>
        <body class="theme-brutus">
            <div class="editorial-grid">
                <div class="card date-card">
                    <h1 id="display-date">{self.payload['date']}</h1>
                </div>
                <div class="card quote-card" id="quote-card-container">
                    <div id="llm-badge"></div>
                    <h2 id="ui-quote" style="color: #ffaa00; font-family: monospace;"></h2>
                    <span style="display:inline-block; margin-top:10px;">📌 系統狀態：<strong id="ui-pain"></strong></span>
                </div>
            </div>

            <script>
                const quotes = {quotes_js}; 
                const isLlmActive = {is_llm_active_js};
                
                window.onload = function() {{
                    const badgeElem = document.getElementById('llm-badge');
                    if (isLlmActive) {{
                        badgeElem.className = 'badge-llm';
                        badgeElem.innerHTML = '⚡ 連線成功！';
                    }} else {{
                        badgeElem.className = 'badge-error';
                        badgeElem.innerHTML = '🚨 API 連線失敗 (詳見下方)';
                    }}
                    document.getElementById('ui-quote').innerText = quotes[0].q;
                    document.getElementById('ui-pain').innerText = quotes[0].p;
                }};
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
