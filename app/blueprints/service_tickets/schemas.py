from app.extensions import ma
from app.models import ServiceTickets


#SCHEMAS
class ServiceTicketsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTickets #using the SQLAlchemy model to create fields used in serialization, deserialization, and validation
    
serviceticket_schema = ServiceTicketsSchema()
servicetickets_schema = ServiceTicketsSchema(many=True) 