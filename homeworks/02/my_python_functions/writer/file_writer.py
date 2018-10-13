import os
import pickle as pkl

class FileWriter:
    
    def __init__(self, path):
        """path - путь до файла"""
        if self._check_path(path):
            self._path = path
            self.file = None
        
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, new_path):
        if self._check_path(new_path):
            self._path=new_path
        else:
            raise Exception('Bad path!')
    
    @path.getter
    def path(self):
        return self._path
    
    @path.deleter
    def path(self):
        del self._path
    
    def _check_path(self, path):
        return os.path.exists(os.path.split(os.path.abspath('path'))[0])
    
    def print_file(self):
        with open(self.path, 'r') as f_obj:
            print(f_obj.read())     
    
    def write(self, some_string):
        with open(self.path, 'a') as f_obj:
            f_obj.write(some_string)
    
    def save_yourself(self, file_name):
        with open(file_name, 'wb') as my_f:
            return pkl.dump(self, my_f)
    
    def __enter__(self):
        self.file = open(self.path, 'a')
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        self.file = None
        if exc_val:
            raise
    
    @classmethod
    def load_file_writer(cls, pickle_file):
        with open(pickle_file, 'rb') as obj:
            return pkl.load(obj)

    # 
    # возможно что то еще.
    # что намеренно упущенно. например что то для контекстного менеджера.