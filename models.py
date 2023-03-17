from datetime import datetime

from mongoengine import EmbeddedDocument, Document, CASCADE
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField, ReferenceField

# Create the models
class Authors(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quotes(Document):
    tags = ListField()
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField()
    