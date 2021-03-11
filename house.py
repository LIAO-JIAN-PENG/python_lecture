import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio
import time
import json

# 偽裝用 Headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
}



async def main():
    '''
    對網站分析後，取得該網址及頁數的相對關係\n
    以下有使用到 fstring 技術 : \n
        就是在字串前加上 f，字串中的{ }內就可以放自己想要的變數\n
    ClientSession 使用方式跟 requests 很像，所以不用太擔心\n
    tasks : 存放打包好的執行函式, 型態 : list\n
    使用 asyncio.gather 打包\n
    ===============================================
    最後在非同步執行結束，寫入 json 檔案\n
    json 檔案需要做一些編碼處理，才可以正常檢視
    '''
    houses = [] # 拿來裝 house dict 資料的 list
    links = list() # 或是 links = []
    for page in range(1, 30):
        links.append(
            f"https://buy.yungching.com.tw/region/住宅_p/高雄市-三民區_c/_rm?pg={page}")
 
    async with ClientSession() as session:
        tasks = [fetch(link, session) for link in links] # 建立任務清單
        await asyncio.gather(*tasks)  # 打包任務清單及執行
    
    with open('永信房屋資料.json', 'w', encoding='utf-8') as jfile:
        json.dump(houses, jfile, ensure_ascii=False)
 
#定義協程(coroutine)
async def fetch(link, session):
    '''
    fetch : 負責網頁爬蟲的部分\n
    link : 網址的連結\n
    session : ClientSession 所建立的連線\n
    ===================================
    以下，我用 beautifulsoup 將我收集到的 html 資料拿來分析\n
    title  : 房子標題\n
    h_type : 房子種類
    old    : 屋齡(年)
    size   : 坪數
    inner  : 室內配房
    price  : 價格(萬)
    '''
    async with session.get(link, headers=headers) as response:  #非同步發送請求
        
        ## 爬蟲程式碼 ##
        html_body = await response.text()
        soup = BeautifulSoup(html_body, 'lxml')
        house_raws = soup.find_all('li', 'm-list-item')

        for raw in house_raws:
            attr = {}
            attr['title'] = raw.find('span').text
            details = raw.find('ul', 'item-info-detail').find_all('li')
            attr['h_type'] = details[0].text.strip()
            attr['old'] = details[1].text.strip()
            attr['size'] = details[4].text.strip()
            attr['inner'] = details[6].text.strip()
            attr['price'] = int(raw.find('div', 'price').text.split()[0].replace(',',''))
            houses.append(attr)
            # print(attr)
 
 
start_time = time.time()  #開始執行時間
loop = asyncio.get_event_loop()  #建立事件迴圈(Event Loop)
loop.run_until_complete(main())  #執行協程(coroutine)
print("花費:" + str(time.time() - start_time) + "秒")