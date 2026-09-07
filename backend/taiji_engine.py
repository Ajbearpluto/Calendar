import os
import json
import datetime
import urllib.request
import urllib.error
import random
import time

def get_available_models(api_key):
    """階段一：不帶任何預設立場，直接向伺服器索取您的金鑰可用的所有模型清單"""
    print("🔍 啟動自動掃雷：正在向 Google 總部查詢可用模型清單...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            # 嚴格篩選出真正支援「文字生成 (generateContent)」的模型
            models = [m['name'] for m in result.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
            if not models:
                raise ValueError("金鑰有效，但未授權任何文字生成模型。")
            print(f"✅ 成功取得 {len(models)} 個候選模型。準備開始測試...")
            return models
    except Exception as e:
        raise ValueError(f"❌ 取得模型清單失敗，請確認金鑰權限: {e}")

def generate_omniverse_data():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ 錯誤：GEMINI_API_KEY 未設定。")
    
    # 取得金鑰專屬的候選名單
    candidate_models = get_available_models(api_key)
    
    tz = datetime.timezone(datetime.timedelta(hours=8))
    today_str = datetime.datetime.now(tz).strftime('%Y-%m-%d')

    print(f"🌌 正在為 {today_str} 進行量子文學創世運算...")

    # 千變萬化的文學資料庫
    styles = [
        "法國名著《小王子》的純真與人生哲理",
        "王小棣導演《魔法阿媽》那種台灣本土的溫暖、遺憾與人情味",
        "《名偵探柯南》般在日常細節中尋找微小真相的推理視角",
        "普契尼歌劇《公主徹夜未眠》那種在深夜裡堅持與盼望的壯麗情感",
        "獨自重裝攀登高海拔百岳（如嘉明湖）時，面對浩瀚大自然的敬畏與內心沉澱",
        "像皮克敏(Pikmin)或史努比(Snoopy)那樣，以幽默可愛的微觀視角看待大人的煩惱",
        "日系雜誌般清新、通透且注重生活微小細節的慢活視角",
        "如同一杯現煮的虹吸式咖啡，在緩慢萃取的等待中體悟時間的禪意"
    ]
    chosen_styles = random.sample(styles, 4)

    prompt = f"""
    你是「太極萬象日曆」的創世神。你的任務是生成 4 段極具「巴納姆效應(Barnum Effect)」的生活散文。
    
    情境與風格分配：
    1. 宇宙一 (都會生存)：請以【{chosen_styles[0]}】的風格來撰寫。
    2. 宇宙二 (慢活細節)：請以【{chosen_styles[1]}】的風格來撰寫。
    3. 宇宙三 (浩瀚自然)：請以【{chosen_styles[2]}】的風格來撰寫。
    4. 宇宙四 (溫暖羈絆)：請以【{chosen_styles[3]}】的風格來撰寫。
    
    【寫作要領】：
    - 內容必須緊扣分配的風格，讓文字有哲理、幽默、或是高山的沉澱感。
    - 必須輸出為純 JSON 陣列，每個物件完全符合以下 6 個 Key 值：
    [
      {{
        "theme": "自訂風格標籤(例如: 星空哲理)",
        "article": "40~60字的情境散文，完美融入指定風格。",
        "quote": "15~25字的一擊必殺金句。",
        "hashtag": "兩個字標籤",
        "do_action": "兩個字的宜行動(如: 仰望)",
        "dont_action": "兩個字的忌禁忌(如: 執著)"
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
    
    raw_text = None
    
    # 階段二：全自動掃雷迴圈。遇到 404 就安靜切換，直到成功為止！
    for model_name in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        print(f"📡 嘗試叩關端點: {model_name} ...")
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                raw_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                print(f"✅ 叩關成功！已確認 {model_name} 為有效端點。")
                break 
        except urllib.error.HTTPError as e:
            if e.code in [404, 403]:
                print(f"⚠️ {model_name} 權限不足或不存在 ({e.code})，自動切換下一組...")
                continue
            elif e.code in [503, 500, 429]:
                print(f"⚠️ 伺服器忙碌 ({e.code})，冷靜 2 秒後切換下一組...")
                time.sleep(2)
                continue
            else:
                print(f"⚠️ 未知錯誤 ({e.code})，跳過此端點...")
                continue
    
    if not raw_text:
        raise ValueError("❌ 慘烈失敗：已耗盡所有候選模型，Google 伺服器全面拒絕連線。")
            
    # 暴力清理 Markdown
    if raw_text.startswith("```json"): raw_text = raw_text[7:]
    elif raw_text.startswith("```"): raw_text = raw_text[3:]
    if raw_text.endswith("```"): raw_text = raw_text[:-3]
    raw_text = raw_text.strip()
    
    try:
        quotes_data = json.loads(raw_text)
        if not isinstance(quotes_data, list) or len(quotes_data) != 4:
            raise ValueError("JSON 結構長度錯誤：必須是 4 個物件的陣列。")
        return quotes_data, today_str
        
    except Exception as e:
        print(f"❌ JSON 解析失敗！原始內容：\n{raw_text}")
        raise e

def main():
    print("🚀 Taiji Genesis Engine: 啟動全自動掃雷版...")
    
    try:
        quotes_data, today_str = generate_omniverse_data()
        quotes_js_string = json.dumps(quotes_data, ensure_ascii=False)
        print("✅ 大腦生成完畢，準備寫入皮囊！")
    except Exception as e:
        raise SystemExit(f"💀 大腦創世失敗，停止注入。錯誤原因: {e}")

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
