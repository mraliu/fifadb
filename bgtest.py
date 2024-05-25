import tkinter
from PIL import ImageTk, Image

root = tkinter.Tk()
root.geometry("1024x768")
root.resizable(False, False)

img = Image.open("images/arsenal.jpg")
img.resize((1024, 500))
print(img.size)
img = ImageTk.PhotoImage(img)

lb1 = tkinter.Label(root, image=img)
lb1.pack()

root.mainloop()