from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database.database import get_db
from ..models.contact import Contact, ContactCreateUpdate

router = APIRouter()

@router.post("/contacts/")
def create_contact(contact: ContactCreateUpdate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/contacts/", response_model=List[Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Contact).offset(skip).limit(limit).all()

@router.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactCreateUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for field, value in contact.dict().items():
        setattr(db_contact, field, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted"}
