import Tkinter as tk
import time
if __name__ == '__main__':
    top = tk.Tk()
    top.title("On Screen Keyboard")

    def click(key):
        if key == "<-":
            entry2 = entry.get()
            pos = entry2.find("")
            pos2 = entry2[pos:]
            entry.delete(pos2, tk.END)
        elif key == " Space ":
            entry.insert(tk.END, ' ')
        else:
            entry.insert(tk.END,key)

    button_list = [
    'q','w','e','r','t','y','u','i','o','p','<-',
    'a','s','d','f','g','h','j','k','l',
    'z','x','c','v','b','n','m'
    ,' Space '
    ]
    entry = tk.Entry(top, width = 84)
    entry.grid(row = 1, columnspan = 15)
    
    btn = list(range(len(button_list)))
    
    

    

    top.mainloop()
#use keyboard2
