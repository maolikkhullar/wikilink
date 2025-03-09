from database import db

class WikipediaDB(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    date_added = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'date_added': self.date_added,
            'user_id': self.user_id
        }