from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

link = db.Table('link',
    db.Column('acc_id', db.Integer, db.ForeignKey('accounts.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)


class Journal(db.Model):
    __tablename__ = 'journals'
    idJ = db.Column(db.Integer, primary_key=True)
    entryJ = db.Column(db.String(400))
    locJ = db.Column(db.String(50))
    entry_date = db.Column(db.DateTime)
    idGrp = db.Column(db.Integer, db.ForeignKey('groups.id'))
    member = db.Column(db.String(20))
    def __repr__(self):
        return '\nID: {}\nEntry: {}\nLocation: {}\nEntry Date: {}\nGroup ID: {}\nMember: {}\n'.format(self.idJ, self.entryJ, self.locJ, self.entry_date, self.idGrp, self.member)


class Account(db.Model, UserMixin):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(30))
    date_created = db.Column(db.DateTime)
    def __repr__(self):
        return '\nID: {}\nUsername: {}\nEmail: {}\nPassword: {}\nDate Created: {}\n'.format(self.id, self.username, self.email, self.password, self.date_created)

@login_manager.user_loader
def load_user(id):
    return Account.query.get(int(id))


class Group(db.Model, UserMixin):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    groupName = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    date_created = db.Column(db.DateTime)
    accs = db.relationship("Account", secondary=link, backref='groups')
    entries = db.relationship("Journal", backref='group')
    def __repr__(self):
        return '\nID: {}\nGroup Name: {}\nPassword: {}\nDate Created: {}\nMembers: {}\n'.format(self.id, self.groupName, self.password, self.date_created, self.accs)