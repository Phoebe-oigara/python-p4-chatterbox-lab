from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    message_list = []
    for message in messages:
        message_list.append({
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(message_list)

@app.route('/messages/<int:id>', methods=['GET'])
def get_message_by_id(id):
    message = Message.query.get(id)
    if message:
        message_data = {
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(message_data)
    else:
        return jsonify({'error': 'Message not found'}), 404

@app.route('/messages', methods=['POST'])
def create_message():
    body = request.json.get('body')
    username = request.json.get('username')
    if body and username:
        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Message created successfully'}), 201
    else:
        return jsonify({'error': 'Missing body or username in request'}), 400
    
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if message:
        body = request.json.get('body')
        if body:
            message.body = body
            db.session.commit()
            return jsonify({'message': 'Message updated successfully'})
        else:
            return jsonify({'error': 'Missing body in request'}), 400
    else:
        return jsonify({'error': 'Message not found'}), 404
    
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'})
    else:
        return jsonify({'error': 'Message not found'}), 404


if __name__ == '__main__':
    app.run(port=5555)
