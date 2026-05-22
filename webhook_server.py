from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print(f"Webhook received: {data}")
        return 'OK', 200
    except Exception as e:
        print(f"Error: {e}")
        return 'Error', 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)