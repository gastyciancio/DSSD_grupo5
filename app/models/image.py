from sqlalchemy import Column, ForeignKey, Integer
from app.db import db
from werkzeug.utils import secure_filename

class Image(db.Model):
    __tablename__="image_table"
    id = db.Column(db.Integer,primary_key=True)
    img = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    coleccion_id = Column(Integer, ForeignKey("coleccion_table.id"))

    @staticmethod
    def save_images(images, coll_id):

        images_to_save = []

        for image in images:
            filename = secure_filename(image.filename)
            is_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

            if is_allowed:
                new_image = Image(img=image.read(), mimetype=image.mimetype, name=filename, coleccion_id=coll_id)
                images_to_save.append(new_image)

        db.session.add_all(images_to_save)
        db.session.commit()

