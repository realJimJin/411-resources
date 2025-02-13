<<<<<<< HEAD
from flask import Flask, make_response, request
=======
from flask import Flask, make_response
>>>>>>> 6afa1ab (added screenshot of curl and flask container running)
import os

app = Flask(__name__)

@app.route('/')
def hello():
    response = make_response(
        {
            'response': 'Hello, World!',
            'status': 200
        }
    )
    return response

@app.route('/repeat', methods=['GET'])
def repeat():
    user_input = request.args.get('input', default='No input provided')  
    return {"body": user_input, "status": 200}

@app.route('/health')
@app.route('/healthcheck')
def health():
    return {"body": "OK", "status": 200}

@app.route('/hang')
def hang():
    while True:
        time.sleep(1)
    return {"status": "hanging"}


if __name__ == '__main__':
    # By default flask is only accessible from localhost.
    # Set this to '0.0.0.0' to make it accessible from any IP address
    # on your network (not recommended for production use)
   # app.run(port=5002)
<<<<<<< HEAD
    app.run(host="0.0.0.0", port=5002, threaded=False)
=======
    app.run(host="0.0.0.0", port=5002)
>>>>>>> 6afa1ab (added screenshot of curl and flask container running)
