from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["J94/Xx2nbDNcuGlAwKvMKBJ7o85u+nKxZcmJMhE4j0wEWNo8mjexGgYayTIGLipy0Wna5MBk5Va6PU9cG2jD+q2dUpIs82s45KvpkSYPoPNBX5jwgFhWGe00iG9nhQwyiFJdzxUdjMWHRDWxafnH8QdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["eb0c550162032c57389aea178cf418fd"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
　# 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
　# 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
　# handleの処理を終えればOK
    return 'OK'

## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################

#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)) #ここでオウム返しのメッセージを返します。

# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    app.run()
