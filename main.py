from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_word = None
flip_timer = 1


def flip_card():
    global current_word
    canvas.itemconfig(bg_image, image=card_back)
    english_word = current_word["English"].item()
    canvas.itemconfig(title_label, text="English")
    canvas.itemconfig(word_label, text=english_word)


def next_card():
    word = flip_cards.sample()
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = word
    canvas.itemconfig(bg_image, image=card_front)
    canvas.itemconfig(title_label, text="German")
    canvas.itemconfig(word_label, text=word["German"].item())
    flip_timer = window.after(3000, flip_card)


def card_remove():
    word = current_word
    flip_cards.drop(word.index, inplace=True)
    next_card()


def on_closing():
    flip_cards.to_csv("data/german_words_update.csv", index=False)
    window.destroy()


# layout
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
bg_image = canvas.create_image(400, 263, image=card_front)
title_label = canvas.create_text(400, 150, text="German", font=("Arial", 40, "italic"))
word_label = canvas.create_text(400, 263, text="German Word", font=("Arial", 40, "bold"))
canvas.grid(row=0, column=0, columnspan=2)
# Buttons
ok_image = PhotoImage(file="images/right.png")
ok_button = Button(image=ok_image, highlightthickness=0, command=card_remove)
nok_image = PhotoImage(file="images/wrong.png")
nok_button = Button(image=nok_image, highlightthickness=0, command=next_card)
ok_button.grid(row=1, column=1)
nok_button.grid(row=1, column=0)

# # Dictionary
# word_read = pandas.read_csv("data/german_words.csv")
# selection = word_read[word_read["English"] == word_read["German"]]
# # clean duplicates and empty
# flip_cards = (word_read.drop(selection.index).dropna())
flip_cards = pandas.read_csv("data/german_words_update.csv")

next_card()
# flip_cards.to_csv("data/german_words_update.csv", index=False)


window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
