from app import app, socketio

if __name__ == '__main__':
    # Eventlet server
    socketio.run(app, host='0.0.0.0', port=5000, certfile='cert.pem', keyfile='key.pem')
