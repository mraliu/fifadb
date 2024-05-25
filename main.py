import tkinter as tk, random, sqlite3
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import os, random

# Pages in function
def searchplayerPage(framename):
    def getfieldheadings():
        cur = conn.cursor()
        sql = 'SELECT * FROM players'
        headings = cur.execute(sql)
        return headings

    def OnDoubleClick(event):
        try:
            item = treeview.selection()[0]
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
        [treeview.delete(item) for item in treeview.get_children()]
        [treeview.insert("", tk.END, text=record[0], values=record[1:]) for record in res.fetchall()]
        treeview.bind("<Double-1>", OnDoubleClick)

    # Main program
    # Data
    getbgimage(framename)

    conn = sqlite3.connect("fifa.db")
    headings = getfieldheadings()
    heading = [field[0] for field in headings.description]

    # Search Player Frame Elements
    scrollbarv = tk.Scrollbar(framename, orient='vertical')
    scrollbarh = tk.Scrollbar(framename, orient='horizontal')

    gkbtn = tk.Button(framename, text="Goalkeeper", command=lambda x="gk":filterdb(x), bg="Green")
    gkbtn.place(x = 50, y = 75, width = 100, height = 20)

    defbtn = tk.Button(framename, text="Defender", command=lambda x="def":filterdb(x), bg="Red")
    defbtn.place(x = 150, y = 75, width = 100, height = 20)

    midbtn = tk.Button(framename, text="Midfielder", command=lambda x="mid":filterdb(x), bg="Aqua")
    midbtn.place(x = 250, y = 75, width = 100, height = 20)

    attbtn = tk.Button(framename, text="Attack", command=lambda x="att":filterdb(x), bg="Brown")
    attbtn.place(x = 350, y = 75, width = 100, height = 20)

    treeview = ttk.Treeview(framename, columns=heading[1:])

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

    searchlbl = tk.Label(framename, text="Search ", font="Tahoma 10")
    searchlbl.place(x=50, y=300)

    # Drop Down menu
    listmenu = tk.StringVar() 
    listmenu.set(heading[0]) 
    drop = tk.OptionMenu(framename, listmenu, *heading) 
    drop.place(x=100, y=295, width=100)

    searchentry  = tk.Entry(framename)
    searchentry.place(x=220, y=300)

    searchbtn  = tk.Button(framename, text="Search", command=searchdb, bg="Gold")
    searchbtn.place(x=350, y=300, height=20)

def startPage(framename):

    getbgimage(framename)

    titleLbl = tk.Label(framename, text="Football Manager", font="Tahoma 26 bold", bg="Grey", fg="White", justify=tk.CENTER)
    titleLbl.place(x=200,y=50, width=400)

    startBtn = tk.Button(framename, text="Start", font="Tahoma 20", bg="Blue", fg="Yellow", command=lambda x="Setup":switchpage(x))
    startBtn.place(x=200,y=150, width=400)

    continueBtn = tk.Button(framename, text="Continue", font="Tahoma 20",  bg="Blue", fg="Yellow", command=lambda x="Load":switchpage(x))
    continueBtn.place(x=200,y=250, width=400)

    quitBtn = tk.Button(framename, text="Quit", font="Tahoma 20",  bg="Blue", fg="Yellow", command=quit)
    quitBtn.place(x=200,y=350, width=400)

def managersetupPage(framename):
    def getTeams():
        return [team[0] for team in sqlite3.connect("fifa.db").cursor().execute('select team_name from teams where league_id =13 and league_name = "Premier League" and fifa_version = 24 ORDER BY team_name').fetchall()]
    
    def saveData():
        name = nameEnt.get()
        team = listmenu.get()

        if name == "":
            messagebox.showwarning("Error", "Please enter a name.")
        else:
            file = open("savedata.txt", "a")
            file.write(name + "," + team + "\n")
            file.close()
        
        switchpage("Team") 

    getbgimage(framename)

    nameLbl = tk.Label(framename, text="Name ", font="Tahoma 14")
    nameLbl.place(x=50,y=50)

    nameEnt = tk.Entry(framename, font="Tahoma 14")
    nameEnt.place(x=120,y=49, height=30)

    teamLbl = tk.Label(framename, text="Team ", font="Tahoma 14")
    teamLbl.place(x=50,y=100)

    teams = getTeams()
    listmenu = tk.StringVar() 
    listmenu.set(teams[0]) 
    drop = tk.OptionMenu(framename, listmenu, *teams) 
    drop.config(font="Tahoma 12")
    drop.place(x=120, y=99, width=200, height=30)

    continueBtn = tk.Button(framename, text="Continue", font="Tahoma 14", bg="Blue", fg="Yellow", command=saveData)
    continueBtn.place(x=50, y=150, width=100, height=30)

    backBtn = tk.Button(framename, text="Back", font="Tahoma 14", bg="Blue", fg="Yellow", command=lambda x="Start":switchpage(x))
    backBtn.place(x=50, y=201, width=100, height=30)

def loadgamePage(framename):
    def openData():
        file = open("savedata.txt")
        txt = file.read()
        return [player for player in txt.splitlines()]    

    def loadData():
        global currentplayer, teamname
        currentplayer = listmenu.get().split(",")[0]
        teamname = listmenu.get().split(",")[1]
        switchpage("Team") 

    getbgimage(framename)

    teamLbl = tk.Label(framename, text="Players ", font="Tahoma 14")
    teamLbl.place(x=50,y=50)

    players = openData()
    listmenu = tk.StringVar() 
    listmenu.set(players[0]) 
    drop = tk.OptionMenu(framename, listmenu, *players) 
    drop.config(font="Tahoma 12")
    drop.place(x=140, y=49, width=200, height=30)

    continueBtn = tk.Button(framename, text="Continue", font="Tahoma 14", bg="Blue", fg="Yellow", command=loadData)
    continueBtn.place(x=50, y=100, width=100, height=30)

    backBtn = tk.Button(framename, text="Back", font="Tahoma 14", bg="Blue", fg="Yellow", command=lambda x="Start":switchpage(x))
    backBtn.place(x=50, y=150, width=100, height=30)
    
def teamPage(framename):
    def getfieldheadings():
        cur = conn.cursor()
        sql = 'SELECT * FROM players'
        headings = cur.execute(sql)
        return headings

    def OnDoubleClick(event):
        try:
            item = treeview.selection()[0]
        except IndexError:
            messagebox.showwarning(message="No player selected.", title="No selection")
        else:
            text = treeview.item(treeview.focus())['values']
            messagebox.showinfo(message=text, title="Player")

    def filterdb(*ptype):
        playerposition = {"gk":["GK"], "def":["RB", "LB", "CB"], "mid":["CM", "CAM", "CDM", "RM", "LM"], "att":["ST", "CF", "LW", "RW"]}
        print("ptype")
        sqlstr=""
        if len(ptype) != 0:
            for idx, position in enumerate(playerposition[ptype[0]]):
                if idx == 0:
                    sqlstr+='"Positions Played" LIKE "%{}%" '.format(position)
                else:
                    sqlstr+='OR "Positions Played" LIKE "%{}%" '.format(position)
            cur = conn.cursor()
            sql = f'SELECT * FROM players WHERE {sqlstr} AND "Club Name" = "{teamname}"'
        else:
            sql = f'SELECT * FROM players WHERE "Club Name" = "{teamname}"'
        print(sql)
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
        [treeview.delete(item) for item in treeview.get_children()]
        [treeview.insert("", tk.END, text=record[0], values=record[1:]) for record in res.fetchall()]
        treeview.bind("<Double-1>", OnDoubleClick)

    # Main program
    # Data
    getbgimage(framename)

    conn = sqlite3.connect("fifa.db")
    
    headings = getfieldheadings()
    heading = [field[0] for field in headings.description]

    # Search Player Frame Elements
    scrollbarv = tk.Scrollbar(framename, orient='vertical')
    scrollbarh = tk.Scrollbar(framename, orient='horizontal')

    gkbtn = tk.Button(framename, text="Goalkeeper", command=lambda x="gk":filterdb(x), bg="Green")
    gkbtn.place(x = 50, y = 75, width = 100, height = 20)

    defbtn = tk.Button(framename, text="Defender", command=lambda x="def":filterdb(x), bg="Red")
    defbtn.place(x = 150, y = 75, width = 100, height = 20)

    midbtn = tk.Button(framename, text="Midfielder", command=lambda x="mid":filterdb(x), bg="Aqua")
    midbtn.place(x = 250, y = 75, width = 100, height = 20)

    attbtn = tk.Button(framename, text="Attack", command=lambda x="att":filterdb(x), bg="Brown")
    attbtn.place(x = 350, y = 75, width = 100, height = 20)

    treeview = ttk.Treeview(framename, columns=heading[1:])

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

    searchlbl = tk.Label(framename, text="Search ", font="Tahoma 10")
    searchlbl.place(x=50, y=300)

    # Drop Down menu
    listmenu = tk.StringVar() 
    listmenu.set(heading[0]) 
    drop = tk.OptionMenu(framename, listmenu, *heading) 
    drop.place(x=100, y=295, width=100)

    searchentry  = tk.Entry(framename)
    searchentry.place(x=220, y=300)

    searchbtn  = tk.Button(framename, text="Search", command=searchdb, bg="Gold")
    searchbtn.place(x=350, y=300, height=20)

# Functions for program
def getcolour():
    rgb = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

def getbgimage(framename):
    # BG image  
    img = random.choice(images)
    bglabel = tk.Label(framename, image=img)
    bglabel.pack()

def switchpage(pagename):
    [frames[frame].place_forget() for frame in frames]
    
    playerLbl.place(x=500,y=0)
    playerLbl.config(text=currentplayer)
    teamLbl.place(x=500,y=25)
    teamLbl.config(text=teamname)

    pageLbl.place(x=5,y=0)
    pageLbl.config(text=pagename)
    frames[pagename].place(x=0,y=50, width=800, height=550)

# Tk Main Window
root = tk.Tk()
root.title("DB window")
root.geometry("800x600")
root.resizable(False, False)

# Image background
# images = [Image.open(os.fsdecode(file)) for file in os.listdir("images")]
images = [ImageTk.PhotoImage(Image.open("images/"+os.fsdecode(file))) for file in os.listdir("images")]


# Pages stored in array
pages = ["Start", "Search", "Setup", "Load", "Team"]
frames = {page:tk.Frame(root, bg=getcolour()) for page in pages}
currentplayer, teamname = "", ""

# Initalise pages
searchplayerPage(frames["Search"])
managersetupPage(frames["Setup"])
startPage(frames["Start"])
loadgamePage(frames["Load"])
teamPage(frames["Team"])

# Initial page
frames["Start"].place(x=0,y=0, width=800, height=600) # INIT starting frame

# File menu
filemenu = tk.Menu(root)
root.config(menu=filemenu)
# Sub menu
subfilemenu = tk.Menu(filemenu)
filemenu.add_cascade(label="DEBUGGING", menu=subfilemenu)
[subfilemenu.add_command(label=page, command=lambda p=page:switchpage(p)) for page in pages] # Pages from loop
subfilemenu.add_command(label="Exit", command=root.quit)

# Page label
pageLbl = tk.Label(root, text="", font="Tahoma 26 bold")
teamLbl = tk.Label(root, text="", font="Tahoma 12 bold")
playerLbl = tk.Label(root, text="", font="Tahoma 12 bold")

root.mainloop()