from tkinter import *
from tkinter import messagebox
import ast

window = Tk()
window.title('SignUp')
window.geometry('925x500+300+200')
# window.wm_iconbitmap('/home/manishankar/Desktop/Strategy/Application-20221206T171247Z-001/Application/stocliq.ico')
window.config(bg="#fff")
window.resizable(False,False)

def signupclick():
    username = user.get()
    password1 = code.get()
    password2 = confirm_code.get()

    if (password1==password2):
        try:
            file = open('datasheet.txt', 'r+')
            d=file.read()
            r=ast.literal_eval(d)

            dict2 = {username:password1}
            r.update(dict2)
            file.truncate(0)
            file.close()

            file=open('datasheet.txt', 'w')
            w=file.write(str(r))

            msg = messagebox.showinfo('Signup', 'Successfully Sign Up.')
        
        except:
            file = open('datasheet.txt','w')
            pp = str({'Username':'password'})
            file.write(pp)
            file.close()
    else:
        messagebox.showwarning("Warning","Both password should be same.")

def sign_in():
    window.destroy()

img = PhotoImage(file=r'/home/manishankar/Desktop/Strategy/Application-20221206T171247Z-001/Application/register.png')
Label(window, image=img, bg='white').place(x=50, y=90)

frame = Frame(window, width=350, height=390, bg='white')
frame.place(x=480, y=50)

heading = Label(frame, text='Sign up', fg = '#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=0)

######################################################
def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name = user.get()
    if name=='':
        user.insert(0,'Username')

user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
user.place(x=30, y=50)
user.insert(0,'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=87)

######################################################

def on_enter(e):
    code.delete(0,'end')

def on_leave(e):
    name = code.get()
    if name=='':
        code.insert(0,'Password')

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
code.place(x=30, y=130)
code.insert(0,'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=157)

######################################################

def on_enter(e):
    confirm_code.delete(0,'end')

def on_leave(e):
    name = confirm_code.get()
    if name=='':
        confirm_code.insert(0,'Confirm Password')

confirm_code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
confirm_code.place(x=30, y=200)
confirm_code.insert(0,'Confirm Password')
confirm_code.bind('<FocusIn>', on_enter)
confirm_code.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=227)

######################################################


def on_enter(e):
    App_code.delete(0,'end')

def on_leave(e):
    name = App_code.get()
    if name=='':
        App_code.insert(0,'App Code')

App_code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
App_code.place(x=30, y=270)
App_code.insert(0,'App Code')
App_code.bind('<FocusIn>', on_enter)
App_code.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=297)

######################################################

Button(frame, width=27, pady=7, text='Sign Up', bg='#57a1f8', fg='white', border=0, command=signupclick).place(x=65, y=320)
label = Label(frame, text="I have an account .", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=90, y=360)

sign_in = Button(frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=sign_in)
sign_in.place(x=190,y=360)

window.mainloop()
