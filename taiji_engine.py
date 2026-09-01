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
        
        # 🧠 【絕對防禦】Python 直接原生演算星座與生肖
        current_star = self.get_star_sign(self.today.month, self.today.day)
        zodiacs = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
        current_zodiac = zodiacs[(self.today.year - 4) % 12]

        self.payload = {
            "date": self.today.strftime("%Y-%m-%d"),
            "star_sign": current_star,
            "star_color": self.star_visuals[current_star]["c"],
            "star_visual": self.star_visuals[current_star]["v"],
            "zodiac_sign": current_zodiac,
            "zodiac_color": self.zodiac_visuals[current_zodiac]["c"],
            "zodiac_visual": self.zodiac_visuals[current_zodiac]["v"],
        }

    def get_star_sign(self, month, day):
        if (month == 1 and day >= 20) or (month == 2 and day <= 18): return "水瓶座"
        if (month == 2 and day >= 19) or (month == 3 and day <= 20): return "雙魚座"
        if (month == 3 and day >= 21) or (month == 4 and day <= 19): return "牡羊座"
        if (month == 4 and day >= 20) or (month == 5 and day <= 20): return "金牛座"
        if (month == 5 and day >= 21) or (month == 6 and day <= 21): return "雙子座"
        if (month == 6 and day >= 22) or (month == 7 and day <= 22): return "巨蟹座"
        if (month == 7 and day >= 23) or (month == 8 and day <= 22): return "獅子座"
        if (month == 8 and day >= 23) or (month == 9 and day <= 22): return "處女座"
        if (month == 9 and day >= 23) or (month == 10 and day <= 23): return "天秤座"
        if (month == 10 and day >= 24) or (month == 11 and day <= 22): return "天蠍座"
        if (month == 11 and day >= 23) or (month == 12 and day <= 21): return "射手座"
        return "摩羯座"

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
        
        # 📸 唯一鎖定最高規格風景照
        self.art_styles = [
            "最高規格「寫實風景照」光學成像參數 (極致寫實、大自然絕美光影、史詩級高山場景)"
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
            try:
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
            except:
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                except:
                    model = genai.GenerativeModel('gemini-1.0-pro')
                    
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
            raw_text = response.text.replace("```json", "").replace("
