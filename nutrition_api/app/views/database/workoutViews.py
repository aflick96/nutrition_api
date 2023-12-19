from flask import Blueprint, request, jsonify
from ...models import db, Muscle, Exercise, Equipment, ExerciseEquipment, ExerciseMuscle, Orientation, MuscleType
import os
import ijson
from sqlalchemy.dialects.postgresql import insert

json_file_path = 'C:\\Users\\flickat1\\Desktop\\Personal\\lightwork\\database_preprocess\\Json\\Data'

workoutDatabaseViews = Blueprint('workoutDatabaseViews', __name__)

@workoutDatabaseViews.route('/populate/MuscleTable')
def populateMuscleTable():
    with open(os.path.join(json_file_path, 'Muscle Table.json'), 'rb') as f:
        for data in ijson.items(f, 'item'):
            
            ori = data.get('Orientation') 
            if ori == 'None': 
                ori = Orientation.NONE
            elif ori == 'Front': 
                ori = Orientation.FRONT
            elif ori == 'Back':
                ori = Orientation.BACK
            
            stmt = insert(Muscle).values(
                MuscleID=data.get('MuscleID'),
                Name=data.get('Name'),
                Orientation=ori
            )

            not_stmt = stmt.on_conflict_do_nothing(
                index_elements=['MuscleID']
            )

            db.session.execute(not_stmt)

        try:
            db.session.commit()
            f.close()
            return jsonify({'message': 'Successfully loaded Muscle Table data.'})
        
        except Exception as e:
            db.session.rollback()
            f.close()
            return jsonify({"error": f"Failed to insert data: {str(e)}"}), 500

@workoutDatabaseViews.route('/populate/ExerciseTable')
def populateExerciseTable():
    with open(os.path.join(json_file_path, 'Exercise Table.json'), 'rb') as f:
        for data in ijson.items(f, 'item'):
                        
            stmt = insert(Exercise).values(
                ExerciseID=data.get('ExerciseID'),
                Name=data.get('Name'),
            )

            not_stmt = stmt.on_conflict_do_nothing(
                index_elements=['ExerciseID']
            )

            db.session.execute(not_stmt)

        try:
            db.session.commit()
            f.close()
            return jsonify({'message': 'Successfully loaded Execise Table data.'})
        
        except Exception as e:
            db.session.rollback()
            f.close()
            return jsonify({"error": f"Failed to insert data: {str(e)}"}), 500

@workoutDatabaseViews.route('/populate/EquipmentTable')
def populateEquipmentTable():
    with open(os.path.join(json_file_path, 'Equipment Table.json'), 'rb') as f:
        for data in ijson.items(f, 'item'):
                        
            stmt = insert(Equipment).values(
                EquipmentID=data.get('EquipmentID'),
                Name=data.get('Name'),
            )

            not_stmt = stmt.on_conflict_do_nothing(
                index_elements=['EquipmentID']
            )

            db.session.execute(not_stmt)

        try:
            db.session.commit()
            f.close()
            return jsonify({'message': 'Successfully loaded Equipment Table data.'})
        
        except Exception as e:
            db.session.rollback()
            f.close()
            return jsonify({"error": f"Failed to insert data: {str(e)}"}), 500  

@workoutDatabaseViews.route('/populate/ExerciseEquipmentTable')
def populateExerciseEquipmentTable():
    with open(os.path.join(json_file_path, 'Exercise Equipment Table.json'), 'rb') as f:
        for data in ijson.items(f, 'item'):
                        
            stmt = insert(ExerciseEquipment).values(
                ExerciseID=data.get('ExerciseID'),
                EquipmentID=data.get('EquipmentID'),
            )

            not_stmt = stmt.on_conflict_do_nothing(
                index_elements=['ExerciseID','EquipmentID']
            )

            db.session.execute(not_stmt)

        try:
            db.session.commit()
            f.close()
            return jsonify({'message': 'Successfully loaded Exercise Equipment Table data.'})
        
        except Exception as e:
            db.session.rollback()
            f.close()
            return jsonify({"error": f"Failed to insert data: {str(e)}"}), 500  


@workoutDatabaseViews.route('/populate/ExerciseMuscleTable')
def populateExerciseMuscleTable():
    with open(os.path.join(json_file_path, 'Exercise Muscle Table.json'), 'rb') as f:
        for data in ijson.items(f, 'item'):

            ty = data.get('Type')
            if ty == 'Primary':
                ty = MuscleType.PRIMARY
            elif ty == 'Secondary':
                ty = MuscleType.SECONDARY

            stmt = insert(ExerciseMuscle).values(
                ExerciseID=data.get('ExerciseID'),
                MuscleID=data.get('MuscleID'),
                Type=ty
            )

            not_stmt = stmt.on_conflict_do_nothing(
                index_elements=['ExerciseID','MuscleID']
            )

            db.session.execute(not_stmt)

        try:
            db.session.commit()
            f.close()
            return jsonify({'message': 'Successfully loaded Exercise Muscle Table data.'})
        
        except Exception as e:
            db.session.rollback()
            f.close()
            return jsonify({"error": f"Failed to insert data: {str(e)}"}), 500  


@workoutDatabaseViews.route('/get')
def getData():
    q = request.args.get(
        'table', 
        default='',
        type=str
    )

    if q == 'Muscle':
        data = Muscle.query.all()
    elif q == 'Exercise':
        data = Exercise.query.all()
    elif q == 'Equipment':
        data = Equipment.query.all()
    elif q == 'ExerciseEquipment':
        data = ExerciseEquipment.query.all()
    elif q == 'ExerciseMuscle':
        data = ExerciseMuscle.query.all()

    res = [d.to_dict() for d in data]
    return jsonify(res)
    

@workoutDatabaseViews.route('/delete')
def deleteData():
    q = request.args.get(
        'table', 
        default='',
        type=str
    )

    try:
        if q == 'Muscle':
            db.session.query(Muscle).delete()
        elif q == 'Exercise':
            db.session.query(Exercise).delete()
        elif q == 'Equipment':
            db.session.query(Equipment).delete()
        elif q == 'ExerciseEquipment':
            db.session.query(ExerciseEquipment).delete()
        elif q == 'ExerciseMuscle':
            db.session.query(ExerciseMuscle).delete()
    
        db.session.commit()
        jsonify({'message': 'Deleted {} table data.'.format(q)})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


