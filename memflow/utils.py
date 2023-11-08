import datetime
import decimal
import json
from enum import Enum
from typing import Dict, List, _GenericAlias, Union


def _list_value(value):
    if isinstance(value, str):
        if value[0] in ['{', '[']:
            return json.loads(value)
        else:
            return value.split(',')
    else:
        return list(value)


def _dict_value(value):
    if isinstance(value, str):
        return json.loads(value)
    else:
        return value


def parse_field_value(field_value):
    if isinstance(field_value, decimal.Decimal):  # Decimal -> float
        field_value = round(float(field_value), 2)
    elif isinstance(field_value, datetime.datetime):  # datetime -> str
        field_value = str(field_value)
    elif isinstance(field_value, list):
        field_value = [parse_field_value(i) for i in field_value]
    if hasattr(field_value, 'to_json'):
        field_value = field_value.to_json()
    elif isinstance(field_value, Enum):
        field_value = field_value.name
    elif isinstance(field_value, Dict):
        val = {}
        for key_ in field_value:
            val[key_] = parse_field_value(field_value[key_])
        field_value = val
    return field_value


def parse_value(func, value, default_value=None):
    if value is not None:
        if func == bool:
            if value in (1, True, "1", "true"):
                return True
            elif value in (0, False, "0", "false"):
                return False
            else:
                raise ValueError(value)

        elif func in (int, float):
            try:
                if isinstance(value, str):
                    value = value.replace(',', '')
                return func(value)
            except ValueError:
                return float('nan')
        elif func == datetime.datetime:
            if isinstance(value, datetime.datetime):
                return value
            elif isinstance(value, str):
                if value:
                    return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                else:
                    return None
            else:
                return None
        elif func in [Dict, dict]:
            return _dict_value(value)
        elif func in [List, list]:
            return _list_value(value)
        elif isinstance(func, _GenericAlias):
            if func.__origin__ in [List, list]:
                list_ = _list_value(value)
                res = []
                for x in list_:
                    res.append(parse_value(func.__args__[0], x))
                return res
            elif func.__origin__ == Union:
                return parse_value(func.__args__[0], value)
        return func(value)
    else:
        return default_value