import os
import json
import datetime
import urllib.request
import urllib.error
import random
import time

def get_available_models(api_key):
    """階段一：向伺服器索取模型清單，並強制過濾掉不聽話的 Gemma 模型"""
    print("🔍 [系統檢視] 正在向 Google 總部獲取 Gemini 模型清單...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            # 嚴格篩選：必須支援文字生成，且名稱必須包含 'gemini' (排除 gemma)
            models = [
                m['name'] for m in result.get('models', []) 
                if 'generateContent' in m.get('supportedGenerationMethods', [])
                and 'gemini' in m['name'].lower()
            ]
            if not models:
                raise ValueError("金鑰有效，但未授權任何 Gemini 文字生成模型。")
            print(f"✅ 成功取得 {len(models)} 個純血 Gemini 候選模型。")
            return models
    except Exception as e:
        raise ValueError(f"❌ 取得模型清單失敗: {e}")

def generate_omniverse_data():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ 錯誤：GEMINI_API_KEY 未設定。")
    
    candidate_models = get_available_models(api_key)
    
    tz = datetime.timezone(datetime.timedelta(hours=8))
    today_str = datetime.datetime.now(tz).strftime('%Y-%m-%d')

    print(f"🌌 正在為 {today_str} 進行量子文學創世運算...")

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
    
    【極度重要：嚴格 JSON 格式】：
    - 絕對不要輸出任何解釋、思考過程或 Markdown 標記以外的文字。
    - 必須輸出為純 JSON 陣列，包含精準的 4 個物件，每個物件 6 個 Key：
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
            "temperature": 0.8
        }
    }
    data = json.dumps(payload).encode('utf-8')
    
    # 階段二：內容防彈驗證迴圈
    for model_name in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        print(f"📡 嘗試叩關端點: {model_name} ...")
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                raw_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                
                # 暴力清理 Markdown
                if raw_text.startswith("```json"): raw_text = raw_text[7:]
                elif raw_text.startswith("```"): raw_text = raw_text[3:]
                if raw_text.endswith("```"): raw_text = raw_text[:-3]
                raw_text = raw_text.strip()
                
                # 【防彈機制】：立刻嘗試解析 JSON，確認產出是否合法
                try:
                    quotes_data = json.loads(raw_text)
                    if isinstance(quotes_data, list) and len(quotes_data) == 4 and "theme" in quotes_data[0]:
                        print(f"✅ 叩關成功！{model_name} 輸出完美 JSON 格式。")
                        return quotes_data, today_str
                    else:
                        print(f"⚠️ {model_name} 輸出結構錯誤 (長度不符)，捨棄並切換下一組...")
                        continue
                except json.JSONDecodeError:
                    print(f"⚠️ {model_name} 未遵守 JSON 格式規定 (出現雜訊)，捨棄並切換下一組...")
                    continue
                    
        except urllib.error.HTTPError as e:
            if e.code in [404, 403]:
                print(f"⚠️ {model_name} 權限不足或不存在 ({e.code})，切換下一組...")
            elif e.code in [503, 500, 429]:
                print(f"⚠️ {model_name} 伺服器忙碌 ({e.code})，冷靜 2 秒後切換下一組...")
                time.sleep(2)
            else:
                print(f"⚠️ {model_name} 未知錯誤 ({e.code})，跳過此端點...")
            continue
    
    raise ValueError("❌ 慘烈失敗：已耗盡所有 Gemini 候選模型，皆無法產出合法 JSON。")

def main():
    print("🚀 Taiji Genesis Engine: 啟動防彈驗證版...")
    
    try:
        quotes_data, today_str = generate_omniverse_data()
        quotes_js_string = json.dumps(quotes_data, ensure_ascii=False)
        print("✅ 嚴格檢驗通過，準備寫入皮囊！")
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
