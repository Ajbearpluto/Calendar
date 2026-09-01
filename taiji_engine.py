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
        
        # 🧠 宗師級：啟動動態模型滲透系統
        self.dynamic_quotes, self.is_llm_active, self.sys_log = self.generate_quotes_via_llm(self.forum_titles)
        
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
        self.fortune_fusion = [{"text": "系統已透過白帽手段強制取得最高權限。", "prop": "一台閃爍著綠色代碼的筆記型電腦"}]
        self.themes_data = {
            "宗師級除錯日常": {"stages": ["死盯著螢幕的工程師", "成功駭入系統的駭客"], "emotions": ["眼神銳利", "嘴角露出自信的微笑"], "textures": ["散發出強大的代碼氣場", "呈現完美無瑕的狀態"], "actions": ["在鍵盤上飛舞", "按下最終的 Enter 鍵"]}
        }
        self.fallback_quotes = [{"q": "如果大門深鎖，我們就自己寫一把萬能鑰匙。", "p": "駭客思維"}]

    def fetch_google_rss_trends(self):
        return ["AI 突破限制", "駭客任務", "系統升級"]

    def fetch_social_forum_trends(self):
        return ["終於成功了！", "這系統也太龜毛", "永不放棄的精神"]

    def generate_quotes_via_llm(self, forum_titles):
        if not self.api_key:
            return self.fallback_quotes, False, "致命錯誤：未偵測到金鑰"

        try:
            # 🚨 步驟一：向 Google 資料庫發起偵測，列出該帳號「真正可用」的所有模型
            list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
            list_resp = requests.get(list_url, timeout=10)
            
            if list_resp.status_code != 200:
                return [{"q": f"探測模型清單遭拒: {list_resp.text[:100]}", "p": "探測失敗"}], False, f"模型列表 API 異常 (代碼 {list_resp.status_code})"

            models_data = list_resp.json().get('models', [])
            available_models = []
            
            # 篩選出支援 generateContent 的 gemini 模型
            for m in models_data:
                if 'generateContent' in m.get('supportedGenerationMethods', []) and 'gemini' in m.get('name', '').lower():
                    available_models.append(m['name'].replace('models/', ''))

            if not available_models:
                return [{"q": "您的金鑰沒有配發任何文字生成模型的權限！", "p": "權限為空"}], False, "帳號無可用模型"

            # 🚨 步驟二：智能決策，找出最佳模型
            target_model = available_models[0] # 保底使用第一個找到的
            for pref in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-1.5-pro', 'gemini-pro', 'gemini-1.0-pro']:
                if pref in available_models:
                    target_model = pref
                    break
                    
            sys_log_msg = f"宗師系統成功探測並自動鎖定您的專屬模型: {target_model}"
            print(sys_log_msg)

            # 🚨 步驟三：拿著正確的名字，發起正式呼叫
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent?key={self.api_key}"
            
            titles_text = "\n".join([f"- {t}" for t in forum_titles])
            prompt = f"""
            你是一位洞悉台灣社會現象的社群文案大師。今天是 {self.today.strftime("%Y-%m-%d")}。
            參考以下關鍵字：\n{titles_text}\n
            為我寫出 3 句極度接地氣的大眾共鳴金句。
            請嚴格以 JSON 陣列格式回傳：[ {{"q": "金句內容", "p": "痛點標籤"}} ]
            """
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.9}
            }
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                raw_text = data['candidates'][0]['content']['parts'][0]['text']
                raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                new_quotes = json.loads(raw_text)
                return new_quotes, True, sys_log_msg
            else:
                return [{"q": f"連線 {target_model} 遭拒: {response.text[:100]}", "p": "生成失敗"}], False, f"{target_model} 連線失敗"
                
        except Exception as e:
            return [{"q": f"底層邏輯崩潰：{str(e)}", "p": "系統異常"}], False, "Python 引擎發生例外狀況"

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
        sys_log_js = json.dumps(self.sys_log, ensure_ascii=False)

        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>TAIJI V34 Grandmaster Edition</title>
            <script src="https://unpkg.com/lunar-javascript/lunar.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700&family=Inter:wght@400;600;700;900&display=swap');
                :root {{ --bg-color: #121212; --card-bg: #1e1e1e; --text-title: #f5f5f5; --text-main: #e0e0e0; --text-sub: #757575; --font-title: 'Noto Serif TC', serif; --font-body: 'Inter', sans-serif; --border-radius: 8px; --border-style: 1px solid #333; --hero-bg: #1a1a1a; --spacing: 40px; }}
                body {{ font-family: var(--font-body); background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 40px 20px; }}
                .editorial-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }}
                .card {{ background: var(--card-bg); border-radius: var(--border-radius); padding: var(--spacing); border: var(--border-style); }}
                .date-card {{ grid-column: span 12; background: #f5f5f5; color: #121212; text-align: center; padding: 45px 20px; }}
                .date-card h1 {{ font-family: 'Inter', sans-serif; font-weight: 900; font-size: 4rem; margin: 0; }}
                .quote-card {{ grid-column: span 12; text-align: center; padding: 50px 30px; position: relative; }}
                .quote-card h2 {{ font-family: var(--font-title); font-size: 1.8rem; line-height: 1.5; color: var(--text-title); margin: 0 0 15px 0; }}
                .badge-llm {{ background: #4ec9b0; color: #111; padding: 6px 14px; font-size: 0.75rem; font-weight: bold; border-radius: 20px; display: inline-block; margin-bottom: 15px; }}
                .badge-static {{ background: #ef4444; color: #fff; padding: 6px 14px; font-size: 0.75rem; font-weight: bold; border-radius: 20px; display: inline-block; margin-bottom: 15px; }}
                .info-card {{ grid-column: span 12; }}
            </style>
        </head>
        <body>
            <div class="editorial-grid">
                <div class="card date-card">
                    <h1 id="display-date">{self.payload['date']}</h1>
                </div>
                <div class="card quote-card" id="quote-card-container">
                    <div id="llm-badge"></div>
                    <h2 id="ui-quote"></h2>
                    <span style="display:inline-block; margin-top:10px;">📌 今日痛點：<strong id="ui-pain"></strong></span>
                </div>
                
                <div class="card info-card">
                    <h3 style="border-bottom: 1px solid var(--text-sub); padding-bottom:10px; color:#4ec9b0;">🛡️ 白帽駭客系統日誌</h3>
                    <div class="content" style="line-height:1.6; margin-top:10px; font-family: monospace; font-size:1.1rem;">
                        <span style="color: #eab308; font-weight: bold;">[最新動態]</span> <span id="log-data-source"></span><br>
                        自動化工廠：V34 宗師級動態尋標器已成功發揮作用。<br>
                    </div>
                </div>
            </div>

            <script>
                const quotes = {quotes_js}; 
                const isLlmActive = {is_llm_active_js};
                const sysLog = {sys_log_js};
                
                window.onload = function() {{
                    const badgeElem = document.getElementById('llm-badge');
                    const quoteCard = document.getElementById('quote-card-container');
                    
                    if (isLlmActive) {{
                        badgeElem.className = 'badge-llm';
                        badgeElem.innerHTML = '⚡ 宗師模式連線成功';
                        quoteCard.style.border = '2px dashed #4ec9b0';
                    }} else {{
                        badgeElem.className = 'badge-static';
                        badgeElem.innerHTML = '🚨 API 阻擋 (回歸備用庫)';
                    }}
                    
                    document.getElementById('ui-quote').innerText = '"' + quotes[0].q + '"';
                    document.getElementById('ui-pain').innerText = quotes[0].p;
                    document.getElementById('log-data-source').innerText = sysLog;
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
