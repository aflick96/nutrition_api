from flask_sqlalchemy import SQLAlchemy
from enum import unique, Enum as E
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable

db = SQLAlchemy()
make_searchable(db.metadata)

class Nutrients(db.Model):
    NutrientID = db.Column(db.Integer, primary_key=True)
    NutrientName = db.Column(db.String(250))
    NutrientGroup = db.Column(db.String(100))

    def to_dict(self):
        return {
            'NutrientID': self.NutrientID,
            'NutrientName': self.NutrientName,
            'NutrientGroup': self.NutrientGroup
        }

class Brands(db.Model):
    BrandID = db.Column(db.Integer, primary_key=True)
    BrandName = db.Column(db.String(250))

    def to_dict(self):
        return{
            'BrandID': self.BrandID,
            'BrandName': self.BrandName
        }


class FoodCategories(db.Model):
    FoodCategoryID = db.Column(db.Integer, primary_key=True)
    FoodCategoryName = db.Column(db.String(1000))

    def to_dict(self):
        return{
            'FoodCategoryID': self.FoodCategoryID,
            'FoodCategoreName': self.FoodCategoryName
        }

class FoodItems(db.Model):

    FoodID = db.Column(db.Integer, primary_key=True)
    FoodName = db.Column(db.String(1000), nullable=False)
    FoodCategoryID = db.Column(db.Integer, db.ForeignKey('food_categories.FoodCategoryID'))
    BrandID = db.Column(db.Integer, db.ForeignKey('brands.BrandID'))
    FoodNameSearchVector = db.Column(TSVectorType('FoodName'))

    category = db.relationship('FoodCategories', backref=db.backref('food_items', lazy=True))
    brand = db.relationship('Brands', backref=db.backref('food_items', lazy=True))

    def to_dict(self):
        return{
            'FoodID': self.FoodID,
            'FoodName': self.FoodName,
            'FoodCategoryID': self.FoodCategoryID,
            'BrandID': self.BrandID,
            'FoodNameSearchVector': self.FoodNameSearchVector
        }
    
    def __repr__(self):
        return f'<FoodItem {self.FoodName}>'


class FoodNutrients(db.Model):
    FoodID = db.Column(db.Integer, db.ForeignKey('food_items.FoodID'), primary_key=True)
    NutrientID = db.Column(db.Integer, db.ForeignKey('nutrients.NutrientID'), primary_key=True)
    NutrientAmount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return{
            'FoodID': self.FoodID,
            'NutrientID': self.NutrientID,
            'NutrientAmount': self.NutrientAmount
        }
    
class Orientation(E):
    FRONT = 'Front'
    BACK = 'Back'
    NONE = 'None'

class MuscleType(E):
    PRIMARY = 'Primary'
    SECONDARY = 'Secondary'

class Muscle(db.Model):
    __tablename__ = 'muscles'
    MuscleID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Orientation = db.Column(db.Enum(Orientation))

    def to_dict(self):
        return {
            'MuscleID': self.MuscleID,
            'Name': self.Name,
            'Orientation': self.Orientation.value
        }

class Exercise(db.Model):
    __tablename__ = 'exercises'
    ExerciseID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(1000), nullable=False)

    def to_dict(self):
        return {
            'ExerciseID': self.ExerciseID,
            'Name': self.Name
        }
    
class Equipment(db.Model):
    __tablename__ = 'equipment'
    EquipmentID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(1000), nullable=False)

    def to_dict(self):
        return {
            'EquipmentID': self.EquipmentID,
            'Name': self.Name
        }

class ExerciseEquipment(db.Model):
    __tablename__ = 'exercise_equipment'
    ExerciseID = db.Column(db.Integer, db.ForeignKey('exercises.ExerciseID'), primary_key=True)
    EquipmentID = db.Column(db.Integer, db.ForeignKey('equipment.EquipmentID'), primary_key=True)

    def to_dict(self):
        return {
            'ExerciseID': self.ExerciseID,
            'EquipmentID': self.EquipmentID
        }

class ExerciseMuscle(db.Model):
    __tablename__ = 'exercise_muscle'
    ExerciseID = db.Column(db.Integer, db.ForeignKey('exercises.ExerciseID'), primary_key=True)
    MuscleID = db.Column(db.Integer, db.ForeignKey('muscles.MuscleID'), primary_key=True)
    Type = db.Column(db.Enum(MuscleType))

    def to_dict(self):
        return {
            'ExerciseID': self.ExerciseID,
            'MuscleID': self.MuscleID,
            'Type': self.Type.value
        }

