from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import datetime

class SubscriptionTier(str, enum.Enum):
    free = "free"
    pro = "pro"
    enterprise = "enterprise"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.free)
    stripe_customer_id = Column(String, nullable=True)
    subscription_end_date = Column(DateTime, nullable=True)

    projects = relationship("Project", back_populates="user")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vision_json = Column(JSON)
    constraints_json = Column(JSON)
    product_spec_json = Column(JSON)
    canvas_json = Column(JSON)
    process_graph_json = Column(JSON)
    finance_data_json = Column(JSON)
    accounting_ledger_json = Column(JSON)
    tax_regime_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="projects")
