import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import ttk
from court import create_court
from update_player_df import update_player_df

players = ['Jokic', 'Murray', 'Brown',
           'Gordon', 'MPJ', 'KCP', 'Braun', 'Green', ]
empty_df = pd.read_csv('empty.csv')
team_data = {i: empty_df for i in players}

# General plot parameters
mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2
# Draw basketball court
fig = plt.figure(figsize=(4, 3.76))
ax = fig.add_axes([0, 0, 1, 1])
ax = create_court(ax, 'black')


def save_shot(shot_made, player_dropdown, play_type_dropdown, shot_type_dropdown, x, y):

    player_val = player_dropdown.get()
    shot_made_val = shot_made.get()
    play_type_val = play_type_dropdown.get()
    shot_type_val = shot_type_dropdown.get()

    # Store shot data in a dictionary
    shot = {
        "x": x,
        "y": y,
        "shot_made": "Make" if shot_made_val == 1 else "Miss",
        "player_name": player_val,
        "play_type": play_type_val,
        "shot_type:": shot_type_val
    }
    # Create DF for shot
    shot_df = pd.DataFrame([shot], index=[0])
    print(shot_df)
    updated_game_df = update_player_df(shot_df, team_data[player_val])
    print(updated_game_df)
    team_data[player_val] = updated_game_df


def record_shot(x, y):
    shot_made = IntVar()
    player = StringVar()
    play_type = StringVar()
    shot_type = StringVar()

    # Make 0r Miss radiobutton
    Radiobutton(window, text="Make", variable=shot_made,
                value=1).place(x=60, y=580)
    Radiobutton(window, text="Miss", variable=shot_made,
                value=0).place(x=140, y=580)

    # Player Label
    Label(window, text="Player:").place(x=60, y=620)
    # Player combobox
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
    player_dropdown.place(x=120, y=620)

    # Play Type Label
    Label(window, text="Play Type:").place(x=60, y=660)
    # Play Type combobox
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
                                    'Offensive Rebounds')
    play_type_dropdown.current()
    play_type_dropdown.place(x=150, y=660)

    # Shot Type Label
    Label(window, text="Shot Type:").place(x=60, y=700)
    # Shot Type combobox
    shot_type_dropdown = ttk.Combobox(window, width=27, textvariable=shot_type)
    shot_type_dropdown['values'] = ('2pt Field Goal',
                                    '3pt Field Goal',
                                    '2pt Free Throws',
                                    '3pt Free Throws',
                                    '2pt And-1',
                                    '3pt And-1'
                                    )
    shot_type_dropdown.current()
    shot_type_dropdown.place(x=155, y=700)

    Button(window, text="Record Shot", width=10, height=1,
           bg="orange", command=lambda: save_shot(shot_made, player_dropdown, play_type_dropdown, shot_type_dropdown, x, y)).place(x=480, y=610)


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
    record_shot(event.x, event.y)


def save_shot_data():
    for i in team_data:
        df = team_data[i]
        df.to_csv(f'{i}.csv', index=False)
        print("Shot data saved to shot_data.csv")


# Create the main window
window = tk.Tk()
window.title("Nuggets")

# Create a canvas widget
canvas = tk.Canvas(window, width=1000, height=1200)
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
