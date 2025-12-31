import random
import tkinter as tk
from tkinter import ttk

class TravellerCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Traveller RPG Character Creator by William Drell")

        # Characteristics section
        ttk.Label(root, text="Characteristics:").grid(row=0, column=0, padx=10, pady=5)
        self.stats_text = tk.Text(root, height=6, width=30)
        self.stats_text.grid(row=1, column=0, padx=10, pady=5)

        ttk.Button(root, text="Roll Characteristics", command=self.roll_stats).grid(row=2, column=0, pady=10)

        # Homeworld section
        ttk.Label(root, text="Homeworld:").grid(row=3, column=0, pady=5)
        self.homeworld_var = tk.StringVar()
        homeworlds = ['High-Tech World', 'Agricultural Planet', 'Desert World', 'Ocean World']
        ttk.OptionMenu(root, self.homeworld_var, homeworlds[0], *homeworlds).grid(row=4, column=0, pady=5)

        ttk.Button(root, text="Generate Character", command=self.generate_character).grid(row=5, column=0, pady=10)

        # Output
        self.output_label = ttk.Label(root, text="")
        self.output_label.grid(row=6, column=0, pady=10)

    def roll_d6(self, num_dice=2):
        return sum(random.randint(1,6) for _ in range(num_dice))
    
    def roll_stats(self):
        stats = {
            'Strength' : self.roll_d6(),
            'Dexterity' : self.roll_d6(),
            'Endurance' : self.roll_d6(),
            'Intelligence' : self.roll_d6(),
            'Education' : self.roll_d6(),
            'Social Standing' : self.roll_d6()
        }
        self.stats_text.delete(1.0, tk.END)
        for stat, value in stats.items():
            self.stats_text.insert(tk.END, f"{stat}: {value}\n")
        return stats
    
    def generate_character(self):
        homeworld = self.homeworld_var.get()
        self.output_label.config(text=f"Character ready! Homeworld: {homeworld}")
        # Add more logic here: save to file, proceed to careers, etc.

if __name__=="__main__":
    root = tk.Tk()
    app = TravellerCreator(root)
    root.mainloop()
