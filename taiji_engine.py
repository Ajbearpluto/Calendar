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
        
        # 執行實彈排雷與生成
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
        self.star_visuals = {"水瓶座": {"c": "星空藍", "v": "發光水波紋"}, "雙魚座": {"c": "海洋藍", "v": "光影小魚"}, "牡羊座": {"c": "火焰紅", "v": "發光羊角"}, "金牛座": {"c": "大地綠", "v": "黃金牛角"}, "雙子座": {"c": "明亮黃", "v": "雙重顏色分裂"}, "巨蟹座": {"c": "珍珠白", "v": "珍珠光澤"}, "獅子座": {"c": "王者金", "v": "黃金皇冠"}, "處女座": {"c": "純淨白", "v": "光芒花瓣"}, "天秤座": {"c": "湖水綠", "v": "黃金小天平"}, "天蠍座": {"c": "深邃紫", "v": "紫色毒刺"}, "射手座": {"c": "自由橘", "v": "光之弓箭"}, "摩羯座": {"c": "沉穩褐", "v": "神秘符文"}}
        self.zodiac_visuals = {"鼠": {"c": "灰曜色", "v": "小老鼠耳朵"}, "牛": {"c": "厚土色", "v": "堅硬牛角"}, "虎": {"c": "霸氣橘", "v": "老虎斑紋"}, "兔": {"c": "櫻花粉", "v": "兔子耳朵"}, "龍": {"c": "神聖金", "v": "威武龍角"}, "蛇": {"c": "翡翠綠", "v": "蛇鱗反光"}, "馬": {"c": "疾風棕", "v": "馬鬃毛光影"}, "羊": {"c": "溫柔白", "v": "綿羊角"}, "猴": {"c": "靈動桃", "v": "猴子尾巴"}, "雞": {"c": "晨曦紅", "v": "鮮豔雞冠"}, "狗": {"c": "忠誠黃", "v": "狗狗耳朵"}, "豬": {"c": "豐饒粉", "v": "粉紅豬鼻子"}}
        self.art_styles = ["極致寫實照"]
        self.fortune_fusion = [
            {"text": "星象顯示有破財危機，請立刻關閉所有購物APP的推播通知。", "prop": "一張正在燃燒的信用卡"},
            {"text": "水星逆行引發通訊危機，今日請再三確認訊息是否發錯群組。", "prop": "一支停在尷尬聊天室畫面的手機"}
        ]
        self.themes_data = {
            "社畜的生存掙扎": {"stages": ["被死線追殺", "眼神空洞"], "emotions": ["無聲尖叫", "放棄思考"], "textures": ["裂開", "石化狀態"], "actions": ["癱瘓", "無力敲擊"]},
            "月光族的月底日常": {"stages": ["準備吃土", "物慾極高"], "emotions": ["驚恐", "心如刀割"], "textures": ["像紙一樣薄", "貧窮裂痕"], "actions": ["抱錢包痛哭", "找發票"]},
            "極致的懶散躺平": {"stages": ["拒絕營業", "物理性登出"], "emotions": ["毫無波瀾", "慵懶"], "textures": ["融化成液體", "軟爛麻糬"], "actions": ["極致鬆弛", "緩慢蠕動"]}
        }
        self.fallback_quotes = [
            {"q": "努力不一定會成功，但不努力一定很輕鬆。", "p": "躺平哲學"},
            {"q": "薪水就像渣男，每個月來一次，沒幾天就消失得無影無蹤。", "p": "金錢焦慮"}
        ]

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
            return ["連假塞車", "物價上漲", "天氣預報不準"]

    def fetch_social_forum_trends(self):
        url = 'https://www.dcard.tw/service/api/v2/posts?popular=true&limit=15'
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
                data = json.loads(response.read())
                return [item['title'] for item in data if 'title' in item][:10]
        except Exception:
            return ["不想上班想離職", "存不到錢好焦慮"]

    def generate_quotes_via_llm(self, forum_titles):
        if not self.api_key:
            return self.fallback_quotes, False, "未偵測到 API 金鑰"

        try:
            # 階段一：取得帳號可用模型清單
            list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
            list_resp = requests.get(list_url, timeout=10)
            if list_resp.status_code != 200:
                return self.fallback_quotes, False, f"清單獲取失敗: 代碼 {list_resp.status_code}"

            models_data = list_resp.json().get('models', [])
            candidate_models = []
            
            for m in models_data:
                name = m.get('name', '').lower()
                # 篩選條件：支援 generateContent 且為 gemini 系列，排除 embedding/vision 專用模型
                if 'generatecontent' in [method.lower() for method in m.get('supportedGenerationMethods', [])] and 'gemini' in name and 'vision' not in name:
                    candidate_models.append(m['name'].replace('models/', ''))

            if not candidate_models:
                return self.fallback_quotes, False, "帳號無可用的生成模型"

            # 階段二：實彈測試 (Ping) - 找出第一個真正存活的節點
            working_model = None
            headers = {"Content-Type": "application/json"}
            test_payload = {"contents": [{"parts": [{"text": "1"}]}]}
            
            for model_name in candidate_models:
                test_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
                try:
                    test_resp = requests.post(test_url, json=test_payload, headers=headers, timeout=5)
                    if test_resp.status_code == 200:
                        working_model = model_name
                        break
                except:
                    continue

            if not working_model:
                return self.fallback_quotes, False, "所有候選模型實測皆遭拒，請確認 API 額度或權限。"

            sys_log_msg = f"V35 實測通過，鎖定模型: {working_model}"

            # 階段三：正式執行文案生成
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{working_model}:generateContent?key={self.api_key}"
            titles_text = "\n".join([f"- {t}" for t in forum_titles])
            prompt = f"""
            你是一位洞悉台灣社會現象的社群文案大師。今天是 {self.today.strftime("%Y-%m-%d")}。
            參考以下 Dcard 熱門標題的社會氛圍：\n{titles_text}\n
            為我寫出 5 句極度接地氣的大眾共鳴金句 (包含生活、上班、缺錢等普世痛點)。
            - 3 句為帶有自我解嘲的「幽默幹話」。
            - 2 句為「正向療癒」的溫暖句子。
            請嚴格以 JSON 陣列格式回傳：[ {{"q": "金句內容", "p": "痛點標籤"}} ]
            """
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.9}
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                raw_text = data['candidates'][0]['content']['parts'][0]['text']
                raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                new_quotes = json.loads(raw_text)
                return new_quotes, True, sys_log_msg
            else:
                return self.fallback_quotes, False, f"{working_model} 生成遭拒: 代碼 {response.status_code}"
                
        except Exception as e:
            return self.fallback_quotes, False, f"執行崩潰：{str(e)}"

    def export_to_html(self):
        themes_js = json.dumps(self.themes_data, ensure_ascii=False)
        quotes_js = json.dumps(self.dynamic_quotes, ensure_ascii=False)
        payload_js = json.dumps(self.payload, ensure_ascii=False)
        real_trends_js = json.dumps(self.real_trends, ensure_ascii=False)
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
            <title>TAIJI V35 Auto-Drive Edition</title>
            <script src="https://unpkg.com/lunar-javascript/lunar.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700&family=Inter:wght@400;600;700;900&display=swap');
                :root {{ --bg-color: #ffffff; --card-bg: #ffffff; --text-title: #111111; --text-main: #333333; --text-sub: #888888; --font-title: 'Noto Serif TC', serif; --font-body: 'Inter', sans-serif; --border-radius: 0px; --border-style: 1px solid #eeeeee; --hero-bg: #f9f9f9; --btn-bg: #111111; --btn-text: #ffffff; --spacing: 40px; }}
                body.theme-popeye {{ --bg-color: #F5F3E9; --text-title: #0d3b66; --border-radius: 12px; --border-style: 2px solid #1a1a1a; --btn-bg: #e63946; }}
                body.theme-brutus {{ --bg-color: #121212; --card-bg: #1e1e1e; --text-title: #f5f5f5; --text-main: #e0e0e0; --text-sub: #757575; --border-radius: 4px; --border-style: 1px solid #333333; --hero-bg: #1a1a1a; --btn-bg: #f5f5f5; --btn-text: #121212; }}
                body.theme-wired {{ --bg-color: #ffffff; --card-bg: #f4f5f7; --text-title: #000000; --text-main: #111111; --text-sub: #6b7280; --border-radius: 16px; --border-style: none; --hero-bg: #ebf5ff; --btn-bg: #2563eb; --btn-text: #ffffff; }}
                body {{ font-family: var(--font-body); background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 40px 20px; transition: all 0.5s ease; }}
                .editorial-grid {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }}
                .card {{ background: var(--card-bg); border-radius: var(--border-radius); padding: var(--spacing); border: var(--border-style); transition: all 0.3s ease; }}
                .date-card {{ grid-column: span 12; background: var(--text-title); color: var(--bg-color); text-align: center; padding: 45px 20px; border: none; }}
                .date-card h1 {{ font-family: 'Inter', sans-serif; font-weight: 900; font-size: 4rem; margin: 0; color: var(--bg-color); letter-spacing: -2px; }}
                .date-card p.lunar {{ font-size: 1.1rem; color: var(--bg-color); opacity: 0.9; letter-spacing: 5px; margin: 15px 0 0 0; text-transform: uppercase; }}
                .headline-card {{ grid-column: span 12; background: var(--hero-bg); text-align: center; padding: 50px 20px; border-bottom: 3px solid var(--text-title); }}
                .headline-card h2 {{ font-family: var(--font-title); font-size: 2.5rem; color: var(--text-title); margin: 0 0 15px 0; }}
                .quote-card {{ grid-column: span 12; text-align: center; padding: 50px 30px; position: relative; }}
                .quote-card h2 {{ font-family: var(--font-title); font-size: 1.8rem; line-height: 1.5; color: var(--text-title); margin: 0 0 15px 0; }}
                .badge-llm {{ background: #4ec9b0; color: #111; padding: 6px 14px; font-size: 0.75rem; font-weight: bold; border-radius: 20px; display: inline-block; margin-bottom: 15px; }}
                .badge-static {{ background: #ef4444; color: #fff; padding: 6px 14px; font-size: 0.75rem; font-weight: bold; border-radius: 20px; display: inline-block; margin-bottom: 15px; }}
                .info-card {{ grid-column: span 6; }} .actor-card {{ grid-column: span 6; }}
            </style>
        </head>
        <body>
            <div class="editorial-grid">
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
                    <h3 style="border-bottom: 1px solid var(--text-sub); padding-bottom:10px;">系統日誌</h3>
                    <div class="content" style="color: var(--text-sub); font-size: 0.85rem; line-height:1.6; margin-top:10px;">
                        <span style="color: #2563eb; font-weight: bold;">[最新動態]</span> <span id="log-data-source"></span><br>
                        自動化工廠：V35 實彈排雷連線系統已啟動。<br>
                    </div>
                </div>

                <div class="card actor-card">
                    <h3 id="title-actor-a" style="border-bottom: 2px solid var(--text-title); padding-bottom:10px; margin-top:0;">A. {self.payload['star_sign']} Slime</h3>
                    <div class="detail-list" style="line-height:1.8; margin-top:10px;">
                        <strong>狀態：</strong><span id="ui-stage-a"></span><br><strong>表情：</strong><span id="ui-emo-a"></span><br>
                        <strong>材質：</strong><span id="ui-tex-a"></span><br><strong>動作：</strong><span id="ui-act-a"></span>
                    </div>
                </div>
            </div>

            <script>
                const themes = {themes_js};
                const quotes = {quotes_js}; 
                const realTrends = {real_trends_js};
                const isLlmActive = {is_llm_active_js};
                const sysLog = {sys_log_js};
                const payload = {payload_js};
                
                const webThemes = [
                    {{ class: '', name: 'KINFOLK 極簡北歐風' }},
                    {{ class: 'theme-popeye', name: 'POPEYE 潮流日雜風' }},
                    {{ class: 'theme-brutus', name: 'BRUTUS 高級暗黑風' }},
                    {{ class: 'theme-wired', name: 'WIRED 前衛科技風' }}
                ];

                function getRandomItem(arr) {{ return arr[Math.floor(Math.random() * arr.length)]; }}
                function getRandomTwo(arr) {{
                    let shuffled = arr.slice(0), i = arr.length, temp, index;
                    while (i--) {{ index = Math.floor((i + 1) * Math.random()); temp = shuffled[index]; shuffled[index] = shuffled[i]; shuffled[i] = temp; }}
                    return shuffled.slice(0, 2);
                }}

                window.onload = function() {{
                    try {{
                        const d = new Date(payload.date + "T00:00:00");
                        if (typeof Lunar !== 'undefined') {{
                            const lunar = Lunar.fromDate(d);
                            let lunarStr = `農曆 ${{lunar.getMonthInChinese()}}月${{lunar.getDayInChinese()}}`;
                            document.getElementById('display-lunar').innerText = lunarStr;
                        }}
                    }} catch (e) {{}}

                    const badgeElem = document.getElementById('llm-badge');
                    const quoteCard = document.getElementById('quote-card-container');
                    
                    if (isLlmActive) {{
                        badgeElem.className = 'badge-llm';
                        badgeElem.innerHTML = '⚡ LLM SOUL ENGINE GENERATED';
                        quoteCard.style.border = '2px dashed #4ec9b0';
                    }} else {{
                        badgeElem.className = 'badge-static';
                        badgeElem.innerHTML = '🚨 雲端 API 未連線 (使用備用庫)';
                    }}

                    document.body.className = getRandomItem(webThemes).class;
                    
                    const selectedThemeName = getRandomItem(Object.keys(themes));
                    const theme = themes[selectedThemeName];
                    const selectedQuote = getRandomItem(quotes);
                    const stages = getRandomTwo(theme.stages);
                    const emos = getRandomTwo(theme.emotions);
                    const texs = getRandomTwo(theme.textures);
                    const acts = getRandomTwo(theme.actions);

                    document.getElementById('ui-scene').innerText = getRandomItem(realTrends);
                    document.getElementById('ui-stage-a').innerText = stages[0];
                    document.getElementById('ui-emo-a').innerText = emos[0];
                    document.getElementById('ui-tex-a').innerText = texs[0];
                    document.getElementById('ui-act-a').innerText = acts[0];
                    
                    document.getElementById('ui-quote').innerText = '"' + selectedQuote.q + '"';
                    document.getElementById('ui-pain').innerText = selectedThemeName + " | " + selectedQuote.p;
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
