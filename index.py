import os
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

app = Flask(__name__)

line_bot_api = LineBotApi('jxUbOjStesgoj0DA97jjeW/ii8k+7Qv4GjOLqyCfI0MtmaXUBeSLPWOVUQCJ56etpmUpRHVIFGc/V0yHNxN9ga7dsIkGz8GOj/DqfIcaj72X8OKd1fQ/2VtRpdK4jZbyeBbwZYm25ZARxiWWZ29TEgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6c358c918933f589e56c419fc412b188')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = os.environ.get('PORT', 3333)
    app.run(
        host='0.0.0.0',
        port=port,
    )
