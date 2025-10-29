from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import ticket_crud
from app import schemas

router = APIRouter()


@router.post("/", response_model=schemas.TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    return ticket_crud.create_ticket(db, ticket)


@router.get("/", response_model=schemas.TicketsPagination)
def list_tickets(page: int = Query(1, ge=1), per_page: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return ticket_crud.get_tickets(db, page=page, per_page=per_page)

@router.get(
    "/{ticket_id}",
    response_model=schemas.TicketRead,
    responses={404: {"description": "Ticket not found"}}
)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = ticket_crud.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put(
    "/{ticket_id}",
    response_model=schemas.TicketRead,
    responses={404: {"description": "Ticket not found"}}
    )
def update_ticket(ticket_id: int, data: schemas.TicketUpdate, db: Session = Depends(get_db)):
    ticket = ticket_crud.update_ticket(db, ticket_id, data)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch(
    "/{ticket_id}/close",
    response_model=schemas.TicketRead,
    responses={404: {"description": "Ticket not found"}}
    )
def close_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = ticket_crud.close_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
