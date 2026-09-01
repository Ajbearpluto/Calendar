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
        self.star_visuals = {"水瓶座": {"c": "星空藍", "v": "周圍環繞著發光的水波紋"}, "雙魚座": {"c": "海洋藍", "v": "頭頂有兩條光影小魚環繞"}, "牡羊座": {"c": "火焰紅", "v": "擁有發光的螺旋羊角"}, "金牛座": {"c": "大地綠", "v": "帶著小巧的黃金牛角"}, "雙子座": {"c": "明亮黃", "v": "身體有著雙重顏色的分裂感"}, "巨蟹座": {"c": "珍珠白", "v": "表面有一層閃亮的珍珠光澤"}, "獅子座": {"c": "王者金", "v": "頭頂戴著一頂微型的黃金皇冠"}, "處女座": {"c": "純淨白", "v": "周圍有純潔的光芒與花瓣飄落"}, "天秤座": {"c": "湖水綠", "v": "頭頂懸浮著一個發光的黃金小天平"}, "天蠍座": {"c": "深邃紫", "v": "背後有一條若隱若現的紫色毒刺光影"}, "射手座": {"c": "自由橘", "v": "背著一把迷你的光之弓箭"}, "摩羯座": {"c": "沉穩褐", "v": "額頭有發光的神秘符文"}}
        self.zodiac_visuals = {"鼠": {"c": "灰曜色", "v": "擁有靈動的小老鼠耳朵"}, "牛": {"c": "厚土色", "v": "帶著堅硬的牛角與鼻環"}, "虎": {"c": "霸氣橘", "v": "身上有著明顯的老虎斑紋"}, "兔": {"c": "櫻花粉", "v": "擁有長長的毛茸茸兔子耳朵"}, "龍": {"c": "神聖金", "v": "頭上長著威武的龍角"}, "蛇": {"c": "翡翠綠", "v": "身體呈現細長且帶有蛇鱗反光"}, "馬": {"c": "疾風棕", "v": "背部有著飄逸的馬鬃毛光影"}, "羊": {"c": "溫柔白", "v": "頭側有捲曲的綿羊角"}, "猴": {"c": "靈動桃", "v": "擁有一條長長的猴子尾巴"}, "雞": {"c": "晨曦紅", "v": "頭頂著鮮豔的雞冠"}, "狗": {"c": "忠誠黃", "v": "有著下垂的可愛狗狗耳朵"}, "豬": {"c": "豐饒粉", "v": "擁有一個可愛的粉紅豬鼻子"}}
        self.art_styles = ["最高規格「頂級寫實照」光學成像參數 (極致寫實、大師級攝影光影)"]
        self.fortune_fusion = [
            {"text": "星象顯示有破財危機，請立刻關閉所有購物APP的推播通知。", "prop": "一張正在燃燒的信用卡"},
            {"text": "水星逆行引發通訊危機，今日請再三確認訊息是否發錯群組。", "prop": "一支停在尷尬聊天室畫面的手機"},
            {"text": "天王星帶來突發變動，原本的完美計畫隨時可能被一場大雨打亂。", "prop": "一雙踩進水坑的白球鞋"}
        ]
        self.themes_data = {
            "社畜的生存掙扎": {"stages": ["被死線追殺的社畜", "眼神空洞的會議參與者"], "emotions": ["發出無聲的尖叫", "徹底放棄思考"], "textures": ["像史萊姆一樣裂開", "變成灰白色的石化狀態"], "actions": ["在辦公桌前癱瘓", "無力地敲擊鍵盤"]},
            "月光族的月底日常": {"stages": ["月底準備吃土的生存者", "物慾極高但沒錢的幻想家"], "emotions": ["看到價格標籤後的驚恐", "心如刀割的痛楚"], "textures": ["變得像紙一樣薄", "表面出現貧窮的裂痕"], "actions": ["抱著空的錢包痛哭", "在地上尋找發票"]},
            "極致的懶散躺平": {"stages": ["拒絕營業的廢物", "試圖物理性登出的人類"], "emotions": ["毫無波瀾，徹底放空", "散發著慵懶的氣息"], "textures": ["融化成一灘液體", "像麻糬一樣軟爛"], "actions": ["展現極致鬆弛感", "緩慢地蠕動"]}
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
            list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
            list_resp = requests.get(list_url, timeout=10)
            if list_resp.status_code != 200:
                return self.fallback_quotes, False, f"清單獲取失敗: 代碼 {list_resp.status_code}"

            models_data = list_resp.json().get('models', [])
            candidate_models = []
            
            for m in models_data:
                name = m.get('name', '').lower()
                if 'generatecontent' in [method.lower() for method in m.get('supportedGenerationMethods', [])] and 'gemini' in name and 'vision' not in name:
                    candidate_models.append(m['name'].replace('models/', ''))

            if not candidate_models:
                return self.fallback_quotes, False, "帳號無可用的生成模型"

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
                return self.fallback_quotes, False, "所有模型實測皆遭拒，請確認 API 額度。"

            sys_log_msg = f"V36 實測通過，鎖定模型: {working_model}"

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
                raw_text = raw_text.replace("```json", "").replace("
