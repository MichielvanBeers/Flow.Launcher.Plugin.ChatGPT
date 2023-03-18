from pathlib import Path
import json

class Settings(dict):

    def __init__(self, filepath):
        super(Settings, self).__init__()
        self._filepath = filepath
        self._save = True
        if Path(self._filepath).exists():
            self._load()
        else:
            data = {}
            self.update(data)
            self.save()

        
    def _load(self):
        data = {}
        with open(self._filepath, 'r') as f:
            try:
                data.update(json.load(f))
            except json.decoder.JSONDecodeError:
                pass

        self._save = False
        self.update(data)
        self._save = True

    def save(self):
        if self._save:
            data = {}
            data.update(self)
            with open(self._filepath, 'w') as f:
                json.dump(data, f, sort_keys=True, indent=4)
        return
    
    def __setitem__(self, key, value):
        super(Settings, self).__setitem__(key, value)
        self.save()

    def __delitem__(self, key):
        super(Settings, self).__delitem__(key)
        self.save()

    def update(self, *args, **kwargs):
        super(Settings, self).update(*args, **kwargs)
        self.save()

    def setdefault(self, key, value=None):
        ret = super(Settings, self).setdefault(key, value)
        self.save()
        return ret
