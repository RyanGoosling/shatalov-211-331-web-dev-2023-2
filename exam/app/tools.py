import hashlib
import uuid
import os
from werkzeug.utils import secure_filename
from models import Image
from app import db, app
import sqlalchemy as sa


class ImageSaver:
    def __init__(self, file):
        self.file = file

    def save(self):
        self.img = self.__find_by_md5_hash()
        if self.img is not None:
            return self.img
        file_name = secure_filename(self.file.filename)
        self.img = Image(
            id=str(uuid.uuid4()),
            file_name=file_name,
            mime_type=self.file.mimetype,
            md5_hash=self.md5_hash)
        try:
            self.file.save(
                os.path.join(app.config['UPLOAD_FOLDER'],
                            self.img.storage_filename))
            db.session.add(self.img)
            db.session.commit()
        except sa.exc.SQLAlchemyError:
            db.session.rollback()
            return None
        except:
            db.session.delete(self.img)
            db.session.commit()
            return None
        return self.img

    def __find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return Image.query.filter(Image.md5_hash == self.md5_hash).first()
    
class ImageDeleter:
    def __init__(self, img):
        self.img = img #img - Image

    def delete(self, n: int):
        """Удалит обложку из хранилища и бд, если её используют n книг"""
        try:
            if len(self.img.books) == n:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],
                                self.img.storage_filename))
                db.session.delete(self.img)
            db.session.commit()
        except sa.exc.SQLAlchemyError:
            db.session.rollback()