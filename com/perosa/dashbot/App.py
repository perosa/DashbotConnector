from flask import Flask, request, Response
import logging
import pyfiglet
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('werkzeug').setLevel(logging.ERROR)


@app.route('/ping')
def index():
    logging.info('/ping')
    return "ping Ok"


@app.route('/send', methods=['POST'])
def send_to_dashbot():
    try:
        logging.info('send/')

        platform = 'google'
        version = '11.1.0-rest'
        api_key = request.args.get('apiKey')
        type = request.args.get('type')

        payload = request.get_json()
        headers = {'Content-Type': 'application/json'}

        p = {'platform': platform, 'v': version, 'type': type, 'apiKey': api_key}
        r = requests.post("https://tracker.dashbot.io/track", params=p, json=payload, headers=headers)

        logging.info(r)

        return "ok"

    except Exception as e:
        logging.error('Error {}'.format(str(e)))
    return Response(str(e), status=500)


if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("Dashbot Agent")
    print(ascii_banner)

    logging.info('Starting up')

    app.run(port=5000, host='0.0.0.0')
