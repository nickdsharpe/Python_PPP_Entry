import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import ttk
from court import create_court

empty_df = pd.read_csv('empty.csv')

# General plot parameters
mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2
# Draw basketball court
fig = plt.figure(figsize=(4, 3.76))
ax = fig.add_axes([0, 0, 1, 1])
ax = create_court(ax, 'black')

team_data = {}




def record_shot(x, y):
    shot_made = IntVar()
    player = StringVar()
    play_type = StringVar()

    # Make 0r Miss radiobutton
    Radiobutton(window,text="Make",variable=shot_made,value=1).place(x=60,y=480)
    Radiobutton(window, text="Miss", variable=shot_made, value=0).place(x=120, y=480)

    # city Label
    Label(window, text="Player:").place(x=60, y=520)
    # city combobox
    player_dropdown = ttk.Combobox(window, width=27, textvariable=player)
    player_dropdown['values'] = ('Jokic',
                              'Murray',
                              'Brown',
                              'Gordon',
                              'MPJ',
                              'KCP',
                              'Braun',
                              'Green',
                              )
    player_dropdown.current()
    player_dropdown.place(x=120,y=520)

    # city Label
    Label(window, text="Play Type:").place(x=60, y=560)
    # city combobox
    play_type_dropdown = ttk.Combobox(window, width=27, textvariable=play_type)
    play_type_dropdown['values'] = ('PNR Ballhandler',
                              'PNR Screener',
                              'DHO Ballhandler',
                              'DHO Screener',
                              'Isolation',
                              'Transition',
                              'Catch & Shoot',
                              'Attacking Closeouts',
                              'Cutting',
                              'Off-Ball Screens',
                              'Off. Rebounds')
    play_type_dropdown.current()
    play_type_dropdown.place(x=140,y=560)

    Button(window, text="Record Shot", width=10, height=1, bg="orange",command=save_shot).place(x=250,y=510)

    def save_shot():

        player_val = player.get()
        shot_made_val = shot_made.get()
        play_type_val = play_type.get()
        
        # Store shot data in a dictionary
        shot = {
            "x": x,
            "y": y,
            "shot_made": "Make" if shot_made_val == 1 else "Miss",
            "player_name": player_val,
            "play_type": play_type_val

        }
        # Create DF for shot
        shot_df = pd.DataFrame([shot], index=[0])
        return shot_df

def get_shot_zone(x, y):
    # Function to determine the shot zone based on the coordinates
    if y <= 60:
        return "Rim"
    elif y <= 80:
        return "Short Mid-Range"
    elif y <= 140:
        return "3PT Arc"
    elif y <= 190:
        return "Lane and Key"
    else:
        return "Unknown"
    
def on_canvas_click(event):
    # Create a DF for the shot
    shot_dataframe = record_shot(event.x, event.y)
    team_data['murray'] = shot_dataframe

def save_shot_data():
    df = team_data['murray']
    df.to_csv("shot_data.csv", index=False)
    print("Shot data saved to shot_data.csv")

# Create the main window
window = tk.Tk()
window.title("Nuggets")

# Create a canvas widget
canvas = tk.Canvas(window, width=500, height=700)
canvas.pack()

# Create the FigureCanvasTkAgg object
canvas_fig = mpl.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=canvas)
canvas_fig.draw()

# Get the rendered figure and add it to the canvas
canvas_fig_widget = canvas_fig.get_tk_widget()
canvas.create_window(0, 0, anchor='nw', window=canvas_fig_widget)

# Bind the canvas click event
canvas_fig_widget.bind("<Button-1>", on_canvas_click)

# Create a button to save shot data
save_button = tk.Button(window, text="Save Shot Data", command=save_shot_data)
save_button.pack()

# Start the main event loop
window.mainloop()