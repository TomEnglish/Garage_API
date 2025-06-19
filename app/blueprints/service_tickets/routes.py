from . import tickets_db
from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.models import ServiceTickets, Mechanics, db
from .schemas import servicetickets_schema, serviceticket_schema, edit_service_ticket_schema
from app.extensions import limiter, cache



# POST '/': Pass in all the required information to create the service_ticket.
@tickets_db.route("/", methods=['POST'])
#@limiter.limit("20/hour") #how many mechanics per day or hour would be reasonabe...not too many
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
def assign_mechanic(ticket_id, mechanic_id):
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
 

# GET '/': Retrieves all service tickets.

@tickets_db.route('/', methods=['GET'])
#@cache.cached(timeout=60)#A Get of ALl tickets is ikey something like a dashboard would pull from frequently
def get_all_servicetickets():
    query = select(ServiceTickets)
    
    tickets = db.session.execute(query).scalars().all()

    return servicetickets_schema.jsonify(tickets), 200

 
 # PUT '/<int:ticket_id>/edit' : Takes in remove_ids, and add_ids
# Use id's to look up the mechanic to append or remove them from the ticket.mechanics list
@tickets_db.route("/<int:ticket_id>/edit/", methods=['PUT'])
def edit_mechanic(ticket_id):
    ticket = db.session.get(ServiceTickets, ticket_id)

    try:
        ticket_updates = edit_service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(ServiceTickets).where(ServiceTickets.id == ticket_id)
    result = db.session.execute(query).scalars().first()
    
    for mechanic_id in ticket_updates["add_mechanic_ids"]:
        query = select(Mechanics).where(Mechanics.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in result.mechanics:
            result.mechanics.append(mechanic)

    for mechanic_id in ticket_updates["remove_mechanic_ids"]:
        query = select(Mechanics).where(Mechanics.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in result.mechanics:
            result.mechanics.remove(mechanic)

    db.session.commit()
    return serviceticket_schema.jsonify(result), 200