import Tkinter
from functools import partial

__author__ = 'leo'


def aa():
    print 'aa'


def bb():
    print 'bb'


root = Tkinter.Tk()

myButton = partial(Tkinter.Button, root, fg='white', bg='blue')

b1 = myButton(text='button 1', command=aa)
b2 = myButton(text='button 2', command=bb)

qb = myButton(text='QUIT', bg='red', command=root.quit)

b1.pack()
b2.pack()
qb.pack(fill=Tkinter.X, expand=True)
root.title('PFAs!')
root.mainloop()
