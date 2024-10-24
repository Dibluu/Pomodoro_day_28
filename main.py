from tkinter import *
import pygame.mixer
import os
import sys

# Fonction pour obtenir le chemin du fichier
def resource_path(relative_path):
    """ Obtenir le chemin absolu d'une ressource, compatible avec PyInstaller """
    try:
        # PyInstaller crée un dossier temporaire lors de l'exécution
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
#Initiale Pygame to play the song
pygame.mixer.init()
#Load a sonor file
alarm_sound = pygame.mixer.Sound(resource_path("assets/alarm.wav"))
# ---------------------------- CONSTANTS ------------------------------- #
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
timer_id = None  # Variable pour stocker l'ID de window.after

#Timer mechanism
def start_timer():
    global REPS
    Minutes_work = WORK_MIN * 60
    Short_break = SHORT_BREAK_MIN * 60
    long_break = LONG_BREAK_MIN * 60
    REPS += 1
    # Augmenter REPS après chaque cycle
    if REPS in [1, 3, 5, 7]:
        # Phases de travail (cycles 0, 2, 4, 6)
        count_down(Minutes_work)
        timer_label.config(text="Focus", fg=RED)

    elif REPS in [2, 4, 6]:
        # Pauses courtes (cycles 1, 3, 5)
        count_down(Short_break)
        timer_label.config(text="Short break", fg=PINK)

    elif REPS == 8:
        # Pause longue après 4 cycles de travail (cycle 7)
        count_down(long_break)
        timer_label.config(text="Long break", fg=GREEN)

    elif REPS == 9:
        # Réinitialiser après la pause longue
        REPS = 0

# Fonction pour jouer l'alarme
def play_alarm():
    alarm_sound.play()  # Joue l'alarme sonore
# Countdown mechanism

def count_down(count):
    global timer_id
    minutes = count // 60
    seconds = count % 60
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds:02d}")  # Formatage des secondes
    if count > 0:
      timer_id = window.after(1000, count_down, count-1)  # 1000 ms = 1 seconde
    else:
        play_alarm()
        start_timer()  # Quand le timer atteint 0, démarrer la prochaine phase

def reset_timer():
    global REPS, timer_id
    if timer_id:
        window.after_cancel(timer_id) #Annuler l'appel à after
    REPS = 0  # Réinitialiser le compteur à 0
    canvas.itemconfig(timer_text, text="00:00")  # Réinitialiser l'affichage à 00:00
    timer_label.config(text="Timer", fg=GREEN)
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Timer label
timer_label = Label(text="Timer", font=(FONT_NAME, 45, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(column=1, row=0)

# Canvas for tomato image and timer text
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file=resource_path("assets/image.png"))
canvas.create_image(100, 112, image=tomato_img)
canvas.tomato_img = tomato_img  # Garde une référence à l'image
canvas.grid(column=1, row=1)

# Timer text
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

# Start button
start_button = Button(text="Start", width=10, bg=PINK, highlightthickness=0, borderwidth=0, bd=0,relief="flat", activebackground=PINK, command=start_timer)
start_button.grid(column=0, row=2)
start_button.config(activebackground=PINK, highlightthickness=0, borderwidth=0, bd=0, highlightbackground=YELLOW)

# Reset button
reset_button = Button(text="Reset", width=10, bg=PINK, highlightthickness=0, borderwidth=0, relief="flat", activebackground=PINK)
reset_button.grid(column=2, row=2)
reset_button.config(activebackground=PINK, highlightthickness=0, borderwidth=0, bd=0, highlightbackground=YELLOW, command=reset_timer)
# Add checkmark
checkmark = Label(text="✅", font=(FONT_NAME, 25, "bold"), bg=YELLOW)
checkmark.grid(column=1, row=3)

window.mainloop()