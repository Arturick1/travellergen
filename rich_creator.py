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
        mod = get_modifier(value)
        mod_str = f"[green]+{mod}[/green]" if mod > 0 else f"[red]{mod}[/red]" if mod < 0 else "0"
        table.add_row(stat, str(value), mod_str)

    print("\n")
    print(Panel(f"[bold yellow]Homeworld:[/bold yellow] {homeworld}", expand=False))
    print(table)

def get_modifier(value):
    if value <= 2:
        return -2
    elif value <= 5:
        return -1
    elif value <= 8:
        return 0
    elif value <= 11:
        return 1
    elif value <= 14:
        return 2
    else:  # 15 or higher
        return 3


def main():
    print(Panel(
        "[bold red]TRAVELLER[/bold red]\n"
        "[bold white]Mongoose First Edition Style[/bold white]\n"
        "[italic cyan]Character Creator[/italic cyan]",
        expand=False
    ))

    name = Prompt.ask("[bold]Enter character name[/bold]", default="Traveller-001")
    
    # --- Characteristics Rolling with Reroll Option ---
    while True:
        print("\n[bold]Generating characteristics...[/bold]\n")
        stats = roll_characteristics()  # This already has the nice rolling animation
        
        # Display the stats in a temporary table
        temp_table = Table(title="[bold cyan]Current Characteristics[/bold cyan]", show_header=True, header_style="bold magenta")
        temp_table.add_column("Characteristic", style="bold")
        temp_table.add_column("Score", justify="center")
        temp_table.add_column("Modifier", justify="center")

        for stat, value in stats.items():
            mod = get_modifier(value)
            mod_str = f"[green]+{mod}[/green]" if mod > 0 else f"[red]{mod}[/red]" if mod < 0 else "0"
            temp_table.add_row(stat, str(value), mod_str)

        print(temp_table)

        # Ask if they want to reroll
        reroll = Prompt.ask(
            "\n[bold yellow]Do you want to keep these stats?[/bold yellow]",
            choices=["y", "n"],
            default="y"
        )

        if reroll == "y":
            print("[bold green]Great! Locking in these characteristics.[/bold green]")
            break  # Exit the loop, proceed with these stats
        else:
            print("[bold red]Rerolling...[/bold red]\n")


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

    with open(f"{name}.txt", "w") as file:
        file.write(f"Character Name: {name}\n")
        file.write(f"Homeworld: {homeworld}\n")
        file.write("\nCharacteristics:\n")
        for stat_name, value in stats.items():
            mod = get_modifier(value)
            mod_str = f"+{mod}" if mod > 0 else str(mod) if mod < 0 else "0"
            file.write(f"{stat_name}: {value} (Modifier: {mod_str})\n")        

    print("\n[bold green]Character creation complete![/bold green]")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()