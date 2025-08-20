from flask import Flask, request, jsonify
from db import SessionLocal, init_db
from models import Client, Workout, NutritionPlan
from datetime import datetime

app = Flask(__name__)

@app.before_first_request
def setup():
    init_db()

@app.route('/clients', methods=['GET', 'POST'])
def clients():
    session = SessionLocal()
    if request.method == 'GET':
        clients = session.query(Client).all()
        result = [
            {'id': c.id, 'name': c.name, 'age': c.age, 'gender': c.gender, 'email': c.email}
            for c in clients
        ]
        session.close()
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        if session.query(Client).filter_by(email=data['email']).first():
            session.close()
            return jsonify({'error': 'Client already exists'}), 400
        client = Client(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            email=data['email']
        )
        session.add(client)
        session.commit()
        result = {'id': client.id, 'name': client.name, 'age': client.age, 'gender': client.gender, 'email': client.email}
        session.close()
        return jsonify(result), 201

@app.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    session = SessionLocal()
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        session.close()
        return jsonify({'error': 'Client not found'}), 404
    result = {'id': client.id, 'name': client.name, 'age': client.age, 'gender': client.gender, 'email': client.email}
    session.close()
    return jsonify(result)

@app.route('/clients/<int:client_id>/workouts', methods=['GET', 'POST'])
def workouts(client_id):
    session = SessionLocal()
    if request.method == 'GET':
        workouts = session.query(Workout).filter_by(client_id=client_id).all()
        result = [
            {'id': w.id, 'date': w.date.isoformat(), 'exercise': w.exercise, 'duration': w.duration,
             'calories_burned': w.calories_burned, 'notes': w.notes}
            for w in workouts
        ]
        session.close()
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        workout = Workout(
            client_id=client_id,
            date=datetime.fromisoformat(data['date']).date() if data.get('date') else datetime.now().date(),
            exercise=data['exercise'],
            duration=data['duration'],
            calories_burned=data['calories_burned'],
            notes=data.get('notes', '')
        )
        session.add(workout)
        session.commit()
        result = {'id': workout.id, 'date': workout.date.isoformat(), 'exercise': workout.exercise, 'duration': workout.duration,
                  'calories_burned': workout.calories_burned, 'notes': workout.notes}
        session.close()
        return jsonify(result), 201

@app.route('/clients/<int:client_id>/nutrition', methods=['GET', 'POST'])
def nutrition(client_id):
    session = SessionLocal()
    if request.method == 'GET':
        plans = session.query(NutritionPlan).filter_by(client_id=client_id).all()
        result = [
            {'id': p.id, 'date': p.date.isoformat(), 'meal': p.meal, 'calories': p.calories,
             'protein': p.protein, 'carbs': p.carbs, 'fats': p.fats, 'notes': p.notes}
            for p in plans
        ]
        session.close()
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        plan = NutritionPlan(
            client_id=client_id,
            date=datetime.fromisoformat(data['date']).date() if data.get('date') else datetime.now().date(),
            meal=data['meal'],
            calories=data['calories'],
            protein=data['protein'],
            carbs=data['carbs'],
            fats=data['fats'],
            notes=data.get('notes', '')
        )
        session.add(plan)
        session.commit()
        result = {'id': plan.id, 'date': plan.date.isoformat(), 'meal': plan.meal, 'calories': plan.calories,
                  'protein': plan.protein, 'carbs': plan.carbs, 'fats': plan.fats, 'notes': plan.notes}
        session.close()
        return jsonify(result), 201

@app.route('/clients/<int:client_id>/analytics', methods=['GET'])
def analytics(client_id):
    session = SessionLocal()
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        session.close()
        return jsonify({'error': 'Client not found'}), 404
    total_burned = session.query(Workout).filter_by(client_id=client_id).with_entities(
        Workout.calories_burned).all()
    total_burned = sum([w[0] for w in total_burned])
    total_consumed = session.query(NutritionPlan).filter_by(client_id=client_id).with_entities(
        NutritionPlan.calories).all()
    total_consumed = sum([n[0] for n in total_consumed])
    session.close()
    return jsonify({
        'client_id': client_id,
        'total_calories_burned': total_burned,
        'total_calories_consumed': total_consumed,
        'net_calories': total_consumed - total_burned
    })

if __name__ == '__main__':
    app.run(debug=True)