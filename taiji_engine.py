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
        self.star_visuals = {"水瓶座": {"c": "星空藍", "v": "發光的水波紋"}, "雙魚座": {"c": "海洋藍", "v": "光影小魚"}, "牡羊座": {"c": "火焰紅", "v": "螺旋羊角"}, "金牛座": {"c": "大地綠", "v": "黃金牛角"}, "雙子座": {"c": "明亮黃", "v": "雙重顏色"}, "巨蟹座": {"c": "珍珠白", "v": "珍珠光澤"}, "獅子座": {"c": "王者金", "v": "黃金皇冠"}, "處女座": {"c": "純淨白", "v": "光芒花瓣"}, "天秤座": {"c": "湖水綠", "v": "黃金小天平"}, "天蠍座": {"c": "深邃紫", "v": "紫色毒刺"}, "射手座": {"c": "自由橘", "v": "光之弓箭"}, "摩羯座": {"c": "沉穩褐", "v": "神秘符文"}}
        self.zodiac_visuals = {"鼠": {"c": "灰曜色", "v": "小老鼠耳朵"}, "牛": {"c": "厚土色", "v": "堅硬牛角"}, "虎": {"c": "霸氣橘", "v": "老虎斑紋"}, "兔": {"c": "櫻花粉", "v": "兔子耳朵"}, "龍": {"c": "神聖金", "v": "威武龍角"}, "蛇": {"c": "翡翠綠", "v": "細長蛇鱗"}, "馬": {"c": "疾風棕", "v": "馬鬃毛"}, "羊": {"c": "溫柔白", "v": "綿羊角"}, "猴": {"c": "靈動桃", "v": "猴子尾巴"}, "雞": {"c": "晨曦紅", "v": "鮮豔雞冠"}, "狗": {"c": "忠誠黃", "v": "可愛狗狗耳朵"}, "豬": {"c": "豐饒粉", "v": "粉紅豬鼻子"}}
        
        # 🎵 V39 聽覺沉浸升級：加入 YouTube 實體音軌 ID
        self.fortune_fusion = [
            {"text": "星象顯示有破財危機，請立刻關閉所有購物APP的推播通知。", "prop": "一張正在燃燒的信用卡", "music_text": "🎶 迷幻爵士 Jazz Hop - 適合沉澱焦慮", "yt_id": "neV3EPgvZ3g"}, 
            {"text": "水星逆行引發通訊危機，今日請再三確認訊息是否發錯群組。", "prop": "一支停在尷尬聊天室畫面的手機", "music_text": "🎶 輕快 Lofi Beats - 保持心情平靜", "yt_id": "8XIGrtnOUtc"}, 
            {"text": "天王星帶來突發變動，原本的完美計畫隨時可能被一場大雨打亂。", "prop": "一雙踩進水坑的白球鞋", "music_text": "🎶 史詩氛圍 Epic Ambient - 迎接未知挑戰", "yt_id": "qH31oZlq-OQ"},
            {"text": "木星能量飽滿，今天是發揮靈感與整理思緒的絕佳時機。", "prop": "一杯冒著熱氣的黑咖啡", "music_text": "🎶 原聲吉他 Acoustic Folk - 專注與純粹", "yt_id": "m1-uVn07Rkw"}
        ]
        self.themes_data = {
            "社畜的生存掙扎": {"stages": ["被死線追殺的社畜", "眼神空洞的參與者"], "emotions": ["發出無聲的尖叫", "徹底放棄思考"], "textures": ["像史萊姆一樣裂開", "變成石化狀態"], "actions": ["在桌前癱瘓", "無力敲擊"]},
            "月光族的月底日常": {"stages": ["月底準備吃土", "物慾極高的幻想家"], "emotions": ["看到價格後的驚恐", "心如刀割"], "textures": ["變得像紙一樣薄", "出現貧窮的裂痕"], "actions": ["抱著錢包痛哭", "尋找發票"]},
            "極致的懶散躺平": {"stages": ["拒絕營業的廢物", "試圖物理性登出"], "emotions": ["徹底放空", "散發著慵懶"], "textures": ["融化成一灘液體", "像麻糬一樣軟爛"], "actions": ["極致鬆弛", "緩慢蠕動"]}
        }
        self.fallback_quotes = [
            {"article": "今天也是努力活得像個人的一天，", "q": "如果不行，那就先當一隻快樂的廢物也沒關係。", "p": "躺平哲學"}, 
            {"article": "我們總是以為熬過這陣子就好，", "q": "後來才發現，這陣子其實是一輩子。", "p": "生活碎片"}
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
            sys_log_msg = f"大腦重構完成，穩定鎖定模型: {working_model}"

            titles_text = "\n".join([f"- {t}" for t in forum_titles])
            prompt = f"你是一位洞悉台灣社會現象的社群文案大師。今天是 {self.today.strftime('%Y-%m-%d')}。參考以下 Dcard 熱門標題的社會氛圍：\n{titles_text}\n為我寫出 5 組日曆圖文 (包含生活、上班等普世痛點)。\n請嚴格以 JSON 陣列格式回傳，每組包含：\n1. article: 30字以內的幽默/療癒前言短文\n2. q: 畫龍點睛的一句金句\n3. p: 痛點標籤\n格式範例：[ {{\\\"article\\\": \\\"短文...\\\", \\\"q\\\": \\\"金句...\\\", \\\"p\\\": \\\"標籤\\\"}} ]"
            
            response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{working_model}:generateContent?key={self.api_key}", json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.9}}, headers=headers, timeout=15)
            
            if response.status_code == 200:
                raw_text = response.json()['candidates'][0]['content']['parts'][0]['text'].replace("```json", "").replace("```", "").strip()
                return json.loads(raw_text), True, sys_log_msg
            return self.fallback_quotes, False, "生成遭拒"
        except Exception as e: return self.fallback_quotes, False, f"執行崩潰：{str(e)}"

    def export_to_html(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, 'template.html')
        output_path = os.path.join(current_dir, 'taiji_dashboard.html')
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except FileNotFoundError:
            print("❌ 錯誤：找不到 template.html！")
            return

        html_content = html_content.replace('__THEMES_JS__', json.dumps(self.themes_data, ensure_ascii=False))
        html_content = html_content.replace('__QUOTES_JS__', json.dumps(self.dynamic_quotes, ensure_ascii=False))
        html_content = html_content.replace('__PAYLOAD_JSON__', json.dumps(self.payload, ensure_ascii=False))
        html_content = html_content.replace('__REAL_TRENDS_JS__', json.dumps(self.real_trends, ensure_ascii=False))
        html_content = html_content.replace('__FORTUNE_JS__', json.dumps(self.fortune_fusion, ensure_ascii=False))
        html_content = html_content.replace('__STAR_VISUALS_JS__', json.dumps(self.star_visuals, ensure_ascii=False))
        html_content = html_content.replace('__ZODIAC_VISUALS_JS__', json.dumps(self.zodiac_visuals, ensure_ascii=False))
        html_content = html_content.replace('__ZODIAC_ADVICES_JS__', json.dumps(self.zodiac_advices, ensure_ascii=False))
        html_content = html_content.replace('__IS_LLM_ACTIVE_JS__', "true" if self.is_llm_active else "false")
        html_content = html_content.replace('__SYS_LOG_JS__', json.dumps(self.sys_log, ensure_ascii=False))
        html_content = html_content.replace('__PAYLOAD_DATE__', self.payload['date'])
        html_content = html_content.replace('__PAYLOAD_STAR__', self.current_star)
        html_content = html_content.replace('__PAYLOAD_ZODIAC__', self.current_zodiac)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

if __name__ == "__main__":
    TaijiOmniverseCalendar().export_to_html()
