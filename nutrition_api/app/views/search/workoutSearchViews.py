from flask import Blueprint, request, jsonify
from sqlalchemy_searchable import search
from ...models import db, Muscle, Exercise, Equipment, ExerciseEquipment, ExerciseMuscle, Orientation, EquipmentGym, Gym, MuscleType

workoutSearchViews = Blueprint('workoutSearchViews', __name__)

#Returns all of the PRIMARY exercises for a muscle group
@workoutSearchViews.route('/getExercisesByMuscleGroup')
def getExercisesByMuscleGroup():
    #Request parameter for the muscle group search/workout/getExercisesByMuscleGroup?muscle_group=
    q = request.args.get('muscle_group', default='', type=str)

    if q:
        muscle = Muscle.query.filter_by(Name=q).first()
        if muscle:
            ex = db.session.query(Exercise).join(
                ExerciseMuscle, ExerciseMuscle.ExerciseID == Exercise.ExerciseID
            ).filter(ExerciseMuscle.MuscleID == muscle.MuscleID,
                     ExerciseMuscle.Type == MuscleType.PRIMARY).all()

            exercises = [{'Name': e.Name} for e in ex]

            return jsonify(exercises)
        
        else:
            return jsonify({'error': 'muscle_group not found'}), 404
    else:
        return jsonify({'error': 'muscle_group is required'}), 400
    

@workoutSearchViews.route('/getEquipmentByGymType')
def getExercisesByGymType():
    q = request.args.get('gym_type', default='', type=str)

    if q:
        gym = Gym.query.filter_by(Name=q).first()
        if gym:
            eq = db.session.query(Equipment).join(
                EquipmentGym, EquipmentGym.EquipmentID == Equipment.EquipmentID
            ).filter(EquipmentGym.GymID == gym.GymID).all()

            equipment = [{'EquipmentID': e.EquipmentID, 'Name': e.Name} for e in eq]

            return jsonify(equipment)

        else:
            return jsonify({'error': 'gym_type not found'}), 404 
    else:
        return jsonify({'error': 'gym_type is required'}), 400
    


