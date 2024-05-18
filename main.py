import tkinter as tk, random
from page1 import * 

def getcolour():
    rgb = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

def switchpage(pagename):
    [frames[frame].place_forget() for frame in frames]
    pageLbl.config(text=pagename)
    frames[pagename].place(x=0,y=50, width=800, height=550)

# Tk Main Window
root = tk.Tk()
root.title("DB window")
root.geometry("800x600")

# Pages stored in array
pages = ["Search", "Products", "Checkout", "Help"]
frames = {page:tk.Frame(root, bg=getcolour()) for page in pages}

# Initalise pages
displayframe(frames["Search"])

# File menu
filemenu = tk.Menu(root)
root.config(menu=filemenu)
# Sub menu
subfilemenu = tk.Menu(filemenu)
filemenu.add_cascade(label="Pages", menu=subfilemenu)
[subfilemenu.add_command(label=page, command=lambda p=page:switchpage(p)) for page in pages] # Pages from loop
subfilemenu.add_command(label="Exit", command=root.quit)

# Page label
pageLbl = tk.Label(root, text="", font="Arial 28")
pageLbl.place(x=50,y=0)

root.mainloop()