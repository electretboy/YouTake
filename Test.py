import tkinter as tk

def option1():
    label.config(text="You chose Option 1")
    
def option2():
    label.config(text="You chose Option 2")
    
def option3():
    label.config(text="You chose Option 3")
    
root = tk.Tk()
root.title("Selection Menu")

option1_button = tk.Button(root, text="Option 1", command=option1)
option1_button.pack()

option2_button = tk.Button(root, text="Option 2", command=option2)
option2_button.pack()

option3_button = tk.Button(root, text="Option 3", command=option3)
option3_button.pack()

label = tk.Label(root, text="Please choose an option")
label.pack()

root.mainloop()
