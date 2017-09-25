from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/")

def get_server_status():

    req_header = {"Origin": "https://developer.riotgames.com",
                  "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                  "X-Riot-Token": "RGAPI-6ac9999a-ae4c-4a74-93e4-c7bc3e6c25e8",
                  "Accept-Language": "en-US,en;q=0.8",
                  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

    url = 'https://na1.api.riotgames.com/lol/status/v3/shard-data'
    sess = requests.Session()
    html = sess.request('GET', url, headers=req_header)

    data = json.loads(html.content.decode('utf-8'))
    server_status = unidecode.unidecode(data['services'][0]['status'])
    if len(data['services'][0]['incidents']) > 0:
        issue = unidecode.unidecode(data['services'][0]['incidents'][0]['updates'][0]['content'])
    else:
        issue = None

    returnTuple = (server_status, issue)

    return returnTuple

def get_client_status():

    req_header = {"Origin": "https://developer.riotgames.com",
                  "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                  "X-Riot-Token": "RGAPI-6ac9999a-ae4c-4a74-93e4-c7bc3e6c25e8",
                  "Accept-Language": "en-US,en;q=0.8",
                  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

    url = 'https://na1.api.riotgames.com/lol/status/v3/shard-data'
    sess = requests.Session()
    html = sess.request('GET', url, headers=req_header)

    data = json.loads(html.content.decode('utf-8'))
    server_status = unidecode.unidecode(data['services'][1]['status'])
    if len(data['services'][1]['incidents']) > 0:
        issue = unidecode.unidecode(data['services'][1]['incidents'][0]['updates'][0]['content'])
    else:
        issue = None

    returnTuple = (server_status, issue)

    return returnTuple

def get_store_status():

    req_header = {"Origin": "https://developer.riotgames.com",
                  "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                  "X-Riot-Token": "RGAPI-6ac9999a-ae4c-4a74-93e4-c7bc3e6c25e8",
                  "Accept-Language": "en-US,en;q=0.8",
                  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

    url = 'https://na1.api.riotgames.com/lol/status/v3/shard-data'
    sess = requests.Session()
    html = sess.request('GET', url, headers=req_header)

    data = json.loads(html.content.decode('utf-8'))
    server_status = unidecode.unidecode(data['services'][2]['status'])
    if len(data['services'][2]['incidents']) > 0:
        issue = unidecode.unidecode(data['services'][2]['incidents'][0]['updates'][0]['content'])
    else:
        issue = None

    returnTuple = (server_status, issue)

    return returnTuple

@ask.launch
def start_skill():
    welcome_message = 'Which service would you like information on?'
    return question(welcome_message)

@ask.intent("ServerIntent")
def share_server_status():
    status = get_server_status()
    status_msg = 'The server is currently {}.'.format(status[0])
    if status[1] is not None:
        status_msg += " There is also an update. {}.".format(status[1])

    return statement(status_msg)

@ask.intent("ClientIntent")
def share_client_status():
    status = get_client_status()
    status_msg = 'The client is currently {}.'.format(status[0])
    if status[1] is not None:
        status_msg += " There is also an update. {}.".format(status[1])

    return statement(status_msg)

@ask.intent("StoreIntent")
def share_store_status():
    status = get_client_status()
    status_msg = 'The store is currently {}.'.format(status[0])
    if status[1] is not None:
        status_msg += " There is also an update. {}.".format(status[1])

    return statement(status_msg)

@ask.intent("AMAZON.StopIntent")
def no_intent():
    bye_text = "Have fun playing!"
    return statement(bye_text)

@ask.intent("AMAZON.HelpIntent")
def help_intent():
    help_text = "Unofficial League of Legends Status Checker is an Alexa skill "
    help_text += "designed to help users check the server status of League of Legends, "
    help_text += "a free MOBA video game, without having to navigate to their website. "
    help_text += "The skill also allows users to check the client and store's statuses. "
    help_text += "To continue with the skill, please choose Server, Client, or Store. "
    help_text += "Which service would you like information on?"
    return question(help_text)

if __name__ == "__main__":
    app.run(debug=True)
