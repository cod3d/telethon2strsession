from peewee import Model, CharField, IntegerField, BlobField


class Session(Model):
    dc_id = IntegerField(primary_key=True)
    server_address = CharField(null=True)
    port = IntegerField(null=True)
    auth_key = BlobField(null=True)
    takeout_id = IntegerField(null=True)
