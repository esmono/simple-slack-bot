# Let's create a BOT 🤖
# Test emoji :robot:


### Alcance de la aplicación.
Crear un bot que pueda reaccionar a diferentes eventos en slack.
:smiling_imp:

### Instalación.
Se necesitan las siguiente variables de entorno:
CLIENT_ID="XXXXXXXXXX.XXXXXXXXXXXX"
CLIENT_SECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
VERIFICATION_TOKEN="XXXXXXXXXXXXXXXXXXXXXXXXX"

Estas credenciales se encuentran en:
Slack API -> APP -> Basic Information -> App Credentials.


Se probó con Python 3.6
Para instalar las librerías de python:
pip install -r requirements.txt


Hay que crear una aplicacion de Slack.
Y hay que agregar la aplicación al slack con un botón!
[-> Botón <-](https://api.slack.com/docs/slack-button#add_the_slack_button)

Importar el repositorio.
git clone git@github.com:esmono/simple-slack-bot.git
// Opcional crear un ambiente virtual
mkvirtualenv --python=/usr/bin/python3.6 bot-chicken
// Instalar los requerimientos (Dentro de la carpeta recién creada)
pip install -r requirements.txt

NOTA: IMPORTANTE! Como no se guarda información hay variables que se almacenan en la instancia de la aplicación,
es importante tenerlo en cuenta para las pruebas.

Podemos usar [https://ngrok.com/](https://ngrok.com/) para crear un tunel entre slack y nuestro localhost.


### First we need the follow things.
- A [Free Heroku account](https://www.heroku.com/) (and [Heroky toolbelt - or CLI tools](https://devcenter.heroku.com/articles/heroku-cli)).
- A Slack team.
- A github account :octocat:.
- Python / JavaScript knowledge.
- Some time :clock1:.

### Create a Slack App.
Let's go to [Slack Api Page](https://api.slack.com/) and hit the Start Building button (Or create new app). It should ask for name and slack workspace.

We need to add one security scope in "OAuth & Permissions".
And add a "Bot Users".

Keep in mind: Slack API have a great github page [https://github.com/slackapi](https://github.com/slackapi)


### Python.
We should use https://github.com/slackapi/python-slackclient
