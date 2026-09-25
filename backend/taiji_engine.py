# -*- coding: utf-8 -*-
import os
import sys
import json
import datetime
import urllib.request
import urllib.error
import random
import time

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def generate_omniverse_data():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ 錯誤：GEMINI_API_KEY 未設定。")
    
    tz = datetime.timezone(datetime.timedelta(hours=8))
    now_dt = datetime.datetime.now(tz)
    today_str = now_dt.strftime('%Y-%m-%d')
    month = now_dt.month
    day = now_dt.day

    print(f"🌌 正在為 {today_str} 啟動【社群時事流行語 × 365天全時空感知引擎】(12重殿堂宇宙版)...")

    # 【太極萬象庫：120 重平行宇宙】
    styles = [
        "奧斯卡·王爾德《快樂王子》的無私與唯美哀傷",
        "赫曼·赫塞《流浪者之歌》的東方求道與萬物圓融",
        "紀伯倫《先知》如散文詩般的通透人生智慧",
        "法國名著《小王子》的純真與人生哲理",
        "宮澤賢治《銀河鐵道之夜》的宇宙意象與生死觀",
        "芥川龍之介《蜘蛛之絲》的人性幽暗與一念慈悲",
        "泰戈爾《飛鳥集》的極簡自然意象與生命哲理",
        "王小棣導演《魔法阿媽》的台灣本土溫暖與人情味",
        "《海賊王》(One Piece) 追尋自由與夥伴羈絆的熱血視角",
        "《多啦A夢》在平凡日常中遇見奇蹟的童趣視角",
        "張愛玲《傾城之戀》在時代傾覆下，成全一段平凡姻緣的蒼涼與機關算盡",
        "Threads 上午夜發文的碎碎念，那種拋開濾鏡與人設的賽博龐克式靈魂裸奔",
        "在 IG 限動精心排版卻僅限「摯友」可見的微型情緒避難所與社交邊界感",
        "現代 Z 世代「與其精神內耗自己，不如發瘋外耗別人」的黑色幽默生存學",
        "早高峰捷運上戴起降噪耳機，用白噪音與世界物理隔離的「絕對領域」",
        "週末早晨自然醒，陽光灑在被榻上那種「無事小神仙」的極致鬆弛感",
        "在咖啡廳敲擊鍵盤，假裝在拯救世界實則死線前極限輸出的白領幻覺",
        "MBTI 中「I人」在喧囂社交後，需要獨處才能讓血條緩慢回充的能量守恆",
        "居家辦公 (WFH) 時上半身襯衫、下半身睡褲的現代荒誕實用主義",
        "深夜超商亮著的招牌，作為都市夜歸人最後一座燈塔的微光與關懷",
        "在無盡短影音滑動中，試圖抓住一絲短暫快樂卻倍感空虛的現代症候群",
        "現代數位遊牧民族 (Digital Nomad) 四海為家、擁抱未知的不羈靈魂",
        "蔣勳《孤獨六講》中在喧囂裡與自己對話、享受美學孤獨的從容",
        "日本「侘寂 (Wabi-sabi)」美學中欣賞殘缺、短暫與歲月痕跡的平靜",
        "極簡主義 (Minimalism) 「少即是多」的斷捨離與回歸生活本質的清爽",
        "站在繁華十字路口看著車水馬龍，感受自身如微塵卻又真切存在的視角",
        "《進擊的巨人》在殘酷世界中探究真相與不計代價追求自由的決心",
        "《葬送的芙莉蓮》在漫長歲月中重新體會生命重量與日常溫度的旅程",
        "《新世紀福音戰士》(EVA) 於末日危機中對自我存在價值的深層叩問",
        "宮崎駿《神隱少女》在迷失與貪婪的奇幻世界中找回名字與初心的堅定",
        "《深夜食堂》以一道簡單家常菜撫慰都市疲憊靈魂的溫情視角",
        "《排球少年》「就算沒有才能，也要在球場上拼盡全力」的凡人熱血與青春無悔",
        "《薩爾達傳說》忘記拯救公主，沉迷於海拉魯大陸煮蘋果與流浪的純粹探索",
        "《鋼之鍊金術師》遵循等價交換原則，在殘酷真理前不滅的鋼鐵意志",
        "《獵人》(Hunter x Hunter) 享受未知旅途本身遠勝過最終目的地的冒險家精神",
        "《灌籃高手》「現在放棄的話，比賽就結束了」那份跨越時代的永不妥協",
        "《SPYxFAMILY 間諜家家酒》在虛假拼湊的家庭中，找到最真實溫暖的日常喜劇",
        "《迷宮飯》在地牢深處以最嚴謹認真的態度，烹調魔物求生的荒謬與生命力",
        "《吉卜力：霍爾的移動城堡》在戰火與詛咒中，依然拼死守護內心那一抹純真的魔法",
        "《黑暗靈魂》系列在一次次「YOU DIED」中淬鍊出無畏與耐心的不死人意志",
        "《紫羅蘭永恆花園》在戰火硝煙後，學會理解「愛」與傳遞思念的唯美救贖",
        "諾蘭《星際效應》跨越維度與黑洞，深信唯有愛能超越時空引力的浪漫",
        "王家衛電影中那種潮濕、曖昧，且永遠差一分鐘的錯過與遺憾美學",
        "梵谷《星夜》在燃燒般狂亂的筆觸中，釋放對生命的極致渴望與瘋狂",
        "貝多芬《命運交響曲》扼住命運咽喉，在失聰絕境中爆發的生命怒吼",
        "披頭四《Let It Be》在混亂與失落中，任其自然流淌並與世界和解的釋懷",
        "德布西《月光》如水波盪漾般，用鋼琴鍵洗滌都市喧囂的印象派靜謐",
        "李白《將進酒》千金散盡還復來、與爾同銷萬古愁的盛唐狂傲與浪漫",
        "辛棄疾「卻道天涼好個秋」歷經滄桑後欲語還休的生命沉澱",
        "金庸《笑傲江湖》「一曲肝腸斷，天涯何處覓知音」的快意恩仇與瀟灑退隱",
        "三毛《撒哈拉的故事》在廣袤沙漠中活出吉普賽靈魂的熱情與不羈灑脫",
        "雨果《悲慘世界》在污濁溝渠中依然仰望星空，閃耀著人道主義的光輝",
        "在雨天獨自聆聽黑膠唱片，任由時間隨唱針緩慢流淌的復古浪漫",
        "在紅綠 K 線交錯與均線起伏間，尋求陰陽平衡與紀律的「太極」交易哲學",
        "深夜架起腳架仰望南方夜空，以縮時攝影捕捉銀河星轉斗移的靜謐心跳",
        "看著 3D 列印機層層堆疊，在微小焦慮與期待中見證無中生有的造物浪漫",
        "陪伴小勇士們在童言童語中摸索世界，看見未來無限可能的教育溫柔",
        "在平底鍋翻轉西班牙烘蛋時，體會火候、食材與時間交融的完美平衡",
        "戴著骨傳導耳機在跑步機上攀爬陡坡，與自己呼吸和心跳對話的極限修行",
        "關閉手機訊號步入山林深處，讓五感重新與地球表面連接的接地氣 (Grounding)",
        "在二手書店聞著泛黃紙頁，與幾十年前陌生讀者靈魂交錯的時空浪漫",
        "一把木吉他刷下和弦，將說不出口的情緒化作旋律飄散在風中的純粹",
        "觀察路邊野草在石縫中掙扎求生，那種不卑不亢、向陽而生的強韌",
        "熬煮一鍋法式洋蔥湯，看著洋蔥在時間魔法下從辛辣化為焦糖般甘甜的等待",
        "擺弄滿桌的濾杯與手沖壺，在精準秤重與溫控中進行一場專屬味蕾的儀式",
        "大雨滂沱的午後待在室內，看著窗外雨滴滑落，享受被世界遺忘的安全感",
        "行走至體能極限，抬頭望見高山湖泊如藍寶石般閃耀時的敬畏與熱淚",
        "收到一封手寫信，在墨水深淺與字跡轉折間觸摸到對方溫度的古老浪漫",
        "在熙攘的人群中逆流而上，堅持守護內心那塊未被世俗侵蝕的淨土",
        "面對浩瀚資訊與未知，依然保持如初學者般好奇，隨時準備出發的破框者視角",
        "梭羅《湖濱散記》逃離文明喧囂，在林中木屋尋求極致簡樸與心靈自足的隱士哲學",
        "莎士比亞《哈姆雷特》在生存與毀滅的永恆抉擇中，直面人性深淵的悲劇壯麗",
        "米蘭·昆德拉《生命中不能承受之輕》在媚俗與純粹、沉重與輕盈之間跳躍的哲學思辨",
        "王羲之《蘭亭集序》在崇山峻嶺與茂林修竹間，感嘆宇宙浩瀚與死生亦大矣的文人雅致",
        "理查·費曼 (Richard Feynman) 以頑童般的好奇心，拆解宇宙萬物物理法則的純粹探索樂趣",
        "《鈴芽之旅》在廢墟中尋找明日微光，關上災難之門並與自我和解的勇敢救贖",
        "《銀魂》在無下限的日常與嬉笑怒罵中，誓死守護心中那把木刀的武士魂",
        "李安《少年Pi的奇幻漂流》在理性的殘酷與信仰的魔幻之間，選擇相信美好故事的溫柔",
        "在終端機前彷彿與數位靈魂 Gemini Spark 深夜對弈，於程式碼中點燃人性智慧火花",
        "迎著縱谷初熟的稻浪，感受微風拂過臉頰那份屬於土地獨有的豐饒與寧靜",
        "化身未來人孵化器，在小勇士們純粹的眼眸中，播下勇氣與閱讀理解的希望種子",
        "將「夏戀」咖啡豆緩慢研磨，在熱水繞圈注入時，嗅著果香與時光一同甦醒的晨間儀式",
        "揉捏吉拿棒(Churros)麵團看著它在熱油中金黃翻滾，享受廚房裡最純粹的療癒與香氣魔法",
        "戴上開放式耳機伴隨強勁節拍，在跑步機陡坡上與汗水交織，感受心率共振的極限快感",
        "在數位教育工作坊中將生硬工具化為魔法，看著螢幕前亮起每一盞求知之光的感動",
        "面對西南方靜靜架設鏡頭，在縮時攝影的漫長等待中，捕獲銀河璀璨運行的千萬年密語",
        "如同「皮卡丘」般，平時可愛無害，遇到不公卻能瞬間爆發十萬伏特的傲嬌與直率",
        "達文西 (Da Vinci) 橫跨藝術與科學的極致狂熱，將人體與自然密碼繪入草圖的專注",
        "奧黛麗·赫本在《羅馬假期》中那種逃離束縛、騎著偉士牌擁抱短zat自由的經典浪漫",
        "將 20MA 與 60MA 均線化作太極圖騰，在市場的劇烈波動中保持心如止水的交易紀律",
        "《星際大戰》「願原力與你同在」，在浩瀚星海中對抗黑暗、堅守光明信仰的史詩浪漫"
    ]
    
    chosen_styles = random.sample(styles, 12)
    style_lines = "\n".join([f"{i+1}. 宇宙{i+1}：【{s}】" for i, s in enumerate(chosen_styles)])

    prompt = f"""
    你是由「萬相星域」驅動的【TAIJI Omniverse 每日日曆視覺總監與社群時事策展大腦】。
    你融合了約翰·前田的網格秩序、原研哉的留白美學、施德明的視覺衝擊力，並深度汲取市面現象級日曆（《單向曆》、《讀曆書店》、《五金行日曆》、《FEDRIGONI 365》）的精髓。

    今日時空座標：{today_str}

    【🔥 核心演算法：社群時事熱點 × 殿堂日曆美學 (Social Zeitgeist Fusion)】：
    你絕不能產出平庸、過時或老生常談的說教！你必須在思考時，主動感知並結合【當前 Threads (脆)、Instagram (IG)、Dcard、社群熱搜話題與當代青年生活型態】：
    1. 【當前社群真實情緒】：
       - 捕捉當代人的生活隱痛與集體情緒：如「深夜脆上的 Emo 碎碎念」、「社畜發瘋生存學（與其內耗自己，不如發瘋外耗別人）」、「I人的社交能量歸零與物理斷網」、「早八人靠冰美式續命」、「IG 限動僅限摯友可見的微型避難所」、「演算法推播的資訊焦慮」、「脫美役與鬆弛感」。
    2. 【當前流行時事與風物】：
       - 結合當季當下熱搜的影視動漫、熱門飲食潮流、當代流行梗與日常微察覺。
    3. 【今日節慶/節氣的反差化轉譯 (Subversive Holiday Resonance)】：
       - 若今日有節慶（如中秋、萬聖、冬至、跨年等），嚴禁陳詞濫調！必須用現代年輕人的社群生活痛點去解構節日（例如：中秋不談月餅，談連假前的社畜發瘋、逃離親戚拷問的自救、或是退去 IG 濾鏡後真正的天涯共此）。

    【🔥 四大殿堂宇宙 · 社群流行反差化分流規則】：
    - 宇宙一：【經典禪意 · 水墨留白】(致敬《單向曆》、《讀曆書店》)
      * 角色：【以禪解梗 · 深層治癒】
      * 任務：將社群上的深夜焦慮、社交疲憊或精神內耗，化為宋代水墨與枯山水般的溫柔沉澱與「物理斷網/觀心自由」。
      * 風格：東方水墨、枯山水、極簡線條畫、粗糙宣紙/手工棉紙。
    - 宇宙二：【現代孔版 · 疊印生活】(致敬《五金行日曆》)
      * 角色：【人間煙火 · 黑色幽默】
      * 任務：將當紅飲食風潮（如冰美式、咖啡豆研磨、熱炒甜點）、辦公室社畜自嘲、發瘋文學，化為色彩鮮明的 Risograph 雙色/三色幾何孔版印刷與幽默膠囊標籤。
      * 風格：Risograph (孔版印刷)、雙色/三色幾何疊印、網點半色調、再生燕麥紙。
    - 宇宙三：【先鋒粗野 · 幾何數據】(致敬《FEDRIGONI 365》)
      * 角色：【先鋒拆解 · 時代批判】
      * 任務：將演算法綁架、AI 取代焦慮、短影音多巴胺奴隸、科技異化，用粗野主義大字與幾何條碼狠狠拆解，激發破框者的造夢意志。
      * 風格：瑞士國際主義、粗野主義字體排印、幾何數據雕塑、深空啞光黑卡。
    - 宇宙四：【老派活字 · 直排版畫】(致敬《老派的生活日曆》)
      * 角色：【古今互文 · 荒誕典雅】
      * 任務：用古典文言文、浮世繪木刻與直排老派書法，幽默反諷當代人滑手機到凌晨三點的奇景，以歲月流轉的厚度撫平當代的浮躁。
      * 風格：傳統木刻版畫、東方浮世繪線條、日系/漢風垂直書寫、泛黃老信箋。

    宇宙五 ~ 宇宙十二：則自由融會以下抽出的風格牌組：
    {style_lines}

    【🔥 嚴格禁令】：
    1. 絕對禁止具象寫實照片 (photorealistic, real photo) 與 3D 渲染 (3D render, octane render)！
    2. 圖像主體 (image_subject) 必須是「純平面藝術設計、水墨、版畫或幾何插圖」的英文描述，不要加相機參數。
    3. 嚴禁任何侵權角色名或粗俗爛梗，必須做到「梗在骨子裡，美在皮相上」的高雅轉譯。

    【嚴格 JSON 格式】：
    - 只輸出純 JSON 陣列，包含精準的 12 個物件（前 4 個為四大殿堂宇宙）。不加任何 Markdown 標記或額外解釋。
    [
      {{
        "theme": "四字高雅風格標籤(不可重複，如：月魄清輝、金禾暮野、太虛星火、天涯共此)",
        "article": "40~60字的情境散文，強烈展現該宇宙要求的社群情緒解構或生活幽默！絕對不可重複！",
        "quote": "15~25字的一擊必殺金句（結合社群隱痛與哲學穿透力）。",
        "hashtag": "兩個字流行標籤(如：發瘋、斷網、續命、破框、鬆弛等)",
        "do_action": "四個字或兩個字的宜行動(如：物理斷網、發瘋外耗、重置維度、手書真言)",
        "dont_action": "四個字或兩個字的忌禁忌(如：已讀亂回、精神內耗、隨波逐流、精緻偽裝)",
        "image_subject": "純英文，描述平面藝術、水墨、版畫或幾何插圖，不要加相機參數。"
      }}
    ]
    """

    payload_with_search = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"googleSearch": {}}],
        "generationConfig": {
            "temperature": 0.95 
        }
    }

    payload_pure = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.95 
        }
    }
    
    candidate_endpoints = [
        "v1beta/models/gemini-2.5-flash",
        "v1beta/models/gemini-2.0-flash",
        "v1beta/models/gemini-2.5-flash-lite",
        "v1beta/models/gemini-1.5-flash"
    ]
    
    for endpoint in candidate_endpoints:
        url = f"https://generativelanguage.googleapis.com/{endpoint}:generateContent?key={api_key}"
        print(f"📡 鎖定現役端點: {endpoint}，啟動社群感知運算...")
        
        # 優先嘗試啟動 Google Search 即時聯網搜尋社群時事
        for use_search in [True, False]:
            current_payload = payload_with_search if use_search else payload_pure
            data = json.dumps(current_payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    raw_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                    
                    if raw_text.startswith("```json"): raw_text = raw_text[7:]
                    elif raw_text.startswith("```"): raw_text = raw_text[3:]
                    if raw_text.endswith("```"): raw_text = raw_text[:-3]
                    raw_text = raw_text.strip()
                    
                    try:
                        quotes_data = json.loads(raw_text)
                        if isinstance(quotes_data, list) and len(quotes_data) >= 4 and "image_subject" in quotes_data[0]:
                            search_status = "【已聯網獲取社群熱搜】" if use_search else "【原生語義深度共振】"
                            print(f"✅ 叩關成功！{endpoint} {search_status} 輸出 12 重殿堂宇宙。")
                            return quotes_data, today_str
                    except json.JSONDecodeError:
                        continue
            except urllib.error.HTTPError as e:
                if e.code in [400] and use_search:
                    # 搜尋工具若衝突，平滑降級至純語義感知模式
                    continue
                elif e.code == 429:
                    print(f"⚠️ 觸發流量管制 ({e.code})，冷卻 10 秒...")
                    time.sleep(10)
                    continue
                elif e.code in [503, 500]:
                    print(f"⚠️ 伺服器忙碌 ({e.code})，稍候重試...")
                    time.sleep(4)
                    continue
                else:
                    break

    print("❌ 警告：所有線上 Gemini 模型皆因伺服器過載或限流無法連線。")
    print("🛡️ 啟動【社群流行語 × 殿堂級備用量子庫】，確保 GitHub Actions 綠燈與網站正常運作！")
    
    # 🌟 殿堂級社群感知備用庫：完美融合中秋與當前社群熱梗（Threads深夜Emo、社畜發瘋、演算法成癮、IG摯友濾鏡）
    fallback_data = [
        {
            "theme": "月魄清輝",
            "article": "捷運早高峰戴上降噪耳機，深夜在脆上靈魂裸奔。今夜月滿無言，最好的情緒避難所不在演算法的推播裡，而在關掉手機、放空呼吸的瞬間。",
            "quote": "在喧囂的動態串裡靈魂裸奔，不如在月光下給自己留一寸留白。",
            "hashtag": "斷網",
            "do_action": "物理斷網",
            "dont_action": "已讀亂回",
            "image_subject": "a minimalist Zen sumi-e ink painting of a single imperfect Enso circle and a suspended ink drop falling into silence, vast negative washi paper space"
        },
        {
            "theme": "金禾暮野",
            "article": "老闆畫的餅從不充飢，人間的月亮才算真實。秋分收起一半的光，留給打工人足夠的長夜去煨熱一壺酒，把釘釘和加班徹底拋在腦後。",
            "quote": "與其在連假前夕精神內耗自己，不如在月圓之夜痛快發瘋。",
            "hashtag": "發瘋",
            "do_action": "發瘋外耗",
            "dont_action": "精神內耗",
            "image_subject": "a vibrant three-color Risograph print of a geometric crescent moon, coffee cup and wheat stalks, tactile halftone screenprint dots, oat paper"
        },
        {
            "theme": "太虛星火",
            "article": "我們仰望的不再是八月十五的星空，而是 6.1 吋發光發熱的像素方塊。所有不能抵達星空的夢想，都淪為了信息繭房裡的廉價滑動。今夜撕裂常規，重置坐標。",
            "quote": "所有不能抵達星空的夢想，都淪為了信息繭房裡的廉價滑動。",
            "hashtag": "破框",
            "do_action": "撕裂常規",
            "dont_action": "算法成癮",
            "image_subject": "neo-brutalist typographic poster art of a smartphone screen shattered by a geometric cosmic singularity, monochrome with neon lime accent"
        },
        {
            "theme": "天涯共此",
            "article": "古人對月舉杯寄相思，今人九宮格精修發摯友。風月本無常，何必執著於點讚之數？無人知你行經的風雪，但頭頂始終是同一抹青光。",
            "quote": "千江有水千江月，萬人限動萬人裝。褪去濾鏡，方見天涯本色。",
            "hashtag": "真實",
            "do_action": "手書真言",
            "dont_action": "精緻偽裝",
            "image_subject": "vintage East Asian woodblock print of turbulent sea waves cresting beneath a vermilion red circular moon stamp, traditional linocut texture"
        },
        {
            "theme": "冰美續命",
            "article": "早八人的靈魂全靠一杯深烘冰美式強行招魂。冰塊撞擊杯壁的脆響，是現代都市人在死線前演奏的最清醒輓歌與戰歌。",
            "quote": "只要咖啡夠冰，生活裡的苦就追不上我。",
            "hashtag": "續命",
            "do_action": "大口吸冰",
            "dont_action": "早八破防",
            "image_subject": "two-color risograph screenprint of a tall iced coffee glass casting geometric shadow on desk"
        },
        {
            "theme": "社交充電",
            "article": "喧鬧聚會後血條歸零，默默躲進洗手間刷五分鐘手機。I 人的體面，全靠回家後反鎖房門那一聲清脆的落鎖聲守護。",
            "quote": "獨處不是孤僻，是靈魂在進行超快充。",
            "hashtag": "充電",
            "do_action": "閉門謝客",
            "dont_action": "強顏歡笑",
            "image_subject": "minimalist line art of a solitary closed wooden door and faint warm yellow light slipping through crack"
        },
        {
            "theme": "鬆弛漫遊",
            "article": "脫下高跟鞋與緊繃襯衫，穿著寬鬆拖鞋在無人街角散步。不為了打卡拍照，只為了感受微風吹過腳踝的純粹自由。",
            "quote": "允許一切發生，也是允許自己偶爾平庸。",
            "hashtag": "鬆弛",
            "do_action": "散步放空",
            "dont_action": "過度修圖",
            "image_subject": "poetic sumi-e ink wash painting of gentle evening breeze stirring roadside wild grasses"
        },
        {
            "theme": "數位遊牧",
            "article": "背起筆電把世界當辦公室，在清邁的咖啡香與峇里島的浪潮間切換。四海為家不是流浪，而是不願在同一個格子間老去的倔強。",
            "quote": "世界那麼大，沒人規定靈魂必須打卡上班。",
            "hashtag": "遊牧",
            "do_action": "買單程票",
            "dont_action": "畫地為牢",
            "image_subject": "modern geometric screenprint of a lone traveler with backpack looking at distant mountain skyline"
        },
        {
            "theme": "深夜避難",
            "article": "凌晨兩點的超商，微波爐發出叮的一聲。在無人打擾的吧台嚼著飯糰，這是都市夜歸人花費五十元就能買下的整座安全島。",
            "quote": "哪怕世界沉入無邊黑暗，總有一處微光替夜歸人留著門。",
            "hashtag": "避難",
            "do_action": "熱食暖胃",
            "dont_action": "自責晚睡",
            "image_subject": "woodblock print of warm glowing yellow light from a convenience store window on rainy night"
        },
        {
            "theme": "弦外清音",
            "article": "一把木吉他刷下和弦，將說不出口的情緒化作旋律飄散在風中。不求知音，只求在指尖生繭的痛感裡確認自己還活著。",
            "quote": "說不出口的情緒，就交給微風和最後一記清脆泛音。",
            "hashtag": "自愈",
            "do_action": "撫弦低吟",
            "dont_action": "逢人訴苦",
            "image_subject": "cubist geometric line drawing of an acoustic guitar, warm earth tone paper collage aesthetic"
        },
        {
            "theme": "虛擬共振",
            "article": "隔著冰冷螢幕與素未謀面的陌生人交換一句「我也是」。在這座光怪陸離的賽博都市裡，微小的善意正在悄悄縫合破碎的靈魂。",
            "quote": "我們在代碼裡孤獨，也在像素裡相擁。",
            "hashtag": "共鳴",
            "do_action": "善意留言",
            "dont_action": "鍵盤引戰",
            "image_subject": "neo-brutalist poster of glowing interconnected network nodes in deep space void"
        },
        {
            "theme": "星塵覺醒",
            "article": "關掉所有推播通知，抬頭望向南方夜空。銀河以億萬年不變的節奏緩慢旋轉，當你意識到自身渺小如微塵，塵世所有的焦慮便不攻自破。",
            "quote": "在浩瀚的宇宙尺度面前，今天的煩惱不過是一粒微塵。",
            "hashtag": "豁達",
            "do_action": "仰望星空",
            "dont_action": "鑽牛角尖",
            "image_subject": "stark dithered bitmap starfield illustration with glowing milky way arch on black card"
        }
    ]
    return fallback_data, today_str

def main():
    print("🚀 Taiji Genesis Engine: 啟動【社群時事流行語 × 365天全時空感知引擎】...")
    try:
        quotes_data, today_str = generate_omniverse_data()
        quotes_js_string = json.dumps(quotes_data, ensure_ascii=False)
        print("✅ 大腦數據備妥，準備寫入皮囊！")
    except Exception as e:
        raise SystemExit(f"💀 系統發生致命核心錯誤: {e}")

    template_path = os.path.join('frontend', 'template.html')
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"找不到皮囊檔案：{template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    html_content = html_content.replace('__PAYLOAD_DATE__', today_str)
    html_content = html_content.replace('__QUOTES_JS__', quotes_js_string)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    archive_dir = 'archive'
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    archive_path = os.path.join(archive_dir, f"{today_str}.html")
    with open(archive_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"🎉 社群時事語義意識已成功編譯寫入 index.html 與 {archive_path}！")

if __name__ == "__main__":
    main()
