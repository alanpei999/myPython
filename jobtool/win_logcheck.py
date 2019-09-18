# win_chklog
# Used for check string in log which created by console
# Release note
# V0.1 : initial bersion
# V0.2 : fix encoding issue and clear log loading path

import sys, getopt
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
root=Tk()
root.title("Check Log v0.2")

def defaultItems():
    listBox1.insert(0, "Fail")
    listBox1.insert(1, "panic")
    listBox1.insert(2, "0x003c: f0")
    listBox1.insert(3, "0x01b8: 77 7f 03 00")
    listBox1.insert(4, "0x0050: 80 00 00 00")
    listBox1.insert(5, "backup bios")
    listBox1.insert(6, "primary bios")

def addItem():
    newItem = entry1_controlBar.get()
    try:
        if newItem == "":
            messagebox.showerror("Error", "Please enter string first!")
        else:
            listBox1.insert(END, newItem)
    except AttributeError:
        messagebox.showerror("Error", "Please enter string first!")

def deleteItem():
    try:
        selected_item=listBox1.curselection()
        for item in selected_item:
            listBox1.delete(item)
    except AttributeError:
        messagebox.showerror("Error", "Please select a string first!")

def loadChkStr():
    file_name=filedialog.askopenfilename(initialdir=" ", title="Select a file", filetypes=(("Txt Files",".txt"),("All files","*.*")))
    entry2_controlBar.insert(END, file_name)
    content=open(file_name).readlines()
    for i in content:
        i = i.strip()                                                     # read file and assign to a list k_str /  str1.strip() : delete "\n"
        listBox1.insert(END, i)

def saveFile():
    myFile=filedialog.asksaveasfile(mode="w", initialdir=" ", defaultextension=".txt")
    if myFile is None:
        return
    for i in range(listBox1.size()):
        content=listBox1.get(i)
        #print(content)
        myFile.write(content + "\n")
    messagebox.showinfo("Success", "Save successfully!")
    myFile.close()

def clearItem():
    listBox1.delete(0, "end")

def loadLog():
    entry1_logBox.delete(0, "end")
    file_name=filedialog.askopenfilename(initialdir=" ", title="Select a file", filetypes=(("Txt Files",".log"),("All files","*.*")))
    entry1_logBox.insert(END, file_name)
    logFName = file_name

def exitApp():
    root.quit()
    root.destroy()
    exit()

def clearTextbox():
    textBox.delete("1.0", END)

def checkLog(FName):
    try:
        f = open(FName, "r", encoding="utf-8")
        article = f.readlines()
        f.close()
    except FileNotFoundError:
        messagebox.showerror("Error","Please load a log file first!!")
    except UnicodeDecodeError:
        # read string from listBox
        f = open(FName, "r")
        article = f.readlines()
        f.close()
    finally:
        keyStr = []

        for i in range(listBox1.size()):
            keyStr.append(listBox1.get(i).lower())          # read file and assign to a list k_str /  str1.strip() : delete "\n"

        keyStr_Cnt = [ 0 for n in range(len(keyStr))]             # k_cnt : according to k_str to create the default veluae 0 for each string
        for context in article:
            for i in range(len(keyStr)):
                  if keyStr[i] in context:
                     keyStr_Cnt[i] = keyStr_Cnt[i] + 1

        for i in range(len(keyStr)):
            strTemp = keyStr[i] + "..............." + str(keyStr_Cnt[i])
            textBox.insert(END, strTemp + "\n")



if __name__ == '__main__':
    # Control Panel - Load config
    controlBar = LabelFrame(root, text="Control Panel")
    controlBar.grid(row=0, column=0, padx=5, pady=10)
    lbl1_controlBar = Label(controlBar, text="Add Check String")
    lbl1_controlBar.grid(row=0, column=0, padx=5, pady=5)
    # Buttons
    entry1_controlBar = Entry(controlBar, width=20)
    entry1_controlBar.grid(row=0, column=1)
    button1_controlBar = Button(controlBar, text="Add", command=lambda: addItem())
    button1_controlBar.grid(row=0, column=2, padx=10)
    button2_controlBar = Button(controlBar, text="Delete", command=lambda: deleteItem())
    button2_controlBar.grid(row=0, column=3, padx=5)
    lbl2_controlBar = Label(controlBar, text="Load/Save Config")
    lbl2_controlBar.grid(row=1, column=0, pady=5)
    entry2_controlBar = Entry(controlBar, width=20)
    entry2_controlBar.grid(row=1, column=1)
    button2_controlBar = Button(controlBar, text="Load", command=lambda: loadChkStr())
    button2_controlBar.grid(row=1, column=2, padx=10)
    button2_controlBar = Button(controlBar, text="Save", command=lambda: saveFile())
    button2_controlBar.grid(row=1, column=3, padx=5)
    button3_controlBar = Button(controlBar, text="Clear", command=lambda: clearItem())
    button3_controlBar.grid(row=1, column=4, padx=5)

    # List box
    itemBox = LabelFrame(root, text="Check String List")
    itemBox.grid(row=1, column=0, padx=5, pady=10)
    listBox1 = Listbox(itemBox, width=56, height=15, selectmode=SINGLE)
    defaultItems()
    listBox1.grid(row=2, column=1, padx=3, pady=3)

    # Text box
    txtBox = LabelFrame(root, text="Log Check Result")
    txtBox.grid(row=1, column=1, padx=5, pady=10)
    textBox = Text(txtBox, height=15, width=45)
    textBox.grid(row=0, column=0, padx=3, pady=3)

    # Control Panel - Load log
    logBox = LabelFrame(root, text="Log Load Box")
    logBox.grid(row=0, column=1, padx=5, pady=10)
    lbl_logBox = Label(logBox, text="Log")
    lbl_logBox.grid(row=0, column=0, padx=5, pady=5)
    entry1_logBox = Entry(logBox, width=45)
    entry1_logBox.grid(row=0, column=1)
    button_logBox = Button(logBox, text="Load", command=lambda: loadLog())
    button_logBox.grid(row=0, column=3, padx=10)
    button_go_logBox = Button(logBox, text="  Ready to Go  ", command=lambda: checkLog(entry1_logBox.get()))
    button_go_logBox.grid(row=1, column=1, padx=60, pady=5, sticky=W)
    button_clr_logBox = Button(logBox, text="  Clear  ", command=lambda: clearTextbox())
    button_clr_logBox.grid(row=1, column=1, padx=50, pady=5, sticky=E)


    # Exit button
    button_exit = Button(root, text=" Exit ", command=lambda: exitApp())
    button_exit.grid(row=2, column=1, sticky=E)



    root.geometry("800x450+300+100")
    root.mainloop()


