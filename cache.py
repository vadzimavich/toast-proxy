from diskcache import Cache as diskCache
import os

class Cache():

    def __init__(self, dir: str, expires: int = None):
        # --- VERCEL FIX START ---
        # Vercel разрешает запись ТОЛЬКО в папку /tmp.
        # Мы перехватываем путь "./cache/..." и меняем его на "/tmp/cache/..."
        
        if dir.startswith("./"):
            dir = dir.replace("./", "/tmp/", 1)
        
        # На случай если путь передан иначе, принудительно добавляем /tmp
        if not dir.startswith("/tmp/"):
            # Очищаем путь от точек и слешей
            clean_path = dir.replace("./", "").lstrip("/")
            dir = f"/tmp/{clean_path}"
            
        # Создаем директорию, если её нет (в /tmp файлы удаляются после простоя)
        try:
            os.makedirs(dir, exist_ok=True)
        except Exception as e:
            print(f"Cache Warning: Could not create directory {dir}: {e}")
        # --- VERCEL FIX END ---

        self.cache = diskCache(dir, sqlite_cache_size=50000, disk_min_file_size=0, eviction_policy='least-recently-stored')
        self.expires = expires

    def set(self, key, value):
        try:
            self.cache.set(key, value, expire=self.expires)
        except Exception as e:
            print(f"Cache Write Error: {e}")

    def get(self, key, default=None):
        try:
            return self.cache.get(key, default)
        except Exception:
            return default
    
    def get_len(self):
        return len(self)
    
    def clear(self):
        return self.cache.clear()

    def expire(self):
        return self.cache.expire()
    
    def close(self):
        return self.cache.close()
    
    def __len__(self):
        return len(self.cache)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()