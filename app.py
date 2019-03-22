import settings, telegram_sender,vk_receiver
from flask import Flask, request, json

telegram = telegram_sender.TelegramSender(settings.tg_bot_token, settings.tg_chat_id)
app = Flask(__name__)


@app.route ("/", methods=['GET'])
def index():
    return 'oooops'

@app.route("/", methods=['POST'])
def processing():
    vk = vk_receiver.VkReceiver(request.data)
    if vk.received_type() == 'confirmation':
        return settings.vk_confirmation
    elif vk.received_type() == 'other':
        return 'ok'
    elif vk.received_type() == 'wall_post_new':
        recived_data = vk.recive_wall_post()
        text = recived_data['text']
        image_url = recived_data['image_url']
        telegram.send_message(text)
        telegram.send_photo(image_url)
        return 'ok'









