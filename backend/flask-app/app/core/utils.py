import json
from bson import json_util
from bson.objectid import ObjectId

def parse_json(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
    return json.loads(json_util.dumps(data))


def str_to_objectid(id_str):
    try:
        return ObjectId(id_str)
    except Exception as e:
        print(f"Error converting string to ObjectId: {e}")
        return None