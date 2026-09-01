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
        # 關鍵：直接將錯誤訊息呈現在畫面上
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
        self.fortune_fusion = [{"text": "今日宜低調行事", "prop": "一個打開卻空無一物的便當盒"}]
        self.themes_data = {"系統偵錯": {"stages": ["等待連線", "準備除錯", "檢查中"], "emotions": ["冷靜", "嚴肅", "專注"], "textures": ["發出電子光芒", "呈現程式碼外觀", "金屬質感"], "actions": ["分析數據", "敲擊鍵盤", "掃描環境"]}}

    def fetch_google_rss_trends(self):
        return ["時事熱點載入中..."]

    def fetch_social_forum_trends(self):
        return ["社群熱點載入中..."]

    def generate_quotes_via_llm(self, forum_titles):
        # 🚨 吐真劑一：如果根本沒抓到金鑰，直接顯示在網頁上！
        if not self.api_key:
            error_msg = "致命錯誤：GitHub Settings 裡找不到 GEMINI_API_KEY，或是設定名稱打錯了！"
            return [{"q": error_msg, "p": "金鑰遺失"}], False
            
        try:
            # 強制使用最穩定的 1.5-flash 直連
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            prompt = f"請回傳一句話：'API 連線完全正常，指揮官您成功了！'。嚴格以 JSON 陣列格式回傳：[ {{\"q\": \"金句內容\", \"p\": \"痛點標籤\"}} ]"
            payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.1}}
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            # 🚨 吐真劑二：如果 Google 拒絕連線，直接把 Google 的回覆印在網頁上！
            if response.status_code != 200:
                error_msg = f"API 拒絕連線 (HTTP {response.status_code}): {response.text[:150]}"
                return [{"q": error_msg, "p": "連線遭拒"}], False
                
            data = response.json()
            raw_text = data['candidates'][0]['content']['parts'][0]['text'].replace("```json", "").replace("```", "").strip()
            new_quotes = json.loads(raw_text)
            
            return new_quotes, True
            
        except Exception as e:
            # 🚨 吐真劑三：如果發生其他系統崩潰，印出崩潰原因！
            error_msg = f"系統執行崩潰：{str(e)}"
            return [{"q": error_msg, "p": "系統異常"}], False

    def export_to_html(self):
        # 為了保持除錯焦點，精簡前端呈現
        quotes_js = json.dumps(self.dynamic_quotes, ensure_ascii=False)
        payload_js = json.dumps(self.payload, ensure_ascii=False)
        is_llm_active_js = "true" if self.is_llm_active else "false"

        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>TAIJI V31 X-RAY Edition</title>
            <style>
                body {{ font-family: sans-serif; background: #121212; color: #fff; text-align: center; padding: 50px; }}
                .status-box {{ padding: 30px; border-radius: 10px; margin: 20px auto; max-width: 600px; font-size: 1.2rem; line-height: 1.5; }}
                .fail {{ background: #4a0000; border: 2px solid #ff4444; }}
                .success {{ background: #003300; border: 2px solid #00ff00; }}
            </style>
        </head>
        <body>
            <h1>TAIJI 系統深度掃描儀</h1>
            <script>
                const isLlmActive = {is_llm_active_js};
                const quotes = {quotes_js};
                
                let boxClass = isLlmActive ? 'status-box success' : 'status-box fail';
                let icon = isLlmActive ? '✅ 連線成功' : '❌ 發現致命錯誤';
                
                document.write(`<div class="${{boxClass}}">`);
                document.write(`<h2>${{icon}}</h2>`);
                document.write(`<strong>診斷結果：</strong><br><br>`);
                document.write(`<span style="color: #ffaa00;">${{quotes[0].q}}</span>`);
                document.write(`</div>`);
            </script>
        </body>
        </html>
        """
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'taiji_dashboard.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

if __name__ == "__main__":
    engine = TaijiOmniverseCalendar()
    engine.export_to_html()
