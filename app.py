import settings, sender, vk_receiver, logging
from flask import Flask, request, json

logging.basicConfig(filename='log.log', format='%(asctime)s :: 	%(levelname)s :: %(name)s :: %(message)s', level=logging.INFO)
logger = logging.getLogger('Vk To Messengers')
telegram = sender.TelegramSender(settings.tg_bot_token, settings.tg_chat_id)
discord = sender.DiscordSender(settings.discord_hook)
sender = sender.Sender([telegram, discord])
recently_posted = 'recently_posted.txt'
with open(recently_posted, 'a'):
    pass
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

        #Проверка на повторную запись. Записываем хеш записи в файл, а в последующем проверяем не публиковали ли мы тоже самое. Бывают повторные колбэки от вк
        repeated_data = False
        post_hash = vk.post_hash()


        with open(recently_posted, "r") as fh:
            for string in fh:
                if string == post_hash + "\n":
                    repeated_data = True

        if repeated_data == False:
            with open(recently_posted, "a") as fh:
                fh.write(post_hash + "\n")


        if repeated_data == True:
            logger.info('Повтор данных от ВК. Не публикуем')
        else:
            logger.info('Будем публиковатьь')
            sender.send_messages(text)
            sender.send_image(image_url)

        return 'ok'









