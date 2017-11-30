# -*- coding: utf-8 -*-
import json
import bot
from flask import Flask, request, make_response

pyBot = bot.Bot()
slack = pyBot.client

app = Flask(__name__)


def _event_handler(event_type, slack_event):
    """
    Función que ayuda a redirigir los eventos de Slack al Bot.

    ----------
    event_type: [str] tipo de evento que se recibe desde Slack.
    slack_event: [dict] respuesta en JSON de una acción en Salck

    ----------
    [obj] Objeto con la respuesta.

    """
    print(slack_event)
    team_id = slack_event['team_id']
    event = slack_event['event']
    # Cambia aquí por el ID de tu bot
    bot_id = 'U87FY8Q0L'
    # TODO: Filter channel to main.
    if event_type == 'member_joined_channel':
        user_id = event['user']
        pyBot.onboarding_message(team_id, user_id)
        return make_response('Mensaje de bienvenida enviado.', 200,)

    elif event_type == 'member_left_channel':
        user_id = event['user']
        pyBot.leaving_channel_message(user_id)

    # Evento - mensaje compartido.
    # Si el usuario ha compartido el mensaje de bienvenida, el tipo de
    # evento será 'message'. Pero también hay que revisar que el mensaje
    # en efecto sea compartido si encontramos la bandera 'is_shared'.
    elif event_type == 'message' and event.get("attachments"):
        user_id = event['user']
        if event['attachments'][0]['is_share']:
            pyBot.update_share(team_id, user_id)
            return make_response(
                'Mensaje de bienvenida actualizado con mensaje compartido',
                200,
            )

    # Evento - Reacción agregada.
    elif event_type == 'reaction_added':
        user_id = event['user']
        pyBot.update_emoji(team_id, user_id)
        return make_response(
            'Mensaje de bienvenida actualizado con un emoji',
            200,
        )

    # Evento - Mensaje fijado.
    elif event_type == 'pin_added':
        user_id = event.get('user')
        pyBot.update_pin(team_id, user_id)
        return make_response(
            'Mensaje de bienvenida actualizado y fijado',
            200,
        )

    # Evento - mensaje directo al bot
    elif event_type == 'message' and event.get('text', '').find('<@{}>'.format(bot_id)) != -1:
        # ¡Están llamando al bot directamente!
        greetings_test = ['hola', 'hello']
        user_id = event.get('user')
        if any(word in event.get('text').lower() for word in greetings_test):
            pyBot.simple_response_message(user_id, event.get('channel'), 'Hola!')
        elif 'donde está tu código' in event.get('text').lower():
            pyBot.simple_response_message(user_id, event.get('channel'), 'https://github.com/esmono/simple-slack-bot')
        else:
            pyBot.simple_response_message(user_id, event.get('channel'), 'No entiendo tu QUERY <¡ O.o ¡>')

    # Evento - No controlado.
    message = 'El evento `{}` no es manejado '.format(event_type)
    return make_response(message, 200, {'X-Slack-No-Retry': 1})


@app.route('/listening', methods=['GET', 'POST'])
def hears():
    """
    Este es la ruta principal donde el bot estará escuchando los eventos
    de Slack.
    _event_handler será el responsable de manejar los eventos y llamar al bot.
    """
    slack_event = json.loads(request.data)

    # Slack - Verificación de la URL.
    # Usamos un apartado especial para manejar la verificación de los endponits
    # por parte de Slack.
    # Más información en: https://api.slack.com/events/url_verification
    if 'challenge' in slack_event:
        return make_response(
            slack_event.get('challenge'),
            200,
            {'content_type': 'application/json'}
        )

    # Slack - Verificación del token.
    # We can verify the request is coming from Slack by checking that the
    # verification token in the request matches our app's settings
    if pyBot.verification != slack_event.get('token'):
        message = 'Token de verificación inválido.'
        # El encabezado "X-Slack-No-Retry" : 1 le dice a Slack que no debe de
        # intentar reenviar la petición.
        make_response(message, 403, {'X-Slack-No-Retry': 1})

    # Evento - Manejamos los eventos de slack
    if 'event' in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)
    # Manejamos las respuestas que no sean de eventos.
    return make_response(
        '¡NO ES UN EVENTO DE SLACK!',
        404,
        {'X-Slack-No-Retry': 1}
    )


@app.route('/thanks', methods=['GET'])
def thanks():
    """
    Esta ruta es llamada por Slack después de que un usuario instala la
    aplicación. Aceptará el código temporal para manejar la autorización
    OAuth.
    """
    print(request.args)
    code_arg = request.args['code']
    if not pyBot.auth(code_arg):
        return make_response(
            'Hubo un error al autorizar la aplicación.',
            500,
            {'X-Slack-No-Retry': 1}
        )
    return make_response(
        'Gracias por Aceptar al BOT',
        200,
        {'X-Slack-No-Retry': 1}
    )


if __name__ == '__main__':
    app.run(debug=True)
