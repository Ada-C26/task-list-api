from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Select
from sqlalchemy.orm import Session
from ..models.base import Base as BaseModel

class BaseRepository:
    __MODEL: type[BaseModel]
    __db: SQLAlchemy

    def __init__(self, database: SQLAlchemy, model_class: type[BaseModel]):
        """ 
        Using a repository pattern for the validation layer

        We can create repository classes for each model that needs this CRUD validation layer
        by inheriting this class and overriding the base model it uses.

        The typehinting isn't necessary but is helpful for code completion.
        """
        self.__MODEL = model_class
        self.__db = database

    def query(self) -> Select:
        return self.__db.select(self.__MODEL)

    def session(self) -> Session:
        return self.__db.session

    def validate(self, record_data):
        """
        The validation function still needs to be overridden with model-specific attributes

        It should return a dictionary of validated attributes and values
        OR return False if the data is invalid.
        """
        return False

    def create(self, record_data: dict):
        """
        This will work with the validation setup of the child class,
        because we're now expanding the validated_data into the 
        model constructor regardless of the specific attributes
        the child repository class will be using.
        """
        validated_data = self.validate(record_data)
        
        if not validated_data:
            return None

        new_item = self.__MODEL(**validated_data)

        self.session().add(new_item)
        self.session().commit()

        return new_item

    def get_one_by_id(self, record_id):
        # Allow the ValueError to raise if invalid
        validated_id = int(record_id)

        query = self.query().where(self.__MODEL.id == validated_id).limit(1)
        
        return self.session().execute(query).scalar_one_or_none()