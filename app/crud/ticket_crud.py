from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketRead
from datetime import datetime
from math import ceil


def create_ticket(db: Session, data: TicketCreate):
    ticket = Ticket(**data.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def get_tickets(db: Session, page: int = 1, per_page: int = 100) -> list[Ticket]:
    total = db.query(Ticket).count()
    total_pages = ceil(total / per_page)
    tickets = db.query(Ticket).offset((page - 1) * per_page).limit(per_page).all()
    #tickets_out = [TicketRead.from_orm(t) for t in tickets]
    tickets_out = [TicketRead.model_validate(t) for t in tickets]
    return {
        "total": total,
        "total_pages": total_pages,
        "current_page": page,
        "per_page": per_page,
        "tickets": tickets_out
    }

def get_ticket(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def update_ticket(db: Session, ticket_id: int, data: TicketUpdate):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ticket, key, value)
    db.commit()
    db.refresh(ticket)
    return ticket

def close_ticket(db: Session, ticket_id: int):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        return None
    ticket.status = "closed"
    ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)
    return ticket
