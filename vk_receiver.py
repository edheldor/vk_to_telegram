import json, logging, hashlib, requests, urllib.request


class VkReceiver:

    def __init__(self, data):
        self.data = json.loads(data)
        self.type = None
        if self.data['type'] == 'confirmation':
            self.type = 'confirmation'
        elif self.data['type'] == 'wall_post_new':
            self.type = 'wall_post_new'
        else:
            self.type = 'other'

        self.logger = logging.getLogger('Vk To Messengers.VkReceiver')
        self.hash = None

    def received_type(self):
        if self.type == 'other':
            self.logger.info("Неподдерживаемый тип поста")
            return 'other'
        elif self.type == 'wall_post_new':
            self.logger.info("Пост на стене")
            return 'wall_post_new'
        elif self.type == 'confirmation':
            self.logger.info("Запрос на подтверждение от ВК callback API")
            return 'confirmation'

    def repost_checker(self):
        return 'copy_history' in self.data['object']

    def calculate_hash(self, text, image_url):
        string_for_hash = "{}{}".format(text, image_url)
        string_for_hash = string_for_hash.encode('utf-8')
        hashed_string = hashlib.md5(string_for_hash)
        hashed_string = hashed_string.hexdigest()
        return hashed_string

    def parse_wall_past(self, data):
        parsed_attachments = dict()
        parsed_attachments['text'] = None
        parsed_attachments['images'] = []
        parsed_attachments['gifs'] = []

        self.logger.info("Начанаем разбор данных от ВК: {}".format(data))
        text = data.get('text')
        parsed_attachments['text'] = text

        if data.get('attachments') == None:
            return parsed_attachments
        else:
            recived_attachments = data['attachments']
            for attachment in recived_attachments:
                if attachment['type'] == 'video':
                    return 'with_video'
                if attachment['type'] == 'photo':
                    photo_url = attachment['photo']['photo_604']
                    parsed_attachments['images'].append(photo_url)
                if attachment['type'] == 'doc':
                    file_ext = attachment['doc'].get('ext')
                    if file_ext == 'gif':
                        gif_url = attachment['doc'].get('url')
                        response = urllib.request.urlopen(gif_url)
                        gif_url = response.url
                        parsed_attachments['gifs'].append(gif_url)
            return parsed_attachments

    def recive_wall_post(self):
        if self.data['type'] == 'wall_post_new':
            # проверяем репост это или оригинальная запись и обрабатываем немного разными способами
            # если это предложка или отложенная запись, ничего не делаем
            if (self.data['object']['post_type'] == 'postpone') or (self.data['object']['post_type'] == 'suggest'):
                return 'postpone_or_suggest'
            if self.repost_checker() == True:
                self.logger.info("Репост")
                self.logger.info(self.data)
                attachments = self.parse_wall_past(self.data['object']['copy_history'][0])
                if attachments == 'with_video':
                    return 'with_video'

                self.hash = self.calculate_hash(attachments['text'], attachments.get('images'))
                self.logger.info("Хэш для записи (репост) {}".format(self.hash))




            else:
                self.logger.info("Не репост, оригинальная запись")
                self.logger.info(self.data)
                attachments = self.parse_wall_past(self.data['object'])
                if attachments == 'with_video':
                    return 'with_video'

                self.hash = self.calculate_hash(attachments['text'], attachments.get('images'))
                self.logger.info("Хэш для записи (оригинальная апись ) {}".format(self.hash))

            return attachments





