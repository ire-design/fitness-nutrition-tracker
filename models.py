from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    age = Column(Integer)
    gender = Column(String(16))
    email = Column(String(128), unique=True)
    workouts = relationship('Workout', back_populates='client')
    nutrition_plans = relationship('NutritionPlan', back_populates='client')

