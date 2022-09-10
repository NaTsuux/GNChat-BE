from datetime import datetime

from sqlalchemy.dialects.mysql import DATETIME

from gnchat.orm import db


class BaseModel(db.Model):
    __abstract__ = True
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return "<{}, id={}>".format(self.__class__, self._id)

    @classmethod
    def get_item(cls, order_by=None, **kwargs):
        result = cls.query.filter_by(**kwargs)
        if order_by:
            result = result.order_by(order_by)
        return result.first()

    def get_items(self, limit=0, order_by=None, **kwargs):
        result = self.query.filter_by(**kwargs)
        if order_by:
            result = result.order_by(order_by)
        if limit:
            result = result.limit(limit)
        return result.all()

    @classmethod
    def insert_item(cls, record):
        if not isinstance(record, cls):
            raise Exception()  # TODO if valid and exception needs more detail
        db.session.add(record)
        db.session.commit()

    def delete_self(self):
        db.session.delete(self)
        db.session.commit()

    def update_item(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        db.session.commit()


class UserModel(BaseModel):
    __tablename__ = 'user'

    user_uuid = db.Column(db.String(36), unique=True, nullable=False, index=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(16), nullable=False)
    latest_read = db.Column(DATETIME(fsp=3), default=datetime.fromtimestamp(0))
    register_time = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def get_user(cls, user_uuid):
        return cls.get_item(user_uuid=user_uuid)

    def to_dict(self):
        return {
            'user_uuid': self.user_uuid,
            'username': self.username,
            'register_time': self.register_time.timestamp()
        }


class MessageModel(BaseModel):
    __tablename__ = 'message'

    message_uuid = db.Column(db.String(36), unique=True, nullable=False)
    is_picture = db.Column(db.Boolean, default=False)
    content = db.Column(db.String(256))
    owner_uuid = db.Column(db.String(36), db.ForeignKey("user.user_uuid"))
    group_id = db.Column(db.Integer, nullable=False)
    send_time = db.Column(DATETIME(fsp=3), nullable=False)

    def to_dict(self):
        return {
            "message_uuid": self.message_uuid,
            "is_picture": self.is_picture,
            "content": self.content,
            "owner_uuid": self.owner_uuid,
            "owner_name": UserModel.get_user(self.owner_uuid).username,
            "group_id": self.group_id,
            "send_time": self.send_time.timestamp(),
        }
