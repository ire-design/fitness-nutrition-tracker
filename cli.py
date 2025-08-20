import click
from colorama import init, Fore
from db import init_db, SessionLocal
from models import Client
from tabulate import tabulate
from datetime import datetime 
from models import Client, Workout

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
