import os, sys, time, json
from tkinter.ttk import *
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import main
import threading

try:
    import ctypes
    from PIL import ImageTk, Image
except:
    os.system('pip install Pillow')
    os.system('pip install pystray')
    os.system('pip install ctypes')

import ctypes
from PIL import ImageTk, Image




# with open('F:\\LOL\\champions.json', 'w', encoding='utf-8') as json_file:
#     json.dump(getChampions, json_file, ensure_ascii=False, indent=4)


START = 1
STOP = 0
EXIT = -1


looping = STOP

win = Tk()

win.title("Auto Picker")

screen_width, screen_height = win.winfo_screenwidth(), win.winfo_screenheight()
width = 500
height = 430
x = (screen_width - width) // 2
y = (screen_height - height) // 2

win.geometry(f"{width}x{height}+{x}+{y}")
win.resizable(False,False)
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
win.iconbitmap('F:\\LOL\\kuro.ico')
# win.config(bg='#000')
win.bind("<Escape>", lambda event: win.destroy())

getChampions = list()
def get_Champions():
    global getChampions
    try:
        getChampions = (main.GetChampionsList())
    except:
        messagebox.showinfo("Thông báo","Lỗi rồi :(")
        sys.exit()
win.bind("<FoucusIn>", get_Champions())

disable_img = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\round_button_disable.png'))
enable_img = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\round_button_enable.png'))
light_img = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\light_mode.png'))
dark_img = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\dark_mode.png'))

start_light = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\start_light_button.png'))
start_dark = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\start_dark_button.png'))

running_light = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\running_light.png'))
running_dark = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\running_dark.png'))
search_img = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\search.png'))

# close_img = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\close.png'))
# close_hover_img = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\close_hover.png'))

# minimize_img = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\minimize.png'))
# minimize_hover_img = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\minimize_hover.png'))
title_img = ImageTk.PhotoImage(Image.open('F:\\LOL\\images\\title.png'))
kuro_image = Image.open('F:\\LOL\\images\\kuro.png')
resize_kuroico = kuro_image.resize((20,20) , Image.BILINEAR)
kuroico = ImageTk.PhotoImage(resize_kuroico)


canvas = Canvas(win,width=width,height=height, highlightthickness=0, background="#fff")
# canvas.place(x=-2,y=-2)
canvas.place(x=0,y=0)
canvas.bind("<Button-1>", lambda event: win.focus_set())

tagname = 'text'

canvas.create_text(
    (width/2,7),
    text="Auto Picker",
    fill="black",
    font="Inika 24 bold",
    anchor="n",
    tag=tagname
)

#Dark mode button
isDarkMode = False
def darkmode():
    global isDarkMode, isStarting
    isDarkMode = not isDarkMode
    if isDarkMode:
        canvas.config(bg="#222")
        canvas.itemconfig('text',fill='white')
        canvas.itemconfig(darkmode_btn, image=light_img)
        if isStarting:
            canvas.itemconfig(start_button, image=running_dark)
        else:
            canvas.itemconfig(start_button, image=start_light)
    else:
        canvas.config(bg="#fff")
        canvas.itemconfig('text',fill='black')
        canvas.itemconfig(darkmode_btn, image=dark_img)
        canvas.itemconfig(start_button, image=start_dark)
        if isStarting:
            canvas.itemconfig(start_button, image=running_light)
        else:
            canvas.itemconfig(start_button, image=start_dark)


darkmode_btn = canvas.create_image(208, 59, image=dark_img,anchor=NW)
canvas.tag_bind(darkmode_btn, "<Enter>", lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(darkmode_btn, "<Leave>", lambda event: canvas.config(cursor=""))
canvas.tag_bind(darkmode_btn, "<Button-1>", lambda event: darkmode() )
# ------------------------------------Auto Match------------------------------------


canvas.create_text(
    (175,110),
    text="Tự động chấp nhận vào trận",
    fill="black",
    font="Calibri 16",
    anchor="nw",
    tag=tagname
)

isAutoMatch = False  # Mặc định là False


def AutoMatch(e):
    global isAutoMatch
    isAutoMatch = not isAutoMatch  # Chuyển đổi trạng thái
    if isAutoMatch:
        canvas.itemconfig(autoMatch, image=enable_img)
    else:
        canvas.itemconfig(autoMatch, image=disable_img)

autoMatch = canvas.create_image(104, 110, image=disable_img, anchor=NW)
canvas.tag_bind(autoMatch, "<Enter>", lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(autoMatch, "<Leave>", lambda event: canvas.config(cursor=""))
canvas.tag_bind(autoMatch, "<Button-1>", AutoMatch)

# ------------------------------------Auto lock ------------------------------------
canvas.create_text(
    (175,158),
    text="Tự động khóa",
    fill="black",
    font="Calibri 16",
    anchor="nw",
    tag=tagname
)

isAutoLock = False
def AutoLock():
    global isAutoLock
    isAutoLock = not isAutoLock
    if isAutoLock:
        canvas.itemconfig(autoLock, image=enable_img)
    else:
        canvas.itemconfig(autoLock, image=disable_img)

autoLock = canvas.create_image(104, 158, image=disable_img,anchor=NW)

canvas.tag_bind(autoLock, "<Enter>", lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(autoLock, "<Leave>", lambda event: canvas.config(cursor=""))
canvas.tag_bind(autoLock, "<Button-1>", lambda event: AutoLock())

# ------------------------------------Auto pick ------------------------------------

canvas.create_text(
    (175,206),
    text="Tự động chọn",
    fill="black",
    font="Calibri 16",
    anchor="nw",
    tag=tagname
)
isAutoPick = False
def AutoPick():
    global isAutoPick
    isAutoPick = not isAutoPick
    if isAutoPick:
        canvas.itemconfig(autoPick, image=enable_img)
    else:
        canvas.itemconfig(autoPick, image=disable_img)

autoPick = canvas.create_image(104, 206, image=disable_img,anchor=NW)

canvas.tag_bind(autoPick, "<Enter>", lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(autoPick, "<Leave>", lambda event: canvas.config(cursor=""))
canvas.tag_bind(autoPick, "<Button-1>",lambda event: AutoPick())
 

#------------------------------------ Input Champions ------------------------------------
# loi = canvas.create_image(305, 206, image=input_img,anchor=NW)
def FindChampion(name,data):
    name = name.lower()
    for champion in data:
        if name in champion['name'].lower():
            return champion['name'], champion['id']
        
champion_name = 'Yasuo'
champion_id = 157
def GetChampion():
    global champion_name,champion_id
    champion_name = input.get()
    if champion_name == "":
        champion_name = "Yasuo"
    result = FindChampion(champion_name,getChampions)
    if result is not None:
        champion_name, champion_id = result
        canvas.itemconfig(GetChampionName, text=champion_name)
    else:
        messagebox.showinfo("Thông con báo","Không có tướng nào tên "+champion_name)
    # if not checkName:
    #     return messagebox.showinfo("Thông con báo","Không có tướng nào tên "+champion_name)
    # canvas.itemconfig(GetChampionName, text=checkName)
    # print(checkId)


input = tk.Entry(canvas,border=2,relief=SOLID,width=12 ,background='white',font = "Calibri 13")
input.bind("<Return>", lambda event: GetChampion())

input.place(x=305,y=206)
search_button = canvas.create_image(417, 206, image=search_img,anchor=NW)
canvas.tag_bind(search_button, "<Enter>", lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(search_button, "<Leave>", lambda event: canvas.config(cursor=""))
canvas.tag_bind(search_button, "<Button-1>", lambda event: GetChampion())


canvas.create_text(
    (width/2-50,250),

    text="Pick: ",
    fill="black",
    font="Calibri 16",
    anchor="nw",
    tag=tagname
)
GetChampionName = canvas.create_text(
    (width/2,250),
    text="Yasuo",
    fill="black",
    font="Calibri 16 bold",
    anchor="nw",
    tag=tagname
)
canvas.create_text(
    (width/2,300),
    text=f"Bạn đang có: {len(getChampions)} vị tướng",
    fill="black",
    font="Calibri 16",
    anchor="center",
    tag=tagname
)


status = canvas.create_text(
    (width/2,325),
    text="Đang check...",
    fill="black",
    font="Calibri 14",
    anchor="center",
    tag=tagname
)

# ------------------------------------ Start Button ------------------------------------


isStarting = False
def start():
    global isStarting, looping
    isStarting = not isStarting
    if isStarting:
        canvas.itemconfig(start_button, image=running_light)
        looping = START
        start_loop()
    else:
        canvas.itemconfig(start_button, image=start_dark)
        looping = STOP

    print("check", looping)
# def run_loop():
#     global isStarting
#     while True:
#         print(isStarting)
#         if isStarting:
#             print("hi")
#             print(champion_id)
#             print(isAutoMatch)
#             print(isAutoLock)
#             print(isAutoPick)
#             time.sleep(1)
#         if not isStarting:
#             break

def run_loop():
    global looping, status
    global isAutoMatch,isAutoPick,isAutoLock
    while True:
        
        if looping == START:
            id = main.getActionId()
            if id:
                canvas.itemconfig(status, text="Đang chọn tướng")
                if isAutoPick:
                    main.pick(id,champion_id)
                if isAutoLock:
                    isLock = main.lock(id)
                    if isLock:
                        canvas.itemconfig(status, text="Đã khóa")
                        # time.sleep(10)
                        for i in range(100):
                            try:
                                PIDLOL = main.check_process_exists(main.LOL)
                            except:
                                PIDLOL = False
                            if PIDLOL:
                                break
                            time.sleep(5)
                        if PIDLOL:
                            canvas.itemconfig(status, text="Đang đi báo")
                            return
                try:
                    PIDLOL = main.check_process_exists(main.LOL)
                except:
                    PIDLOL = False
                if PIDLOL:
                    canvas.itemconfig(status, text="Đang đi báo")
            else:
                if isAutoMatch: 
                    isMatching = main.isMatchFound()
                    if isMatching == "Invalid":
                        canvas.itemconfig(status, text="Đang tìm trận")
                        time.sleep(1)
                    elif isMatching == "InProgress":
                        canvas.itemconfig(status, text="Tìm thấy trận")
                        main.acceptMatch()
                    elif main.PID:
                        canvas.itemconfig(status, text="Đang ở sảnh")
                else:
                    canvas.itemconfig(status, text="Đang ở sảnh")

            time.sleep(0.1)
        if looping == STOP:
            time.sleep(1)
            print("Waiting")
        if looping == EXIT:
            break
        
def start_loop():
    thread = threading.Thread(target=run_loop)
    thread.daemon = True
    thread.start()

start_button = canvas.create_image(195, 345, image=start_dark,anchor=NW)
canvas.tag_bind(start_button, "<Enter>", lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(start_button, "<Leave>", lambda event: canvas.config(cursor=""))
canvas.tag_bind(start_button, "<Button-1>", lambda event: start())

canvas.create_text(
    (width/2,height-20),
    text="Code by Inaiyo Kuro",
    fill="black",
    font="Calibri 13",
    anchor="center",
    tag=tagname
)




win.mainloop()
looping = STOP

# win.overrideredirect(True) # Hidden
# def get_pos(e):
#     xwin = win.winfo_x()
#     ywin = win.winfo_y()

#     startx = e.x_root
#     starty = e.y_root
#     ywin = ywin - starty
#     xwin = xwin - startx
#     def move_window(e):
#         win.geometry(f"+{e.x_root + xwin}+{e.y_root + ywin}")
#     startx = e.x_root
#     starty = e.y_root
    
#     canvas1.bind("<B1-Motion>", move_window)
    


# def frame_mapped(e):
#     # win.update_idletasks()
#     # win.overrideredirect(True)
#     # win.state('normal')



# canvas1 = Canvas(win,width=500,height=30,border=0,bg="#fff",borderwidth=0,highlightthickness=0)
# canvas1.place(x=0, y=0, anchor="nw")
# canvas1.bind("<Button-1>", get_pos)
# canvas1.create_image(30,30/2-7, image=title_img,anchor=NW)
# canvas1.create_image(5,30/2-10, image=kuroico,anchor=NW)
# # canvas1.bind("<Map>", frame_mapped)


# def on_enter():
#     canvas1.itemconfig(close_btn,image=close_hover_img)

# def on_leave():
#     canvas1.itemconfig(close_btn,image=close_img)

# close_btn = canvas1.create_image(455,0, image=close_img,anchor=NW)
# canvas1.tag_bind(close_btn, "<Enter>", lambda event: on_enter())
# canvas1.tag_bind(close_btn, "<Leave>", lambda event: on_leave())
# canvas1.tag_bind(close_btn, "<Button-1>", lambda event: win.destroy())


# def minimize():
#     win.update_idletasks()
#     win.overrideredirect(False) # Hidden
#     win.state('iconic')

#     print(win.state())
#     if win.state() == 'iconic':
#         print("Check ",win.state())
#     if win.state() == 'normal':
#         win.overrideredirect(True)

# def check():
#     win.overrideredirect(True)
#     win.state('normal')
# win.bind("<FocusIn>", check)


# def on_enter_minimize():
#     canvas1.itemconfig(minimize_btn,image=minimize_hover_img)
# def on_leave_minimize():
#     canvas1.itemconfig(minimize_btn,image=minimize_img)

# minimize_btn = canvas1.create_image(455,0, image=minimize_img,anchor=NE)
# canvas1.tag_bind(minimize_btn, "<Enter>", lambda event: on_enter_minimize())
# canvas1.tag_bind(minimize_btn, "<Leave>", lambda event: on_leave_minimize())
# canvas1.tag_bind(minimize_btn, "<Button-1>", lambda event: minimize())

