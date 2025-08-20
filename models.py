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

class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    date = Column(Date)
    exercise = Column(String(128))
    duration = Column(Float)  # in minutes
    calories_burned = Column(Float)
    notes = Column(Text)
    client = relationship('Client', back_populates='workouts')

class NutritionPlan(Base):
    __tablename__ = 'nutrition_plans'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    date = Column(Date)
    meal = Column(String(128))
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)
    notes = Column(Text)
    client = relationship('Client', back_populates='nutrition_plans')