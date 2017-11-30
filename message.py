# -*- coding: utf-8 -*-
import yaml


class Message(object):
    """
    Objeto para crear y manejar el mensaje de bienvenida a Slack.
    """
    def __init__(self):
        super(Message, self).__init__()
        self.channel = ""
        self.timestamp = ""
        self.text = ('Bienvenido a Grupo Abraxas y a su comunidad en Slack, nos alegra tenerte aquí!.'
                     '\nEmpieza probando la funcionalidad de Slack.')
        self.emoji_attachment = {}
        self.pin_attachment = {}
        self.share_attachment = {}
        self.attachments = [self.emoji_attachment,
                            self.pin_attachment,
                            self.share_attachment]

    def create_attachments(self):
        with open('welcome.json') as json_file:
            json_dict = yaml.safe_load(json_file)
            json_attachments = json_dict['attachments']
            [self.attachments[i].update(json_attachments[i]) for i
             in range(len(json_attachments))]
