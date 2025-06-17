
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)



# customers, service_tickets, service_mechanics, mechanics
# cust: id, name, email, phone
# st: id, VIN, serv_date, serv_desc, cust_id
# sm: ticket_id, mechanic_id
# mech: id, name, phone, email, salary
#cust_id->cust_id // st_id-> ticket_id // mech_id <- mech_id

service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    db.Column('service_ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(225),nullable=False)
    email: Mapped[str] = mapped_column(db.String(360),nullable=False,unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), unique=True)
    password: Mapped[str] = mapped_column(db.String(225),nullable=False)

    tickets: Mapped[List['ServiceTickets']] = db.relationship(back_populates='customer')
    


class ServiceTickets(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(30), nullable=False, unique=True)
    service_date: Mapped[date] = mapped_column(db.Date)
    service_desc: Mapped[str] = mapped_column(db.String(300))
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    customer: Mapped[Customer] = db.relationship(back_populates='tickets')
    mechanics: Mapped[List['Mechanics']] = db.relationship(secondary='service_mechanics', back_populates='service_tickets')

class Mechanics(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(225),nullable=False)
    email: Mapped[str] = mapped_column(db.String(360),nullable=False,unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), unique=True)
    salary: Mapped[float] = mapped_column(db.Numeric(10,2), nullable=False)

    service_tickets: Mapped[List['ServiceTickets']] = db.relationship(secondary='service_mechanics', back_populates='mechanics')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(225),nullable=False)
    email: Mapped[str] = mapped_column(db.String(360),nullable=False,unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), unique=True)


# For practice, further extend the models you created for your mechanic shop API. 
# Create a schema for your Customer model, and routes to accomplish all four CRUD 
# operations to Create, Read, Update, and 
# Delete customers similar to how Dylan added CRUD for the Library members in the above videos.
# qwAnd don't forget to test each endpoint as you go
