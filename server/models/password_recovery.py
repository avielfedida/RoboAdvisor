from app.extensions import db


class PasswordRecovery(db.Model):
    # Define the table name
    __tablename__ = 'passwords_recovery'

    # Set columns for the table
    id = db.Column(db.String, primary_key=True)
    member_email = db.Column(db.String, db.ForeignKey('members.email'), nullable=False)
    is_used = db.Column(db.Boolean, default=False)
