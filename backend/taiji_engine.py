import os
import json
import urllib.request
import urllib.error

def main():
    print("🚀 Taiji Genesis Engine: 啟動『探路者』診斷模式...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ 錯誤：GEMINI_API_KEY 未設定。")

    # 聽從系統建議，呼叫 ListModels 端點
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    req = urllib.request.Request(url)

    try:
        print("📡 正在向 Google 伺服器請求可用模型清單 (ListModels)...")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("✅ 成功取得模型清單！以下是您的金鑰支援的生成模型：\n")
            
            if 'models' in result:
                for model in result['models']:
                    # 過濾出支援 "generateContent" (文字生成) 的模型
                    if 'supportedGenerationMethods' in model and 'generateContent' in model['supportedGenerationMethods']:
                        print(f" - 實際端點名稱 (name): {model['name']}")
                        print(f"   顯示名稱 (displayName): {model['displayName']}")
                        print(f"   版本 (version): {model['version']}")
                        print("-" * 40)
            else:
                print("⚠️ 伺服器回傳成功，但清單中沒有模型。")
                
    except urllib.error.HTTPError as e:
        error_info = e.read().decode('utf-8')
        print(f"❌ 致命連線錯誤 (狀態碼: {e.code}): {error_info}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
