import json

# 歌詞內容（直接貼上原本的樣子）
lyrics_text = """열두시가 되면 닫혀요, 조금만 서둘러 줄래요?
Knock, knock, knock, knock, knock on my door
Knock, knock, knock, knock, knock on my door
밤이 되면 내 맘속에 출입문이 열리죠
누군가 필요해 (해), someone else (else)
자꾸자꾸 서성이네, 몰래몰래 훔쳐보네
Knock, knock, knock, knock, knock on my door (door)
Knock, knock, knock, knock, knock on my door (door)
보나마나 또 playboy, 떠보나마나 bad boy
확신이 필요해 (해), knock, knock
내 맘이 열리게 두드려줘
세게 쿵, 쿵, 다시 한 번 쿵, 쿵 (쿵)
Baby, knock, knock, knock, knock, knock on my door
Knock, knock, knock, knock, knock
쉽게 열리지는 않을 거야 (say that you're mine)
내일도 모레도 다시 와줘
준비하고 기다릴게 (knock, knock, knock)
Baby, knock, knock, knock, knock, knock on my door
Knock, knock, knock, knock, knock
들어도 계속 듣고 싶은 걸, knock on my door (door)
필요 없어 gold key or get lucky
진심이면 everything's gonna be okay
어떡해? 벌써 왔나 봐, 잠시만 기다려 줄래요?
혼자 있을 때 훅 들어와, 정신 없이 날 흔들어 놔
지금이 딱 널 위한 show time (time), make it yours
댕댕 울리면 매일 찾아와줄래? (찾아와줄래?)
뱅뱅 돌다간 잠들어 버릴 걸요
Knock, knock, knock, knock, knock on my door (door)
Knock, knock, knock, knock, knock on my door (door)
Come in, come in, come in, baby, take my hands
내 맘이 열리게 두드려줘
세게 쿵, 쿵, 다시 한 번 쿵, 쿵 (쿵)
Baby, knock, knock, knock, knock, knock on my door
Knock, knock, knock, knock, knock (knock, knock)
쉽게 열리지는 않을 거야 (say that you're mine)
내일도 모레도 다시 와줘
준비하고 기다릴게 (knock, knock, knock)
Baby, knock, knock, knock, knock, knock on my door
Knock, knock, knock, knock, knock
들어도 계속 듣고 싶은 걸, knock on my door (door)
Hey (hey), hey (hey)
이 시간이 지나면 (지나면)
굳어있던 내 맘이, 내, 내 맘이
아이스크림처럼 녹아 버릴 테니까 (come knock on my door)
내 맘이 열리게 두드려줘 (oh)
세게 쿵, 쿵, 다시 한 번 쿵, 쿵 (쿵)
Baby, knock, knock, knock, knock, knock on my door (oh)
Knock, knock, knock, knock, knock (oh)
쉽게 열리지는 않을 거야 (say that you're mine, oh)
내일도 모레도 다시 와줘 (다시 와줘)
준비하고 기다릴게 (knock, knock, knock, baby)
Baby, knock, knock, knock, knock, knock on my door
Knock, knock, knock, knock, knock (knock on my door)
들어도 계속 듣고 싶은 걸, knock on my door (knock on my door)
Knock, knock, knock, knock on my door (oh)
(I'm freakin', freakin' out) knock, knock
(Freakin' out, out, knock, knock) knock, knock on my door
Knock, knock, knock, knock on my door
Knock, knock, knock, knock, knock on my door
Knock, knock, knock, knock, knock on my door (door)"""

file_path = 'music_data.json'

# 1. 讀取檔案
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. 找到歌並更新歌詞
for song in data:
    if song.get('title') == 'KNOCK KNOCK':
        song['lyrics'] = lyrics_text # Python 會自動幫你把換行轉成 \n 存進去
        print("找到歌曲，正在更新歌詞...")
        break

# 3. 儲存檔案
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("更新完成！")