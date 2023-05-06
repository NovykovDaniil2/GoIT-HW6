from mongoengine import Document
from mongoengine.fields import StringField, BooleanField

class Users(Document):
    fullname = StringField()
    profession = StringField()
    phone = StringField()
    email = StringField()
    sms_mailed = BooleanField(default=False)
    email_mailed = BooleanField(default=False)
    mailing_prefer = StringField()


