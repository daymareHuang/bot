import requests, math, datetime, schedule, time
from bs4 import BeautifulSoup
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from dotenv import load_dotenv
import threading
from flask import Flask, abort, request

load_dotenv()

app = Flask(__name__)

line_bot_api= LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
print(line_bot_api)
print(handler)

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature from request header
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)

    try:
        # Handle webhook body
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    # Return a 200 OK status code
    return 'OK', 200



# @app.route("/freeGameInfo", methods=["POST"])
# 限時免費遊戲
def freeGameInfo():
     # 取得 X-Line-Signature Header
   
    url = 'https://www.ptt.cc/bbs/Steam/search?q=%E9%99%90%E5%85%8D' 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.ptt.cc/bbs/Steam',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
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


# def run_schedule():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
        

# 一個訊息處理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # user_message = event.message.text
    # reply_message = "感謝您的訊息"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=freeGameInfo())
    )

# 主函數
if __name__ == "__main__":
    # schedule.every().day.at("04:20").do(countDownFree)

    # # 啟動排程任務執行
    # schedule_thread = threading.Thread(target=run_schedule)
    # schedule_thread.daemon = True  # 設置為守護線程，當主線程結束時，這個線程會自動終止
    # schedule_thread.start()

    # 啟動 Flask 伺服器
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=10000)
