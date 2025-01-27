import requests, math, datetime, schedule, time
from bs4 import BeautifulSoup
import os
import threading
from flask import Flask

# Telegram Bot 配置
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
WEBHOOK_URL = f"https://dinobot-dkup.onrender.com/{BOT_TOKEN}"
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
   return "Telegram Bot is runnung!", 200

response = requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    params={"url": WEBHOOK_URL},
)

if response.status_code == 200:
    print("Webhook 設置成功")
else:
    print(f"設置 Webhook 失敗: {response.text}")

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
    schedule.every().day.at("04:20").do(countDownFree)

    # 啟動排程任務執行
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.daemon = True  # 設置為守護線程，當主線程結束時，這個線程會自動終止
    schedule_thread.start()

    # 啟動 Flask 伺服器
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
