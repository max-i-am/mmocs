from flask import session, render_template, redirect, url_for
from app import app
from flask_login import login_required, current_user

# Initial route showing the positions if logged in. Otherwise user is redirected to login
@app.route('/')
@app.route('/index')
@login_required
def index():
    positions = current_user.positions
    return render_template('index.html', title="Positions", positions=positions)

# Route for the chat for a given position. Can only be accessed if logged in and position is assigned
@app.route('/position/<positionlink>')
@login_required
def chats(positionlink):
    positions = current_user.positions
    session['name'] = ''
    session['position'] = ''
    session['role'] = ''
    session['loops'] = {}

    if any(position.name == positionlink for position in positions):

        session['name'] = current_user.username
        session['position'] = positionlink

        for position in positions:
            if position.name == positionlink:
                role = position.role
                session['role'] = role.name
                role_loops = role.loops

                for role_loop in role.loops:
                    session['loops'][role_loop.loop.name] = [role_loop.full_access, False]

                return render_template('chat.html', title="Chat", position=position.name, role=role.name,
                                       role_loops=role_loops)

    else:
        return redirect(url_for('index'))
