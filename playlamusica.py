import os
import random
import pygame
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Scale, Button, Label, Entry
from tkinter import Listbox, Canvas
from ttkthemes import ThemedTk

# Initialize pygame
pygame.init()

# Path to the music folder
MUSIC_FOLDER = 'allmusic'

# Initialize timer variables
TIMER_LENGTH = 60  # Default timer length in seconds
TIMER_RUNNING = False
TIMER_PAUSED = False
TIMER_REMAINING = TIMER_LENGTH
CURRENT_TRACK_LENGTH = 0  # Track length in seconds
PAUSED_POSITION = 0  # Store the paused position
CURRENT_SONG_PAUSED = True  # Track if the current song is paused

QUEUE = []
QUEUE_INDEX = 0

def add_songs_to_queue():
    global QUEUE
    # Get a list of music files in the folder
    music_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith('.mp3')]

    # Shuffle the music files to randomize the order
    random.shuffle(music_files)

    # Add the shuffled music files to the queue
    QUEUE.extend(music_files)

def play_random_music():
    global TIMER_RUNNING, TIMER_REMAINING, CURRENT_TRACK_LENGTH, CURRENT_SONG_PAUSED, QUEUE, QUEUE_INDEX

    # If the queue is empty, add songs to it
    if not QUEUE:
        add_songs_to_queue()

    # Check if there are more songs in the queue
    if QUEUE_INDEX < len(QUEUE):
        next_song = QUEUE[QUEUE_INDEX]
        QUEUE_INDEX += 1
        music_path = os.path.join(MUSIC_FOLDER, next_song)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
        CURRENT_TRACK_LENGTH = pygame.mixer.Sound(music_path).get_length()
        update_status(f'Now Playing: {next_song}')
        update_track_time_label(CURRENT_TRACK_LENGTH)
        CURRENT_SONG_PAUSED = False
        update_queue_display()
    else:   
        update_status("Queue is empty")
        add_songs_to_queue()

def update_queue_display():
    queue_listbox.delete(0, tk.END)  # Clear the queue listbox
    for index, song in enumerate(QUEUE, start=1):
        queue_listbox.insert(tk.END, f"{index}. {song}")

def handle_music_end(event):
    if event.type == pygame.USEREVENT:
        play_next_in_queue()

def start_timer():
    global TIMER_LENGTH, TIMER_RUNNING, TIMER_REMAINING
    if TIMER_RUNNING:
        reset_timer()
    else:
        try:
            TIMER_LENGTH = int(timer_length_entry.get())

            TIMER_RUNNING = True
            TIMER_PAUSED = False
            TIMER_REMAINING = TIMER_LENGTH
            timer_label.config(text=f'Time Left: {TIMER_REMAINING} seconds')
            reset_timer()
            TIMER_RUNNING = True
        except ValueError:
            pass
    countdown()

def stop_music():
    pygame.mixer.music.stop()
    update_status('Music Stopped')
    reset_timer()

def update_playback_time_label():
    global CURRENT_SONG_PAUSED
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() / 1000  # Convert to seconds
        remaining_time = max(0, CURRENT_TRACK_LENGTH - current_time)
        update_track_time_label(remaining_time)
        if remaining_time == 0:
            play_next_in_queue()
    elif not CURRENT_SONG_PAUSED:
        # Music has ended, play a new song
        play_next_in_queue()
    app.after(1000, update_playback_time_label)

def change_volume(val):
    volume = float(val) / 200
    pygame.mixer.music.set_volume(volume)

def scroll_status_label():
    if canvas.find_withtag("status"):
        x, _ = canvas.coords("status")
    else:
        x = canvas_width  # Initial position when there's no "status" text

    canvas.move("status", -1, 0)

    if x < -canvas_width / 2:
        canvas.coords("status", canvas_width * 5, canvas_height / 2)
    canvas.after(30, scroll_status_label)

def update_status(text):
    canvas.delete("status")
    canvas.create_text(canvas_width, canvas_height / 2, text=text, font=("Helvetica", 14), tags="status", anchor="e")

def pause_resume_music():
    global CURRENT_SONG_PAUSED, PAUSED_POSITION
    try:
        if CURRENT_SONG_PAUSED:
            pygame.mixer.music.unpause()
            CURRENT_SONG_PAUSED = False
            pygame.mixer.music.set_pos(PAUSED_POSITION)  # Resume from the paused position
        else:
            PAUSED_POSITION = pygame.mixer.music.get_pos() / 1000  # Store the current position
            pygame.mixer.music.pause()
            CURRENT_SONG_PAUSED = True
    except pygame.error as e:
        print(f"An error occurred: {e}")

def pause_resume_timer():
    global TIMER_RUNNING, TIMER_PAUSED
    if TIMER_RUNNING:
        TIMER_RUNNING = False
        TIMER_PAUSED = True
    elif TIMER_PAUSED:
        TIMER_RUNNING = True
        TIMER_PAUSED = False
        countdown()

def reset_timer():
    global TIMER_RUNNING, TIMER_PAUSED, TIMER_REMAINING
    TIMER_RUNNING = False
    TIMER_PAUSED = False
    TIMER_REMAINING = TIMER_LENGTH
    timer_label.config(text=f'Time Left: {TIMER_REMAINING} seconds')

def countdown():
    global TIMER_REMAINING, CURRENT_SONG_PAUSED, PAUSED_POSITION
    if TIMER_RUNNING and not TIMER_PAUSED and TIMER_REMAINING > 0:
        TIMER_REMAINING -= 1
        timer_label.config(text=f'Time Left: {TIMER_REMAINING} seconds')
        app.after(1000, countdown)
    elif TIMER_REMAINING == 0:
        PAUSED_POSITION = pygame.mixer.music.get_pos() / 1000
        pygame.mixer.music.pause()
        CURRENT_SONG_PAUSED = True

def update_track_time_label(time_remaining):
    track_time_label.config(text=f'Track Time Left: {int(time_remaining)} seconds')

def play_next_in_queue():
    global QUEUE, CURRENT_TRACK_LENGTH, CURRENT_SONG_PAUSED
    if QUEUE:
        selected_index = queue_listbox.curselection()
        if selected_index:
            index_to_skip = selected_index[0]
            skip_to_song(index_to_skip)
        else:
            next_song = QUEUE.pop(0)  # Remove the first song from the queue
            QUEUE.append(next_song)  # Put the first song at the end of the queue
            music_path = os.path.join(MUSIC_FOLDER, next_song)
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()
            CURRENT_TRACK_LENGTH = pygame.mixer.Sound(music_path).get_length()
            update_status(f'Now Playing: {next_song}')
            update_track_time_label(CURRENT_TRACK_LENGTH)
            CURRENT_SONG_PAUSED = False
            update_queue_display()
    else:
        add_songs_to_queue()
        play_next_in_queue()

def skip_to_song(index):
    global QUEUE
    if 0 <= index < len(QUEUE):  # Check if the index is valid and not the currently playing song
        # Remove the selected song from the queue
        selected_song = QUEUE.pop(index)
        # Insert the selected song at the front of the queue
        QUEUE.insert(0, selected_song)
        update_queue_display()
        play_next_in_queue()

# Initialize the Tkinter app
app = ThemedTk(theme='arc')  # Use the 'arc' theme for a modern look
app.title("Music Player")
pygame.mixer.music.set_endevent(pygame.USEREVENT)

# Bind the music end event
app.bind(pygame.USEREVENT, handle_music_end)

damn = Label(app, text="Harry's Music Player", font=("Helvetica", 20, "bold"))
damn.pack()


# Create UI elements
queue_label = Label(app, text="Queue", font=("Helvetica", 16, "bold"))
queue_label.pack()

queue_listbox = Listbox(app, height=5, width=40, font=("Helvetica", 12))
queue_listbox.pack()

start_resume_button = Button(app, text="Start/Skip Music", command=play_next_in_queue, style='TButton')
pause_resume_button = Button(app, text="Pause/Resume Music", command=pause_resume_music, style='TButton')
volume_label = Label(app, text="Volume", font=("Helvetica", 14))
volume_scale = Scale(app, from_=0, to=200, orient='horizontal', command=change_volume)
canvas_width = 400  # Adjust the width as needed
canvas_height = 30  # Adjust the height as needed
canvas = Canvas(app, width=canvas_width, height=canvas_height)
timer_label = Label(app, text=f'Time Left: {TIMER_LENGTH} seconds', font=("Helvetica", 14))
timer_length_entry = Entry(app, width=5, font=("Helvetica", 12))
timer_length_label = Label(app, text="Timer Length (s):", font=("Helvetica", 14))
start_timer_button = Button(app, text="Start/Reset Timer", command=start_timer, style='TButton')
pause_resume_timer_button = Button(app, text="Pause/Resume Timer", command=pause_resume_timer, style='TButton')

track_time_label = Label(app, text="Track Time Left: N/A seconds", font=("Helvetica", 12))
track_time_label.pack()

# Apply styles to buttons
style = ttk.Style()
style.configure('TButton', font=("Helvetica", 12))

# Place UI elements on the window
start_resume_button.pack(pady=5)
pause_resume_button.pack(pady=5)
volume_label.pack()
volume_scale.pack()
canvas.pack(pady=10)
timer_label.pack()
timer_length_label.pack()
timer_length_entry.pack()
start_timer_button.pack()
pause_resume_timer_button.pack()

# Start scrolling the status label
add_songs_to_queue()
update_playback_time_label()
canvas.after(40, scroll_status_label)

# Start the Tkinter main loop
app.mainloop()
