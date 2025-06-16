from . import tickets_db
from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.models import ServiceTickets, Mechanics, db
from .schemas import servicetickets_schema, serviceticket_schema


# POST '/': Pass in all the required information to create the service_ticket.
@tickets_db.route("/", methods=['POST'])
def create_ticket():
    try:
        ticket_data = serviceticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check if a ticket with the same VIN already exists
    query = select(ServiceTickets).where(ServiceTickets.vin == ticket_data['vin'])
    existing_ticket = db.session.execute(query).scalars().first() # Use .first() as VIN is unique
    if existing_ticket:
        return jsonify({"error": f"Service ticket with VIN {ticket_data['vin']} already exists"}), 400
    
    new_ticket = ServiceTickets(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return serviceticket_schema.jsonify(new_ticket), 201


# PUT '/<ticket_id>/assign-mechanic/<mechanic-id>: Adds a relationship between a service ticket and the mechanics. (Reminder: use your relationship attributes! They allow you the treat the relationship like a list, able to append a Mechanic to the mechanics list).
@tickets_db.route("/<ticket_id>/assign-mechanic/<mechanic_id>", methods=['PUT'])
def assign_mechanic(ticket_id,mechanic_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not ticket:
        return jsonify({"error": "Ticket not found."}), 404
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    ticket.mechanics.append(mechanic)
    db.session.commit()
    serialized_ticket = serviceticket_schema.dump(ticket)
    message = f"Mechanic {mechanic.name} (ID: {mechanic.id}) assigned to Ticket ID: {ticket.id}"
    return jsonify(message=message, ticket=serialized_ticket), 200
 


# PUT '/<ticket_id>/remove-mechanic/<mechanic-id>: Removes the relationship from the service ticket and the mechanic.
@tickets_db.route("/<ticket_id>/remove-mechanic/<mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not ticket:
        return jsonify({"error": "Ticket not found."}), 404
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    ticket.mechanics.remove(mechanic)
    db.session.commit()
    serialized_ticket = serviceticket_schema.dump(ticket)
    message = f"Mechanic {mechanic.name} (ID: {mechanic.id}) removed from Ticket ID: {ticket.id}"
    return jsonify(message=message, ticket=serialized_ticket), 200

# GET '/': Retrieves all service tickets.
@tickets_db.route('/', methods=['GET'])
def get_all_servicetickets():
    query = select(ServiceTickets)
    
    tickets = db.session.execute(query).scalars().all()

    return servicetickets_schema.jsonify(tickets), 200