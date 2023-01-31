from app import db
from app.models import User, Position, Role, Loop, RoleLoops, Message
from datetime import datetime, timedelta
from uuid import uuid4

"""
Script to create sample users, positions, roles, loops, and messages
Usage:
1. Delete old database if available
2. Execute create_dummy_data.py to create the database with db.create_all() and fill the database with sample data
"""

PASSWORD = "2simple"
USERS = ["developer", "maxi", "insa", "anna", "thomas", "maika"]
POSITIONS = [("frontend-developer", "Position for frontend-developer"),
             ("backend-developer", "Position for backend-developer"),
             ("payload-engineer", "Position for payload-engineer"),
             ("system-engineer", "Position for system-engineer"),
             ("electrician", "Position for electrician"),
             ("technician", "Position for technician")]
ROLES = [("r-developer", "Role for developer"), ("r-engineer", "Role for engineer"),
         ("r-electrician", "Role for electrician"), ("r-technician", "Role for technician")]
LOOPS = [("Loop1", "Main loop"), ("Loop2", "Loop for engineers"),
         ("Loop3", "Loop for electricians"), ("Loop4", "Loop for technicians")]
MESSAGES = [("@backend-developer Houston, we have a problem!", "frontend-developer"),
            ("@technician That's one small step for a man, one giant leap for mankind.", "payload-engineer"),
            ("@frontend-developer I see earth! It is so beautiful.", "electrician"),
            ("Across the sea of space, the stars are other suns.", "technician"),
            ("@frontend-developer The universe is under no obligation to make sense to you.", "backend-developer"),
            ("@electrician Planets move in ellipses with the sun at one focus.", "system-engineer")]


def insert_data():
    create_users(USERS)
    create_positions(POSITIONS)
    create_roles(ROLES)
    create_loops(LOOPS)
    create_assocs_up(USERS, POSITIONS)
    create_assocs_pr(POSITIONS)
    create_assocs_rl(ROLES, LOOPS)
    create_dummy_messages(LOOPS, MESSAGES)


def create_users(users):
    for user in users:
        u = User(username=user)
        u.set_password(PASSWORD)
        db.session.add(u)
    db.session.commit()


def create_positions(positions):
    for position in positions:
        p = Position(name=position[0], description=position[1])
        db.session.add(p)
    db.session.commit()


def create_roles(roles):
    for role in roles:
        r = Role(name=role[0], description=role[1])
        db.session.add(r)
    db.session.commit()


def create_loops(loops):
    for loop in loops:
        l = Loop(name=loop[0], description=loop[1])
        db.session.add(l)
    db.session.commit()


def create_assocs_up(users, positions):
    for user in users:
        if user == "developer":
            for position in positions:
                u = User.query.filter_by(username=user).first()
                p = Position.query.filter_by(name=position[0]).first()
                u.add_position(p)
                db.session.commit()
        elif user == "maxi":
            u = User.query.filter_by(username=user).first()
            p = Position.query.filter_by(name="payload-engineer").first()
            u.add_position(p)
            db.session.commit()
        elif user == "insa":
            u = User.query.filter_by(username=user).first()
            p = Position.query.filter_by(name="electrician").first()
            u.add_position(p)
            db.session.commit()
        elif user == "anna":
            u = User.query.filter_by(username=user).first()
            p = Position.query.filter_by(name="technician").first()
            u.add_position(p)
            db.session.commit()
        elif user == "thomas":
            u = User.query.filter_by(username=user).first()
            p = Position.query.filter_by(name="system-engineer").first()
            u.add_position(p)
            db.session.commit()
        elif user == "maika":
            u = User.query.filter_by(username=user).first()
            p = Position.query.filter_by(name="backend-developer").first()
            u.add_position(p)
            db.session.commit()
        else:
            print("WARNING: User without Positions defined!")
            break


def create_assocs_pr(positions):
    for position in positions:
        if position[0] == "frontend-developer" or position[0] == "backend-developer":
            p = Position.query.filter_by(name=position[0]).first()
            r = Role.query.filter_by(name="r-developer").first()
            p.add_role(r)
            db.session.commit()
        elif position[0] == "payload-engineer" or position[0] == "system-engineer":
            p = Position.query.filter_by(name=position[0]).first()
            r = Role.query.filter_by(name="r-engineer").first()
            p.add_role(r)
            db.session.commit()
        elif position[0] == "electrician":
            p = Position.query.filter_by(name=position[0]).first()
            r = Role.query.filter_by(name="r-electrician").first()
            p.add_role(r)
            db.session.commit()
        elif position[0] == "technician":
            p = Position.query.filter_by(name=position[0]).first()
            r = Role.query.filter_by(name="r-technician").first()
            p.add_role(r)
            db.session.commit()
        else:
            print("WARNING: Position without Role defined!")
            break


def create_assocs_rl(roles, loops):
    for role in roles:
        if role[0] == "r-developer":
            for loop in loops:
                r = Role.query.filter_by(name=role[0]).first()
                l = Loop.query.filter_by(name=loop[0]).first()
                rl = RoleLoops()
                rl.set_access(True)
                rl.set_loop(l)
                r.add_loop(rl)
                db.session.commit()
        elif role[0] == "r-engineer":
            r = Role.query.filter_by(name=role[0]).first()
            l = Loop.query.filter_by(name="Loop2").first()
            rl = RoleLoops()
            rl.set_access(True)
            rl.set_loop(l)
            r.add_loop(rl)
            db.session.commit()
            set_main_loop_monitor(role[0])
        elif role[0] == "r-electrician":
            r = Role.query.filter_by(name=role[0]).first()
            l = Loop.query.filter_by(name="Loop3").first()
            rl = RoleLoops()
            rl.set_access(True)
            rl.set_loop(l)
            r.add_loop(rl)
            db.session.commit()
            set_main_loop_monitor(role[0])
        elif role[0] == "r-technician":
            r = Role.query.filter_by(name=role[0]).first()
            l = Loop.query.filter_by(name="Loop4").first()
            rl = RoleLoops()
            rl.set_access(True)
            rl.set_loop(l)
            r.add_loop(rl)
            db.session.commit()
            set_main_loop_monitor(role[0])
        else:
            print("WARNING: Role without loops defined!")
            break


def set_main_loop_monitor(role):
    r = Role.query.filter_by(name=role).first()
    l = Loop.query.filter_by(name="Loop1").first()
    rl = RoleLoops()
    rl.set_access(False)
    rl.set_loop(l)
    r.add_loop(rl)
    db.session.commit()


def create_dummy_messages(loops, messages):
    for loop in loops:
        if loop[0] == "Loop1":
            l = Loop.query.filter_by(name=loop[0]).first()
            for i in range(6):
                time = datetime.utcnow().replace(microsecond=0) - timedelta(hours=i)
                uuid = uuid4().hex
                m = Message(message_id=uuid, message=messages[0][0], timestamp=time, author=messages[0][1], loop=l)
                db.session.add(m)
                db.session.commit()

            for i in range(6):
                time = datetime.utcnow().replace(microsecond=0) - timedelta(hours=i)
                uuid = uuid4().hex
                m = Message(message_id=uuid, message=messages[4][0], timestamp=time, author=messages[4][1], loop=l)
                db.session.add(m)
                db.session.commit()

        elif loop[0] == "Loop2":
            l = Loop.query.filter_by(name=loop[0]).first()
            time = datetime.utcnow().replace(microsecond=0) - timedelta(hours=1)
            uuid1 = uuid4().hex
            m = Message(message_id=uuid1, message=messages[1][0], timestamp=time, author=messages[1][1], loop=l)
            db.session.add(m)
            uuid2 = uuid4().hex
            m = Message(message_id=uuid2, message=messages[5][0], timestamp=time, author=messages[5][1], loop=l)
            db.session.add(m)
            time = datetime.utcnow().replace(microsecond=0) - timedelta(hours=2)
            uuid3 = uuid4().hex
            m = Message(message_id=uuid3, message=messages[0][0], timestamp=time, author=messages[0][1], loop=l)
            db.session.add(m)
            db.session.commit()

        elif loop[0] == "Loop3":
            l = Loop.query.filter_by(name=loop[0]).first()
            time = datetime.utcnow().replace(microsecond=0) - timedelta(hours=1)
            uuid1 = uuid4().hex
            m = Message(message_id=uuid1, message=messages[2][0], timestamp=time, author=messages[2][1], loop=l)
            db.session.add(m)
            time = datetime.utcnow().replace(microsecond=0) - timedelta(hours=2)
            uuid2 = uuid4().hex
            m = Message(message_id=uuid2, message=messages[0][0], timestamp=time, author=messages[0][1], loop=l)
            db.session.add(m)
            db.session.commit()

        elif loop[0] == "Loop4":
            l = Loop.query.filter_by(name=loop[0]).first()
            time = datetime.utcnow().replace(microsecond=0) - timedelta(hours=1)
            uuid1 = uuid4().hex
            m = Message(message_id=uuid1, message=messages[3][0], timestamp=time, author=messages[3][1], loop=l)
            db.session.add(m)
            time = datetime.utcnow().replace(microsecond=0) - timedelta(hours=2)
            uuid2 = uuid4().hex
            m = Message(message_id=uuid2, message=messages[0][0], timestamp=time, author=messages[0][1], loop=l)
            db.session.add(m)
            db.session.commit()

        else:
            print("WARNING: This Loop is not defined yet!")
            break


def database_error():
    db.session.rollback()


if __name__ == "__main__":
    db.create_all()
    insert_data()
    #database_error()
