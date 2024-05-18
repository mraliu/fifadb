import tkinter as tk, sqlite3
from tkinter import ttk
from tkinter import messagebox
conn = sqlite3.connect("fifa.db")

def getfieldheadings():
    cur = conn.cursor()
    sql = 'SELECT * FROM players'
    headings = cur.execute(sql)
    return headings

def OnDoubleClick(event):
    try:
        item = treeview.selection()[0]
        # print(treeview.item(treeview.focus()))
    except IndexError:
        messagebox.showwarning(message="No player selected.", title="No selection")
    else:
        text = treeview.item(treeview.focus())['values']
        messagebox.showinfo(message=text, title="Player")

def filterdb(ptype):
    playerposition = {"gk":["GK"], "def":["RB", "LB", "CB"], "mid":["CM", "CAM", "CDM", "RM", "LM"], "att":["ST", "CF", "LW", "RW"]}
    
    sqlstr=""
    for idx, position in enumerate(playerposition[ptype]):
        if idx == 0:
            sqlstr+='"Positions Played" LIKE "%{}%" '.format(position)
        else:
            sqlstr+='OR "Positions Played" LIKE "%{}%" '.format(position)
    cur = conn.cursor()
    sql = f'SELECT * FROM players WHERE {sqlstr}'
    res = cur.execute(sql)
    # Clear the treeview
    for item in treeview.get_children():
      treeview.delete(item)
    # Loop through db and add to treeview
    for record in res.fetchall():
        treeview.insert("", tk.END, text=record[0], values=record[1:])
    treeview.bind("<Double-1>", OnDoubleClick)

def searchdb():
    item = searchentry.get()
    cur = conn.cursor()
    sql = f'SELECT * FROM players WHERE "{listmenu.get()}" LIKE "%{item}%"'
    res = cur.execute(sql)
    for item in treeview.get_children():
      treeview.delete(item)
    # Loop through db and add to treeview
    for record in res.fetchall():
        treeview.insert("", tk.END, text=record[0], values=record[1:])
    treeview.bind("<Double-1>", OnDoubleClick)

headings = getfieldheadings()
heading = []

for field in headings.description:
    heading.append(field[0])

heading = tuple(heading)

# Tk Main Window
root = tk.Tk()
root.title("DB window")
root.geometry("800x600")

def searchPlayerFrame():
    for frame in frames:
        frame.place_forget()
    frames[0].place(x=0,y=50, width=800, height=550)

def myteam():
    for frame in frames:
        frame.place_forget()
    frames[1].place(x=0,y=50, width=800, height=550)

def About():
    print("This is a simple example of a menu")
    
menu = tk.Menu(root)
root.config(menu=menu)

# Menus
filemenu = tk.Menu(menu)
helpmenu = tk.Menu(menu)

menu.add_cascade(label="Game", menu=filemenu)
filemenu.add_command(label="Search Player", command=searchPlayerFrame)
filemenu.add_command(label="My team", command=myteam)
filemenu.add_command(label="Exit", command=root.quit)

menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)
                     
# The frames                     
frames = [tk.Frame(root, bg="Blue"), tk.Frame(root, bg="Green")]

# Search Player Frame Elements
scrollbarv = tk.Scrollbar(frames[0], orient='vertical')
scrollbarh = tk.Scrollbar(frames[0], orient='horizontal')

gkbtn = tk.Button(frames[0], text="Goalkeeper", command=lambda x="gk":filterdb(x), bg="Green")
gkbtn.place(x = 50, y = 75, width = 100, height = 20)

defbtn = tk.Button(frames[0], text="Defender", command=lambda x="def":filterdb(x), bg="Red")
defbtn.place(x = 150, y = 75, width = 100, height = 20)

midbtn = tk.Button(frames[0], text="Midfielder", command=lambda x="mid":filterdb(x), bg="Aqua")
midbtn.place(x = 250, y = 75, width = 100, height = 20)

attbtn = tk.Button(frames[0], text="Attack", command=lambda x="att":filterdb(x), bg="Brown")
attbtn.place(x = 350, y = 75, width = 100, height = 20)

treeview = ttk.Treeview(frames[0], columns=heading[1:])

for idx, head in enumerate(heading):
    if idx==0:
        treeview.column("#0", anchor=tk.CENTER, stretch=tk.NO, width=100)
        treeview.heading("#0", text=head)
    else:
        treeview.column(head, anchor=tk.CENTER, stretch=tk.NO, width=100)
        treeview.heading(head, text=head)

treeview.place(x=50,y=125, width=700, height=150)

scrollbarv.place(x=759, y=125, height=150) 
scrollbarh.place(x=50, y=275, width=700)

scrollbarv.config(command = treeview.yview)
scrollbarh.config(command = treeview.xview)

searchlbl = tk.Label(frames[0], text="Search ", font="Arial 10")
searchlbl.place(x=50, y=300)

# Drop Down menu
listmenu = tk.StringVar() 
listmenu.set(heading[0]) 
drop = tk.OptionMenu(frames[0], listmenu, *heading) 
drop.place(x=100, y=295, width=100)

searchentry  = tk.Entry(frames[0])
searchentry.place(x=220, y=300)

searchbtn  = tk.Button(frames[0], text="Search", command=searchdb, bg="Gold")
searchbtn.place(x=350, y=300, height=20)


# Initial Frame
frames[0].place(x=0,y=50, width=800, height=550)

root.mainloop()