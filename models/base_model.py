#!/usr/bin/python3
"""
Base Model Module
"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """BaseModel class that defines common attributes for other classes"""

    timeformat = "%Y-%m-%dT%H:%M:%S.%f"

    def __init__(self, *args, **kwargs):
        """Initializes BaseModel with attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

        if kwargs:
            self.set_attributes_from_dict(kwargs)

        models.storage.new(self)

    def set_attributes_from_dict(self, attr_dict):
        """Sets object attributes from a dictionary"""
        for key, value in attr_dict.items():
            if key != "__class__":
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the object"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.to_dict()
        )

    def save(self):
        """Updates the updated_at attribute and saves the instance"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing keys/values
        of __dict__ of the instance. nu_d is short for new dictionary"""
        nu_d = self.__dict__.copy()

        if "created_at" in nu_d and isinstance(nu_d["created_at"], datetime):
            nu_d["created_at"] = nu_d["created_at"].strftime(self.timeformat)

        if "updated_at" in nu_d and isinstance(nu_d["updated_at"], datetime):
            nu_d["updated_at"] = nu_d["updated_at"].strftime(self.timeformat)

        nu_d["__class__"] = self.__class__.__name

        return nu_d
