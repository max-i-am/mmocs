from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


# Table to create the connection between users and positions
user_positions = db.Table('user_positions',
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                          db.Column('position_id', db.Integer, db.ForeignKey('position.id'))
                          )


# Model describing a user with id, username, password and positions
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    positions = db.relationship('Position', secondary=user_positions)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_position(self, position):
        if not self.is_assigned(position):
            self.positions.append(position)

    def is_assigned(self, position):
        return self.query.join(user_positions).filter((user_positions.c.user_id == self.id) &
                                                      (user_positions.c.position_id == position.id)).count() > 0


# Allowing Flask to load the user based on the id 
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Model describing a position with id, name, description and the assigned role
class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=True)
    description = db.Column(db.String(140))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='positions')

    def __repr__(self):
        return '<Position: {}>'.format(self.name)

    def add_role(self, role):
        if not self.role_id and not self.role:
            self.role_id = role.id
            self.role = role


# Model describing the connection between roles, loops and the specified rights
class RoleLoops(db.Model):
    __tablename__ = 'role_loops'
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    loop_id = db.Column(db.Integer, db.ForeignKey('loop.id'), primary_key=True)
    full_access = db.Column(db.Boolean, default=False)
    loop = db.relationship("Loop")

    def set_access(self, boolean):
        self.full_access = boolean

    def set_loop(self, loop):
        self.loop = loop


# Model describing a role with id, name, description, assigned positions and loops
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=True)
    description = db.Column(db.String(140))
    positions = db.relationship('Position', back_populates='role')
    loops = db.relationship(RoleLoops)

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

    def add_loop(self, role_loop):
        if not self.is_assigned(role_loop):
            self.loops.append(role_loop)

    def is_assigned(self, role_loop):
        return self.query.join(RoleLoops).filter((RoleLoops.role_id == self.id) &
                                                 (RoleLoops.loop_id == role_loop.loop.id)).count() > 0


# Model describing a loop with id, name, description and messages
class Loop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=True)
    description = db.Column(db.String(140))
    messages = db.relationship('Message', backref='loop')

    def __repr__(self):
        return '<Loop: {}>'.format(self.name)

    def append_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages


# Model describing a message with an internal id, an additional message id, message text, timestamp, author and loop
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String, index=True, unique=True)
    message = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author = db.Column(db.String)
    loop_id = db.Column(db.Integer, db.ForeignKey('loop.id'))

    def __repr__(self):
        return '<Message: {}, {}, {}>'.format(self.loop, self.author, self.message)

    def get_message_id(self):
        return self.message_id

    def get_content(self):
        return self.message

    def get_timestamp(self):
        return self.timestamp

    def get_author(self):
        return self.author
