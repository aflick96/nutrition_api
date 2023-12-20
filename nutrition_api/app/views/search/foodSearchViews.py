from flask import Blueprint, request, jsonify
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import search
from ...models import db, Nutrients, Brands, FoodCategories, FoodItems, FoodNutrients

foodSearchViews = Blueprint('foodSearchViews', __name__)

@foodSearchViews.route('/getFoodNames')
def getFoodNames():
    q = request.args.get('keyword', default='', type=str)
    food_items = FoodItems.query.filter(FoodItems.FoodName.ilike(f'{q}%')).all()
    if food_items:
        res = [{'FoodID': food_item.FoodID, 'FoodName': food_item.FoodName, 'FoodVector': food_item.FoodNameSearchVector} for food_item in food_items]
        return jsonify(res)
    else:
        return jsonify({'result': 'No result for {}'.format(q)})
    
@foodSearchViews.route('/getFoodNames/fuzzySearch')
def getFoodNameSuggestions():
    q = request.args.get('keyword', default='', type=str)    
    search_query = search(FoodItems.query, q)
    matched_items = search_query.limit(25).all()
    if matched_items:
        res = [{'FoodID': food_item.FoodID, 'FoodName' : food_item.FoodName} for food_item in matched_items]
        return jsonify(res)
    else:
        return jsonify('Null')
    
@foodSearchViews.route('/getFoodNutrientFacts')
def getFoodNutrients():
    q = request.args.get('foodid', default='', type=str)
    try:
        food_id = int(q)
    except ValueError:
        return jsonify({'error': 'Invalid FoodID'}), 400
    
    res = db.session.query(FoodNutrients, Nutrients).join(Nutrients, FoodNutrients.NutrientID == Nutrients.NutrientID).filter(FoodNutrients.FoodID == food_id).all()

    nutrients_data = []

    for food_nutrient, nutrient in res:
        nutrient_info = nutrient.to_dict()
        nutrient_info.update(food_nutrient.to_dict())
        nutrients_data.append(nutrient_info)

    return jsonify(nutrients_data)

