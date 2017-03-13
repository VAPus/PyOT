import config
"""
try:
    from ujson import loads, load
    from ujson import dumps, load
except:
    try:
        from cjson import decode as loads
        from cjson import encode as dumps
    except:
        try:
            from simplejson import dump, load, dumps, loads
        except:
            from json import dumps, loads, dump, load
"""
from json import dumps, loads, dump, load
