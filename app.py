from flask import Flask, request, jsonify
from telethon import TelegramClient, sync
import os

app = Flask(__name__)

# Retrieve environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Load the session file
client = TelegramClient('session_name', api_id, api_hash)

@app.route('/search_user', methods=['GET'])
async def search_user():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    try:
        await client.start()
        user = await client.get_entity(username)
        user_details = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'id': user.id
        }
        await client.disconnect()
        return jsonify(user_details), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
