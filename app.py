import settings, sender, vk_receiver, logging
from flask import Flask, request, json

logging.basicConfig(filename='log.log', format='%(asctime)s :: 	%(levelname)s :: %(name)s :: %(message)s', level=logging.INFO)
logger = logging.getLogger('Vk To Messengers')
telegram = sender.TelegramSender(settings.tg_bot_token, settings.tg_chat_id)
discord = sender.DiscordSender(settings.discord_hook)
sender = sender.Sender([telegram, discord])
app = Flask(__name__)

logger.info('Старт веб сервера')

@app.route ("/", methods=['GET'])
def index():
    return 'oooops'

@app.route("/", methods=['POST'])
def processing():
    vk = vk_receiver.VkReceiver(request.data)
    received_type = vk.received_type()

    if received_type == 'confirmation':
        return settings.vk_confirmation
    elif received_type == 'other':
        return 'ok'
    elif received_type == 'wall_post_new':
        recived_data = vk.recive_wall_post()
        text = recived_data['text']
        image_url = recived_data['image_url']

        sender.send_messages(text)
        sender.send_image(image_url)

        return 'ok'









