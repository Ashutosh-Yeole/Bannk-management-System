import os
import tkinter
import threading
from tkinter import *
from os import path,getcwd
from tkinter import messagebox
from time import gmtime,strftime

RES = path.abspath(getcwd()) + "\\assets\\"
REC = path.abspath(getcwd()) + "\\database\\records\\"
MAL = path.abspath(getcwd()) + "\\database\\internel\\mails.txt"
DATA = path.abspath(getcwd()) + "\\database\\profiles\\"
SER = path.abspath(getcwd()) + "\\database\\internel\\series.txt"
BLK = path.abspath(getcwd()) + "\\database\\internel\\blocklist.txt"
BLK_LST = []
SS_LIST = []
FLAG = 1
MAX_TRANSFER = 50000

def get_ss_path():
    if path.exists(path.expanduser("~") + "\\Pictures\\Screenshots") == True:
        return path.expanduser("~") + "\\Pictures\\Screenshots\\"
    elif path.exists(path.expanduser("~") + "\\OneDrive\\Pictures\\Screenshots") == True:
        return path.expanduser("~") + "\\OneDrive\\Pictures\\Screenshots\\"
    else:
        return None

def get_list_ss():
    global SS_LIST
    if get_ss_path() != None:
        for dirs in os.listdir(get_ss_path()):
            SS_LIST.append(dirs)

def anti_ss():
    global SS_LIST,FLAG
    if get_ss_path() == None:
        pass
    else:
        while FLAG == 1:
            try:
                for dirs in os.listdir(get_ss_path()):
                    if dirs not in SS_LIST:
                        ss_path = get_ss_path() + dirs
                        os.remove(ss_path)
            except KeyboardInterrupt:
                FLAG = 0

def get_name(num):
    fp = open(DATA + num,"r+")
    line = fp.readlines()[1].strip("\n")
    return line

def balance(num):
    fp = open(DATA + num,"r+")
    line = fp.readlines()[4].strip("\n")
    return int(line)

def mail_exists(mail):
    mails = open(MAL,"r+").readlines()
    for line in mails:
        if line.strip("\n") == mail:
            return True
    return False

def logout(node):
    node.destroy()

def isblock(num):
    fp8 = open(BLK,"r").readlines()
    for line in fp8:
        c_num = line.strip("\n")
        if(num == c_num):
            return 0
    return 1

def update_h(num,info):
    try:
        fp9 = open(REC + str(num),"a")
    except:
        pass
    else:
        fp9.write(str(strftime("[%d-%m-%Y] [%H:%M:%S] | ")) + str(info))
        fp9.close()

def update_mail(num,mail):
    fp5 = open(DATA + num,"r+")
    o_mail = str(fp5.readlines()[2])
    fp5.close()
    fp6 = open(MAL,"r+")
    c_state = fp6.readlines()
    idx = c_state.index(o_mail)
    c_state[idx] = str(mail) + "\n"
    fp6.seek(0)
    for lines in c_state:
        fp6.write(lines)
    fp6.close()
    
def block_hwn(num):
    if BLK_LST.count(num) < 3:
        BLK_LST.append(num)
    elif BLK_LST.count(num) == 3:
        messagebox.showerror("Error","Your account is locked.\nIf it was mistake kindly contact admin")
        fp7 = open(BLK,"a")
        fp7.write(num + "\n")
        fp7.close()
        for i in BLK_LST:
            if(i == num):
                BLK_LST.remove(num)

def show_bal(num):
    messagebox.showinfo("Balance","Your current balance "+str(balance(num)))

def change_mail(num,mail):
    if "@gmail.com" not in mail:
        messagebox.showerror("Error","Enter valid gmail")
    elif mail == "" or mail == " ":
        messagebox.showerror("Error","Fields cant be empty")
    elif mail_exists(mail) == True:
        messagebox.showerror("ERROR","Account associated to entered mail already exists")
    else:
        update_mail(num,mail)
        fp5 = open(DATA + num,"r+")
        cur_state = fp5.readlines()
        cur_state[2] = str(mail) + "\n"
        fp5.seek(0)
        for lines in cur_state:
            fp5.write(lines)
        fp5.close()
        messagebox.showinfo("Success","Login again to see changes")

def change_name(num,name):
    if name.isdigit == True:
        messagebox.showerror("Error","Name must contain at least one character")
    elif name == "" or name == " ":
        messagebox.showerror("Error","Fields cant be empty")
    else:
        fp5 = open(DATA + num,"r+")
        cur_state = fp5.readlines()
        cur_state[1] = str(name) + "\n"
        fp5.seek(0)
        for lines in cur_state:
            fp5.write(lines)
        fp5.close()
        messagebox.showinfo("Success","Login again to see changes")

def change(acc_num,type):
    child1 = tkinter.Tk()
    child1.geometry("500x500")
    child1.maxsize(500,500)
    child1.minsize(500,500)
    child1.configure(background="#0a0100")
    if type == 0:
        child1.title("Bank Management System - Change name")
        ent6 = Entry(child1,width=20)
        ent6.place(x=250,y=200)
        lbl0 = Label(child1,text="New name",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=150,y=200)
        btn3 = Button(child1,text="Change",command=lambda:change_name(acc_num,ent6.get()),bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",width=10).place(x=200,y=250)
    elif type == 1:
        child1.title("Bank Management System - Change gmail")
        ent6 = Entry(child1,width=20)
        ent6.place(x=250,y=200)
        lbl0 = Label(child1,text="New gmail",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=150,y=200)
        btn3 = Button(child1,text="Change",command=lambda:change_mail(acc_num,ent6.get()),bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",width=10).place(x=200,y=250)

def withdraw(amt,acc):
    if amt.isdigit == False:
        messagebox.showerror("Error","Amount must be a number")
    elif int(amt) > balance(acc):
        messagebox.showerror("Failed","You dont have enough balance to withdraw")
    else:
        fp5 = open(DATA + acc,"r+")
        cur_state = fp5.readlines()
        cur_state[4] = str(int(cur_state[4].strip("\n")) - int(amt)) + "\n"
        fp5.seek(0)
        for lines in cur_state:
            fp5.write(lines)
        fp5.close()
        update_h(acc,str("Deducted " + str(amt) + "\n"))
        messagebox.showinfo("Success",amt+" deducted from account "+acc)

def deposit(amt,acc):
    if amt.isdigit == False:
        messagebox.showerror("Error","Amount must be a number")
    else:
        fp6 = open(DATA + acc,"r+")
        cur_state = fp6.readlines()
        cur_state[4] = str(int(cur_state[4].strip("\n")) + int(amt)) + "\n"
        fp6.seek(0)
        for lines in cur_state:
            fp6.write(lines)
        fp6.close()
        update_h(acc,str("Deposited " + str(amt) + "\n"))
        messagebox.showinfo("Success",amt+" deposited to "+acc)

def transfer(parent,acc_frm,acc_to,amt):
    if amt.isdigit == False:
        messagebox.showerror("Error","Amount must be a number")
    elif int(amt) > balance(acc_frm):
        messagebox.showerror("Failed","You dont have enough balance to transfer")
    elif int(amt) > MAX_TRANSFER:
        messagebox.showerror("Failed","You can not transfer more than " + str(MAX_TRANSFER))
    else:
        fp3 = open(DATA + acc_frm,"r+")
        try:
            fp4 = open(DATA + acc_to,"r+")
        except FileNotFoundError:
            fp3.close()
            messagebox.showerror("Failed","Account "+str(acc_to)+" does not exists")
        else:
            cur_state = fp3.readlines()
            cur_state_d = fp4.readlines()
            cur_state[4] = str(int(cur_state[4].strip("\n")) - int(amt)) + "\n"
            cur_state_d[4] = str(int(cur_state_d[4].strip("\n")) + int(amt)) + "\n"
            fp3.seek(0)
            fp4.seek(0)
            fp3.writelines(cur_state)
            fp4.writelines(cur_state_d)
            fp3.close()
            fp4.close()
            parent.destroy()
            update_h(acc_frm,str("Trasfered " + str(amt) + " to " + str(acc_to)+"\n"))
            update_h(acc_to,str("Recived " + str(amt) + " from " + str(acc_frm)+"\n"))
            messagebox.showinfo("Success",amt+" transfered to "+acc_to)

def history(acc_num):
    win = tkinter.Tk()
    win.geometry("400x250")
    win.maxsize(400,250)
    win.minsize(400,250)
    win.title("Transaction history")
    #win.iconbitmap(RES + "icon.ico")
    s_bar = Scrollbar(win)
    s_bar.pack(side=RIGHT,fill=Y)
    s_bar.pack(side=BOTTOM,fill=X)
    frec = open(REC + acc_num,'r').read()
    txtInventory = Text(win, wrap='word',padx=10,pady=10)
    txtInventory.pack(fill='both',padx=10,pady=10)
    txtInventory.insert('end',frec)

def update_profile(num):
    child2 = tkinter.Tk()
    child2.geometry("500x500")
    child2.maxsize(500,500)
    child2.minsize(500,500)
    child2.configure(background="#0a0100")
    #child2.iconbitmap(RES + "icon.ico")
    child2.title("Bank Management System - Update profile " + get_name(num))
    Label(child2,text="Update profile - "+get_name(num),bg="#0022c9",fg="#f7fafa",font=("Arial",12)).place(x=0,y=0)
    btn0 = Button(child2,text="Change name",bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",height=5,width=20,command=lambda:change(num,0)).place(x=150,y=150)
    btn1 = Button(child2,text="Change email",bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",height=5,width=20,command=lambda:change(num,1)).place(x=150,y=260)

def deposit_ui(acc_num):
    child1 = tkinter.Tk()
    child1.geometry("500x500")
    child1.maxsize(500,500)
    child1.minsize(500,500)
    child1.title("Bank Management System - Deposit")
    child1.configure(background="#0a0100")
    #child1.iconbitmap(RES + "icon.ico")
    ent6 = Entry(child1,width=20)
    ent6.place(x=250,y=200)
    lbl1 = Label(child1,text="Amount",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=200)
    btn3 = Button(child1,text="Deposit",command=lambda:deposit(ent6.get(),acc_num),bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",width=10).place(x=200,y=270)

def withdraw_ui(acc_num):
    child1 = tkinter.Tk()
    child1.geometry("500x500")
    child1.maxsize(500,500)
    child1.minsize(500,500)
    child1.title("Bank Management System - Withdraw")
    child1.configure(background="#0a0100")
    #child1.iconbitmap(RES + "icon.ico")
    ent6 = Entry(child1,width=20)
    ent6.place(x=250,y=200)
    lbl1 = Label(child1,text="Amount",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=200)
    btn3 = Button(child1,text="Withdraw",command=lambda:withdraw(ent6.get(),acc_num),bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",width=10).place(x=200,y=270)
    
def transfer_ui(acc_num):
    child1 = tkinter.Tk()
    child1.geometry("500x500")
    child1.maxsize(500,500)
    child1.minsize(500,500)
    child1.title("Bank Management System - Transfer")
    child1.configure(background="#0a0100")
    #child1.iconbitmap(RES + "icon.ico")
    ent6 = Entry(child1,width=20)
    ent6.place(x=250,y=200)
    ent7 = Entry(child1,width=20)
    ent7.place(x=250,y=230)
    lbl0 = Label(child1,text="Account number",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=200)
    lbl1 = Label(child1,text="Amount",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=230)
    btn3 = Button(child1,text="Transfer",command=lambda:transfer(child1,acc_num,ent6.get(),ent7.get()),bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",width=10).place(x=200,y=270)
    
def logged_in(acc_num,acc_pin):
    child2 = tkinter.Tk()
    child2.geometry("500x500")
    child2.maxsize(500,500)
    child2.minsize(500,500)
    child2.configure(background="#0a0100")
    #child2.iconbitmap(RES + "icon.ico")
    child2.title("Bank Management System - Logged in as " + get_name(acc_num))
    btn6 = Button(child2,text="Welcome "+get_name(acc_num) +"!",bg="#0022c9",fg="#f7fafa",font=("Arial",12),command=lambda:update_profile(acc_num)).place(x=0,y=0)
    btn0 = Button(child2,text="Transfer",bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",height=5,width=10,command=lambda:transfer_ui(acc_num)).place(x=150,y=100)
    btn1 = Button(child2,text="Deposit",bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",height=5,width=10,command=lambda:deposit_ui(acc_num)).place(x=250,y=100)
    btn2 = Button(child2,text="Withdraw",bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",height=5,width=10,command=lambda:withdraw_ui(acc_num)).place(x=150,y=210)
    btn3 = Button(child2,text="History",bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",height=5,width=10,command=lambda:history(acc_num)).place(x=250,y=210)
    btn4 = Button(child2,text="logout",bg="#f2021e",font=("Arial",12),fg="#f7fafa",command=lambda:logout(child2)).place(x=445,y=0)
    btn5 = Button(child2,text="Show balance",bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",height=5,width=20,command=lambda:show_bal(acc_num)).place(x=155,y=320)

def login(acc_num,acc_pin):
    try:
        fp = open(DATA + acc_num)
    except FileNotFoundError:
        messagebox.showerror("Error","Invalid credentials")
    else:
        line = fp.readline().strip("\n")
        if line != acc_pin:
            block_hwn(acc_num)
            messagebox.showerror("Error","Invalid credentials")
        else:
            fp.close()
            if isblock(acc_num) == 0:
                messagebox.showerror("Error","Your account is locked.\nIf it was mistake kindly contact admin")
            else:
                logged_in(acc_num,acc_pin)

def recover(parent,acc_num,acc_mail):
    if acc_num == " " or acc_num == "" or acc_mail == " " or acc_mail == "":
        messagebox.showerror("ERROR","Fields can not be empyt")
    else:
        try:
            fp = open(DATA + acc_num,"r").readlines()
        except FileNotFoundError:
            messagebox.showerror("Error","Invalid credentials")
        c_mail = fp[2].strip("\n")
        if "@gmail.com" not in acc_mail:
            messagebox.showerror("Error","Enter valid gmail")
        elif c_mail != acc_mail:
            messagebox.showerror("Error","Invalid credentials")
        else:
            messagebox.showinfo("Info","Recovery mail sent to " + acc_mail)
            parent.destroy()

def f_pass():
    child1 = tkinter.Tk()
    child1.geometry("500x500")
    child1.maxsize(500,500)
    child1.minsize(500,500)
    child1.title("Bank Management System - Recover account")
    child1.configure(background="#0a0100")
    #child1.iconbitmap(RES + "icon.ico")
    ent6 = Entry(child1,width=20)
    ent6.place(x=250,y=200)
    ent7 = Entry(child1,width=20)
    ent7.place(x=250,y=230)
    lbl0 = Label(child1,text="Account number",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=200)
    lbl1 = Label(child1,text="Registered gmail",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=230)
    btn3 = Button(child1,text="Recover",command=lambda:recover(child1,ent6.get(),ent7.get()),bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",width=10).place(x=200,y=270)

def p_data(parent,acc_name,acc_pin,acc_mail,acc_bas):
    m_list = open(MAL,"r").readlines()
    if acc_pin.isdigit() == False:
        messagebox.showerror("Error","Account pin can contain numbers only")
    elif len(acc_pin) != 4:
        messagebox.showerror("Error","Account pin must be 4 digit long")
    elif acc_name.isdigit == True:
        messagebox.showerror("Error","Account name must conatin at least 1 character")
    elif "@gmail.com" not in acc_mail:
        messagebox.showerror("Error","Enter valid gmail")
    elif acc_pin == "" or acc_pin == " " or acc_name == " " or acc_name == "" or acc_bas == " " or acc_bas == "":
        messagebox.showerror("ERROR","Fields can not be empyt")
    elif mail_exists(acc_mail) == True:
        messagebox.showerror("ERROR","Account associated to entered mail already exists")
    else:
        fp0 = open(SER,"r+")
        acc_num = fp0.readline().strip('\n')
        fp0.seek(0)
        fp0.write(str((int(acc_num) + 1)))
        fp0.close()
        fp1 = open(DATA + acc_num,"w")
        fp2 = open(MAL,"a")
        fp3 = open(REC + acc_num,"w")
        fp1.write(str(acc_pin) + "\n")
        fp1.write(str(acc_name) + "\n")
        fp1.write(str(acc_mail) + "\n")
        fp1.write(str(acc_num) + "\n")
        fp1.write(str(acc_bas) + "\n")
        fp2.write(str(acc_mail) + "\n")
        fp3.write("Date                    | Activity\n")
        fp0.close()
        fp1.close()
        fp2.close()
        fp3.close()
        messagebox.showinfo("Congratulations","Account created successfully\nYour account number : " + acc_num)
        parent.destroy()

def crt_acc():
    child0 = tkinter.Tk()
    child0.geometry("500x500")
    child0.maxsize(500,500)
    child0.minsize(500,500)
    child0.title("Bank Management System - Create account")
    child0.configure(background="#0a0100")
    #child0.iconbitmap(RES + "icon.ico")
    ent3 = Entry(child0,width=20)
    ent3.place(x=250,y=200)
    ent4 = Entry(child0,width=20)
    ent4.place(x=250,y=230)
    ent5 = Entry(child0,width=20)
    ent5.place(x=250,y=260)
    ent6 = Entry(child0,width=20)
    ent6.place(x=250,y=290)
    lbl3 = Label(child0,text="Enter name",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=200)
    lbl4 = Label(child0,text="Account pin",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=230)
    lbl5 = Label(child0,text="Enter gmail",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=260)
    lbl5 = Label(child0,text="Base Amount",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=290)
    btn3 = Button(child0,text="Create",command=lambda:p_data(child0,ent3.get(),ent4.get(),ent5.get(),ent6.get()),bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",width=10).place(x=200,y=330)

def bank():
    window = tkinter.Tk()
    window.geometry("500x500")
    window.maxsize(500,500)
    window.minsize(500,500)
    window.title("Bank Management System")
    window.configure(background="#0a0100")
    #window.iconbitmap(RES + "icon.ico")
    ent0 = Entry(window,width=20)
    ent0.place(x=250,y=200)
    ent1 = Entry(window,width=20,show="●")
    ent1.place(x=250,y=230)
    lbl0 = Label(window,text="Account number",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=200)
    lbl1 = Label(window,text="Account Pin",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=100,y=230)
    lbl2 = Label(window,text="Don't have an account?",bg="#0a0100",fg="#f7fafa",font=("Arial",12)).place(x=120,y=362)
    btn0 = Button(window,text="Login",bg="#0cd2e8",font=("Arial",12),fg="#f7fafa",width=10,command=lambda:login(ent0.get(),ent1.get())).place(x=200,y=300)
    btn1 = Button(window,text="forgot pin?",bg="#0a0100",fg="#f7fafa",borderwidth=0,command=f_pass).place(x=220,y=335)
    btn2 = Button(window,text="Create one",bg="#0a0100",fg="#0cd2e8",font=("Arial",12),command=crt_acc,borderwidth=0).place(x=285,y=360)
    window.mainloop()

ss_block = threading.Thread(target=anti_ss,daemon=True)
ss_block.start()
bank()
FLAG = 0
ss_block.join()