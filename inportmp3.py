import json
import os

# --- 設定區 ---
json_filename = 'music_data.json'  # 您的 JSON 檔名
mp3_folder = 'MP3'                 # 您的 MP3 資料夾名稱

# 1. 讀取目前的 JSON 資料
try:
    with open(json_filename, 'r', encoding='utf-8') as f:
        music_data = json.load(f)
    print(f"目前 JSON 共有 {len(music_data)} 筆歌曲資料。")
except FileNotFoundError:
    print(f"找不到 {json_filename}，將建立新檔案。")
    music_data = [] # 如果沒有檔案，就從空清單開始

# 2. 取得 MP3 資料夾內的所有檔案
try:
    # 這裡過濾掉非 mp3 結尾的檔案，避免讀到垃圾檔
    mp3_files = [f for f in os.listdir(mp3_folder) if f.lower().endswith('.mp3')]
    print(f"在 '{mp3_folder}' 資料夾中找到 {len(mp3_files)} 個 MP3 檔案。")
except FileNotFoundError:
    print(f"找不到資料夾 '{mp3_folder}'，請確認路徑。")
    exit()

#用來紀錄哪些 MP3 檔案已經被配對到了
matched_mp3_files = set()

# 3. 第一階段：更新現有歌曲 (Update Existing)
update_count = 0
print("\n--- 正在比對現有資料 ---")

for song in music_data:
    # 取得歌名，並做「正規化」處理以便比對
    song_title_clean = song['title'].replace(" ", "").lower()
    
    # 如果這首歌已經有 mp3 路徑且檔案存在，就跳過 (或是你要強制更新也可以)
    # 這裡我們假設要重新掃描一次
    
    found = False
    for filename in mp3_files:
        # 把檔名也做正規化 (去掉 .mp3，去掉空格，轉小寫)
        filename_clean = filename.replace(".mp3", "").replace(" ", "").lower()
        
        # ★★★ 比對邏輯 ★★★
        if song_title_clean == filename_clean or song_title_clean in filename_clean:
            # 配對成功
            song['mp3'] = f"{mp3_folder}/{filename}"
            matched_mp3_files.add(filename) # 標記這個檔案已被使用
            found = True
            update_count += 1
            # print(f"✅ 更新路徑: {song['title']}") 
            break # 找到就跳出，換下一首

# 4. 第二階段：加入新歌曲 (Add New)
new_add_count = 0
print("\n--- 正在檢查是否有新歌 ---")

for filename in mp3_files:
    # 如果這個檔案 不在「已配對」的名單中，代表它是新的
    if filename not in matched_mp3_files:
        # 自動產生歌名 (移除 .mp3 副檔名)
        new_title = filename.replace(".mp3", "")
        
        # 建立新的歌曲物件 (樣板)
        new_song = {
            "title": new_title,
            "artist": "TWICE",  # 預設歌手
            "duration": "",     # 暫時留空，或之後用程式讀取長度
            "url": "",          # 暫時留空
            "cover": "",        # 暫時留空
            "mp3": f"{mp3_folder}/{filename}",
            "lyrics": ""
        }
        
        music_data.append(new_song)
        matched_mp3_files.add(filename) # 雖然這行沒用到，但好習慣是標記起來
        new_add_count += 1
        print(f"🆕 新增歌曲: {new_title}")

# 5. 寫回 JSON 檔案
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(music_data, f, ensure_ascii=False, indent=4)

print("-" * 30)
print(f"作業完成！")
print(f"📊 更新舊歌路徑：{update_count} 首")
print(f"➕ 新增 MP3 歌曲：{new_add_count} 首")
print(f"📂 目前總歌曲數：{len(music_data)} 首")