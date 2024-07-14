import random
import tkinter as tk
from tkinter import filedialog

combinations_list = {}
numberofsimulations = 10000 # Self explanitory, I was tired of digging for this every time I wanted to change it, so later on if you see some variable shenanigans, that's why. 
# later on, I have a section commented out which prints off hands that where not combo. You might want to change this number to prevent printing off thousands of hands
tempCombo = []

def check_combo(hand, combos):
    for combo in combos:
        if all(card in hand for card in combo):
            return True        
    return False

def simulate(num_trials, deck, combos):
    success_count = 0
    multiple_prosp_count = 0
    pot_of_prosperity = 'Prosperity'  # Assuming this is how the card is identified in the deck list. It automatically capitalizes he first letter of the card name. If prosp isn't listed as 'Prosperity', then it won't count. 

    for _ in range(num_trials):
        random.shuffle(deck)
        hand = deck[:5]

        if check_combo(hand, combos):
            success_count += 1
        elif pot_of_prosperity in hand:
            top_6_cards = deck[6:12]

            for card in top_6_cards:
                new_hand = hand[:5] + [card]
                if check_combo(new_hand, combos):
                    success_count += 1
                    break
##        else:
##            # Print the hand if it fails to contain a combo. I  find this useful to print the non-combo hands to make sure I didn't miss anthing. Be careful, if you run the simulation 10,000 times and your brick rate is 50%, it'll print off 5000 hands... Ask me how I know...
##            hand.sort()
##            print(f"Hand without combo: {hand}")
 
    return success_count

def add_card():
    card_name = entry.get().strip().capitalize()
    if card_name:
        if card_name in players_deck:
            players_deck[card_name] += 1
        else:
            players_deck[card_name] = 1
        update_deck_list_and_label()
        
def remove_card():
    card_name = entry.get().strip().capitalize()
    if card_name in players_deck:
        players_deck[card_name] -= 1
        if players_deck[card_name] == 0:
            del players_deck[card_name]
        update_deck_list_and_label()

def save_deck(deck_data, combo_data, filename):
    with open(filename, 'w') as file:
        file.write("[DECK]\n")
        for card, count in deck_data.items():
            file.write(f"{count}x - {card}\n")
        file.write("[COMBOS]\n")
        for combo in combo_data:
            file.write(f"{combo}\n")

def save_deck_to_file():

    # This is the path that I am storing this in. It helps to make a whole folder for this.
    
    initial_dir = r"C:\Users\HP\Documents\Anthonys Random Docs\Deck List Folder\Test"
    filename = filedialog.asksaveasfilename(initialdir=initial_dir, defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        combos = [combinations_listbox.get(i) for i in range(combinations_listbox.size())]
        save_deck(players_deck, combos, filename)

def load_deck(filename):
    loaded_deck = {}
    loaded_combos = []
    section = None
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "[DECK]":
                section = "deck"
            elif line == "[COMBOS]":
                section = "combos"
            elif section == "deck":
                count, card = line.split('x - ')
                loaded_deck[card] = int(count)
            elif section == "combos":
                loaded_combos.append(line)
    return loaded_deck, loaded_combos

def load_deck_from_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        deck, combos = load_deck(filename)
        players_deck.clear()
        players_deck.update(deck)
        update_deck_list_and_label()
        combinations_listbox.delete(0, tk.END)
        for combo in combos:
            combinations_listbox.insert(tk.END, combo)

def update_deck_list_and_label():
    deck_list.delete(0, tk.END)
    for card, count in players_deck.items():
        deck_list.insert(tk.END, f"{count}x - {card}")
    deck_label.config(text=f"Deck List ({sum(players_deck.values())}):")

def populate_entry_field(event):
    selected_item = deck_list.curselection()
    if selected_item:
        card_name = deck_list.get(selected_item[0]).split(" - ")[1].strip()
        entry.delete(0, tk.END)
        entry.insert(0, card_name)

def remove_card_from_combo(event):
    index = combo_listbox.curselection()
    if index:
        combo_listbox.delete(index)

def remove_combo(event):
    selected_index = combinations_listbox.curselection()
    if selected_index:
        combinations_listbox.delete(selected_index[0])

def add_combination():
    global combo_selection_window
    combo_selection_window = tk.Toplevel(root)
    combo_selection_window.title("Select Combo Cards")

    deck_label = tk.Label(combo_selection_window, text="Deck List:")
    deck_label.grid(row=0, column=0, padx=5, pady=5)

    deck_listbox = tk.Listbox(combo_selection_window, width=40)
    deck_listbox.grid(row=1, column=0, padx=5, pady=5)
    for card in players_deck:
        deck_listbox.insert(tk.END, card)

    deck_listbox.bind("<Double-1>", lambda event: select_card(event, deck_listbox))

    combo_label = tk.Label(combo_selection_window, text="Combo Pieces:")
    combo_label.grid(row=0, column=1, padx=5, pady=5)

    global combo_listbox
    combo_listbox = tk.Listbox(combo_selection_window, width=40)
    combo_listbox.grid(row=1, column=1, padx=5, pady=5)
    combo_listbox.bind("<Double-1>", remove_card_from_combo)

    done_button = tk.Button(combo_selection_window, text="Done", command=finalize_combination)
    done_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

def finalize_combination():
    global tempCombo
    selected_combo = [combo_listbox.get(i) for i in range(combo_listbox.size())]
    tempCombo.extend(selected_combo)
    combo_selection_window.destroy()
    
    formatted_combinations = [" + ".join(tempCombo)]
    
    for combo in formatted_combinations:
        combinations_listbox.insert(tk.END, combo)
    
    tempCombo.clear()

def select_card(event, listbox):
    selected_index = listbox.curselection()
    if selected_index:
        card_name = listbox.get(selected_index[0])
        combo_listbox.insert(tk.END, card_name)

def run_simulation():
    global success_label
    
    simnumber = numberofsimulations 

    deck = []
    
    for card, count in players_deck.items():
        deck.extend([card] * count)
    
    combos = [tuple(combo.split(" + ")) for combo in combinations_listbox.get(0, tk.END)]
    
    success_count = simulate(simnumber, deck, combos)
 
    success_percentage = (success_count / simnumber) * 100
    
    success_label.config(text=f"Success: {success_percentage:.2f}%")

root = tk.Tk()
root.title("Deck Builder")
root.configure(background="#6D2932")

players_deck = {}  

# Deck List
deck_frame = tk.Frame(root)
deck_frame.grid(row=0, column=0, pady=10)

deck_label = tk.Label(deck_frame, text="Deck List:")
deck_label.grid(row=0, column=0)

deck_list = tk.Listbox(deck_frame, width=40)
deck_list.configure(background="#C7B7A3")
deck_list.grid(row=1, column=0)

deck_list.bind("<<ListboxSelect>>", populate_entry_field)

# Combinations List
combo_frame = tk.Frame(root)
combo_frame.grid(row=1, column=0, pady=10)

combo_label = tk.Label(combo_frame, text="Combinations:")
combo_label.grid(row=0, column=0)

combinations_listbox = tk.Listbox(combo_frame, width=40)
combinations_listbox.configure(background="#C7B7A3")
combinations_listbox.grid(row=1, column=0)

combinations_listbox.bind("<Double-1>", remove_combo)

# Card Entry, Add Button, Remove Button
entry_frame = tk.Frame(root)
entry_frame.grid(row=2, column=0, pady=5, padx=5)

entry_label = tk.Label(entry_frame, text="Enter Card Name:")
entry_label.grid(row=0, column=0)

entry = tk.Entry(entry_frame, width=20)
entry.grid(row=0, column=1, padx=10)
entry.bind("<Return>", lambda event: add_card())


add_button = tk.Button(entry_frame, text="Add", command=add_card)
add_button.grid(row=0, column=2, padx=5)

remove_button = tk.Button(entry_frame, text="Remove", command=remove_card)
remove_button.grid(row=0, column=3, padx=5)

add_combo_button = tk.Button(root, text="Add Combination", command=add_combination)
add_combo_button.grid(row=3, column=0, pady=5)

# Save Deck Button
save_deck_button = tk.Button(deck_frame, text="Save Deck", command=save_deck_to_file)
save_deck_button.grid(row=5, column=0, padx=5, pady=5)

# Load Deck Button
load_deck_button = tk.Button(deck_frame, text="Load Deck", command=load_deck_from_file)
load_deck_button.grid(row=6, column=0, padx=5, pady=5)

# Simulator Button
simulation_button = tk.Button(root, text="Run Simulation", command=run_simulation)
simulation_button.grid(row=4, column=0, pady=5)

success_label = tk.Label(root, text="Success: -")
success_label.grid(row=6, column=0, pady=5)

update_deck_list_and_label()

root.mainloop()
