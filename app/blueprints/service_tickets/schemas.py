from marshmallow import fields, validate
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

class InventoryItemQuantitySchema(ma.Schema):
    inventory_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))

class EditServiceTicketsInventorySchema(ma.Schema):
    items_to_add_or_update = fields.List(
        fields.Nested(InventoryItemQuantitySchema),
        required=False # Allow requests that only remove items
    )
    remove_inventory_ids = fields.List(
        fields.Integer(),
        required=False # Allow requests that only add/update items
    )

    class Meta:
        # Ensure at least one operation is specified if needed, or handle empty requests in the route
        fields = ("items_to_add_or_update", "remove_inventory_ids")

edit_service_ticket_inventory_schema = EditServiceTicketsInventorySchema()