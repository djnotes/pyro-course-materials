import redis
import dill

class Cache:
    def __init__(self):
        self.db = redis.Redis(host = "redis")

    def update_user_session(self, uid, key, value):
        _s = self.db.get(uid)
        if _s:
            s = dill.loads(_s)
            s[key] = value
        else:
            s = {key:value}
        self.db.set(uid, dill.dumps(s), ex = 600)

    def get_session_item(self, uid, key):
        _s = self.db.get(uid)
        if _s:
            s = dill.loads(_s)
            if key in s:
                return s[key]
            return None
        return None
    
    def clear_session(self, uid):
        self.db.delete(uid)
    

        
                