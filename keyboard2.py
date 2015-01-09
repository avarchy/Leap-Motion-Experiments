import Tkinter as tk
from functools import partial

def click(btn):
    # test the button command click
    global written
    if btn == '<-':
        written = written[:-1]
    elif btn == ' Space ':
        written = written+"%s" % " "
    else:
        written = written+"%s" % btn
    root.title(written)
root = tk.Tk()
root.title("On Screen Keyboard")
written=''
tk.Entry(root,width=84)
lf = tk.LabelFrame(root, text="", bd=3)
lf.pack(padx=15, pady=10)

btn_list = [
['q','w','e','r','t','y','u','i','o','p','<-'],
    [' ','a','s','d','f','g','h','j','k','l'],
    [' ',' ','Shift','z','x','c','v','b','n','m'],
    [' Space '] ]

n = 0

for i in range(len(btn_list)):
               n+=len(btn_list[i])
btn = list(range(int(n)))
n=0
for r in range(len(btn_list)):
    for c in range(len(btn_list[r])):
               cmd = partial(click, btn_list[r][c])
               if btn_list[r][c]==' ':
                   btn[n] = tk.Button(lf, text='',height=5, width=3, command=cmd)
                   btn[n].grid(row=r, column=c)
               btn[n] = tk.Button(lf, text=btn_list[r][c],height=5, width=5, command=cmd)
               btn[n].grid(row=r, column=c, columnspan=2)
               n+=1

root.mainloop()
