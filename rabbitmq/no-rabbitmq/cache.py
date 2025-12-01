import redis
import dill

DEFAULT_SESSION_LIFETIME = 300

class Cache:
    def __init__(self):
        self.db = redis.Redis(host = "redis")

    def update_user_session(self, uid, key, value, ex=DEFAULT_SESSION_LIFETIME ):
        _s = self.db.get(uid)
        if _s:
            s = dill.loads(_s)
            s[key] = value
        else:
            s = {key:value}
        self.db.set(uid, dill.dumps(s), ex = DEFAULT_SESSION_LIFETIME)

    def get_session_item(self, uid, key, default = None):
        _s = self.db.get(uid)
        if _s:
            s = dill.loads(_s)
            if key in s:
                return s[key]
            return default
        return default
    
    def clear_session(self, uid):
        self.db.delete(uid)
    
    def clear_all_sessions(self):
        self.db.flushdb()
    
        
                