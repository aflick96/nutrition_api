from flask import Blueprint, request, jsonify
from sqlalchemy_searchable import search
from sqlalchemy import cast, String
from sqlalchemy.sql import func
from ...models import db, Muscle, Exercise, Equipment, ExerciseEquipment, ExerciseMuscle, Orientation, EquipmentGym, Gym, MuscleType, Plan, PlanWorkout, PlanWorkoutExercise

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
    
#Returns the equipment associated with a specific gym selection
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
    
@workoutSearchViews.route('/getPrebuiltPlansAvailable', methods=['POST'])
def getPrebuiltPlansAvailable():
    # Extract the list of EquipmentID's posted to the route
    posted_equipment_ids = set(request.json.get('data', []))

    # Fetch EquipmentID's for each PlanID
    subquery = (db.session.query(Plan.PlanID, ExerciseEquipment.EquipmentID)
                .join(PlanWorkout, Plan.PlanID == PlanWorkout.PlanID)
                .join(PlanWorkoutExercise, PlanWorkout.PlanWorkoutID == PlanWorkoutExercise.PlanWorkoutID)
                .join(ExerciseEquipment, PlanWorkoutExercise.ExerciseID == ExerciseEquipment.ExerciseID)
                .filter(ExerciseEquipment.EquipmentID != 0)
                .distinct()
                .subquery())
    
    # Aggregate EquipmentID's per PlanID using string_agg with explicit casting
    equipment_per_plan = (db.session.query(subquery.c.PlanID, func.string_agg(cast(subquery.c.EquipmentID, String), ','))
                          .group_by(subquery.c.PlanID)
                          .all())

    # Filter Plans where all of its EquipmentID's are in the posted list
    matching_plan_ids = [plan_id for plan_id, equipment_ids in equipment_per_plan
                         if set(map(int, equipment_ids.split(','))).issubset(posted_equipment_ids)]

    # Return the matching PlanID's
    return jsonify({'matching_plan_ids': matching_plan_ids})
