import json

#参考サイト
#https://segafreder.hatenablog.com/entry/2017/10/01/140125

class JsonSerializable():
    OBJECT_TYPE = "#TYPE"
    def __init__(self) -> None:
        pass

    @staticmethod
    def encoder(o:"JsonSerializable"):
        data = vars(o)
        data[JsonSerializable.OBJECT_TYPE] = type(o).__name__
        return data
    
    @staticmethod
    def myhook(dict, globals_dict):
        if JsonSerializable.OBJECT_TYPE in dict.keys():
            obj_type = dict.pop(JsonSerializable.OBJECT_TYPE)
            datacls = globals_dict[obj_type]
            return datacls(**dict)
        return dict # 他の型はdefaultのデコード方式を使用

class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, JsonSerializable): # NotSettedParameterは'NotSettedParameter'としてエンコード
            return JsonSerializable.encoder(o)
        return super(MyJSONEncoder, self).default(o) # 他の型はdefaultのエンコード方式を使用


def dump(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, cls=MyJSONEncoder)

def load(file_path, globals_dict):
    with open(file_path, 'r') as f:
        data =  json.load(f, object_hook= lambda d : JsonSerializable.myhook(dict=d, globals_dict=globals_dict))
    return data