# Service_Ticket: Create the following routes to Create service tickets, assign mechanics, remove mechanics, and retrieve all service tickets.
# POST '/': Pass in all the required information to create the service_ticket.
# PUT '/<ticket_id>/assign-mechanic/<mechanic-id>: Adds a relationship between a service ticket and the mechanics. (Reminder: use your relationship attributes! They allow you the treat the relationship like a list, able to append a Mechanic to the mechanics list).
# PUT '/<ticket_id>/remove-mechanic/<mechanic-id>: Removes the relationship from the service ticket and the mechanic.
# GET '/': Retrieves all service tickets.