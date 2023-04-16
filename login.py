from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import ast
from kite_mani import *
from nsepython import *
from time import sleep
from datetime import datetime,timedelta
import sqlite3

SYMBOL_LIST = ["NSE:NIFTY BANK", "NSE:NIFTY 50", "NSE:NIFTY FIN SERVICE", "NSE:NIFTY FMCG", "NSE:NIFTY IT"]
kite = None

i = 0

def create_user_table():
    conn = sqlite3.connect("datasheet.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY  autoincrement, username TEXT, password TEXT, start_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, expiry_date TIMESTAMP, package TEXT, status BOOLEAN)")
    conn.commit()
    conn.close()

def create_package_table():
    conn = sqlite3.connect("datasheet.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS package(id integer PRIMARY KEY  autoincrement, name TEXT, day integer, price integer)")
    conn.commit()
    conn.close()

create_package_table()

# def save_date():
#     now_date = datetime.now().date()
#     conn = sqlite3.connect("datasheet.db")
#     c = conn.cursor()
#     c.execute("UPDATE users SET expiry_date = (?), status = (?) WHERE id = 9", (now_date, True))
#     conn.commit()
#     conn.close()
# save_date()

def get_enToken(root):
    token = Toplevel(root)
    token.title("StoCliQ")
    token.geometry('500x300+500+300')
    token.config(bg="#fff")

    def start_with_token():
        symbol = symbolEntry.get()
        Token = enTokenEntry.get()

        if symbol in SYMBOL_LIST:
            if Token:
                global kite
                kite = KiteApp(enctoken=Token) 
                kite_ob = kite.quote("NSE:NIFTY BANK")
                if not kite_ob:
                    messagebox.showwarning("Warning","Invalid Token.")
                    token.destroy()
                else:
                    token.destroy()
                    root.destroy()
                    collectingPage(symbol)

            else:
                messagebox.showwarning("Warning","All fields are required.")
        else:
            messagebox.showwarning("Warning","Please select the valid symbol.")
        

    Label(token, text="Select Symbol", font=23, bg="white").place(x=60, y=50)
    symbolEntry = ttk.Combobox(token, 
                            values=SYMBOL_LIST, width=20, font=20) 
    symbolEntry.place(x=200, y=50)

    Label(token, text="enToken", font=23, bg="white").place(x=60, y=90)
    enTokenEntry = Entry(token, width=22, bd=2, font=20)
    enTokenEntry.place(x=200, y=90)

    Button(token, text="Run", font=20, width=11, height=1, command=start_with_token).place(x=200, y=130)
    token.mainloop()

def get_credential(root):
    credential = Toplevel(root)
    credential.title("StoCliQ")
    credential.geometry('500x300+500+300')
    credential.config(bg="#fff")

    def start_with_credential():
        symbol = symbolEntry.get()
        username = usernameEntry.get()
        password = passwordEntry.get()
        app_code = appcodeEntry.get()

        if symbol in SYMBOL_LIST:
            if username and password and app_code:
                global kite
                try:
                    enctoken = get_enctoken(username, password, app_code)
                    kite = KiteApp(enctoken=enctoken)
                except:
                    messagebox.showwarning("Warning","Invalid Credential.")
                    credential.destroy()
                else:
                    credential.destroy()
                    root.destroy()
                    collectingPage(symbol)
            else:
                messagebox.showwarning("Warning","All fields are required.")
        else:
            messagebox.showwarning("Warning","Please select the valid symbol.")
        

    Label(credential, text="Select Symbol", font=23, bg="white").place(x=60, y=50)
    symbolEntry = ttk.Combobox(credential, 
                            values=SYMBOL_LIST, width=20, font=20) 
    symbolEntry.place(x=200, y=50)

    Label(credential, text="Username", font=23, bg="white").place(x=60, y=90)
    usernameEntry = Entry(credential, width=22, bd=2, font=20)
    usernameEntry.place(x=200, y=90)

    Label(credential, text="Password", font=23, bg="white").place(x=60, y=130)
    passwordEntry = Entry(credential, width=22, bd=2, font=20)
    passwordEntry.place(x=200, y=130)

    Label(credential, text="App Code", font=23, bg="white").place(x=60, y=170)
    appcodeEntry = Entry(credential, width=22, bd=2, font=20)
    appcodeEntry.place(x=200, y=170)    

    codebtn = Button(credential, text="Run", font=20, width=11, height=1, command=start_with_credential)
    codebtn.place(x=230, y=210)
    credential.mainloop()

def collectingPage(symbol):  
    start_at = datetime.now()
    collecting = Tk()    
    collecting.title("StoCliQ")
    collecting.geometry('925x500+300+200')
    collecting.config(bg="#fff")
    if not running_status() or start_at.weekday() == 5 or start_at.weekday() == 6:
        messagebox.showerror("Warning","Market is closed now.")
        collecting.destroy()
    else:
        Label(collecting, text=symbol, font="arial 25", bg="white").pack(pady=25)

        close_P_label = Label(collecting, text="PREVIOUS CLOSE", font=("arial 13"), bg='white')
        close_P_label.place(x=30, y=80)

        open_P_label = Label(collecting, text="TODAY'S OPEN", font=("arial 13"), bg='white')
        open_P_label.place(x=200, y=80)    

        open_p = Label(collecting, text="44078.13", font=('Microsoft YaHei UI Light', 11, 'bold'), bg='white')
        open_p.place(x=230, y=110)
        
        close_p = Label(collecting, text="44078.13", font=('Microsoft YaHei UI Light', 11, 'bold'), bg='white')
        close_p.place(x=60, y=110)

        NSELIVE_label = Label(collecting, text="NSE LIVE", font=("arial 11"), bg='white')
        NSELIVE_label.place(x=300, y=170)

        c= Canvas(collecting,width=12, height=12, bd = 0, bg="white")
        c.place(x=375, y=170)
        c.create_oval(3,3,13,13, fill = "green")

        live_p = Label(collecting, text="44078.13", font=('Microsoft YaHei UI Light', 25, 'bold'), bg='white')
        live_p.place(x=400, y=200)

        at_label = Label(collecting, text="2022-12-02 10:33:45", font=("arial 11"), bg='white')
        at_label.place(x=400, y=250)

        progress_label = Label(collecting, text="Collecting data... ", font=("arial 13"), bg='white')
        progress_label.place(x=400, y=350)

        progress = ttk.Progressbar(collecting, orient = HORIZONTAL, length=500, mode='determinate')
        progress.place(x=230, y=390)

        def get_market():
            if running_status():
                try:
                    bank_nifty = kite.quote(symbol) 

                    tradingsymbol = bank_nifty[symbol]['tradingsymbol']

                    instrument_token = bank_nifty[symbol]['instrument_token']

                    op = bank_nifty[symbol]['ohlc']['open']
                    open_p.config(text=op)

                    cp = bank_nifty[symbol]['ohlc']['close']
                    close_p.config(text=cp)

                    hp = bank_nifty[symbol]['ohlc']['high']

                    lp = bank_nifty[symbol]['ohlc']['low']

                    latestp = bank_nifty[symbol]['last_price']
                    live_p.config(text=latestp)

                    timestamp = bank_nifty[symbol]['timestamp']
                    at_label.config(text=timestamp)
                    
                    filename = str(datetime.now().date())
                    if os.path.isfile(f"{filename}.txt"):
                        with open(f"{filename}.txt", "a") as f:
                            f.write(f"LIVE, {tradingsymbol}, {instrument_token}, {op}, {hp}, {lp}, {cp}, {latestp}, {timestamp}\n")
                    else:
                        with open(f"{filename}.txt", "a") as f:
                            f.write(f"Type, symbol, instrument_token, open price, high price, low price, close price, live price, Time\n")
                            f.write(f"LIVE, {tradingsymbol}, {instrument_token}, {op}, {hp}, {lp}, {cp}, {latestp}, {timestamp}\n")
                    live_p.after(1000, get_market)
                except:
                    messagebox.showerror("Error","Something went wrong.")

        def get_total_seconds():
            total_seconds = int((start_at - datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)).total_seconds())
            return total_seconds

        def get_current_seconds():
            current_seconds = int((datetime.now() - start_at).total_seconds())
            return current_seconds

        def load():
            if running_status():
                per_c = round(((get_current_seconds()/get_total_seconds())*100), 1)
                txt = "Collecting data... " + (str(per_c)+'%')
                progress_label.config(text=txt)
                progress_label.after(1000, load)
                progress['value'] = per_c

        get_market()
        load()
        collecting.mainloop()
# collectingPage()
def zerodha_credential_page():
    screen = Tk()
    screen.title("StoCliQ")
    screen.geometry('925x500+300+200')
    screen.config(bg="#fff")
    
    def typebtn():
        type = TypeEntry.get()
        if type == 'enToken':
            get_enToken(screen)
        elif type == 'Credential':
            get_credential(screen)
        else:
            messagebox.showwarning("Warning","Invalid Inputs.")



    Label(screen, text="Provide your Zerodha Credential.", font="arial 25", bg="white").pack(pady=25)
    Label(text="Select Type", font=23, bg="white").place(x=135, y=100)

    # #entry
    TypeEntry = ttk.Combobox(screen, 
                            values=[
                                    "enToken", 
                                    "Credential"], width=48, font=20) 
    TypeEntry.place(x=250, y=100)

    Button(text="Submit", font=20, width=11, height=1, command=typebtn).place(x=400, y=140)

    screen.mainloop()

def registration_page(root):
    window = Toplevel(root)
    window.title('SignUp')
    window.geometry('925x500+300+200')
    window.wm_iconbitmap(r'C:\Users\jaiswalm\Downloads\Kite_Zerodha-main\Application\stocliq.ico')
    window.config(bg="#fff")
    window.resizable(False,False)

    def signupclick():
        username = user.get()
        password1 = code.get()
        password2 = confirm_code.get()
        if (password1==password2):
            try:
                conn = sqlite3.connect("datasheet.db")
                c = conn.cursor()
                c.execute(f"SELECT * FROM users WHERE username = '{username}'")
                res = c.fetchall()
                if len(res) > 0:
                    messagebox.showwarning("Warning","Username already exist.")
                else:
                    c.execute(f"SELECT * FROM users")
                    res = c.fetchall()
                    if len(res) > 0:
                        for item in res:                        
                            c.execute("INSERT INTO users(username, password, start_at, expiry_date, package, status) VALUES(?,?,?,?,?,?)",(username, password1, item[3], item[4],item[5],item[6]))
                            break
                    else:
                        now_date = datetime.now().date()
                        expiry_date = now_date + timedelta(days=7)
                        c.execute("INSERT INTO users(username, password, start_at, expiry_date, package, status) VALUES(?,?,?,?,?,?)",(username, password1, now_date, expiry_date,'trial',True))
                    messagebox.showinfo('Signup', 'Successfully Sign Up.')
                window.destroy()
                conn.commit()
                conn.close()
            except:
                file = open('datasheet.txt','w')
                pp = str({'Username':'password'})
                file.write(pp)
                file.close()
        else:
            messagebox.showwarning("Warning","Both password should be same.")

    def sign_in():
        window.destroy()

    img = PhotoImage(file=r'C:\Users\jaiswalm\Downloads\Kite_Zerodha-main\Application\register.png')
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

    Button(frame, width=27, pady=7, text='Sign Up', bg='#57a1f8', fg='white', border=0, command=signupclick).place(x=65, y=270)
    label = Label(frame, text="I have an account .", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
    label.place(x=90, y=340)

    sign_in = Button(frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=sign_in)
    sign_in.place(x=190,y=340)

    window.mainloop()


root = Tk()
# get_enToken(root)
# get_credential(root)
root.title('StoCliQ')
root.geometry('925x500+300+200')
root.wm_iconbitmap(r'C:\Users\jaiswalm\Downloads\Kite_Zerodha-main\Application\stocliq.ico')
root.config(bg="#fff")
root.resizable(False,False)

def loginclick():
    username = user.get()
    password = code.get()
    if (username and password):   
        conn = sqlite3.connect("datasheet.db")
        c = conn.cursor()
        c.execute(f"SELECT id, expiry_date, status FROM users WHERE username = '{username}' and password = '{password}' and status = 1")
        res = c.fetchall()
        if res:
            if datetime.now() > datetime.strptime(res[0][1], "%Y-%m-%d"):
                c.execute(f"UPDATE users SET status = {False} WHERE id = {res[0][0]}")
                conn.commit()
                conn.close()
                messagebox.showerror("Warning","Your plan has been expired. Renew now!")
            else:
                root.destroy()   
                zerodha_credential_page()
        else:
            c.execute(f"SELECT id, expiry_date, status FROM users WHERE username = '{username}' and password = '{password}' and status = 0")
            res = c.fetchall()
            if res:
                messagebox.showerror("Warning","Your plan has been expired. Renew now!")
            else:
                messagebox.showerror("Warning","Invalid Username and Pasword.")
            conn.commit()
            conn.close()
    else:
        messagebox.showerror("Warning","Invalid Username and Pasword.")

def register():
    registration_page(root)

img = PhotoImage(file=r'C:\Users\jaiswalm\Downloads\Kite_Zerodha-main\Application\login.png')
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=480, y=70)

heading = Label(frame, text='Sign in', fg = '#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

######################################################
def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name = user.get()
    if name=='':
        user.insert(0,'Username')

user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
user.place(x=30, y=80)
user.insert(0,'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

######################################################

def on_enter(e):
    code.delete(0,'end')

def on_leave(e):
    name = code.get()
    if name=='':
        code.insert(0,'Password')

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
code.place(x=30, y=150)
code.insert(0,'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

######################################################

Button(frame, width=27, pady=7, text='Sign In', bg='#57a1f8', fg='white', border=0, command=loginclick).place(x=50, y=204)
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)

sign_up = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=register)
sign_up.place(x=225,y=270)

root.mainloop()
