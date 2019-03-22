import json

class VkReceiver:


    def __init__(self, data):
        self.data = json.loads(data)
        self.type = None
        if self.data['type'] == 'confirmation':
            self.type = 'confirmation'
        elif self.data['type'] == 'wall_post_new':
            self.type = 'wall_post_new'
        else: self.type = 'other'


    def received_type(self):
        if self.type == 'other':
            return 'other'
        elif self.type == 'wall_post_new':
            return 'wall_post_new'
        elif self.type == 'confirmation':
            return 'confirmation'

    def repost_checker(self):
        return 'copy_history' in self.data['object']

    def recive_wall_post(self):
        if self.data['type'] == 'wall_post_new':
            #проверяем репост это или оригинальная запись и обрабатываем немного разными способами

            if self.repost_checker() == True:
                text = self.data['object']['copy_history'][0]['text']
                if self.data['object']['copy_history'][0]['attachments'][0]['type'] == 'photo':
                    image_url = self.data['object']['copy_history'][0]['attachments'][0]['photo']['photo_604']
                else:
                    image_url = None
            else:
                text = self.data['object']['text']
                if self.data['object']['attachments'][0]['type'] == 'photo':
                    image_url = self.data['object']['attachments'][0]['photo']['photo_604']
                else:
                    image_url = None



            return {'text':text, 'image_url': image_url}





