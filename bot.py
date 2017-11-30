# -*- coding: utf-8 -*-
import os
import message

from slackclient import SlackClient

# Variable para guardar los equipos, con su código, que han autorizado
# la aplicación.
authed_teams = {}


class Bot(object):
    """ Iniciamos nuestro BOT """
    def __init__(self):
        super(Bot, self).__init__()
        self.name = 'chicken-bot'
        self.emoji = ':cubimal_chick:'
        self.oauth = {
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.environ.get('CLIENT_SECRET'),
            # Es importante considerar el alcance de nuestra aplicación, de
            # esto depende las acciones que se pueden realizar.
            'scope': 'bot'
        }
        self.verification = os.environ.get('VERIFICATION_TOKEN')

        # NOTA: Python-slack requiere una conexión con un cliente para generar
        # un token de oauth. Crearemos un cliente sin autenticación pasando una
        # cadena vacía que luego recibiremos cuando la aplicación sea aceptada.
        self.client = SlackClient("")
        # Usaremos una variable global para almacenar los mensajes generados
        # y sus respuestas.
        self.messages = {}

    def auth(self, code):
        """
        Autenticación con OAuth.
        La información es guardada en la variable global del bot.

        ----------
        code: [str] código temporal enviado por Slack para generar
        el OAUTH token.
        """
        auth_response = self.client.api_call(
            'oauth.access',
            client_id=self.oauth['client_id'],
            client_secret=self.oauth['client_secret'],
            code=code
        )
        if not auth_response.get('ok', False):
            return False

        team_id = auth_response["team_id"]
        authed_teams[team_id] = {
            'bot_token': auth_response['bot']['bot_access_token']
        }
        # Con el token generado volvemos a realizar la conexión con el
        # cliente de Slack
        self.client = SlackClient(authed_teams[team_id]['bot_token'])
        return True

    def open_dm(self, user_id):
        """
        Abre un nuevo DM al usuario indicado.

        ----------
        user_id: [str] id del usuario asociado a Slack.

        ----------
        dm_id: [str] id del DM creado por este método.
        """
        new_dm = self.client.api_call('im.open', user=user_id)
        if not new_dm.get('ok'):
            return False
        channel = new_dm.get('channel')
        dm_id = channel.get('id')
        return dm_id

    def onboarding_message(self, team_id, user_id):
        """
        Crea y  manda un mensaje de bienvenida a un nuevo usuario.
        ----------
        team_id: [str] id del equipo de Slack asociado al evento
        user_id: [str] id del usuario de Slack asociado al evento
        """

        if self.messages.get(team_id):
            self.messages[team_id].update({user_id: message.Message()})
        else:
            self.messages[team_id] = {user_id: message.Message()}
        message_obj = self.messages[team_id][user_id]
        message_obj.channel = self.open_dm(user_id)
        message_obj.create_attachments()
        post_message = self.client.api_call(
            'chat.postMessage',
            channel=message_obj.channel,
            username=self.name,
            icon_emoji=self.emoji,
            text=message_obj.text,
            attachments=message_obj.attachments
        )
        timestamp = post_message['ts']
        message_obj.timestamp = timestamp

    def leaving_channel_message(self, user_id):
        channel = self.open_dm(user_id)
        message = '@chicken te está observando :cubimal_chick:'
        self.client.api_call(
            "chat.postMessage",
            channel=channel,
            username=self.name,
            icon_emoji=self.emoji,
            text=message
        )

    def update_emoji(self, team_id, user_id):
        """
        Update onboarding welcome message after recieving a "reaction_added"
        event from Slack. Update timestamp for welcome message.
        Parameters
        ----------
        team_id : str
            id of the Slack team associated with the incoming event
        user_id : str
            id of the Slack user associated with the incoming event
        """
        # These updated attachments use markdown and emoji to mark the
        # onboarding task as complete
        completed_attachments = {"text": ":white_check_mark: "
                                         "~*Add an emoji reaction to this "
                                         "message*~ :thinking_face:",
                                 "color": "#439FE0"}
        # Grab the message object we want to update by team id and user id
        message_obj = self.messages[team_id].get(user_id)
        # Update the message's attachments by switching in incomplete
        # attachment with the completed one above.
        message_obj.emoji_attachment.update(completed_attachments)
        # Update the message in Slack
        post_message = self.client.api_call("chat.update",
                                            channel=message_obj.channel,
                                            ts=message_obj.timestamp,
                                            text=message_obj.text,
                                            attachments=message_obj.attachments
                                            )
        # Update the timestamp saved on the message object
        message_obj.timestamp = post_message["ts"]

    def update_pin(self, team_id, user_id):
        """
        Update onboarding welcome message after recieving a "pin_added"
        event from Slack. Update timestamp for welcome message.
        Parameters
        ----------
        team_id : str
            id of the Slack team associated with the incoming event
        user_id : str
            id of the Slack user associated with the incoming event
        """
        # These updated attachments use markdown and emoji to mark the
        # onboarding task as complete
        completed_attachments = {"text": ":white_check_mark: "
                                         "~*Pin this message*~ "
                                         ":round_pushpin:",
                                 "color": "#439FE0"}
        # Grab the message object we want to update by team id and user id
        message_obj = self.messages[team_id].get(user_id)
        # Update the message's attachments by switching in incomplete
        # attachment with the completed one above.
        message_obj.pin_attachment.update(completed_attachments)
        # Update the message in Slack
        post_message = self.client.api_call("chat.update",
                                            channel=message_obj.channel,
                                            ts=message_obj.timestamp,
                                            text=message_obj.text,
                                            attachments=message_obj.attachments
                                            )
        # Update the timestamp saved on the message object
        message_obj.timestamp = post_message["ts"]

    def update_share(self, team_id, user_id):
        """
        Update onboarding welcome message after recieving a "message" event
        with an "is_share" attachment from Slack. Update timestamp for
        welcome message.
        Parameters
        ----------
        team_id : str
            id of the Slack team associated with the incoming event
        user_id : str
            id of the Slack user associated with the incoming event
        """
        # These updated attachments use markdown and emoji to mark the
        # onboarding task as complete
        completed_attachments = {"text": ":white_check_mark: "
                                         "~*Share this Message*~ "
                                         ":mailbox_with_mail:",
                                 "color": "#439FE0"}
        # Grab the message object we want to update by team id and user id
        message_obj = self.messages[team_id].get(user_id)
        # Update the message's attachments by switching in incomplete
        # attachment with the completed one above.
        message_obj.share_attachment.update(completed_attachments)
        # Update the message in Slack
        post_message = self.client.api_call("chat.update",
                                            channel=message_obj.channel,
                                            ts=message_obj.timestamp,
                                            text=message_obj.text,
                                            attachments=message_obj.attachments
                                            )
        # Update the timestamp saved on the message object
        message_obj.timestamp = post_message["ts"]
