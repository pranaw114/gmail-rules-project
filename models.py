from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Text, DateTime, Integer, Index

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True)
    gmail_id = Column(String, unique=True, nullable=False, index=True)
    thread_id = Column(String, index=True)
    sender = Column(String, index=True)
    to = Column(String)
    subject = Column(String, index=True)
    snippet = Column(Text)
    body = Column(Text)
    received = Column(DateTime, index=True)

Index('ix_emails_composite', Email.sender, Email.subject)
