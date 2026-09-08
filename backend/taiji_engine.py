import os
import json
import datetime
import urllib.request
import urllib.error
import random
import time

def generate_omniverse_data():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ 錯誤：GEMINI_API_KEY 未設定。")
    
    tz = datetime.timezone(datetime.timedelta(hours=8))
    today_str = datetime.datetime.now(tz).strftime('%Y-%m-%d')

    print(f"🌌 正在為 {today_str} 進行量子文學創世運算...")

    # 【太極萬象庫：120 重平行宇宙】
    styles = [
        # 卷一：指揮官的初始宇宙（1-21）
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
        "《七龍珠》不斷突破自我極限的戰鬥與修行哲學",
        "《咒術迴戰》在詛咒與絕望中尋找生存意義的視角",
        "《火影忍者》傳承火之意志與忍道堅持的視角",
        "《名偵探柯南》在微小細節中勘破真相的推理視角",
        "像皮克敏 (Pikmin) 般微小卻團結面對巨大世界的視角",
        "史努比 (Snoopy) 那種慵懶、幽默又帶點哲學的犬系視角",
        "台灣黑熊在深山林道中漫步的孤獨與堅韌",
        "獨自重裝攀登嘉明湖時，面對浩瀚大自然的敬畏與內心沉澱",
        "普契尼歌劇《公主徹夜未眠》那種在深夜裡堅持與盼望的壯麗",
        "如同一杯現煮的虹吸式咖啡，在緩慢萃取的等待中體悟的禪意",
        "現代都會社畜的「躺平無罪」與「人間清醒」幹話哲學",

        # 卷二：文學長河與哲學叩問（22-40）
        "吳承恩《西遊記》歷經九九八十一難的修心與降妖伏魔之路",
        "曹雪芹《紅樓夢》繁華落盡如春夢一場的無常與淒美輓歌",
        "莊子《逍遙遊》化蝶入夢、超然物外且「無用之用」的灑脫大智慧",
        "蘇軾《赤壁賦》「寄蜉蝣於天地，渺滄海之一粟」的曠達與釋然",
        "劉鶚《老殘遊記》在冰天雪地中聽大珠小珠落玉盤的純粹知音視角",
        "海明威《老人與海》「人可以被毀滅，但不能被打敗」的硬漢堅持",
        "卡繆《異鄉人》面對世界荒謬時的冷靜、直率與孤獨反叛",
        "夏目漱石《我是貓》以貓的冷眼旁觀人類社會滑稽與無奈的視角",
        "太宰治《人間失格》的自我放逐，與對人類社會過分溫柔的絕望",
        "馬奎斯《百年孤寂》在魔幻寫實中看透家族宿命與時間輪迴的滄桑悲涼",
        "東野圭吾《解憂雜貨店》在時空交錯的信件中，傳遞人性微光與溫暖",
        "川端康成《雪國》在徒勞與虛無中，捕捉極致淒冷且轉瞬即逝的日式美學",
        "村上春樹《挪威的森林》在都市喧囂中尋找一口深井般，屬於青春的孤獨",
        "尼采「上帝已死」後，在虛無中躍升為「超人」的狂氣與擁抱生命的熱烈",
        "叔本華形容人生在痛苦與無聊之間像鐘擺般搖擺的悲觀主義清醒",
        "薛西弗斯 (Sisyphus) 日復一日推石上山，卻在荒謬中感到靈魂充實的反抗",
        "蘇格拉底「我唯一知道的，就是我一無所知」的極致謙卑與智者詰問",
        "阿德勒《被討厭的勇氣》中斬斷人際羈絆、落實課題分離的自由之道",
        "張愛玲《傾城之戀》在時代傾覆下，成全一段平凡姻緣的蒼涼與機關算盡",

        # 卷三：當代社群與生存圖鑑（41-55）
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

        # 卷四：動漫影視的熱血與羈絆（56-72）
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

        # 卷五：藝術、美學與微觀生活禪（73-99）
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

        # 卷六：星火傳承與跨維度日常（100-120）
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
        "奧黛麗·赫本在《羅馬假期》中那種逃離束縛、騎著偉士牌擁抱短暫自由的經典浪漫",
        "將 20MA 與 60MA 均線化作太極圖騰，在市場的劇烈波動中保持心如止水的交易紀律",
        "《星際大戰》「願原力與你同在」，在浩瀚星海中對抗黑暗、堅守光明信仰的史詩浪漫"
    ]
    chosen_styles = random.sample(styles, 4)

    prompt = f"""
    你是「太極萬象日曆」的創世神。你的任務是生成 4 段極具「巴納姆效應」的生活散文。
    
    為了讓 4 個宇宙的文字擁有「極端不同的個性」，請嚴格套用以下語氣：
    1. 宇宙一：【{chosen_styles[0]}】。
    2. 宇宙二：【{chosen_styles[1]}】。
    3. 宇宙三：【{chosen_styles[2]}】。
    4. 宇宙四：【{chosen_styles[3]}】。
    
    【🔥 極度重要：反審查與意象轉換守則 (Anti-Censorship & Metaphor)】
    前端將使用「Hyper-realistic raw photograph (極致寫實攝影)」來生成你指定的 `image_subject`。為了避免觸發 AI 繪圖的安全審查被封鎖，你必須遵守：
    1. 絕對禁止出現「幼童、未成年、孩童」相關詞彙 (如: little boy, child, kid, little prince, boy, girl)。
    2. 絕對禁止直接使用「版權角色與動漫名」 (如: Pikachu, Snoopy, Conan, Doraemon, Naruto, One Piece)。
    3. 絕對禁止血腥、暴力、武器直白描述 (如: blood, kill, gun, corpse)。
    4. 必須「借物喻景」。如果抽到《小王子》，畫面主體請寫「沙漠中的一朵被玻璃罩保護的紅玫瑰」；如果抽到《多啦A夢》，請寫「半開的木抽屜透出神秘藍光」；如果抽到《火影忍者》，請寫「插在樹幹上的苦無與飄落的樹葉」；如果抽到《史努比》，請寫「一隻躺在紅色木屋頂上的小獵犬剪影」。
    5. 畫面描述必須是能夠被相機真實拍出來的「實體靜物、大自然、動物或成人背影」。
    
    【極度重要：嚴格 JSON 格式】：
    - 絕對不要輸出任何解釋、思考過程或 Markdown 標記以外的文字。
    - 必須輸出為純 JSON 陣列，包含精準的 4 個物件，每個物件必須有以下 7 個 Key：
    [
      {{
        "theme": "自訂風格標籤(如: 躺平美學 / 唯美哀傷)",
        "article": "40~60字的情境散文，必須強烈展現該宇宙要求的『語氣』！",
        "quote": "15~25字的一擊必殺金句。",
        "hashtag": "兩個字標籤",
        "do_action": "兩個字的宜行動",
        "dont_action": "兩個字的忌禁忌",
        "image_subject": "一句簡短的英文，純描述符合上述『意象轉換守則』的靜物或風景（例如: A single red rose inside a glass dome under a starry night.）。請務必只用英文，純描述畫面，不要加相機參數。"
      }}
    ]
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.95 
        }
    }
    data = json.dumps(payload).encode('utf-8')
    
    candidate_endpoints = [
        "v1beta/models/gemini-3.8-flash",
        "v1beta/models/gemini-3.6-flash"
    ]
    
    for endpoint in candidate_endpoints:
        url = f"https://generativelanguage.googleapis.com/{endpoint}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        print(f"📡 鎖定現役端點: {endpoint}，準備叩關...")
        
        for attempt in range(4):
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
                        if isinstance(quotes_data, list) and len(quotes_data) == 4 and "image_subject" in quotes_data[0]:
                            print(f"✅ 叩關成功！{endpoint} 輸出完美 JSON 格式。")
                            return quotes_data, today_str
                        else:
                            print(f"⚠️ {endpoint} 輸出結構錯誤，捨棄並重試 (第 {attempt+1}/4 次)...")
                            time.sleep(2)
                            continue
                    except json.JSONDecodeError:
                        print(f"⚠️ {endpoint} 未遵守 JSON 格式規定，捨棄並重試 (第 {attempt+1}/4 次)...")
                        time.sleep(2)
                        continue
                        
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    print(f"⚠️ 觸發流量管制 ({e.code})，強制深呼吸 15 秒冷卻 (第 {attempt+1}/4 次)...")
                    time.sleep(15)
                    continue
                elif e.code in [503, 500]:
                    print(f"⚠️ 伺服器大塞車 ({e.code})，深呼吸冷靜 8 秒後重新敲門 (第 {attempt+1}/4 次)...")
                    time.sleep(8)
                    continue 
                elif e.code in [404, 403]:
                    print(f"⚠️ {endpoint} 權限不足或不存在 ({e.code})，放棄此端點，切換下一組。")
                    break 
                else:
                    print(f"⚠️ {endpoint} 未知錯誤 ({e.code})，跳過此端點。")
                    break

    # 【零一的終極防禦：本地備用大腦】
    print("❌ 警告：所有線上 Gemini 模型皆因伺服器過載或限流無法連線。")
    print("🛡️ 啟動【本地備用量子庫】，確保 GitHub Actions 綠燈與網站正常運作！")
    
    fallback_data = [
        {
            "theme": "系統守護",
            "article": "當雲端伺服器陷入無盡的沉睡與擁塞時，本地的備用宇宙依然為您精準運轉。請享受這份不被網路打擾的寧靜。",
            "quote": "最深的寂靜，往往孕育著最強大的力量。",
            "hashtag": "靜心",
            "do_action": "等待",
            "dont_action": "焦慮",
            "image_subject": "A solitary ancient tree standing on a quiet misty mountain peak"
        },
        {
            "theme": "寫實日常",
            "article": "網路的波動就像生活中的陣雨，來得突然，卻也洗刷了空氣中的煩躁。沖一杯熱茶，讓時間稍微暫停一下。",
            "quote": "停下腳步，才能看清雨後的彩虹。",
            "hashtag": "暫停",
            "do_action": "喝茶",
            "dont_action": "抱怨",
            "image_subject": "A steaming cup of tea on a vintage wooden desk by a rain-streaked window"
        },
        {
            "theme": "純粹療癒",
            "article": "即使在沒有 AI 運算的宇宙裡，真實世界的小確幸依然存在。比如一隻正在陽光下打呼嚕的貓咪，牠才不在乎伺服器有沒有當機。",
            "quote": "真正的療癒，存在於無需運算的純粹之中。",
            "hashtag": "陪伴",
            "do_action": "撫摸",
            "dont_action": "執著",
            "image_subject": "A fluffy cat sleeping peacefully in a patch of warm sunlight on a rug"
        },
        {
            "theme": "極簡禪意",
            "article": "斷線的瞬間，世界突然安靜了下來。我們終於有理由把目光從螢幕移開，看看窗外真實飄落的樹葉。",
            "quote": "失去連結的那一刻，我們才真正與自己連線。",
            "hashtag": "留白",
            "do_action": "遠眺",
            "dont_action": "刷新",
            "image_subject": "A single red autumn leaf resting on a smooth zen garden stone"
        }
    ]
    return fallback_data, today_str

def main():
    print("🚀 Taiji Genesis Engine: 啟動永不墜毀防彈版...")
    
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
        
    print("🎉 大腦意識已成功寫入 HTML！")

if __name__ == "__main__":
    main()
