from app.extensions import db
from sqlalchemy.orm import relationship


class Cluster(db.Model):
    # Define the table name
    __tablename__ = 'clusters'

    # Set columns for the table
    title = db.Column('title', db.String, primary_key=True)
    description = db.Column('description', db.String)
    topics = relationship("Topic", backref='cluster')

    def as_dict(self):
        cluster_as_dict = {
            'title': self.title,
            'description': self.description,
        }
        return cluster_as_dict
