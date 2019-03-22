import requests

#proxies = {
#  'http': 'http://150.109.194.70:1080',
#  'https': 'https://150.109.194.70:1080',
#}
#requests.get(url, proxies=proxies)


class TelegramSender():


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
        url = self.create_url('sendMessage', self.chat_id) +  '&text={}'.format(text)
        requests.get(url)

    def send_photo(self, photo_url):
        url = self.create_url('sendPhoto', self.chat_id) + '&photo={}'.format(photo_url)
        requests.get(url)
