import click
from colorama import init, Fore
from db import init_db

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
