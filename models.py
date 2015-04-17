import datetime
from flask import url_for
from config import db

class Object(db.Document):
    name = db.StringField(max_length=255, required=True, unique=True)
    description = db.StringField(required=True)
    tags = db.ListField(db.ReferenceField('Tag'))

    def get_absolute_url(self):
        return url_for('object', kwargs={"slug": self.name})

    def __unicode__(self):
        return self.title

    meta = {
        # 'allow_inheritance': True,
        # 'collection': 'objects',
        'indexes': ['-name'],
        'ordering': ['-name']
    }

class Tag(db.EmbeddedDocument):
    name = db.StringField(max_length=255, required=True, unique=True)
    description = db.StringField(required=True)
    objects = db.ListField(db.ReferenceField('Object'))

    def get_absolute_url(self):
        return url_for('tag', kwargs={"slug": self.name})


tag = Tag(name="test",description="test description")
tag.save()