from database import db

class Tags(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(255), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('wikipedia_db.id', ondelete='CASCADE'), nullable=False)