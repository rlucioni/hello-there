import os
from time import sleep

import requests
from flask import abort, Flask, jsonify, request
from zappa.async import task


app = Flask(__name__)


def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']

    return is_token_valid and is_team_id_valid


@task
def hello_there_task(response_url):
    sleep(5)

    data = {
        'response_type': 'in_channel',
        'text': 'You _are_ a bold one.',
    }

    requests.post(response_url, json=data)


@app.route('/hello-there', methods=['POST'])
def hello_there():
    if not is_request_valid(request):
        abort(400)

    hello_there_task(request.form['response_url'])

    return jsonify(
        response_type='in_channel',
        text='<https://youtu.be/frszEJb0aOo|General Kenobi!>',
    )
