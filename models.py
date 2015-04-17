import datetime
from flask import url_for
from config import db

class Object(db.Document):
    name = db.StringField(max_length=255, required=True)
    description = db.StringField(max_length=255, required=True)
    tags = db.ListField(db.ReferenceField('Tag'))

    def get_absolute_url(self):
        return url_for('object', kwargs={"slug": self.name})

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

class Tag(db.EmbeddedDocument):
    name = db.StringField(max_length=255, required=True)
    description = db.StringField(max_length=255, required=True)
    tags = db.ListField(db.ReferenceField('Object'))

    def get_absolute_url(self):
        return url_for('tag', kwargs={"slug": self.name})
