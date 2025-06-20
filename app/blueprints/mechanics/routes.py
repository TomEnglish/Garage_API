from . import mechanics_db
from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.models import Mechanics, db
from .schemas import mechanic_schema, mechanics_schema
from app.utils.util import encode_mec_token, mec_token_required


@mechanics_db.route("/", methods=['POST'])
@mec_token_required
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Mechanics).where(Mechanics.email == mechanic_data['email']) #Checking our db for a member with this email
    existing_mechanic = db.session.execute(query).scalars().all()
    if existing_mechanic:
        return jsonify({"error": "Email already associated with a mechanic."}), 400
    
    new_mechanic = Mechanics(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201



@mechanics_db.route('/', methods=['GET'])
def get_mechanics_list():
    query = select(Mechanics)
    # Placeholder: return actual data
    
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200

@mechanics_db.route('/volume/', methods=['GET'])
def get_mechanics_list_by_work_vol():
    query = select(Mechanics)
    # Placeholder: return actual data
    
    mechanics = db.session.execute(query).scalars().all()
    mechanics.sort(key=lambda mechanics:len(mechanics.service_tickets), reverse=True)

    return mechanics_schema.jsonify(mechanics), 200


#UPDATE SPECIFIC EMPLOYEE/MECHANIC
@mechanics_db.route("/<int:mechanic_id>", methods=['PUT'])
@mec_token_required
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

#DELETE SPECIFIC MEMBER
@mechanics_db.route("/<int:mechanic_id>", methods=['DELETE'])
@mec_token_required
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f'Mechanic id: {mechanic_id}, successfully deleted.'}), 200