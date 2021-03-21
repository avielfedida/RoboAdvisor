from app.extensions import db
import datetime


class Message(db.Model):
    # Define the table name
    __tablename__ = 'messages'

    # Set columns for the table
    id = db.Column( db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow)
    content = db.Column('content', db.JSON, nullable=False)
    member_email = db.Column('member_email', db.String, db.ForeignKey('members.email'), nullable=False)
    topic_id = db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), nullable=False)

    def as_dict(self):
        message_as_dict = {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.strftime('%m-%d-%Y'),
            'topic_id': self.topic_id,
            'member_email': self.member_email
        }
        return message_as_dict
