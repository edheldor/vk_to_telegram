import vk_api, settings, telegram_sender
from flask import Flask, request, json

telegram = telegram_sender.TelegramSender(settings.tg_bot_token, settings.tg_chat_id)
app = Flask(__name__)


@app.route ("/", methods=['GET'])
def index():
    return 'oooops'

@app.route("/", methods=['POST'])
def processing():
    data = json.loads(request.data)

    if 'type' not in data.keys():
        return 'ok'
    if data['type'] == 'confirmation':
        return settings.vkConfirmation
    elif data['type'] == 'wall_post_new':
        text = data['object']['copy_history'][0]['text']
        if data['object']['copy_history'][0]['attachments'][0]['type'] == 'photo':
            imageUrl = data['object']['copy_history'][0]['attachments'][0]['photo']['photo_807']

        telegram.send_message(text)
        if (imageUrl):
            telegram.send_photo(imageUrl)

        return 'ok'



