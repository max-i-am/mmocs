import functools
from flask import session, request
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio, db
from app.models import Loop, Message
from uuid import uuid4
from datetime import datetime, timedelta
import csv

# Defines the number of hours for which messages are loaded
LOADING_PERIOD_OLD_MESSAGES = 24


# Tag to verify that only authenticated clients can send and receive messages
def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


# Initial SocketIO connect event 
@socketio.on('connect')
@authenticated_only
def connect(auth):
    print("Connected!")


# Event which registers the client with a specified loop
@socketio.on('join')
@authenticated_only
def on_join(data):
    loop = data['loop']
    if loop in session['loops']:
        join_room(loop)

        session['loops'][loop][1] = True

        # Store that somebody is listening to the room
        logging_room_entries((session['name'], session['position'], loop, "join"))


# Event triggering to load old messages from the database
@socketio.on('load-messages')
@authenticated_only
def load_messages(data):
    loops = data['loops']
    allowed_loops = session['loops'].keys()
    old_messages = dict()

    for loop in loops:
        if loop in allowed_loops:
            loop_db = Loop.query.filter_by(name=loop).first()
            time = datetime.utcnow().replace(microsecond=0) - timedelta(hours=LOADING_PERIOD_OLD_MESSAGES)

            messages_loop = db.session.query(Message).filter((Message.timestamp >= time) &
                                                          (Message.loop_id == loop_db.id)).all()

            for message in messages_loop:
                old_messages[message.get_message_id()] = (message.get_content(), message.get_author(), loop,
                                                          message.get_timestamp().isoformat())

    emit('old-messages', old_messages, to=request.sid)


# Event for sending a message to a specified loop and storing the message for on-demand retrieval
@socketio.on('message')
@authenticated_only
def handle_message(data):
    loop = data['loop']
    
    if isinstance(loop, str):
        if session['loops'].get(loop)[0]:

            message_id = uuid4().hex
            replacement_message_id = [data['tmpMessageId'],  message_id]

            # Emits the message id to the sender of the message to add to the message
            emit('ack-with-messageid', replacement_message_id, to=request.sid)

            # Set include_self to False -> The sender does not receive his own message again.
            emit('message', {'position': session['position'], 'loop': loop, 'messageid': message_id,
                             'message': data['message']}, room=loop, include_self=False)

            loop_db = Loop.query.filter_by(name=loop).first()
            message_db = Message(message_id=message_id, message=data['message'],
                                 timestamp=datetime.utcnow().replace(microsecond=0), author=session['position'],
                                 loop=loop_db)

            db.session.add(message_db)
            db.session.commit()


# Event which deregisters the user from the specified loop
@socketio.on('leave')
@authenticated_only
def on_leave(data):
    loop = data['loop']
    if loop in session['loops']:
        leave_room(loop)

        session['loops'][loop][1] = False

        # Store that somebody stopped listening to the room
        logging_room_entries((session['name'], session['position'], loop, "leave"))


# Event disconnecting the user
@socketio.on('disconnect')
@authenticated_only
def disconnect():
    for loop in session['loops']:
        if session['loops'][loop][1]:
            logging_room_entries((session['name'], session['position'], loop, "leave"))

    print("Disconnected!")


# Logging function triggered at different events to write the room log
def logging_room_entries(entry):
    data = [entry[0], entry[1], entry[2], datetime.utcnow(), entry[3]]

    with open('./roomLogging/entries.csv', 'a+', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
