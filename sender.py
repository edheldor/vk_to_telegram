import requests, json
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




class TelegramSender(ToMessengerSender):


    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.url = 'http://api.telegram.org/bot{}/'.format(bot_token)
        self.chat_id = chat_id

    def create_url(self, url_type, chat_id):
        if url_type == 'sendMessage':
            return self.url + 'sendMessage?chat_id={}'.format(chat_id)
        elif url_type == 'sendPhoto':
            return self.url + 'sendPhoto?chat_id={}'.format(chat_id)

    def send_message(self, text):
        text = quote(text)
        url = self.create_url('sendMessage', self.chat_id) +  '&text={}'.format(text)
        requests.get(url)

    def send_image(self, photo_url):
        url = self.create_url('sendPhoto', self.chat_id) + '&photo={}'.format(photo_url)
        requests.get(url)

    def send_video(self, video_url):
        self.send_message(video_url)


class DiscordSender(ToMessengerSender):


    def __init__(self, hook_url):
        self.hook_url = hook_url

    def send_message(self, text):
        requests.post(self.hook_url, {'content': text})

    #гифка или картинка
    def send_image(self, url):
        to_send_data = {}
        to_send_data["embeds"] = []
        embed = {}
        embed["image"] = {'url': url}
        to_send_data["embeds"].append(embed)
        requests.post(self.hook_url, data=json.dumps(to_send_data), headers={"Content-Type": "application/json"})


    def send_video(self, video_url):
        self.send_message(video_url)

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
