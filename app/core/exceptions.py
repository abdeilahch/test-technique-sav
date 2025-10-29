from fastapi import HTTPException, status

class TicketNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

class InvalidTicketStatus(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ticket status")
