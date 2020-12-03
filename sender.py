import requests, json, logging
from urllib.parse import quote
from abc import  ABC, abstractmethod


class ToMessengerSender(ABC):


    @abstractmethod
    def send_message(self, text):
       pass

    @abstractmethod
    def send_image(self, image_url):
        pass

    @abstractmethod
    def send_video(self, video_url):
        pass

    @abstractmethod
    def send_gif(self, gif_url):
        pass




class TelegramSender(ToMessengerSender):


    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.url = 'http://api.telegram.org/bot{}/'.format(bot_token)
        self.chat_id = chat_id
        self.logger = logging.getLogger('Vk To Messengers.TelegramSender')

    def create_url(self, url_type, chat_id):
        if url_type == 'sendMessage':
            return self.url + 'sendMessage?chat_id={}'.format(chat_id)
        elif url_type == 'sendPhoto':
            return self.url + 'sendPhoto?chat_id={}'.format(chat_id)

    def send_message(self, text):
        text_to_log = text
        text_to_send = quote(text)
        url = self.create_url('sendMessage', self.chat_id) +  '&text={}'.format(text_to_send)
        requests.get(url)
        self.logger.info("Отправлен текст в телеграм")
        self.logger.info("Адрес {}".format(url))
        self.logger.info('Содержимое: {}'.format(text_to_log))

    def send_image(self, photo_url):
        url = self.create_url('sendPhoto', self.chat_id) + '&photo={}'.format(quote(photo_url))
        requests.get(url)
        self.logger.info("Отправлена картинка в телеграм")
        self.logger.info("Адрес {}".format(url))
        self.logger.info('Содержимое: {}'.format(photo_url))

    def send_video(self, video_url):
        self.send_message(video_url)

    def send_gif(self, gif_url):
        self.send_message(gif_url)


class DiscordSender(ToMessengerSender):


    def __init__(self, hook_url):
        self.hook_url = hook_url
        self.logger = logging.getLogger('Vk To Messengers.DiscordSender')

    def send_message(self, text):
        requests.post(self.hook_url, {'content': text})
        self.logger.info("Отправлено сообщение в дискорд")
        self.logger.info("Адрес {}".format(self.hook_url))
        self.logger.info('Содержимое: {}'.format(text))

    #гифка или картинка
    def send_image(self, url):
        to_send_data = {}
        to_send_data["embeds"] = []
        embed = {}
        embed["image"] = {'url': url}
        to_send_data["embeds"].append(embed)
        requests.post(self.hook_url, data=json.dumps(to_send_data), headers={"Content-Type": "application/json"})
        self.logger.info("Отправлена гифка или картинка в дискорд")
        self.logger.info("Адрес {}".format(self.hook_url))
        self.logger.info('Содержимое: {}'.format(to_send_data))


    def send_video(self, video_url):
        self.send_message(video_url)

    def send_gif(self, gif_url):
        self.send_video(gif_url)

    #https://gist.github.com/Birdie0/78ee79402a4301b1faf412ab5f1cdcf9
    # def send_video(self, url):
    #     to_send_data = {}
    #     to_send_data["embeds"] = []
    #     embed = {}
    #     embed["video"] = {'url': url}
    #     to_send_data["embeds"].append(embed)
    #     requests.post(self.hook_url, data=json.dumps(to_send_data), headers={"Content-Type": "application/json"})
    #
    # def send_url(self, url):
    #     to_send_data = {}
    #     to_send_data["embeds"] = []
    #     embed = {}
    #     embed["url"] = url
    #     to_send_data["embeds"].append(embed)
    #     requests.post(self.hook_url, data=json.dumps(to_send_data), headers={"Content-Type": "application/json"})


class Sender():
    def __init__(self, senders: ToMessengerSender):
        self.senders = []
        for sender in senders:
            self.senders.append(sender)

    def send_messages(self, text):
        for sender in self.senders:
            sender.send_message(text)

    def send_image (self, image_url):
        for sender in self.senders:
            sender.send_image(image_url)

    def send_gif(self, gif_url):
        for sender in self.senders:
            sender.send_gif(gif_url)
