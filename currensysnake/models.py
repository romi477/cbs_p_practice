from peewee import (SqliteDatabase, Model, IntegerField, DoubleField,
                    DateTimeField, datetime as peewee_datetime)


db = SqliteDatabase('currency_snake.db')

class BaseModel(Model):
    class Meta:
        database = db


class XRate(BaseModel):
    class Meta:
        db_table = 'xrates'
        indexes = (
            (('from_currency', 'to_currency'), True),
        )

    from_currency = IntegerField()
    to_currency = IntegerField()
    rate = DoubleField()
    updated = DateTimeField(default=peewee_datetime.datetime.now())

    def __repr__(self):
        return f'XRate <{self.from_currency} --> {self.to_currency}, {self.rate}>'
