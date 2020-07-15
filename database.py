import os
import pickle 
import pwd
from serving import Serving
import time

## Database class. The data is a set of objects. dirname is the name of the directory (preferrably hidden) in the user's home directory. 
# filename is the file to be stored in the directory. fieldname is the string for the field of the objects that will be accessed for 
# sorting and comparison purposes (the Database assumes data-type homogeneity)
class Database:
    def __init__(self,data = [], dirpath="", filename = "", fieldname ="" ):
        self.data = data
        self.dirpath = dirpath
        self.fieldname = fieldname
        self._index = -1
        if self.dirpath[-1] == "/":
            self.pathname = self.dirpath + filename
        else:
            self.pathname = self.dirpath + "/" + filename
        self.load_list()
        self.sort()

    def __iter__(self):
        return self
    def __next__(self):
        if self._index == len(self.data)-1:
            self._index = -1
            raise StopIteration
        self._index += 1
        return self.data[self._index]
    def __getitem__(self,i):
        return self.data[i]
    def __len__(self):
        return len(self.data)

    # This overwrites the database file with the current values in the list
    def commit(self):
        with open(self.pathname, "wb") as f:
            for obj in self.data:
                pickle.dump(obj,f)

    # Method to remove items by index
    def pop(self,index):
        item = self.data.pop(index)
        self.commit()
        return item

    # Method to be called from user side for adding new items
    def add(self,new_item):
        if not self.item_exists(new_item):
            self.put(new_item)
            self._save_item(new_item)

    # Method that primarily checks for duplicates
    def item_exists(self,new_item):
        #self.sort()
        for item in self.data:
            if self.current_field(item) == self.current_field(new_item):
                return True
        return False

    def sort(self):
        if self.fieldname != "":
            self.data.sort(key = self.current_field)

    # ( Needs additional work for better modularity as it currently depends on the existence of a name field in the item )
    def current_field(self,item):
        exec("global value; value = item." + self.fieldname)
        if isinstance(value, str):
            return value.lower()
        return value

    # Add item to main list
    def put(self, new_item):
        self.data.append(new_item)
        self.sort()
        '''if len(self.data) > 1:   
            for i in range(len(self.data)-1):
                if self.current_field(new_item) > self.current_field(self.data[i]) and self.current_field(new_item) < self.current_field(self.data[i+1]):
                    self.data.insert(i+1,new_item)
            if i == len(self.data) - 1:
                print("Appended.")
                self.data.append(new_item)
        else:
            print("Appended.")
            self.data.append(new_item)'''


    def load_list(self):
        if os.path.isfile(self.pathname):
            with open(self.pathname,"rb") as f:
                while True:
                    try:
                        current_object = pickle.load(f)
                        self.data.append(current_object)
                    except EOFError:
                        break

    ## The save_data method will do a couple of things: first, it checks if the file exists in the current directory. If the file
    # does not exist, then it will be created in a hidden directory within the user's home directory. Because the database checks for
    # duplicates during the creation of a new object, the _save_item method doesn't have to worry about that.
    def _save_item(self,new_object):
        write_options = "wb"
        if os.path.isfile(self.pathname):
            write_options = "ab"
        elif not self._check_hidden_dir():
            os.mkdir(self.dirpath)
        with open(self.pathname,write_options) as f:
            pickle.dump(new_object,f)
        #self._write_item(new_object,write_options)
                
    def _check_hidden_dir(self):
        dir_exists = False
        if os.path.exists(self.dirpath):
            dir_exists = True
        else:
            dir_exists = False
        return dir_exists
