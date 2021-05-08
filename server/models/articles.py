from app.extensions import db


class Article(db.Model):
    # Define the table name
    __tablename__ = 'articles'

    # Set columns for the table
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    title = db.Column('title', db.String)
    description = db.Column('description', db.String)
    file = db.Column('file', db.String)

    def as_dict(self):
        article_as_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'file': self.file
        }
        return article_as_dict
