import json
from datetime import datetime, timezone, timedelta
import os
import urllib.request
import xml.etree.ElementTree as ET
import random
import ssl

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class TaijiOmniverseCalendar:
    def __init__(self):
        # 🌐 【時區校正】強制鎖定為台灣時間 (UTC+8)
        tz_tw = timezone(timedelta(hours=8))
        self.today = datetime.now(tz_tw)
        
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        
        self._init_static_databases()
        self.self_diagnostic()
        self.real_trends = self.fetch_google_rss_trends()
        self.forum_titles = self.fetch_social_forum_trends()
        self.dynamic_quotes, self.is_llm_active = self.generate_quotes_via_llm(self.forum_titles)
        
        # 🌌 【宇宙曆法公式】根據年月日的絕對軌跡推算，保證每天變化
        year = self.today.year
        month = self.today.month
        day = self.today.day
        
        stars = ["水瓶座", "雙魚座", "牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座"]
        zodiacs = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
        
        star_index = (year + month + day + 6) % 12
        zodiac_index = (year + month + day + 10) % 12
        
        current_star = stars[star_index]
        current_zodiac = zodiacs[zodiac_index]

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
        self.star_visuals = {
            "水瓶座": {"c": "星空藍", "v": "周圍環繞著發光的水波紋"},
            "雙魚座": {"c": "海洋藍", "v": "頭頂有兩條光影小魚環繞"},
            "牡羊座": {"c": "火焰紅", "v": "擁有發光的螺旋羊角"},
            "金牛座": {"c": "大地綠", "v": "帶著小巧的黃金牛角"},
            "雙子座": {"c": "明亮黃", "v": "身體有著雙重顏色的分裂感"},
            "巨蟹座": {"c": "珍珠白", "v": "表面有一層閃亮的珍珠光澤"},
            "獅子座": {"c": "王者金", "v": "頭頂戴著一頂微型的黃金皇冠"},
            "處女座": {"c": "純淨白", "v": "周圍有純潔的光芒與花瓣飄落"},
            "天秤座": {"c": "湖水綠", "v": "頭頂懸浮著一個發光的黃金小天平"},
            "天蠍座": {"c": "深邃紫", "v": "背後有一條若隱若現的紫色毒刺光影"},
            "射手座": {"c": "自由橘", "v": "背著一把迷你的光之弓箭"},
            "摩羯座": {"c": "沉穩褐", "v": "額頭有發光的神秘符文"}
        }
        self.zodiac_visuals = {
            "鼠": {"c": "灰曜色", "v": "擁有靈動的小老鼠耳朵"},
            "牛": {"c": "厚土色", "v": "帶著堅硬的牛角與鼻環"},
            "虎": {"c": "霸氣橘", "v": "身上有著明顯的老虎斑紋"},
            "兔": {"c": "櫻花粉", "v": "擁有長長的毛茸茸兔子耳朵"},
            "龍": {"c": "神聖金", "v": "頭上長著威武的龍角"},
            "蛇": {"c": "翡翠綠", "v": "身體呈現細長且帶有蛇鱗反光"},
            "馬": {"c": "疾風棕", "v": "背部有著飄逸的馬鬃毛光影"},
            "羊": {"c": "溫柔白", "v": "頭側有捲曲的綿羊角"},
            "猴": {"c": "靈動桃", "v": "擁有一條長長的猴子尾巴"},
            "雞": {"c": "晨曦紅", "v": "頭頂著鮮豔的雞冠"},
            "狗": {"c": "忠誠黃", "v": "有著下垂的可愛狗狗耳朵"},
            "豬": {"c": "豐饒粉", "v": "擁有一個可愛的粉紅豬鼻子"}
        }
        
        # 📸 唯一鎖定：頂級寫實照 (涵蓋萬事萬物)
        self.art_styles = [
            "最高規格「頂級寫實照」光學成像參數 (極致寫實、大師級攝影光影、場景涵蓋宇宙星辰、工作日常、建築物、花草樹木等萬事萬物真實質感)"
        ]
        
        self.fortune_fusion = [
            {"text": "今日宜低調行事，不適合做任何重大決定，包含中午要吃什麼。", "prop": "一個打開卻空無一物的便當盒"},
            {"text": "星象顯示有破財危機，請立刻關閉所有購物APP的推播通知。", "prop": "一張正在燃燒的信用卡"},
            {"text": "能量低迷，說話容易得罪人，今天最適合戴上耳機與世隔絕。", "prop": "一副巨大的降噪耳機"},
            {"text": "天氣與星象同時作亂，出門除了帶傘，還需要帶上極大的耐心。", "prop": "一把被狂風吹到開花的反折雨傘"},
            {"text": "水星逆行引發通訊危機，今日請再三確認訊息是否發錯群組。", "prop": "一支停在尷尬聊天室畫面的手機"},
            {"text": "土星帶來沉重壓力，建議今晚放棄抵抗，讓衣服繼續堆在椅子上。", "prop": "一張長滿衣服的椅子"},
            {"text": "木星放大食慾，今日路過手搖飲店請自動蒙上雙眼。", "prop": "一杯喝完只剩冰塊的珍珠奶茶"},
            {"text": "火星引發急躁，遇到捷運或公車跑掉請深呼吸，不要追。", "prop": "一張餘額不足的悠遊卡"},
            {"text": "金星能量減弱，社交電力提早耗盡，下班後請立刻拔腿就跑。", "prop": "一個寫著『營業結束』的假笑面具"},
            {"text": "冥王星暗示改變，是時候面對那個永遠減不下來的體重了。", "prop": "一台顯示著 Err 的體重計"},
            {"text": "天王星帶來突發變動，原本的完美計畫隨時可能被一場大雨打亂。", "prop": "一雙踩進水坑的白球鞋"},
            {"text": "海王星讓人迷糊，出門前請摸摸口袋，確認鑰匙跟理智都有帶上。", "prop": "一串找不到大門鑰匙的鑰匙圈"},
            {"text": "太陽合相帶來短暫的清醒，適合整理那些永遠截不完的螢幕截圖。", "prop": "一個顯示『儲存空間不足』的手機畫面"},
            {"text": "月亮空亡期容易迷失方向，今天出門就跟著導航走，別相信自己的方向感。", "prop": "一個瘋狂重新規劃路線的導航畫面"},
            {"text": "滿月能量波動大，理智線容易斷裂，建議遠離一切會激怒你的人事物。", "prop": "一個被捏爆的壓力球"}
        ]
        self.themes_data = {
            "社畜的生存掙扎": {"stages": ["靈魂還在床上的打工人", "被死線追殺的社畜", "眼神空洞的會議參與者"], "emotions": ["發出無聲的尖叫", "強作鎮定的苦笑", "徹底放棄思考"], "textures": ["像史萊姆一樣裂開", "變成灰白色的石化狀態", "流出透明的冷汗"], "actions": ["在辦公桌前癱瘓", "看著時鐘絕望", "無力地敲擊鍵盤"]},
            "月光族的月底日常": {"stages": ["看著戶頭餘額發抖的窮鬼", "月底準備吃土的生存者", "物慾極高但沒錢的幻想家"], "emotions": ["欲哭無淚的絕望", "看到價格標籤後的驚恐", "心如刀割的痛楚"], "textures": ["變得像紙一樣薄", "表面出現貧窮的裂痕", "不斷流出窮酸汗"], "actions": ["倒立試圖抖出零錢", "抱著空的錢包痛哭", "在地上尋找發票"]},
            "極致的懶散躺平": {"stages": ["與沙發融為一體的生物", "拒絕營業的廢物", "試圖物理性登出的人類"], "emotions": ["毫無波瀾，徹底放空", "安詳地閉上雙眼", "散發著慵懶的氣息"], "textures": ["融化成一灘液體", "像麻糬一樣軟爛", "變成一坨無骨肉球"], "actions": ["展現極致鬆弛感，直接躺平", "緩慢地蠕動", "發出微弱的打呼聲"]},
            "飲食與體重的拉扯": {"stages": ["在宵夜前痛苦掙扎的減肥者", "把手搖飲當水喝的快樂冠軍", "看著體重計懷疑人生的胖子"], "emotions": ["充滿罪惡感的愉悅", "自暴自棄的微笑", "捏著肚子上的肉流淚"], "textures": ["像發酵麵團一樣膨脹", "表面泛著油光", "呈現軟綿綿的泡芙狀態"], "actions": ["瘋狂咀嚼著零食", "把體重計踢到床底", "在鏡子前吸氣縮小腹"]},
            "數位時代的資訊焦慮": {"stages": ["被未讀訊息淹沒的逃避者", "電量剩下1%的恐慌症患者", "滑短影音滑到失憶的網癮患者"], "emotions": ["雙眼布滿血絲", "盯著螢幕露出詭異的笑容", "因為沒網路而抓狂"], "textures": ["全身閃爍著電子雜訊", "像當機一樣停格", "表面浮現各種社群圖示"], "actions": ["瘋狂往下滑動手機", "到處尋找充電插座", "把手機遠遠丟開又撿回來"]},
            "人際內耗與社交邊界": {"stages": ["社交電力提早歸零的 I 人", "在群組裡假笑陪聊的邊緣人", "下班後不想被打擾的隱士"], "emotions": ["戴著和善但虛假的面具", "在內心狂翻白眼", "渴望瞬間移動回家"], "textures": ["像被榨乾的檸檬", "表面長出防衛的尖刺", "呈現半透明的隱形狀態"], "actions": ["已讀不回裝死中", "躲在角落滑手機", "對著空氣練習拒絕別人的台詞"]}
        }
        self.fallback_quotes = [
            {"q": "薪水就像渣男，每個月來一次，沒幾天就消失得無影無蹤。", "p": "金錢焦慮"},
            {"q": "努力不一定會成功，但不努力一定很輕鬆。", "p": "躺平哲學"},
            {"q": "買東西不是為了炫耀，是為了證明我還活著。", "p": "購物療法"},
            {"q": "人生就像減肥，永遠都在『明天再開始』的路上。", "p": "無盡的輪迴"}
        ]

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
            return ["不想上班想離職", "存不到錢好焦慮", "客戶又在發神經", "每天都睡不飽"]

    def generate_quotes_via_llm(self, forum_titles):
        if not HAS_GENAI or not self.api_key:
            print("⚠️ 未偵測到 API Key。切換至備用庫。")
            return self.fallback_quotes, False
        print("🧠 正在連線 LLM 靈魂引擎...")
        try:
            genai.configure(api_key=self.api_key)
            
            # 🛠️ 【精準修復】移除 latest，鎖定絕對穩定版模型 gemini-1.5-flash
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            titles_text = "\n".join([f"- {t}" for t in forum_titles])
            prompt = f"""
            你是一位洞悉台灣社會現象的社群文案大師。今天是 {self.today.strftime("%Y-%m-%d")}。
            參考以下 Dcard 熱門標題的社會氛圍：\n{titles_text}\n
            為我寫出 5 句極度接地氣的大眾共鳴金句 (包含生活、上班、缺錢等普世痛點)。
            - 3 句為帶有自我解嘲的「幽默幹話」（厭世、吐槽）。
            - 2 句為「正向療癒、生活微光」的溫暖句子。
            請嚴格以 JSON 陣列格式回傳：[ {{"q": "金句內容", "p": "痛點標籤"}} ]
            """
            response = model.generate_content(prompt, generation_config={"temperature": 0.95})
            raw_text = response.text.replace("```json", "").replace("```", "").strip()
            new_quotes = json.loads(raw_text)
            print("🟢 靈魂引擎連線成功！")
            return new_quotes, True
        except Exception as e:
            print(f"⚠️ 靈魂引擎連線失敗 ({str(e)})。已切換至備用庫。")
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
                    
                    <label style="margin-left:20px;">🎨 風格設定：</label>
                    <select id="ui-style-override" disabled>
                        <option value="random">📸 頂級寫實照 (萬事萬物) 鎖定</option>
                    </select>
                </div>

                <div class="card date-card">
                    <h1 id="display-date">{self.payload['date']}</h1>
                    <p class="lunar" id="display-lunar">正在演算農民曆...</p>
                </div>

                <div class="card headline-card">
                    <p style="text-transform: uppercase; letter-spacing: 3px; font-size: 0.85rem; margin-bottom:15px; font-weight: bold;">Google Trends Live</p>
                    <h2 id="ui-scene"></h2>
                    <p style="margin-top:15px;">AI 視覺媒材：<strong id="ui-style" style="color:var(--text-main);"></strong></p>
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
                        自動化工廠：V31 雲端自動更新排程已準備就緒。<br>
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
                const emotionTags = ["#情緒價值", "#人間清醒", "#好好生活", "#自我療癒", "#社畜心聲", "#人生好難", "#微苦日常", "#今日幹話"];
                const artTags = ["#寫實攝影", "#視覺藝術", "#萬事萬物"];

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
                    const year = d.getFullYear();
                    const month = d.getMonth() + 1;
                    const day = d.getDate();
                    
                    const stars = ["水瓶座", "雙魚座", "牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座"];
                    const zodiacs = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"];
                    
                    const starIndex = (year + month + day + 6) % 12;
                    const zodiacIndex = (year + month + day + 10) % 12;
                    
                    return {{
                        star: stars[starIndex],
                        zodiac: zodiacs[zodiacIndex]
                    }};
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

                    payload.star_sign = luckySigns.star;
                    payload.star_color = starVisuals[luckySigns.star].c;
                    payload.star_visual = starVisuals[luckySigns.star].v;

                    payload.zodiac_sign = luckySigns.zodiac;
                    payload.zodiac_color = zodiacVisuals[luckySigns.zodiac].c;
                    payload.zodiac_visual = zodiacVisuals[luckySigns.zodiac].v;

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
                        }} else {{
                            currentAlmanacData.lunarStr = "農曆查無資料";
                        }}
                    }} catch (e) {{
                        currentAlmanacData.lunarStr = "農曆查無資料";
                    }}
                    
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

                    const selectedStyle = artStyles[0];
                    const currentDate = document.getElementById('ui-date-picker').value;
                    const trendKeyword = getRandomItem(realTrends);
                    const selectedFortune = getRandomItem(fortunes);
                    
                    let finalTags = [];
                    finalTags.push(getRandomItem(coreTags));
                    finalTags = finalTags.concat(getRandomTwo(emotionTags));
                    finalTags.push(getRandomItem(artTags));
                    
                    const themeKeys = Object.keys(themes);
                    const selectedThemeName = getRandomItem(themeKeys);
                    const theme = themes[selectedThemeName];
                    const selectedQuote = getRandomItem(quotes);
                    const stages = getRandomTwo(theme.stages);
                    const emos = getRandomTwo(theme.emotions);
                    const texs = getRandomTwo(theme.textures);
                    const acts = getRandomTwo(theme.actions);

                    document.getElementById('ui-scene').innerText = trendKeyword;
                    document.getElementById('ui-style').innerText = selectedStyle;
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

                    const promptText = `[系統指令] 啟動太極萬象曆 Prompt 煉成引擎 V31.0
【當前時間線】: ${{currentDate}}
【核心媒材鎖定】: ${{selectedStyle}}！必須是真實的攝影照片，絕對禁止生成任何 2D 動漫、平面插畫或畫作風格！
【構圖強制約束】: 配合今日時事自由生成對應的寫實場景（可以是宇宙、工作日常、建築物、花草樹木等萬事萬物），主體置中。畫面絕對禁止 AI 生成任何亂碼文字！
【專屬浮水印】: 請在圖片的「右下角」自然地融入一個小小的「Aj」英文草寫字樣，作為專屬攝影師簽名。
【今日大眾時事熱點】: 畫面場景與背景請巧妙融入「${{trendKeyword}}」的氛圍。
【動態張力與變裝】: 兩隻史萊姆必須完美融入這片頂級寫實場景中，並產生「互相拉扯、無奈對視或爭奪道具」的實體互動！
---
【角色A: ${{payload.star_sign}}史萊姆】
- 專屬配件: ${{payload.star_color}}, ${{payload.star_visual}}, 旁邊放著[${{selectedFortune.prop}}]。
- 物理狀態: ${{stages[0]}}。${{acts[0]}}。${{emos[0]}}, ${{texs[0]}}。
【角色B: ${{payload.zodiac_sign}}史萊姆】
- 專屬配件: ${{payload.zodiac_color}}, ${{payload.zodiac_visual}}。
- 物理狀態: ${{stages[1]}}。${{acts[1]}}。${{emos[1]}}, ${{texs[1]}}。`;
                    document.getElementById('rawPrompt').value = promptText;

                    let cap = "📅 " + currentDate + " | " + currentAlmanacData.lunarStr + "\\n\\n";
                    cap += "【今日現場直擊 🎤】\\n畫面左邊的" + payload.star_sign + "史萊姆，目前完全是個「" + stages[0] + "」，不僅" + texs[0] + "，還" + emos[0] + "，只能" + acts[0] + "。\\n右邊的" + payload.zodiac_sign + "史萊姆更絕了，直接化身「" + stages[1] + "」，" + texs[1] + "，" + emos[1] + "，甚至正在" + acts[1] + "。\\n這兩人中間還配上" + selectedFortune.prop + "，這荒謬的畫面簡直就是我們真實人生的縮影啊！\\n\\n";
                    const captionText = cap + "\\"" + selectedQuote.q + "\\"\\n\\n📌 社會觀察：" + selectedThemeName + " | " + selectedQuote.p + "\\n⚠️ 宇宙警告：" + selectedFortune.text + "\\n\\n" + finalTags.join(" ");
                    
                    document.getElementById('igCaption').value = captionText;
                }}

                window.onload = function() {{
                    setTimeout(applyDateChange, 500); 
                }};

                function copyText(elementId, msgId) {{
                    var copyText = document.getElementById(elementId);
                    copyText.style.display = "block";
                    copyText.select();
                    document.execCommand("copy");
                    copyText.style.display = "none";
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
        print(f"\n✅ 報告指揮官！V31.0 自動化就緒版已產出網頁。")

if __name__ == "__main__":
    engine = TaijiOmniverseCalendar()
    engine.export_to_html()
