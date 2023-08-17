import random
from tkinter import *
import math
import json
from tkinter import messagebox


LIGHTGREY = '#cad2c5'
DARKGREY = '#2f3e46'
timer = None
text = ''
count_min = 3
count_sec = 60
len_cust_text = 0
mistakes = []

with open("data.json", mode="r") as file:
    # reading old data
    data = json.load(file)


def count_results(min_left, sec_left, len_entry, mist): #Count result and show results in popup window
    num_mistakes = len(mist)
    min = 2-min_left
    sec = 60 - int(sec_left)
    typing_time = min + sec/60
    symbols_per_min = round(len_entry/typing_time)
    message = f'You typed {len_entry} characters in {min} min {sec} sec. Number of mistakes: {num_mistakes}. Your rate is {symbols_per_min} symbols per minute'
    messagebox.showinfo(title="Your results", message=message)


def check(): #Mistakes checking and highlighting
    global mistakes
    global len_cust_text
    cust_text = entry_text.get(1.0, END)
    len_cust_text = len(cust_text) - 1
    if len_cust_text > 0:
        for letter in range(len_cust_text):
            index_s = '1.' + str(letter)
            index_n = '1.' + str(letter + 1)
            if cust_text[letter] != text[letter]:
                text_label.tag_configure("red", foreground="#ff0000") #mistakes highlighting in red
                text_label.tag_add("red", index_s, index_n)
                if index_s not in mistakes: #adding mistakes to the list to count a number of mistakes
                    mistakes.append(index_s)
            else:
                text_label.tag_configure('green', foreground='#5ba45b') #correct entered text highlighting in green
                text_label.tag_add('green', index_s, index_n)


def count_down(count): #timer
    global timer
    global count_min
    global count_sec
    count_min = math.floor(count/60)
    count_sec = count%60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    clock.config(text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count -1)
        check()
    elif count == 0:
        stop.invoke()


def start(): #change text labels and show typing text
    global text
    label.config(text='GO!', foreground='red')
    text = random.choice(data)
    text_label.configure(state="normal")
    text_label.delete(1.0, END)
    text_label.insert(1.0, text)
    text_label.configure(state="disabled")
    entry_text.delete(1.0, END)
    count_down(180)


def stop(): #changing text labels, resetting the timer, launching the results calculation function
    window.after_cancel(timer)
    label.config(text="Your Typing Test", foreground=DARKGREY)
    text_label.configure(state="normal")
    text_label.delete(1.0, END)
    text_label.insert(1.0, "After starting test you will see the typing text here")
    text_label.configure(state="disabled")
    clock.config(text="00:00")
    entry_text.delete(1.0, END)
    entry_text.insert(1.0, "Enter the Text here")
    if len_cust_text > 0:
        count_results(min_left=count_min, sec_left=count_sec, len_entry=len_cust_text, mist=mistakes)


window = Tk()
window.title("Typing Test")
window.geometry("1000x700")
window.config(pady=30, padx=50, bg=LIGHTGREY)

label = Label(window, text='Your Typing Test',  font=('Times', 20, "italic", 'bold'), borderwidth=5, bg=LIGHTGREY, foreground=DARKGREY)
label.place(x=350, y=20)

clock = Label(window, text='00:00', font=('Times', 20, "bold"), borderwidth=5, bg=LIGHTGREY, relief="sunken", width=5)
clock.place(x=800, y=20)

KEYBOARD = PhotoImage(file="ten-finger-typing.png")
KEYBOARD = KEYBOARD.subsample(2, 2)
# print(KEYBOARD.width())

keyboard = Label(image=KEYBOARD, bg=LIGHTGREY)
keyboard.place(x=260, y=70)


text_label = Text(window, font=('Times', 14), width=95, height=8, wrap="word", relief="ridge", pady=5, padx=5)
text_label.insert(1.0, 'After starting test you will see the typing text here')
text_label.place(x=20, y=250)


entry_text = Text(window, relief='ridge', width=108, height=9, wrap="word")
entry_text.insert(1.0, "Enter the Text here")
entry_text.place(x=20, y=450)

start = Button(text='Start', width=20, command=start)
start.place(x=50, y=620)

stop = Button(text='Stop', width=20, command=stop)
stop.place(x=700, y=620)


window.mainloop()