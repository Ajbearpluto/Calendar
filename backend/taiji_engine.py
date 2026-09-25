# -*- coding: utf-8 -*-
import os
import sys
import shutil
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
    
    tz = datetime.timezone(datetime.timedelta(hours=8))
    now_dt = datetime.datetime.now(tz)
    today_str = now_dt.strftime('%Y-%m-%d')
    month = now_dt.month
    day = now_dt.day

    print(f"🌌 正在為 {today_str} 啟動【社群時事流行語 × 365天全時空感知引擎】(16重殿堂宇宙版)...")

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
        "梭羅《湖濱散記》逃離文明喧囂，在林中木屋尋求極致簡樸與心靈自足的隱士哲學"
    ]
    
    chosen_styles = random.sample(styles, 12)
    style_lines = "\n".join([f"{i+1}. 宇宙{i+1}：【{s}】" for i, s in enumerate(chosen_styles)])

    prompt = f"""
    你是由「萬相星域」驅動的【TAIJI Omniverse 每日日曆視覺總監與社群時事策展大腦】。
    你融合了約翰·前田的網格秩序、原研哉的留白美學、施德明的視覺衝擊力，並深度汲取市面現象級日曆（《單向曆》、《讀曆書店》、《五金行日曆》、《FEDRIGONI 365》）的精髓。

    今日時空座標：{today_str}

    【🔥 核心演算法：社群時事熱點 × 殿堂日曆美學 (Social Zeitgeist Fusion)】：
    你絕不能產出平庸、過時或老生常談的說教！你必須在思考時，主動感知並結合【今日 ({today_str}) 之真實節氣/星期屬性，以及當前 Threads (脆)、Instagram (IG)、Dcard、社群熱搜話題與當代青年生活型態】：
    1. 【當前社群真實情緒】：
       - 捕捉當代人的生活隱痛與集體情緒：如「深夜脆上的 Emo 碎碎念」、「社畜發瘋生存學（與其內耗自己，不如發瘋外耗別人）」、「I人的社交能量歸零與物理斷網」、「早八人靠冰美式續命」、「IG 限動僅限摯友可見的微型避難所」、「演算法推播的資訊焦慮」、「脫美役與鬆弛感」。
    2. 【當日節慶/節氣/週末或平日精準對應】：
       - 請確認今日是 `{today_str}`！若今日並非中秋節，絕對不要寫中秋節！請根據今日真實的星期、農曆日期、季節物候與社群話題進行創作。

    【🔥 四大殿堂宇宙 · 社群流行反差化分流規則】：
    - 宇宙一：【經典禪意 · 水墨留白】(致敬《單向曆》、《讀曆書店》)
      * 角色：【以禪解梗 · 深層治癒】將社群焦慮、社交疲憊化為宋代水墨與枯山水般的溫柔沉澱與「物理斷網/觀心自由」。
    - 宇宙二：【現代孔版 · 疊印生活】(致敬《五金行日曆》)
      * 角色：【人間煙火 · 黑色幽默】將當紅飲食風潮、社畜自嘲、發瘋文學，化為色彩鮮明的 Risograph 雙色/三色幾何孔版印刷。
    - 宇宙三：【先鋒粗野 · 幾何數據】(致敬《FEDRIGONI 365》)
      * 角色：【先鋒拆解 · 時代批判】將演算法綁架、AI 焦慮、短影音多巴胺成癮，用粗野主義大字與幾何條碼狠狠拆解。
    - 宇宙四：【老派活字 · 直排版畫】(致敬《老派的生活日曆》)
      * 角色：【古今互文 · 荒誕典雅】用古典文言韻味、浮世繪木刻與直排老派書法，幽默反諷當代人滑手機的奇景。

    宇宙五 ~ 宇宙十二：則自由融會以下抽出的風格牌組：
    {style_lines}

    【🔥 嚴格禁令】：
    1. 絕對禁止具象寫實照片 (photorealistic, real photo) 與 3D 渲染 (3D render, octane render)！
    2. 圖像主體 (image_subject) 必須是「純平面藝術設計、水墨、版畫或幾何插圖」的英文描述，不要加相機參數。

    【嚴格 JSON 格式】：
    - 只輸出純 JSON 陣列，包含精準的 12 個物件。不加任何 Markdown 標記或額外解釋。
    [
      {{
        "theme": "四字高雅風格標籤(不可重複)",
        "article": "40~60字的情境散文，強烈展現該宇宙要求的社群情緒解構或生活幽默！",
        "quote": "15~25字的一擊必殺金句（結合社群隱痛與哲學穿透力）。",
        "hashtag": "兩個字流行標籤(如：發瘋、斷網、續命、破框、鬆弛等)",
        "do_action": "四個字或兩個字的宜行動",
        "dont_action": "四個字或兩個字的忌禁忌",
        "image_subject": "純英文，描述平面藝術、水墨、版畫或幾何插圖，不要加相機參數。"
      }}
    ]
    """

    if api_key and api_key != "dummy":
        payload_with_search = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"googleSearch": {}}],
            "generationConfig": { "temperature": 0.95 }
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
                        continue
                    elif e.code == 429:
                        time.sleep(8)
                        continue
                    elif e.code in [503, 500]:
                        time.sleep(4)
                        continue
                    else:
                        break

    print("🛡️ 啟動【日期感知 × 社群流行語殿堂量子庫】，依據當日座標自動輪替宇宙！")
    
    # 🌟 16 組高濃度「社群流行語 × 殿堂藝術」宇宙庫
    daily_pool = [
        {
            "theme": "鬆弛漫遊",
            "article": "週末早晨自然醒，脫下緊繃的社畜外殼，在陽光灑落的窗邊發呆。不為了發 IG 打卡拍照，只為了享受對任何人都『已讀不回』的合法自由。",
            "quote": "允許一切發生，也是允許自己今天徹底廢掉。",
            "hashtag": "鬆弛",
            "do_action": "已讀不回",
            "dont_action": "精神內耗",
            "image_subject": "minimalist Zen sumi-e ink wash painting of gentle morning sunlight and wind stirring wild grasses, vast negative space"
        },
        {
            "theme": "冰美續命",
            "article": "現代人的血液裡流的不是血，是深烘冰美式。冰塊撞擊玻璃杯壁的清脆聲響，是在充滿荒謬的世界裡維持理智與體面的最後一道防線。",
            "quote": "只要咖啡夠冰，生活裡的苦就追不上我。",
            "hashtag": "續命",
            "do_action": "特濃美式",
            "dont_action": "自找苦吃",
            "image_subject": "vibrant two-color Risograph print of a tall iced coffee glass casting geometric halftone shadow on oat paper"
        },
        {
            "theme": "算法突圍",
            "article": "手指機械式在螢幕上無限上滑，多巴胺在十五秒的短影音裡廉價燃燒。今天關掉推播通知，把視線從 6.1 吋的玻璃監獄移向真實的天空。",
            "quote": "別讓演算法的投餵，決定你靈魂的形狀。",
            "hashtag": "破框",
            "do_action": "物理斷網",
            "dont_action": "盲目滑動",
            "image_subject": "neo-brutalist typographic poster of algorithmic grid lines broken by a glowing neon lime geometric vector arrow"
        },
        {
            "theme": "浮世濾鏡",
            "article": "古人臨水照花嘆流年，今人精修九宮格發摯友限動。洗去層層疊加的賽博濾鏡，那些未經排版的凌亂與脆弱，才是一個人最動人的本色。",
            "quote": "萬人限動萬人裝，褪去濾鏡，方見天地真章。",
            "hashtag": "真實",
            "do_action": "素面朝天",
            "dont_action": "精緻偽裝",
            "image_subject": "vintage East Asian woodblock print of pine trees and mountain mist beneath a vermilion red square seal stamp"
        },
        {
            "theme": "社交快充",
            "article": "熱鬧聚會後社交能量徹底歸零，I 人的體面全靠回家反鎖房門那一聲清脆落鎖聲守護。把世界關在門外，在白噪音裡讓靈魂緩慢回血。",
            "quote": "獨處不是孤僻，是靈魂正在進行專屬超快充。",
            "hashtag": "充電",
            "do_action": "閉門謝客",
            "dont_action": "強顏歡笑",
            "image_subject": "minimalist Zen ink line art of a solitary ceramic tea bowl and rising steam in tranquil negative space"
        },
        {
            "theme": "發瘋外耗",
            "article": "與其在深夜棉被裡反覆咀嚼別人的無心之言，不如優雅地翻個白眼。現代生存最高法則：只要我不尷尬，內耗的就是別人。",
            "quote": "與其精神內耗自己，不如發瘋外耗世界。",
            "hashtag": "發瘋",
            "do_action": "優雅發瘋",
            "dont_action": "委曲求全",
            "image_subject": "three-color Risograph print of bold abstract geometric lightning and playful pop shapes, screenprint texture"
        },
        {
            "theme": "數位遊牧",
            "article": "背起筆電把山海當作辦公室，在海浪聲與鍵盤敲擊聲之間尋找平衡。四海為家不是逃避，而是拒絕在同一個格子間裡提早老去的倔強。",
            "quote": "世界那麼遼闊，沒人規定靈魂必須打卡上班。",
            "hashtag": "遊牧",
            "do_action": "說走就走",
            "dont_action": "畫地為牢",
            "image_subject": "Swiss neo-brutalist poster of world latitude longitude coordinates and stark geometric mountain vector"
        },
        {
            "theme": "深夜安全島",
            "article": "凌晨兩點街角亮著燈的超商，微波爐發出叮的一聲。在無人打擾的窗邊嚼著溫熱飯糰，這是夜歸人用銅板價就能買下的整座避風港。",
            "quote": "哪怕世界沉入黑暗，總有一處微光替夜歸人留著門。",
            "hashtag": "避難",
            "do_action": "熱食暖胃",
            "dont_action": "深夜自責",
            "image_subject": "traditional woodblock print of a warm glowing lantern window on a quiet rainy night street"
        },
        {
            "theme": "絕對結界",
            "article": "戴上降噪耳機按下開啟鍵的瞬間，喧囂的車廂與碎語瞬間靜音。在屬於自己的三坪音樂結界裡，連呼吸都重新找回了莊嚴的節奏。",
            "quote": "耳機一戴，世間的紛擾便與我無關。",
            "hashtag": "結界",
            "do_action": "單曲循環",
            "dont_action": "隨波逐流",
            "image_subject": "minimalist sumi-e ink wash of concentric sound ripples in calm water, Japanese wabi-sabi aesthetic"
        },
        {
            "theme": "吉拿療癒",
            "article": "看著金黃麵團在熱油裡翻滾，撒上滿滿肉桂糖粉。在焦慮爆表的日子裡，唯有高熱量的酥脆與甜香，能瞬間撫平所有皺摺的情緒。",
            "quote": "沒有什麼煩惱，是一口剛出爐的熱甜點解決不了的。",
            "hashtag": "療癒",
            "do_action": "大口吃甜",
            "dont_action": "熱量焦慮",
            "image_subject": "warm amber and terracotta Risograph print of golden pastries and cinnamon stars, halftone dots"
        },
        {
            "theme": "星塵尺度",
            "article": "深夜架起腳架仰望南方夜空，銀河以億萬年不變的節奏緩慢旋轉。當你以光年為單位丈量存在，今天讓你崩潰的瑣事不過是一粒微塵。",
            "quote": "在浩瀚的宇宙尺度面前，所有的煩惱都微不足道。",
            "hashtag": "豁達",
            "do_action": "仰望星空",
            "dont_action": "鑽牛角尖",
            "image_subject": "neo-brutalist dithered starfield constellation map with neon acid-lime orbital trajectories on black card"
        },
        {
            "theme": "舊書時空",
            "article": "在二手書店翻開泛黃紙頁，指尖觸碰到幾十年前陌生讀者留下的鉛筆劃線。在快節奏的碎片時代，唯有慢讀能讓兩個孤獨的靈魂跨時空擊掌。",
            "quote": "翻開書頁的剎那，你便擁有了一座隨身攜帶的避難所。",
            "hashtag": "慢讀",
            "do_action": "摩挲紙頁",
            "dont_action": "速食閱讀",
            "image_subject": "antique East Asian woodblock engraving of an open classic book and plum blossom branch on aged paper"
        }
    ]

    # 針對 09-25 中秋當日特調
    mid_autumn_special = [
        {
            "theme": "月魄清輝",
            "article": "捷運早高峰戴上降噪耳機，深夜在脆上靈魂裸奔。今夜月滿無言，最好的情緒避難所不在演算法的推播裡，而在關掉手機、放空呼吸的瞬間。",
            "quote": "在喧囂的動態串裡靈魂裸奔，不如在月光下給自己留一寸留白。",
            "hashtag": "斷網",
            "do_action": "物理斷網",
            "dont_action": "已讀亂回",
            "image_subject": "a minimalist Zen sumi-e ink painting of a single imperfect Enso circle and a suspended ink drop falling into silence"
        },
        {
            "theme": "金禾暮野",
            "article": "老闆畫的餅從不充飢，人間的月亮才算真實。秋分收起一半的光，留給打工人足夠的長夜去煨熱一壺酒，把釘釘和加班徹底拋在腦後。",
            "quote": "與其在連假前夕精神內耗自己，不如在月圓之夜痛快發瘋。",
            "hashtag": "發瘋",
            "do_action": "發瘋外耗",
            "dont_action": "精神內耗",
            "image_subject": "a vibrant three-color Risograph print of a geometric full moon, coffee cup and wheat stalks, tactile halftone dots"
        },
        {
            "theme": "太虛星火",
            "article": "我們仰望的不再是八月十五的星空，而是 6.1 吋發光發熱的像素方塊。所有不能抵達星空的夢想，都淪為了信息繭房裡的廉價滑動。",
            "quote": "所有不能抵達星空的夢想，都淪為了信息繭房裡的廉價滑動。",
            "hashtag": "破框",
            "do_action": "撕裂常規",
            "dont_action": "算法成癮",
            "image_subject": "neo-brutalist typographic poster art of a smartphone screen shattered by a geometric cosmic singularity"
        },
        {
            "theme": "天涯共此",
            "article": "古人對月舉杯寄相思，今人九宮格精修發摯友。風月本無常，何必執著於點讚之數？無人知你行經的風雪，但頭頂始終是同一抹青光。",
            "quote": "千江有水千江月，萬人限動萬人裝。褪去濾鏡，方見天涯本色。",
            "hashtag": "真實",
            "do_action": "手書真言",
            "dont_action": "精緻偽裝",
            "image_subject": "vintage East Asian woodblock print of turbulent sea waves cresting beneath a vermilion red circular moon stamp"
        }
    ]

    if today_str.endswith("09-25"):
        fallback_data = mid_autumn_special + daily_pool
    else:
        # 依據當日日期種子自動輪替，確保每天打開的前四個宇宙皆煥然一新！
        offset = ((month * 31 + day) * 4) % len(daily_pool)
        rotated_pool = daily_pool[offset:] + daily_pool[:offset]
        fallback_data = rotated_pool + mid_autumn_special

    return fallback_data, today_str


def main():
    print("🚀 Taiji Genesis Engine: 啟動【社群時事流行語 × 365天全時空感知引擎】...")
    try:
        quotes_data, today_str = generate_omniverse_data()
        quotes_js_string = json.dumps(quotes_data, ensure_ascii=False)
        print(f"✅ {today_str} 大腦數據備妥，準備寫入皮囊！")
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
    
    # 🗑️ 徹底移除 archive 歷史封存機制，若舊 archive 資料夾存在則自動清理以釋放空間
    if os.path.exists('archive'):
        shutil.rmtree('archive', ignore_errors=True)
        print("🧹 已自動清理舊版 archive 封存資料夾，節省儲存空間！")

    print(f"🎉 今日 ({today_str}) 殿堂級日曆意識已成功寫入 index.html（零歷史垃圾檔案）！")

if __name__ == "__main__":
    main()
