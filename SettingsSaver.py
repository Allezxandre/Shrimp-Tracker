import pickle
import gzip
from os import path
from pathlib import Path
from typing import Optional


class FilenameCache(object):
    def __init__(self, filename):
        self.filename = filename
        self.circle = None
        self.kalman = None
        self.mask = None


class SettingsSaver(object):

    def __init__(self):
        from appdirs import AppDirs
        app_dirs = AppDirs('ShrimpTracker', 'GeorgiaTech')
        self.cache_dir = app_dirs.user_cache_dir
        self.data_dir = app_dirs.user_data_dir
        self.cache = {}
        self.__load_cache()

    def __assert_exists(self):
        for directory in [self.cache_dir, self.data_dir]:
            Path(directory).mkdir(parents=True, exist_ok=True)

    @property
    def cache_file(self):
        return path.join(self.cache_dir, 'cache.pklz')

    def __load_cache(self):
        try:
            print("Opening cache in '%s'"%self.cache_file)
            if path.exists(self.cache_file):
                with gzip.open(self.cache_file, 'rb') as f:
                    cache_object = pickle.load(f)
                    if type(cache_object) is dict:
                        self.cache = cache_object
                    else:
                        self.cache = {}
            else:
                with open(self.cache_file[0:-1], 'rb') as f:
                    cache_object = pickle.load(f)
                    if type(cache_object) is dict:
                        self.cache = cache_object
                    else:
                        self.cache = {}
        except FileNotFoundError:
            print('Cache does not exist')
            self.cache = {}

    def clear_cache(self, filename):
        self.cache[filename] = FilenameCache(filename)
        self.cache[filename].kalman = None
        self.cache[filename].circle = None
        self.cache[filename].mask = None
        self.save_cache()

    def add_to_cache(self, filename, kalman=None, circle=None, mask=None):
        if filename not in self.cache or (not isinstance(self.cache[filename], FilenameCache)):
            self.cache[filename] = FilenameCache(filename)
        if kalman is not None:
            self.cache[filename].kalman = kalman
        if circle is not None:
            self.cache[filename].circle = circle
        if mask is not None:
            self.cache[filename].mask = mask
        self.save_cache()

    def read_from_cache(self, filename) -> Optional[FilenameCache]:
        if filename not in self.cache:
            self.cache[filename] = FilenameCache(filename)
        return self.cache[filename]

    def save_cache(self):
        self.__assert_exists()
        with gzip.open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f, pickle.HIGHEST_PROTOCOL)
