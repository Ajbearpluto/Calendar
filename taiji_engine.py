import os
import json
import datetime

def main():
    print("🌌 Taiji Engine V2: 啟動平行宇宙渲染與時光機備份...")

    # 1. 取得台灣時間的今日日期 (確保跨日時區正確)
    tz = datetime.timezone(datetime.timedelta(hours=8))
    now = datetime.datetime.now(tz)
    today_str = now.strftime('%Y-%m-%d')
    archive_filename = f"{today_str}.html"

    # =====================================================================
    # 🤖 [保留您的 AI 生成邏輯] 
    # 這裡請替換成您原本呼叫 Gemini 或其他 AI 產生 __QUOTES_JS__ 的邏輯
    # =====================================================================
    print(f"正在為 {today_str} 生成宇宙碎片...")
    
    # 假資料範例 (請替換為您實際的 AI 產出結果)
    ai_generated_quotes = [
        {
            "style": "微小幸運",
            "article": f"【{today_str} 日常碎片】\n今天的雲層很厚，但在下班那一刻，剛好漏出了一道光。",
            "q": "宇宙正在偷偷塞給你小確幸，接住它！",
            "p": "日常觀察",
            "do": "買彩券",
            "dont": "過度思考"
        }
    ]
    
    # 將 AI 生成的字典轉換為 JSON 字串，準備注入 HTML
    quotes_js_string = json.dumps(ai_generated_quotes, ensure_ascii=False)
    # =====================================================================

    # 2. 讀取前端母版 (路徑已變更為 frontend/template.html)
    # 確保 GitHub Actions 執行時抓得到正確的相對路徑
    template_path = os.path.join('frontend', 'template.html')
    
    if not os.path.exists(template_path):
        print(f"❌ 嚴重錯誤：找不到母版檔案 {template_path}！請確認資料夾結構。")
        return

    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 3. 注入靈魂 (替換日期與 JSON 資料)
    html_content = html_content.replace('__PAYLOAD_DATE__', today_str)
    html_content = html_content.replace('__QUOTES_JS__', quotes_js_string)

    # 4. 寫入根目錄的 index.html (今日的首頁門面)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ index.html 已成功更新！(今日門面)")

    # 5. 啟動時光機！寫入 archive/YYYY-MM-DD.html (歷史備份)
    archive_dir = 'archive'
    # 如果 archive 資料夾不存在，系統會自動建立一個
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print("📁 首次建立 archive 時光機資料夾")
        
    archive_path = os.path.join(archive_dir, archive_filename)
    with open(archive_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ 歷史備份已安全封存：{archive_path}")

    print("🚀 宇宙渲染完畢，準備推送到 GitHub Pages！")

if __name__ == "__main__":
    main()
