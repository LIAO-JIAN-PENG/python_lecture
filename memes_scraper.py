import requests
from bs4 import BeautifulSoup
import os
from aiohttp import ClientSession
import aiofiles
import asyncio
import time

def get_image_link():
    '''
    使用 headers 偽裝成瀏覽器\n
    url 使用的是 dcard API version 2，使用方法在 Dcard API 教學\n
    GET 請求取得 json 型態的資料\n
    links 儲存從 json 資料中的圖片網址\n
    ================================\n
    回傳 : links 圖片網址 (型態: List)\n
    '''
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    url = 'https://www.dcard.tw/service/api/v2/forums/meme/posts?popular=true&limit=100'
    res = requests.get(url, headers=headers)
    articles = res.json()
    links = []
    for article in articles:
        links.append(article['mediaMeta'][0]['url']) # 圖片檔案在mediaMeta下
    return links

async def main():
    '''
    執行非同步網頁請求\n
    使用 aiohttp 中的 ClientSession 請求\n
    ClientSession 使用方式跟 requests 很像，所以不用太擔心\n
    tasks : 存放打包好的執行函式, 型態 : list\n
    使用 asyncio.gather 打包\n
    '''
    links = get_image_link() # 取得連結
    async with ClientSession() as session: # 開啟連線通道
        tasks = [fetch(i, links[i], session) for i in range(len(links))]
        await asyncio.gather(*tasks)

# 定義協程(coroutine)
async def fetch(num, link, session):
    '''
    fetch : 負責網頁爬蟲的部分\n
    num : 給圖檔的名字 0 ~ len(nums)\n
    link : 此圖檔的連結\n
    session : ClientSession 所建立的連線\n
    ===================================
    首先，確認連項狀況 == 200
    建立名為 meme 的資料夾路徑
    使用 aio 系列的 aiofiles 寫入檔案, 'wb', 因為是圖檔所以用二進位寫入
    '''
    async with session.get(link) as response:  #非同步發送請求
        if response.status==200: # 確認連線狀況
            if not os.path.exists('meme/'): # 建立名為 meme 的資料夾路徑
                os.makedirs('meme/')
            f= await aiofiles.open(f'meme/{num}.jpg',mode='wb') # 寫入圖檔, 二進位
            await f.write(await response.read())
            await f.close()

# 計算時間
start_time = time.time()
# 這邊的問題我有上網找了，但是好像目前只有這個解法，所以先這樣寫
# asyncio.run(main())
loop = asyncio.get_event_loop()  #建立事件迴圈(Event Loop)
loop.run_until_complete(main())  #執行協程(coroutine)
# loop.close()
print("花費:" + str(time.time() - start_time) + "秒")