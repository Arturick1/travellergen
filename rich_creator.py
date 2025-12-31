from optparse import Values
import random
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.progress import track
import time

def roll_2d6():
    return random.randint(1, 6) + random.randint(1, 6)

def roll_characteristics():
    stats = ["Strength", "Dexterity", "Endurance", "Intelligence", "Education", "Social Standing"]
    values = {}
    
    print(Panel("[bold green]Rolling Characteristics (2d6 each)...[/bold green]", expand=False))
    
    for stat in track(stats, description="Rolling dice"):
        time.sleep(0.5)  # Small delay for dramatic effect
        values[stat] = roll_2d6()
    
    return values

def display_character_sheet(name, homeworld, stats):
    table = Table(title=f"[bold cyan]Character: {name}[/bold cyan]", show_header=True, header_style="bold magenta")
    table.add_column("Characteristic", style="bold")
    table.add_column("Score", justify="center")
    table.add_column("Modifier", justify="center")

    for stat, value in stats.items():
        mod = (value - 7) // 3  # Classic Traveller DM formula
        mod_str = f"[green]+{mod}[/green]" if mod > 0 else f"[red]{mod}[/red]" if mod < 0 else "0"
        table.add_row(stat, str(value), mod_str)

    print("\n")
    print(Panel(f"[bold yellow]Homeworld:[/bold yellow] {homeworld}", expand=False))
    print(table)

def main():
    print(Panel(
        "[bold red]TRAVELLER[/bold red]\n"
        "[bold white]Mongoose First Edition Style[/bold white]\n"
        "[italic cyan]Character Creator[/italic cyan]",
        expand=False
    ))

    name = Prompt.ask("[bold]Enter character name[/bold]", default="Traveller-001")
    
    print("\n[bold]Generating characteristics...[/bold]\n")
    stats = roll_characteristics()

    print(f"\n[bold]{stats}\n")


    homeworlds = [
        "High-Tech World", "Agricultural Planet", "Desert World",
        "Ocean World", "Asteroid Belt", "Vacuum World", "Industrial World"
    ]
    
    print("\n[bold]Select Homeworld:[/bold]")
    for i, world in enumerate(homeworlds, 1):
        print(f"[yellow]{i}[/yellow]. {world}")
    
    choice = IntPrompt.ask("Choose a number", choices=[str(i) for i in range(1, len(homeworlds)+1)], default=1)

    

    homeworld = homeworlds[choice - 1]

    display_character_sheet(name, homeworld, stats)


    print("\n[bold green]Character creation complete![/bold green]")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()