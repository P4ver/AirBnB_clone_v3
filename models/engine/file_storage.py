#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """tests methods"""
        storage = FileStorage()
        storage.reload()
        state_data = {"name": "Taza"}
        state_instance = State(**state_data)
        ret_state = storage.get(State, state_instance.id)
        self.assertEqual(state_instance, ret_state)
        fk_state_id = storage.get(State, 'fake_id')
        self.assertEqual(fk_state_id, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        storage = FileStorage()
        storage.reload()
        state_data = {"name": "Safi"}
        state_instance = State(**state_data)
        storage.new(state_instance)
        city_data = {"name": "Anassi","state_id":state_instance.id}
        city_instance = City(**city_data)
        storage.new(city_instance)
        storage.save()
        state_occu = storage.count(State)
        self.assertEqual(state_occu, len(storage.all(state)))
        all_occu = storage.count(State)
        self.assertEqual(all_occu, len(storage.all()))