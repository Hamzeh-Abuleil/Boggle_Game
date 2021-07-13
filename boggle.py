import tkinter as tk
from boggle_board_randomizer import randomize_board

initial = [[''] * 4] * 4
time = 180
game_on = False
windows = []
wrd_lst = []
button_lst = {}
head_lst = [1]


def dictionary(filename):
    """read the dictionary"""
    lst = []
    with open(filename, 'r') as file:
        all_words = file.readlines()
        for word in all_words:
            word = word[:len(word) - 1]
            lst.append(word)
    return lst


def check_word():
    """check if the chosen word is in the dictionary"""
    global wrd_lst, head_lst
    if not wrd_lst:
        word_display['text'] = ""
    word = "".join(wrd_lst)
    all_words = dictionary('boggle_dict.txt')
    if word in all_words and word:
        update_score(word)
    else:
        word_display['fg'] = 'red'

    head_lst = [1]
    wrd_lst = []
    for button in button_lst:
        button['bg'] = 'white'


def generate_button(letters):
    """plot buttons on the screen"""
    global button_lst
    for i in range(16):
        row = i // 4
        column = i % 4
        button_1 = tk.Button(button_frame, text=letters[row][column],
                             bg='white')
        button_1.place(relheight=0.25, relwidth=0.25, relx=(i % 4) * 0.25,
                       rely=(i // 4) * 0.25)
        button_lst[button_1] = (row, column)
        button_1.configure(command=cmd_button(button_1))


def check_left(prev_button, cur_button):
    """check if the clicked button could be to the left of the last button"""

    if button_lst[cur_button][0] == button_lst[prev_button][0] and \
            button_lst[cur_button][1] == button_lst[prev_button][1] - 1:
        return True
    return False


def check_right(prev_button, cur_button):
    """check if the clicked button could be to the right of the last button"""

    if button_lst[cur_button][0] == button_lst[prev_button][0] and \
            button_lst[cur_button][1] == button_lst[prev_button][1] + 1:
        return True
    return False


def check_up(prev_button, cur_button):
    """check if the clicked button could be to the top of the last button"""

    if button_lst[cur_button][1] == button_lst[prev_button][1] and \
            button_lst[cur_button][0] == button_lst[prev_button][0] - 1:
        return True
    return False


def check_down(prev_button, cur_button):
    """check if the clicked button could be to the bottom of the last button"""

    if button_lst[cur_button][1] == button_lst[prev_button][1] and \
            button_lst[cur_button][0] == button_lst[prev_button][0] + 1:
        return True
    return False


def check_up_left(prev_button, cur_button):
    """check if the clicked button could be to the top_left of the last
    button"""

    if button_lst[cur_button][0] == button_lst[prev_button][0] - 1 and \
            button_lst[cur_button][1] == button_lst[prev_button][1] - 1:
        return True
    return False


def check_up_right(prev_button, cur_button):
    """check if the clicked button could be to the top_right of the last
     button"""

    if button_lst[cur_button][0] == button_lst[prev_button][0] - 1 and \
            button_lst[cur_button][1] == button_lst[prev_button][1] + 1:
        return True
    return False


def check_down_left(prev_button, cur_button):
    """check if the clicked button could be to the bottom_left of the last
     button"""

    if button_lst[cur_button][1] == button_lst[prev_button][1] - 1 and \
            button_lst[cur_button][0] == button_lst[prev_button][0] + 1:
        return True
    return False


def check_down_right(prev_button, cur_button):
    """check if the clicked button could be to the botom_right of the last
     button"""

    if button_lst[cur_button][1] == button_lst[prev_button][1] + 1 and \
            button_lst[cur_button][0] == button_lst[prev_button][0] + 1:
        return True
    return False


def check_click_legal(prev_button, cur_button):
    """check if the chosen button could be added"""

    if cur_button['bg'] != 'Cyan':
        if check_left(prev_button, cur_button) or\
                check_right(prev_button, cur_button) or\
                check_up(prev_button, cur_button) or\
                check_down(prev_button, cur_button) or\
                check_up_left(prev_button, cur_button) or\
                check_up_right(prev_button, cur_button) or\
                check_down_left(prev_button, cur_button) or\
                check_down_right(prev_button, cur_button):
            return True

    return False


def update_empty_lst(button_1):
    """update the word list when it's empty"""

    word_display['fg'] = 'black'
    head_lst[0] = button_1
    button_1['bg'] = 'Cyan'
    wrd_lst.append(button_1['text'])
    word_display.configure(text="".join(wrd_lst))


def update_lst(button_1):
    """update the word list when there is at least one letter inside"""

    if head_lst:

        if check_click_legal(head_lst[-1],
                             button_1) and button_1 not in head_lst:
            button_1['bg'] = 'Purple'
            wrd_lst.append(button_1['text'])
            head_lst.append(button_1)
            word_display.configure(text="".join(wrd_lst))
        for i in head_lst:
            if i != head_lst[-1]:
                i['bg'] = 'Cyan'


def cmd_button(button_1):
    """update the display label and add the letter chosen to a list"""

    def append_func():
        if button_1['text'] != "":
            global wrd_lst
            pure_lst = [i for i in wrd_lst if i != ""]
            if not pure_lst:
                update_empty_lst(button_1)

            else:
                update_lst(button_1)

    return append_func


def start_game(cur_button):
    """initialize the game and start the time"""

    global time, game_on, wrd_lst
    initialize()
    time = 180
    game_on = True
    cmd_refresh()
    window.after(1000, minus_time(cur_button))
    cur_button.configure(text='stop')


def cmd_start(cur_button):
    """generate command for event:click start_button"""

    def func():
        if not game_on:
            start_game(cur_button)
        else:
            new_game(cur_button)
    return func


def change_stopwatch(timez):
    """change the presented time on the stopwatch"""

    m = timez // 60
    s2 = timez % 60
    s1 = 0 if s2 < 10 else ""
    now = f"{m}:{s1}{s2}"
    stopwatch.configure(text=now)


def change_timer_color(timez):
    """change the bg color of the stopwatch"""

    if timez > 90:
        stopwatch.configure(bg='green')
    if 31 <= timez <= 90:
        stopwatch.configure(bg='yellow')
    elif 0 <= timez <= 30:
        stopwatch.configure(bg='red')


def minus_time(cur_button):
    """generate a function that calculates the current remained time"""

    def func():
        global time, game_on
        time -= 1
        if game_on:
            change_stopwatch(time)
            change_timer_color(time)
            if time == 0:
                game_on = True
                new_game(cur_button)
            else:
                window.after(1000, minus_time(cur_button))
    return func


def initialize():
    """clear the score and the current word list"""

    score['text'] = 'Score: 0'
    correct_words.delete(0, 'end')


def refresh():
    """get list of letters of the board"""

    letters = randomize_board()
    return letters


def cmd_refresh():
    """command when click the Refresh Button, present new letters
    on the buttons"""
    if game_on:
        global wrd_lst, head_lst
        letters = refresh()
        generate_button(letters)
        wrd_lst = []
        head_lst = [1]
        for button in button_lst:
            button['bg'] = 'white'
        word_display['text'] = ""


def close():
    """close all windows"""
    if windows:
        for wind in windows:
            if type(wind) is tuple:
                wind[0].destroy()
                windows.remove(wind)
        for i in windows:
            i.destroy()


def new_round(new_window):
    """generate the function for the command when one chose to play agian"""

    global game_on
    game_on = False

    def func():
        new_window.destroy()
        windows.remove(new_window)
        window.after(1000)
        new_button = tk.Button(start_frame, text='Start', bg='orchid3')
        new_button.place(relheight=0.8, relwidth=0.1, relx=0.45, rely=0.1)
        new_button['command'] = cmd_start(new_button)
    return func


def build_second_window():
    """initial new window which asks for new game"""

    new_window = tk.Tk()
    windows.append(new_window)
    new_window.protocol("WM_DELETE_WINDOW", new_round(new_window))

    ask = tk.Label(new_window, text='Would You Like To Play Again?', bg='Cyan')
    ask.pack(fill=tk.X)

    frame = tk.Frame(new_window)
    frame.pack()

    yes_button = tk.Button(frame, text='Yes', bg='green',
                           command=new_round(new_window))
    yes_button.pack(side=tk.LEFT)

    no_button = tk.Button(frame, text='No', bg='red',
                          command=close)
    no_button.pack(side=tk.LEFT)


def new_game(cur_button):
    """initialize a new game"""

    global wrd_lst
    wrd_lst = []
    word_display['text'] = ""
    cur_button.destroy()
    generate_button(initial)
    build_second_window()


def update_score(wrd):
    """calculates and update the Score and display it"""

    if wrd not in correct_words.get(0, 'end'):
        correct_words.insert(tk.END, wrd)
        current = int(score['text'][7:])
        new = len(wrd) ** 2
        score.configure(text=f"Score: {current + new}")
        word_display['fg'] = 'green'
    else:
        word_display['fg'] = 'orange'


def surprise(event):
    """little surprising function"""
    def on_close():
        windows.remove(window_3)
        window_3.destroy()

    if 174 <= event.x <= 186 and 204 <= event.y <= 219:
        window_3 = tk.Tk()
        windows.append(window_3)
        surprise_label = tk.Label(window_3, height=5, width=30,
                                  text="ONLY FEW PEOPLE CAN REACH HERE!")
        surprise_label.pack()
        window_3.protocol("WM_DELETE_WINDOW", on_close)
        window_3.after(1500, on_close)
        score['bg'] = 'Gold'


def ask_func():
    """ask if you want to quit on clicking X"""
    def remove_option_window():
        """removes the external window"""
        for wind in windows:
            if type(wind) is tuple:
                wind[0].destroy()
                windows.remove(wind)
    remove_option_window()

    def stay():
        """removes teh external window and stay with the main one"""
        count = 0
        for wind in windows:
            if type(wind) is tuple:
                wind[0].destroy()
                windows.remove(wind)
                count += 1
        if count == 0:
            option_window.destroy()
            windows.remove(option_window)

    option_window = tk.Tk()
    windows.append((option_window,1))
    option_window.protocol('WM_DELETE_WINDOW',remove_option_window)

    ask = tk.Label(option_window, text='Would You Like To Leave?', bg='Cyan')
    ask.pack(fill=tk.X)

    frame = tk.Frame(option_window)
    frame.pack()

    yes_button = tk.Button(frame, text='Yes', bg='green',
                           command=close)
    yes_button.pack(side=tk.LEFT)

    no_button = tk.Button(frame, text='No', bg='red',
                          command=stay)
    no_button.pack(side=tk.LEFT)


window = tk.Tk()
windows.append(window)
window.protocol("WM_DELETE_WINDOW", ask_func)
"""this is the main window which has all the frames"""

root_frame = tk.Frame(window)
root_frame.pack()
"""this is the frame for all the frames"""

upper_frame = tk.Frame(root_frame, height=10)
upper_frame.pack()
"""this is the upper border"""

left_frame = tk.Frame(root_frame, width=10)
left_frame.pack(side=tk.LEFT)
"""this is the left border"""

bottom_frame = tk.Frame(root_frame, height=10)
bottom_frame.pack(side=tk.BOTTOM)
"""this is the bottom border"""

main_frame = tk.Frame(root_frame)
main_frame.pack(side=tk.LEFT)
"""this is the main frame"""

right_frame = tk.Frame(root_frame, width=10)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)
"""this is the right border"""

left_image = tk.PhotoImage(file='images/left.png')
word_frame = tk.Frame(main_frame)
word_frame.pack(side=tk.LEFT)
"""the frame which consists the left label"""

words = tk.Label(word_frame, image=left_image)
words.pack()
"""this is the background for the stopwatch and score board"""

sep_frame_1 = tk.Frame(main_frame, width=10)
sep_frame_1.pack(side=tk.LEFT, fill=tk.Y)
"""this separates the left frame from the middle frame for aesthetic reasons"""

start_board_frame = tk.Frame(main_frame)
start_board_frame.pack(side=tk.LEFT, fill=tk.Y)
"""this is the frame to put the start frame and the board frame"""

start_frame = tk.Frame(start_board_frame)
start_frame.pack(side=tk.TOP)
"""this is the frame to put the board that has the Quit, Start and Refresh
 Button"""

start_image = tk.PhotoImage(file='images/up.png')
start = tk.Label(start_frame, image=start_image)
start.pack()
"""this is the background for the Quit, Start and Refresh Button"""

start_button = tk.Button(start_frame, text='Start', bg='orchid3')
start_button.place(relheight=0.8, relwidth=0.1, relx=0.45, rely=0.1)
start_button['command'] = cmd_start(start_button)
"""this is the Start Button"""

refresh_button = tk.Button(start_frame, text='Refresh', command=cmd_refresh)
refresh_button.place(relheight=0.6, relwidth=0.1, relx=0.89, rely=0.2)
"""this is the Refresh Button"""

quit_button = tk.Button(start_frame, text='Quit', bg='red',
                        command=ask_func)
quit_button.place(relheight=0.6, relwidth=0.05, relx=0.01, rely=0.2)
"""this is the Quit Button"""

sep_frame_2 = tk.Frame(start_board_frame, height=10)
sep_frame_2.pack(fill=tk.X)
"""this separates the middle frame from the top frame for aesthetic reasons"""

board_frame = tk.Frame(start_board_frame)
board_frame.pack(side=tk.TOP, expand=1, fill=tk.BOTH)
"""this is the frame to put the background label for the buttons"""

img = tk.PhotoImage(file='images/board.png')
board = tk.Label(board_frame, image=img)
board.pack(fill=tk.BOTH, expand=1)
board.bind("<Button-1>", surprise)
"""this is the background for the buttons"""

word_display = tk.Label(board_frame, bg='white', font=("Helvetica", 15))
word_display.place(relheight=0.11, relwidth=0.405, relx=0.54, rely=0.01)
"""this is the label that displays the current chosen word"""

check_button = tk.Button(board_frame, text='Check Word / Reset Word',
                         bg='Cyan', command=check_word)
check_button.place(relheight=0.06, relwidth=0.405, relx=0.54, rely=0.135)
"""this is the button that the user click it to finish choosing a word"""

button_frame = tk.Frame(board_frame)
button_frame.pack()
button_frame.place(relheight=0.69, relwidth=0.405, relx=0.54, rely=0.20)
generate_button(initial)
"""this is the frame that put all the buttons"""

sep_frame_3 = tk.Frame(main_frame, width=10)
sep_frame_3.pack(side=tk.LEFT, fill=tk.Y)
"""this separates the middle frame from the right frame for 
aesthetic reasons"""


title_time_frame = tk.Frame(main_frame)
title_time_frame.pack(side=tk.LEFT, fill=tk.BOTH)
"""this is frame to put all the frames on the right"""

image = tk.PhotoImage(file='images/boggle.png')
title = tk.Label(title_time_frame, image=image, bg='pink')
title.pack(side=tk.TOP)
"""this is the background for the found words"""

sep_frame_4 = tk.Frame(title_time_frame, height=10)
sep_frame_4.pack(fill=tk.X)
"""this separates the top frame from the middle frame for aesthetic reasons"""

time_frame = tk.Frame(title_time_frame)
time_frame.pack(fill=tk.BOTH, expand=1)
"""this is the frame to put background for found words"""

time_image = tk.PhotoImage(file='images/right.png')
time_label = tk.Label(time_frame, image=time_image)
time_label.pack(fill=tk.BOTH, expand=1)
"""this is the background for the found words"""

inside_word_frame = tk.Frame(time_frame)
inside_word_frame.pack()
inside_word_frame.place(relheight=0.8, relwidth=0.9, relx=0.05, rely=0.05)
"""this is the frame to put found words in"""


words_bar = tk.Scrollbar(inside_word_frame)
words_bar.pack(side=tk.RIGHT, fill=tk.Y)
"""this is the vertical scrollbar for found words"""

words_bar_2 = tk.Scrollbar(inside_word_frame, orient=tk.HORIZONTAL)
words_bar_2.pack(side=tk.BOTTOM, fill=tk.X)
"""this is the horizontal scrollbar for found words"""


correct_words = tk.Listbox(inside_word_frame, bg='LightSkyBlue2',
                           yscrollcommand=words_bar.set,
                           xscrollcommand=words_bar_2.set)
correct_words.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
"""this present the found words"""

words_bar.config(command=correct_words.yview)
words_bar_2.config(command=correct_words.xview)
"""connect the scrollbars with the listbox"""

score = tk.Label(word_frame, text='Score: 0', bg='black', fg='white',
                 font=("Helvetica", 15))
score.place(relheight=0.1, relwidth=0.9, relx=0.05, rely=0.115)
"""this is the label that display current score"""

stopwatch = tk.Label(word_frame, text='3:00', bg='green', fg='white',
                     font=("Helvetica", 40))
stopwatch.place(relheight=0.1, relwidth=0.9, relx=0.05, rely=0.01)
"""this is the label that display the remained time"""

tk.mainloop()
