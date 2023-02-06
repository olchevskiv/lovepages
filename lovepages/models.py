from . import db 
from flask_login import UserMixin 
from sqlalchemy.sql import func
from sqlalchemy import inspect

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_date = db.Column(db.DateTime(timezone=True))
    update_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    sub_title = db.Column(db.String(40))
    widgets = db.relationship("Widget", primaryjoin="Page.id == Widget.page_id")
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_date = db.Column(db.DateTime(timezone=True))
    update_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Widget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    type = db.Column(db.String(20))
    width = db.Column(db.Integer)
    index = db.Column(db.Integer)
    content = db.Column(db.Text)
    posx  = db.Column(db.Integer)
    posy = db.Column(db.Integer)

    font_size = db.Column(db.Integer)
    font_color = db.Column(db.String(50))
    font_family = db.Column(db.String(50))

    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_date = db.Column(db.DateTime(timezone=True))
    update_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class User_Page(db.Model):
    __tablename__ = 'user_page'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description =  db.Column(db.String(128))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_date = db.Column(db.DateTime(timezone=True))
    update_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User_Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_date = db.Column(db.DateTime(timezone=True))
    update_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User_Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128))
    password = db.Column(db.String(255))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_date = db.Column(db.DateTime(timezone=True))
    update_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(50))
    user_agent = db.Column(db.String(128))
    success = db.Column(db.Boolean())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(42), unique=True, nullable=False)
    display_name = db.Column(db.String(128))
    birthdate = db.Column(db.Date())
    last_login = db.Column(db.DateTime(timezone=True))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_date = db.Column(db.DateTime(timezone=True))
    update_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notes = db.relationship('Note', primaryjoin='User.id==Note.create_user_id')
    pages = db.relationship("Page", secondary="user_page",
                        primaryjoin="User.id == User_Page.user_id", secondaryjoin="Page.id == User_Page.page_id")
    active = db.Column(db.Boolean(), default=True)

   