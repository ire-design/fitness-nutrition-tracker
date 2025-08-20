import click
from colorama import init, Fore
from db import init_db, SessionLocal
from models import Client

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