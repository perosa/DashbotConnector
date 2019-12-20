from flask import Flask, request, Response
import logging
import pyfiglet
import requests
import os

try:
    app = Flask(__name__)

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
except Exception as e:
    logging.exception("Error at startup")


@app.route('/ping')
def ping():
    """
    Ping the endpoint
    :return:
    """
    logging.info('/ping')
    return "ping Ok"


@app.route('/send', methods=['POST'])
def send_to_dashbot():
    """
    Endpoint
    :return:
    """
    try:
        logging.info('send/')

        # validate(request)

        platform = 'google'
        version = '11.1.0-rest'
        api_key = request.headers['API_KEY']
        type = 'incoming'

        payload = request.get_json()
        headers = {'Content-Type': 'application/json'}

        if api_key is None:
            logging.warning("API_KEY is undefined")
            return "Not sent: API_KEY is undefined"
        else:
            p = {'platform': platform, 'v': version, 'type': type, 'apiKey': api_key}
            r = requests.post("https://tracker.dashbot.io/track", params=p, json=payload, headers=headers)
            logging.info(r)
            return "ok"

    except Exception as e:
        logging.exception("Unexpected error")
        return Response(str(e), status=500)


def validate(request):
    token = os.getenv('DASHBOT_TOKEN', 'tokenUndefined')
    logging.info(token)

    header = request.headers['Authorization']
    logging.info(header)

    if header == None or (header != 'Bearer ' + token):
        raise Exception('Invalid token {} '.format(header))


def get_port():
    """
    Retrieves port
    :return:
    """
    return int(os.environ.get("PORT", 5000))


if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("Dashbot Agent")
    print(ascii_banner)

    logging.info('Starting up')

    app.run(debug=True, port=get_port(), host='0.0.0.0')
