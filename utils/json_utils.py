import datetime
import collections

__author__ = 'alexanderventura'


def serialize(sql_alchemy_model):

    def is_date(column):
        column_ptype = column.type.python_type
        check = column_ptype is datetime.datetime
        return check

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


def serialize_collection(collection):
    return [serialize(model) for model in collection]


def to_json(f):

    def handle_object(*args, **kwargs):
        sql_alchemy_model = f(*args, **kwargs)

        if isinstance(sql_alchemy_model, collections.Iterable):
            return serialize_collection(sql_alchemy_model)
        return serialize(sql_alchemy_model)

    return handle_object
