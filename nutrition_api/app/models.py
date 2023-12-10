from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    category = db.relationship('FoodCategories', backref=db.backref('food_items', lazy=True))
    brand = db.relationship('Brands', backref=db.backref('food_items', lazy=True))

    def to_dict(self):
        return{
            'FoodID': self.FoodID,
            'FoodName': self.FoodName,
            'FoodCategoryID': self.FoodCategoryID,
            'BrandID': self.BrandID
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





