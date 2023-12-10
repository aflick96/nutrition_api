# from flask import Blueprint, jsonify
# import requests
# from ..models import db, Nutrients, Brands, FoodCategories, FoodItems, FoodNutrients
# import json
# import ijson
# from sqlalchemy.dialects.postgresql import insert

# file_path = r'C:\Users\flickat1\Desktop\Personal\lw\api\nutrition_api\app\json_data'

# databaseViews = Blueprint('databaseViews', __name__)

# # @databaseViews.route('/getFood')
# # def getFood():
# #     res = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?query=cheese&data_Type=Branded&sortBy=lowercaseDescription.keyword&sortOrder=asc&api_key={}'.format(app.config['API_KEY']))
# #     if res.status_code == 200:
# #         data = res.json()
# #         descriptions = [item['description'].title() for item in data.get('foods', [])]
# #     return descriptions

# @databaseViews.route('/populateNutrients')
# def populateNutrients():
#     with open(file_path + '\\updatedNutrients.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
    
#     for nut_info in data:
    
#         curr_nutrient = Nutrients.query.get(nut_info['NutrientID']) 

#         if not curr_nutrient:            
#             nutrient = Nutrients(
#                 NutrientID=nut_info['NutrientID'],
#                 NutrientName=nut_info['NutrientName'],
#                 NutrientGroup=nut_info['NutrientGroup']
#             )
#             db.session.add(nutrient)

#     try:
#         db.session.commit()
#         return jsonify({'message': 'Nutrient successfully populated.'})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500


# @databaseViews.route('/fetchNutrients')
# def fetchNutrients():
#     data = Nutrients.query.all()
#     res = [d.to_dict() for d in data]
#     return jsonify(res)

# @databaseViews.route('/deleteNutrients')
# def deleteNutrients():
#     try:
#         # Delete all records from FoodNutrients
#         db.session.query(Nutrients).delete()

#         # Commit the changes to the database
#         db.session.commit()

#         return jsonify({'message': 'All nutrient records have been deleted.'})

#     except Exception as e:
#         # If an error occurs, rollback the session
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# @databaseViews.route('/populateBrands')
# def populateBrands():
#     with open(file_path + '\\brands.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
    
#     for d in data:
        
#         curr_d = Brands.query.get(d['BrandID']) 

#         if not curr_d:            
#             brand = Brands(
#                 BrandID=d['BrandID'],
#                 BrandName=d['BrandName']
#             )

#             db.session.add(brand)

#     try:
#         db.session.commit()
#         return jsonify({'message': 'Brands successfully populated.'})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

# @databaseViews.route('/fetchBrands')
# def fetchBrands():
#     data = Brands.query.all()
#     res = [d.to_dict() for d in data]
#     return jsonify(res)

# @databaseViews.route('/deleteBrands')
# def deleteBrands():
#     try:
#         # Delete all records from FoodNutrients
#         db.session.query(Brands).delete()

#         # Commit the changes to the database
#         db.session.commit()

#         return jsonify({'message': 'All nutrient records have been deleted.'})

#     except Exception as e:
#         # If an error occurs, rollback the session
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# @databaseViews.route('/populateFoodCategories')
# def populateFoodCategories():
#     with open(file_path + '\\foodCategories.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
    
#     for d in data:
        
#         curr_d = FoodCategories.query.get(d['FoodCategoryID']) 

#         if not curr_d:

#             # if len(d['FoodCategoryName']) > 100: d['FoodCategoryName'] = d['FoodCategoryName'][:100]  

#             cat = FoodCategories(
#                 FoodCategoryID=d['FoodCategoryID'],
#                 FoodCategoryName=d['FoodCategoryName']
#             )

#             db.session.add(cat)

#     try:
#         db.session.commit()
#         return jsonify({'message': 'Food Categories successfully populated.'})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

# @databaseViews.route('/fetchFoodCategories')
# def fetchFoodCategories():
#     data = FoodCategories.query.all()
#     res = [d.to_dict() for d in data]
#     return jsonify(res)

# @databaseViews.route('/deleteFoodCategories')
# def deleteFoodCategories():
#     try:
#         # Delete all records from FoodNutrients
#         db.session.query(FoodCategories).delete()

#         # Commit the changes to the database
#         db.session.commit()

#         return jsonify({'message': 'All nutrient records have been deleted.'})

#     except Exception as e:
#         # If an error occurs, rollback the session
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# @databaseViews.route('/populateFoodItems')
# def populateFoodItems():
#     with open(file_path + '\\UpdatedFoodItemsTable.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
    
#     for d in data:
        
#         curr_d = FoodItems.query.get(d['FoodID']) 

#         if not curr_d:

#             it = FoodItems(
#                 FoodID=d['FoodID'],
#                 FoodName=d['FoodName'],
#                 FoodCategoryID=d['FoodCategoryID'],
#                 BrandID=d['BrandID']
#             )

#             db.session.add(it)

#     try:
#         db.session.commit()
#         return jsonify({'message': 'Food Items successfully populated.'})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

# @databaseViews.route('/fetchFoodItems')
# def fetchFoodItems():
#     data = FoodItems.query.all()
#     res = [d.to_dict() for d in data]
#     return jsonify(res)

# @databaseViews.route('/deleteFoodItems')
# def deleteFoodItems():
#     try:
#         # Delete all records from FoodNutrients
#         db.session.query(FoodItems).delete()

#         # Commit the changes to the database
#         db.session.commit()

#         return jsonify({'message': 'All nutrient records have been deleted.'})

#     except Exception as e:
#         # If an error occurs, rollback the session
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# @databaseViews.route('/populateFoodNutrients')
# def populateFoodNutrients():
#     filename = file_path + '\\UpdatedFoodNutrientsTable.json'
#     # batch_size = 1000
#     # batch = []
#     # batch_count = 0

#     with open(filename, 'rb') as file:

#         for d in ijson.items(file, 'item'):
#             stmt = insert(FoodNutrients).values(
#                 FoodID=d['FoodID'],
#                 NutrientID=d['NutrientID'],
#                 NutrientAmount=d['NutrientAmount']
#             )
#             do_nothing_stmt = stmt.on_conflict_do_nothing(
#                 index_elements=['FoodID', 'NutrientID']
#             )

#             db.session.execute(do_nothing_stmt)

#         try:
#             db.session.commit()
#             return jsonify({'message': 'Food Nutrients successfully populated.'})

#         except Exception as e:
#             db.session.rollback()
#             return jsonify({"error": str(e)}), 500

#     #     for d in ijson.items(file, 'item'):
#     #         nuts = FoodNutrients(
#     #             FoodID=d['FoodID'],
#     #             NutrientID=d['NutrientID'],
#     #             NutrientAmount=d['NutrientAmount']  
#     #         )
#     #         batch.append(nuts)

#     #         if len(batch) >= batch_size:
#     #             print(batch)
#     #             db.session.add_all(batch)
#     #             try:
#     #                 db.session.commit()
#     #                 batch_count += 1
#     #                 print('batch {} commited'.format(batch_count))
#     #                 batch = []
#     #             except Exception as e:
#     #                 print('rolledback')
#     #                 db.session.rollback()

#     # if batch:
#     #     db.session.add_all(batch)
#     #     try:
#     #         db.session.commit()
#     #     except Exception as e:
#     #         db.session.rollback()

#     # return jsonify({'message': 'Food nutrients successfully loaded.'})            

# @databaseViews.route('/fetchFoodNutrients')
# def fetchFoodNutrients():
#     data = FoodNutrients.query.all()
#     res = [d.to_dict() for d in data]
#     return jsonify(res)


# @databaseViews.route('/getRowCount')
# def getCounter():
#     return jsonify({'count': db.session.query(db.func.count(FoodNutrients.FoodID)).scalar()})

# @databaseViews.route('/deleteFoodNutrients')
# def deleteFoodNutrients():
#     try:
#         # Delete all records from FoodNutrients
#         db.session.query(FoodNutrients).delete()

#         # Commit the changes to the database
#         db.session.commit()

#         return jsonify({'message': 'All food nutrients records have been deleted.'})

#     except Exception as e:
#         # If an error occurs, rollback the session
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500
