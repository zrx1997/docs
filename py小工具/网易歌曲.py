import requests
import re
 

song_id = '287021'  # 要下载歌曲的ID
file = "./"  # 保存音乐的文件路径,最后加斜杠
wurl = "https://link.hhtjim.com/163/"#外链生成地址
wang_url = "https://music.163.com/song?id=" + song_id
song_url = wurl + song_id + ".mp3"
# 获取歌曲16进制编码
song = requests.get(song_url).content
# 获取歌曲名称
song_names = requests.get(wang_url).text
song_name = re.findall('<em class="f-ff2">.*</em>', song_names)[0].lstrip('<em class="f-ff2">').rstrip('</em>')
# 保存文件
with open(file + song_name + '.mp3', 'wb') as f:
    f.write(song)
    print(song_url + ' 歌名：' + song_name)