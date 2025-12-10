import pandas as pd
import json
import re

# 檔案名稱設定
csv_file = 'Songs_Table.csv'   # 您的歌曲資料表
json_file = 'music_data.json'  # 輸出給網頁用的 JSON

def get_embed_url(url):
    """
    將各種 YouTube 網址格式轉換為 Embed 格式
    支援: youtu.be, watch?v=, embed/
    """
    if pd.isna(url) or url == 'Null' or str(url).strip() == '':
        return ""
    
    url = str(url).strip()
    
    # 使用正規表達式抓取 Video ID (最準確的方法)
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    else:
        # 如果無法辨識 ID，但網址看起來像網址，就回傳原網址(或可選擇回傳空值)
        return ""

try:
    # 1. 讀取 CSV (處理編碼，若是 Excel 轉出的通常是 utf-8-sig 或 cp950)
    # 先嘗試 utf-8，若失敗可改用 cp950 (Big5)
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file, encoding='cp950')

    print(f"已讀取 {len(df)} 筆歌曲資料...")

    # 2. 轉換資料
    output_data = []
    
    # 為了合併歌手名稱，我們這裡做簡化處理：
    # 直接讀取 Songs_Table，若您需要歌手名，建議先用上一個腳本合併 Artists_Table
    # 這裡示範「如何產生崁入碼」的核心邏輯
    
    success_count = 0
    fail_count = 0

    for index, row in df.iterrows():
        raw_url = row['YouTube 連結'] # 您的 CSV 欄位名稱
        title = row['歌曲名']
        
        embed_url = get_embed_url(raw_url)
        
        # 只有當成功產生崁入碼時才加入列表 (或者您希望保留無連結的歌也可以)
        if embed_url:
            output_data.append({
                "title": str(title),
                "artist": "TWICE", # 若未合併歌手表，暫時預設 TWICE，或需合併 Artists_Table
                "duration": str(row['歌曲時長']),
                "url": embed_url,  # 這是轉換後的崁入碼！
                "cover": ""        # 圖片路徑
            })
            success_count += 1
        else:
            fail_count += 1

    # 3. 存檔
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print("-" * 30)
    print(f"轉換完成！")
    print(f"成功轉換: {success_count} 首")
    print(f"無效連結: {fail_count} 首")
    print(f"檔案已儲存為: {json_file}")
    print("-" * 30)
    
    # 顯示前 3 筆範例給使用者看
    print("範例資料 (前3筆):")
    for item in output_data[:3]:
        print(f"歌名: {item['title']}")
        print(f"崁入碼: {item['url']}")
        print("-" * 10)

except FileNotFoundError:
    print(f"錯誤：找不到檔案 {csv_file}")