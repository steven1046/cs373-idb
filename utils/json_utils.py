import datetime

__author__ = 'alexanderventura'


def to_json(f):
    def is_date(column):
        column_ptype = column.type.python_type
        check = column_ptype is datetime.datetime
        return check

    def serialize(*args, **kwargs):
        sql_alchemy_model = f(*args, **kwargs)
        if sql_alchemy_model is None:
            return {}
        else:
            sql_alchemy_columns = sql_alchemy_model.__class__.__table__.columns

            columns = [c.key for c in sql_alchemy_columns]
            jsonable = {c: getattr(sql_alchemy_model, c) for c in columns}
            date_columns = [c.key for c in filter(is_date, sql_alchemy_columns)]

        for c in date_columns:
            jsonable[c] = str(jsonable[c])

        return jsonable
    return serialize
