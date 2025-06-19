from marshmallow import fields
from app.extensions import ma
from app.models import ServiceTickets
import re

#SCHEMAS
class ServiceTicketsSchema(ma.SQLAlchemyAutoSchema):
    customer_id = fields.Integer(required=True)
    class Meta:
        model = ServiceTickets #using the SQLAlchemy model to create fields used in serialization, deserialization, and validation
        include_fk = True # Include foreign keys like customer_id for loading
    
serviceticket_schema = ServiceTicketsSchema()
servicetickets_schema = ServiceTicketsSchema(many=True) 

class EditServiceTicketsSchema(ma.Schema):

    remove_mechanic_ids = fields.List(fields.Integer(), required=True)

    add_mechanic_ids = fields.List(fields.Integer(), required=True)

    class Meta:

        fields = ("remove_mechanic_ids", "add_mechanic_ids")


edit_service_ticket_schema = EditServiceTicketsSchema()