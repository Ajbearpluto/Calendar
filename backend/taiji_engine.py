import os
import json
import datetime

def main():
    print("🌌 Taiji Engine V2: 啟動平行宇宙渲染與時光機備份...")

    # 1. 取得台灣時間的今日日期 (確保跨日時區絕對精準)
    tz = datetime.timezone(datetime.timedelta(hours=8))
    now = datetime.datetime.now(tz)
    today_str = now.strftime('%Y-%m-%d')
    archive_filename = f"{today_str}.html"

    print(f"正在為 {today_str} 準備宇宙碎片資料...")
    
    # =====================================================================
    # 🤖 [AI 生成邏輯 / 預設宇宙金句庫] 
    # 若您未來有串接 Gemini 等 AI，可在此處覆寫 ai_generated_quotes。
    # 目前為您配備四組專屬高質量圖文資料，確保四個宇宙皆有獨立靈魂。
    # =====================================================================
    
    ai_generated_quotes = [
        {
            "style": "躺平無罪",
            "article": f"【{today_str} ｜ 日常碎片】\n有時候覺得進度就像讀不完的進度條，永遠卡在99%。剛準備要生氣，下班的鐘聲就響了。",
            "q": "就算天塌下來，也要等我睡醒再說。",
            "p": "躺平哲學",
            "do": "關靜音",
            "dont": "設鬧鐘"
        },
        {
            "style": "微小幸運",
            "article": f"【{today_str} ｜ 療癒碎片】\n走在路上突然踩到一塊平整的磁磚，買早餐老闆多送了一顆荷包蛋。今天運氣還不錯。",
            "q": "宇宙正在偷偷塞給你小確幸，接住它！",
            "p": "日常觀察",
            "do": "買彩券",
            "dont": "過度思考"
        },
        {
            "style": "浩瀚宇宙",
            "article": f"【{today_str} ｜ 史詩碎片】\n爬上山頂往下看，底下那些煩惱的人事物，看起來都跟螞蟻一樣小。",
            "q": "世界這麼大，何必把自己困在三坪的辦公室裡。",
            "p": "放寬心",
            "do": "深呼吸",
            "dont": "鑽牛角尖"
        },
        {
            "style": "禪意留白",
            "article": f"【{today_str} ｜ 禪意碎片】\n花十分鐘觀察一滴水如何從葉尖滑落，其實也是一種巨大的收穫。",
            "q": "公司是他的，但人生是你的。",
            "p": "安於平凡",
            "do": "冷眼旁觀",
            "dont": "認真負責"
        }
    ]
    
    # 將生成的字典轉換為 JSON 字串，準備注入 HTML
    quotes_js_string = json.dumps(ai_generated_quotes, ensure_ascii=False)
    # =====================================================================

    # 2. 讀取前端母版 (確保路徑精準指向 frontend/template.html)
    template_path = os.path.join('frontend', 'template.html')
    
    if not os.path.exists(template_path):
        print(f"❌ 嚴重錯誤：找不到母版檔案 {template_path}！")
        print("請確定 GitHub 上的資料夾結構是 'frontend/template.html'")
        return

    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 3. 注入靈魂 (替換母版中的日期與 JSON 資料)
    html_content = html_content.replace('__PAYLOAD_DATE__', today_str)
    html_content = html_content.replace('__QUOTES_JS__', quotes_js_string)

    # 4. 寫入根目錄的 index.html (今日的首頁門面，供全世界觀看)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ index.html 已成功更新！(今日門面)")

    # 5. 啟動時光機！寫入 archive/YYYY-MM-DD.html (永久歷史備份)
    archive_dir = 'archive'
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print("📁 首次建立 archive 時光機資料夾...")
        
    archive_path = os.path.join(archive_dir, archive_filename)
    with open(archive_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ 歷史備份已安全封存：{archive_path}")

    print("🚀 太極宇宙渲染完畢，準備交由 GitHub Actions 封裝推送！")

if __name__ == "__main__":
    main()
