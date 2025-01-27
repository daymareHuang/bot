import requests, math, datetime, schedule, time
from bs4 import BeautifulSoup

# Telegram Bot 配置
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


# 限時免費遊戲
def freeGameInfo():
    url = 'https://www.ptt.cc/bbs/Steam/search?q=%E9%99%90%E5%85%8D'  # 替換為你的目標網站
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,"html5lib")
        titles = soup('div', class_='r-ent')
        now = datetime.datetime.now()
        today = (" " + str(now.month)+ "/"+ str(now.day)) if now.month < 10 else (str(now.month)+ "/"+ str(now.day))
        output = ''
        for i in titles:
          if (i.find('a')!= None) and (i.find('div', class_="date").get_text() == today) :
            output = output + i.find('a').get_text() + i.find('div', class_="date").get_text() + '\n' + 'https://www.ptt.cc/'+i.find('a')['href']  +'\n\n'
        if output != "":
          return "\n===================" + today + " 今日限免 " + "===================\n".join(output)
        else:
          return "\n===================" + today + " 今日限免 " + "===================\n" + "******************* 今日沒有限免 ********************"
        # 假設你想提取特定的標題
        # titles = [item.text for item in soup.find_all('h2')]  # 修改根據目標網站結構
        # return '\n'.join(titles)
    else:
        return f"無法訪問網站，狀態碼：{response.status_code}"





# 發送訊息到 Telegram
def send_message_to_telegram(message):
    data = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(TELEGRAM_API_URL, data=data)
    if response.status_code == 200:
        print("訊息已發送！")
    else:
        print(f"發送失敗，狀態碼：{response.status_code}, 回應：{response.text}")


def countDownFree():
    scraped_data = freeGameInfo()
    # 傳遞爬蟲結果到 Telegram
    if scraped_data:
        send_message_to_telegram(f"{scraped_data}")
    else:
        send_message_to_telegram("爬蟲沒有獲得任何數據。")



# 主函數
if __name__ == "__main__":
  schedule.every().day.at("10:30").do(countDownFree)
  # 現在這裡是在UTC+0 所以要檢查時間 如果要排程了話
  # print("當前系統時間:", time.strftime("%Y-%m-%d %H:%M:%S"))
  # print("開始定時任務...")
  # 爬取資料
  while True:
    schedule.run_pending()
    time.sleep(1)
