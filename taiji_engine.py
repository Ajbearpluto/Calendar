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
        
        self.dynamic_quotes, self.is_llm_active, self.sys_log = self.generate_quotes_via_llm(self.forum_titles)
        self.zodiac_advices = self.generate_daily_zodiac_advices()
        
        year, month, day = self.today.year, self.today.month, self.today.day
        stars = ["水瓶座", "雙魚座", "牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座"]
        zodiacs = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
        self.current_star = stars[(year + month + day + 6) % 12]
        self.current_zodiac = zodiacs[(year + month + day + 10) % 12]

        self.payload = {
            "date": self.today.strftime("%Y-%m-%d"),
            "star_sign": self.current_star,
            "zodiac_sign": self.current_zodiac,
        }

    def _init_static_databases(self):
        # Fallback 備用庫也升級加上 style, do, dont
        self.fallback_quotes = [
            {"style": "極致反差", "article": "看著陽光灑在辦公桌的植栽上，生機盎然。就像我滿滿的待辦事項，永遠長不完。", "q": "生活不只有詩和遠方，還有眼前的無薪加班。", "p": "社畜之淚", "do": "喝杯手搖", "dont": "看存摺"}, 
            {"style": "躺平無罪", "article": "今天鬧鐘響了三次，我終於領悟了一個宇宙真理。", "q": "努力不一定會成功，但不努力一定很輕鬆。", "p": "躺平哲學", "do": "準時下班", "dont": "自找麻煩"}
        ]
        
    def generate_daily_zodiac_advices(self):
        advices = [
            "今天適合整理環境，丟掉不必要的雜物，能帶來意想不到的好運。", "工作上可能會遇到固執的同事，深呼吸，用柔和的語氣能化解僵局。",
            "靈感爆發的一天！把腦中閃過的點子立刻記下來，未來會派上用場。", "財運微幅上升，但切忌衝動購物，把錢投資在學習上會更有價值。",
            "感情方面需要多一點傾聽，少一點說教，對方其實只需要你的陪伴。", "體能狀態極佳，下班後去流點汗吧！這能幫你洗刷一整天的疲憊。",
            "計畫趕不上變化，與其死磕到底，不如順應局勢，換個方式會更輕鬆。", "今天你的直覺非常準確，如果在兩個選擇中猶豫，請相信你的第一反應。",
            "人際關係出現微妙的化學反應，主動對陌生人微笑，會開啟一段好緣分。", "情緒稍顯低落，給自己泡杯好茶或咖啡，安靜獨處半小時能滿血復活。",
            "長輩或長官會給你重要的建議，就算當下覺得刺耳，也請先收進心裡。", "適合規劃長遠目標的一天，哪怕只是寫下第一步，宇宙都會開始幫你。"
        ]
        random.seed(self.today.strftime("%Y%m%d"))
        random.shuffle(advices)
        stars = ["水瓶座", "雙魚座", "牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座"]
        return dict(zip(stars, advices))

    def fetch_google_rss_trends(self):
        url = 'https://trends.google.com.tw/trending/rss?geo=TW'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                root = ET.fromstring(response.read())
                return [item.find('title').text for item in root.findall('./channel/item')[:15]]
        except Exception: return ["寧靜時光", "自我療癒"]

    def fetch_social_forum_trends(self):
        url = 'https://www.dcard.tw/service/api/v2/posts?popular=true&limit=15'
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
                return [item['title'] for item in json.loads(response.read()) if 'title' in item][:10]
        except Exception: return ["不想上班想離職", "存不到錢好焦慮"]

    def generate_quotes_via_llm(self, forum_titles):
        if not self.api_key: return self.fallback_quotes, False, "未偵測到 API 金鑰"
        try:
            list_resp = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}", timeout=10)
            if list_resp.status_code != 200: return self.fallback_quotes, False, "清單獲取失敗"
            models_data = list_resp.json().get('models', [])
            candidate_models = [m['name'].replace('models/', '') for m in models_data if 'generatecontent' in [method.lower() for method in m.get('supportedGenerationMethods', [])] and 'gemini' in m.get('name', '').lower() and 'vision' not in m.get('name', '').lower()]
            if not candidate_models: return self.fallback_quotes, False, "帳號無可用的生成模型"

            working_model = None
            headers = {"Content-Type": "application/json"}
            for model_name in candidate_models:
                try:
                    if requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}", json={"contents": [{"parts": [{"text": "1"}]}]}, headers=headers, timeout=5).status_code == 200:
                        working_model = model_name; break
                except: continue

            if not working_model: return self.fallback_quotes, False, "所有模型實測皆遭拒"
            sys_log_msg = f"V45 迷因教主多重情緒框架已啟動, 使用模型: {working_model}"

            titles_text = "\n".join([f"- {t}" for t in forum_titles])
            
            # 🔥 核心升級：強制 AI 使用五種不同的情緒框架，並加入宜忌
            prompt = f"""
            你是一位洞悉台灣社會現象的社群文案大師（兼具迷因教主與心理導師的靈魂）。今天是 {self.today.strftime('%Y-%m-%d')}。
            參考以下 Dcard 熱門標題的社會氛圍：\n{titles_text}\n
            請為我寫出 5 組適合發布在 Threads (脆) 上的日曆圖文。
            請嚴格依照以下 5 種指定的「情緒框架」各寫一組，不准重複：
            1. 【極致反差】：唯美畫面開場 ➡️ 殘酷社畜或生活現實結尾（地獄幽默）。
            2. 【滿血復活】：遇到鳥事或疲憊 ➡️ 轉念一想，突然充滿幹勁與熱情（積極正向）。
            3. 【人間清醒】：看透職場或人際的虛偽 ➡️ 決定放過自己，冷靜從容（通透哲學）。
            4. 【躺平無罪】：壓力山大 ➡️ 決定放棄掙扎，理直氣壯當個快樂廢物（負能量釋放）。
            5. 【微小幸運】：發現日常中微不足道的美好 ➡️ 帶來療癒感與時來運轉的暗示（純粹溫暖）。

            請嚴格以 JSON 陣列格式回傳，每組包含以下 key：
            - style: 標註上述的風格名稱 (如 "極致反差")
            - article: 50字以內的微型短文，節奏要快，充滿畫面感。
            - q: 畫龍點睛的一句強烈金句。
            - p: 痛點或共鳴標籤 (不需要加#字號)。
            - do: 今日宜 (2到4字，帶有黑色幽默或生活感，例如：準時閃人、大口吃肉)
            - dont: 今日忌 (2到4字，例如：點開群組、量體重)
            """
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.9,
                    "response_mime_type": "application/json"
                }
            }
            response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{working_model}:generateContent?key={self.api_key}", json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                raw_text = response.json()['candidates'][0]['content']['parts'][0]['text']
                # 自動清理可能的 Markdown 標籤
                raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                return json.loads(raw_text), True, sys_log_msg
            return self.fallback_quotes, False, "生成遭拒"
        except Exception as e: return self.fallback_quotes, False, f"執行崩潰：{str(e)}"

    def export_to_html(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, 'template.html')
        output_path = os.path.join(current_dir, 'index.html') 
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except FileNotFoundError:
            print("❌ 錯誤：找不到 template.html！")
            return

        html_content = html_content.replace('__QUOTES_JS__', json.dumps(self.dynamic_quotes, ensure_ascii=False))
        html_content = html_content.replace('__PAYLOAD_JSON__', json.dumps(self.payload, ensure_ascii=False))
        html_content = html_content.replace('__ZODIAC_ADVICES_JS__', json.dumps(self.zodiac_advices, ensure_ascii=False))
        html_content = html_content.replace('__IS_LLM_ACTIVE_JS__', "true" if self.is_llm_active else "false")
        html_content = html_content.replace('__SYS_LOG_JS__', json.dumps(self.sys_log, ensure_ascii=False))
        
        # 移除上一版的靜態字典，因為我們接下來會用皮囊重構
        html_content = html_content.replace('__PAYLOAD_DATE__', self.payload['date'])
        html_content = html_content.replace('__PAYLOAD_STAR__', self.current_star)
        html_content = html_content.replace('__PAYLOAD_ZODIAC__', self.current_zodiac)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

if __name__ == "__main__":
    TaijiOmniverseCalendar().export_to_html()
