import click
from colorama import init, Fore, Style
from db import init_db, SessionLocal
from tabulate import tabulate
from datetime import date
from models import Client, Workout, NutritionPlan

init(autoreset=True)
DARK_GREEN = Fore.GREEN

@click.group()
def cli():
    """Fitness and Nutrition Tracker CLI"""
    pass

@cli.command()
def init():
    """Initialize the database"""
    init_db()
    click.echo(DARK_GREEN + "Database initialized.")
    
@cli.command()
@click.option('--name', prompt='Client name')
@click.option('--age', prompt='Age', type=int)
@click.option('--gender', prompt='Gender')
@click.option('--email', prompt='Email')
def add_client(name, age, gender, email):
    """Add a new client"""
    session = SessionLocal()
    if session.query(Client).filter_by(email=email).first():
        click.echo(DARK_GREEN + f"Client with email {email} already exists.")
        session.close()
        return
    client = Client(name=name, age=age, gender=gender, email=email)
    session.add(client)
    session.commit()
    click.echo(DARK_GREEN + f"Added client {name}!")
    session.close()

@cli.command()
def list_clients():
    """List all clients"""
    session = SessionLocal()
    clients = session.query(Client).all()
    if clients:
        table = [[c.id, c.name, c.age, c.gender, c.email] for c in clients]
        click.echo(DARK_GREEN + tabulate(table, headers=["ID", "Name", "Age", "Gender", "Email"], tablefmt="github"))
    else:
        click.echo(DARK_GREEN + "No clients found.")
    session.close()

@cli.command()
@click.option('--client_id', prompt='Client ID', type=int)
@click.option('--exercise', prompt='Exercise')
@click.option('--duration', prompt='Duration (min)', type=float)
@click.option('--calories_burned', prompt='Calories burned', type=float)
@click.option('--notes', prompt='Notes', default="")
def add_workout(client_id, exercise, duration, calories_burned, notes):
    """Add a workout for a client"""
    session = SessionLocal()
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        click.echo(DARK_GREEN + "Client not found.")
        session.close()
        return
    workout = Workout(client_id=client_id, date=date.today(), exercise=exercise,
                      duration=duration, calories_burned=calories_burned, notes=notes)
    session.add(workout)
    session.commit()
    click.echo(DARK_GREEN + f"Workout for {client.name} added!")
    session.close()

@cli.command()
@click.option('--client_id', prompt='Client ID', type=int)
def list_workouts(client_id):
    """List all workouts for a client"""
    session = SessionLocal()
    workouts = session.query(Workout).filter_by(client_id=client_id).all()
    if workouts:
        table = [[w.id, w.date, w.exercise, w.duration, w.calories_burned, w.notes] for w in workouts]
        click.echo(DARK_GREEN + tabulate(
            table,
            headers=["ID", "Date", "Exercise", "Duration", "Calories Burned", "Notes"],
            tablefmt="github"
        ))
    else:
        click.echo(DARK_GREEN + "No workouts found.")
    session.close()

@cli.command()
@click.option('--client_id', prompt='Client ID', type=int)
@click.option('--meal', prompt='Meal')
@click.option('--calories', prompt='Calories', type=float)
@click.option('--protein', prompt='Protein (g)', type=float)
@click.option('--carbs', prompt='Carbs (g)', type=float)
@click.option('--fats', prompt='Fats (g)', type=float)
@click.option('--notes', prompt='Notes', default="")
def add_nutrition(client_id, meal, calories, protein, carbs, fats, notes):
    """Add a nutrition plan for a client"""
    session = SessionLocal()
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        click.echo(DARK_GREEN + "Client not found.")
        session.close()
        return
    nutrition_plan = NutritionPlan(client_id=client_id, date=date.today(), meal=meal,
                              calories=calories, protein=protein, carbs=carbs, fats=fats, notes=notes)
    session.add(nutrition_plan)
    session.commit()
    click.echo(DARK_GREEN + f"Nutrition plan for {client.name} added!")
    session.close()

@cli.command()
@click.option('--client_id', prompt='Client ID', type=int)
def list_nutrition(client_id):
    """List all nutrition plans for a client"""
    session = SessionLocal()
    plans = session.query(NutritionPlan).filter_by(client_id=client_id).all()
    if plans:
        table = [[p.id, p.date, p.meal, p.calories, p.protein, p.carbs, p.fats, p.notes] for p in plans]
        click.echo(DARK_GREEN + tabulate(
            table,
            headers=["ID", "Date", "Meal", "Calories", "Protein", "Carbs", "Fats", "Notes"],
            tablefmt="github"
        ))
    else:
        click.echo(DARK_GREEN + "No nutrition plans found.")
    session.close()

@cli.command()
@click.option('--client_id', prompt='Client ID', type=int)
def analytics(client_id):
    """Show analytics for a client (total calories burned and consumed)"""
    session = SessionLocal()
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        click.echo(DARK_GREEN + "Client not found.")
        session.close()
        return

    total_burned = session.query(Workout)\
        .filter_by(client_id=client_id)\
        .with_entities(Workout.calories_burned)\
        .all()
    total_burned = sum([w[0] for w in total_burned])

    total_consumed = session.query(NutritionPlan)\
        .filter_by(client_id=client_id)\
        .with_entities(NutritionPlan.calories)\
        .all()
    total_consumed = sum([n[0] for n in total_consumed])

    click.echo(
        DARK_GREEN + f"Analytics for {client.name}:\n"
        f"Total Calories Burned: {total_burned}\n"
        f"Total Calories Consumed: {total_consumed}\n"
        f"Net Calories: {total_consumed - total_burned}"
    )
    session.close()

if __name__ == '__main__':
    cli()