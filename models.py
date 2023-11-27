from main import db


class Medecine(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(255), nullable=False)
     price = db.Column(db.Float, nullable=False)
     text = db.Column(db.Text, nullable=False)
     item_image_path = db.Column(db.String(255), nullable=False, )