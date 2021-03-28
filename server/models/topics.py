from app.extensions import db
from sqlalchemy.orm import relationship
import datetime


class Topic(db.Model):
    # Define the table name
    __tablename__ = 'topics'

    # Set columns for the table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column('title', db.String)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow)
    member_email = db.Column('member_email', db.String, db.ForeignKey('members.email'), nullable=False)
    cluster_title = db.Column('cluster_title', db.String, db.ForeignKey('clusters.title'), nullable=False)
    messages = relationship("Message", backref='topic')

    def as_dict(self):
        topic_as_dict = {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.strftime('%m-%d-%Y'),
            'cluster_title': self.cluster_title,
            'member_email': self.member_email
        }
        return topic_as_dict

