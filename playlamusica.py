import os
import random
import pygame
import tkinter as tk
from tkinter import Scale, Button, Label, Entry

# Initialize pygame
pygame.init()

# Path to the music folder
music_folder = 'C:/Users/harry/PycharmProjects/UDMusicPlayer/allmusic'

# Initialize timer variables
timer_length = 60  # Default timer length in seconds
timer_running = False
timer_paused = False
timer_remaining = timer_length
current_track_length = 0  # Track length in seconds
paused_position = 0  # Store the paused position
current_song_paused = True  # Track if the current song is paused

# Function to play random music
def play_random_music():
    global timer_running, timer_remaining, current_track_length, current_song_paused
    try:
        # Get a list of music files in the folder
        music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
        
        if music_files:
            # Choose a random music file
            random_music = random.choice(music_files)
            
            # Create the full path to the selected music file
            music_path = os.path.join(music_folder, random_music)
            
            # Load and play the music
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()
            current_track_length = pygame.mixer.Sound(music_path).get_length()
            update_status(f'Now Playing: {random_music}')
            update_track_time_label(current_track_length)
            current_song_paused = False

            # Set an event to trigger when the music ends
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            
            # Start the timer for the next song
            timer_remaining = timer_length
            #countdown()
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to handle the music end event
def handle_music_end(event):
    if event.type == pygame.USEREVENT:
        play_random_music()

# Function to start the timer
def start_timer():
    global timer_length, timer_running, timer_remaining
    if timer_running:
        reset_timer()
    else:
        timer_length = int(timer_length_entry.get())
        
        timer_running = True
        timer_paused = False
        timer_remaining = timer_length
        timer_label.config(text=f'Time Left: {timer_remaining} seconds')
        reset_timer()
        timer_running = True
        countdown()

# Function to stop the music
def stop_music():
    pygame.mixer.music.stop()
    update_status('Music Stopped')
    reset_timer()

# Function to update playback time label
def update_playback_time_label():
    global current_song_paused
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() / 1000  # Convert to seconds
        remaining_time = max(0, current_track_length - current_time)
        update_track_time_label(remaining_time)
        if remaining_time == 0:
            play_random_music()
    elif not current_song_paused:
        # Music has ended, play a new song
        play_random_music()
    app.after(1000, update_playback_time_label)

# Function to change the volume
def change_volume(val):
    volume = int(val) / 100
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

# Function to update the status label
def update_status(text):
    canvas.delete("status")
    canvas.create_text(canvas_width, canvas_height / 2, text=text, font=("Helvetica", 14), tags="status", anchor="e")


# Function to pause/resume music
def pause_resume_music():
    global current_song_paused, paused_position
    try:
        if current_song_paused:
            pygame.mixer.music.unpause()
            current_song_paused = False
            pygame.mixer.music.set_pos(paused_position)  # Resume from the paused position
        else:
            paused_position = pygame.mixer.music.get_pos() / 1000  # Store the current position
            pygame.mixer.music.pause()
            current_song_paused = True
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to pause/resume the timer
def pause_resume_timer():
    global timer_running, timer_paused
    if timer_running:
        timer_running = False
        timer_paused = True
    elif timer_paused:
        timer_running = True
        timer_paused = False
        countdown()

# Function to reset the timer
def reset_timer():
    global timer_running, timer_paused, timer_remaining
    timer_running = False
    timer_paused = False
    timer_remaining = timer_length
    timer_label.config(text=f'Time Left: {timer_remaining} seconds')

# Timer countdown function
def countdown():
    global timer_remaining, current_song_paused, paused_position
    if timer_running and not timer_paused and timer_remaining > 0:
        timer_remaining -= 1
        timer_label.config(text=f'Time Left: {timer_remaining} seconds')
        app.after(1000, countdown)
    elif timer_remaining == 0:
        paused_position = pygame.mixer.music.get_pos() / 1000 
        pygame.mixer.music.pause()
        current_song_paused = True

# Function to update the track time label
def update_track_time_label(time_remaining):
    track_time_label.config(text=f'Track Time Left: {int(time_remaining)} seconds')

pygame.init()
# Create the main application window
app = tk.Tk()
app.title("Music Player")
pygame.mixer.music.set_endevent(pygame.USEREVENT)

app.bind(pygame.USEREVENT, handle_music_end)

# Create UI elements
start_resume_button = Button(app, text="Start/Skip Music", command=play_random_music)
pause_resume_button = Button(app, text="Pause/Resume Music", command=pause_resume_music)
volume_label = Label(app, text="Volume")
volume_scale = Scale(app, from_=0, to=100, orient='horizontal', command=change_volume)
canvas_width = 400  # Adjust the width as needed
canvas_height = 30  # Adjust the height as needed
canvas = tk.Canvas(app, width=canvas_width, height=canvas_height)
timer_label = Label(app, text=f'Time Left: {timer_length} seconds')
timer_length_entry = Entry(app, width=5)
timer_length_label = Label(app, text="Timer Length (s):")
start_timer_button = Button(app, text="Start/Reset Timer", command=start_timer)
pause_resume_timer_button = Button(app, text="Pause/Resume Timer", command=pause_resume_timer)

track_time_label = Label(app, text="Track Time Left: N/A seconds")
track_time_label.pack()

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

update_playback_time_label()
canvas.after(40, scroll_status_label)
# Start the Tkinter main loop
app.mainloop()
