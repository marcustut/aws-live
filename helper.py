import json
from typing import List, Optional, Text, Any, TypedDict
from datetime import datetime
from werkzeug.datastructures import MultiDict
from argon2 import PasswordHasher

ph = PasswordHasher()


class CursorPagination(TypedDict):
    cursor: Optional[int]
    limit: int


def parse_cursor_pagination(args: MultiDict[str, str]) -> Optional[CursorPagination]:
    if 'limit' not in args:
        return None
    return {
        'cursor': int(args['cursor']) if 'cursor' in args else None,
        'limit': int(args['limit']),
    }


def date_hook(json_dict: dict[Text, Any]):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
        except:
            pass
    return json_dict


def is_valid_json_string(value: Any) -> bool:
    if not isinstance(value, str):
        return False

    if '{' not in value or '}' not in value:
        return False

    try:
        json.loads(value)
    except ValueError as e:
        return False

    return True


def parse_nested_json(value: dict[Text, Any]) -> dict[Text, Any]:
    for item in value.items():
        if is_valid_json_string(item[1]):
            value[item[0]] = json.loads(item[1], object_hook=date_hook)
    return value


def parse_nested_json_from_list(values: List[dict[Text, Any]]) -> List[dict[Text, Any]]:
    return [parse_nested_json(value) for value in values]


def hash_password(text: str) -> str:
    return ph.hash(text)
