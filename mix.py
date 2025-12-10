import pandas as pd
import json

# 1. 讀取 CSV 檔案
df_songs = pd.read_csv('Songs_Table.xlsx - Songs_Table.csv')
df_artists = pd.read_csv('Artists_Table.xlsx - Artists_Table.csv')
df_relations = pd.read_csv('Artists_Songs.xlsx - Artists_Songs.csv')

# 2. 清理欄位名稱 (去除可能的空白)
df_songs.columns = df_songs.columns.str.strip()
df_artists.columns = df_artists.columns.str.strip()
df_relations.columns = df_relations.columns.str.strip()

# 3. 處理 YouTube 連結 (將 youtu.be 轉為 embed 格式以便網頁播放)
def convert_yt_link(url):
    if pd.isna(url): return ""
    if "youtu.be" in url:
        return url.replace("youtu.be/", "www.youtube.com/embed/")
    if "watch?v=" in url:
        return url.replace("watch?v=", "embed/")
    return url

df_songs['EmbedLink'] = df_songs['YouTube 連結'].apply(convert_yt_link)

# 4. 資料合併 (Merge)
# 邏輯：歌曲表 -> 關聯表(找創作者ID) -> 創作者表(找名字)

# 先合併 歌曲 與 關係表
# 假設 Artists_Songs 的 '曲名' 欄位其實是對應 Songs_Table 的 '歌曲識別碼'
merged = pd.merge(df_songs, df_relations, left_on='歌曲識別碼', right_on='曲名', how='left')

# 再合併 創作者表 (Artists_Songs 的 '創作者名稱' 對應 Artists_Table 的 '創作者識別碼')
merged = pd.merge(merged, df_artists, left_on='創作者名稱_y', right_on='創作者識別碼', how='left')

# 5. 整理資料格式 (因為一首歌可能有多個創作者，我們要把創作者合併成字串)
# 只保留需要的欄位
final_df = merged[['歌曲識別碼', '歌曲名', 'EmbedLink', '歌曲時長', '創作者名稱_x', '圖片_x']].copy()
final_df.rename(columns={
    '歌曲名': 'title', 
    'EmbedLink': 'url', 
    '歌曲時長': 'duration',
    '創作者名稱_x': 'artist', # 這裡假設合併後抓到了名字，若無則需調整邏輯
    '圖片_x': 'cover'
}, inplace=True)

# 去除重複 (如果是單純展示歌曲)
final_df = final_df.drop_duplicates(subset=['歌曲識別碼'])

# 填補空值
final_df.fillna("", inplace=True)

# 6. 匯出成 JSON
data_list = final_df.to_dict(orient='records')
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)

print(f"成功轉換 {len(data_list)} 筆歌曲資料！請查看 data.json")