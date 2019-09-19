# BMC Flash ROM stress for Windows
#  Work project:   
#  version v.03
#  Release date : 2019/9/16
#  V0.2 : add stop button
#  V0.3 : fix issue  - "alert : no such alert"  and add wait function for confirm element appeared

import time, threading, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

defUrl = "192.168.101.100"
defTotalloop = 5
defUsrname = "admin"
defPasswd = "admin"
defROM1 = ""
defROM2 = ""
defVer1 = "2.15.0"
defVer2 = "2.16.0"
global goBrowser
global goUrl
global goTotalloop
global goUsrname
global goPasswd
global goVer1
global goVer2
global goROM1
global goROM2
global runLoop
global stopFlag

browserList = ["Chrome", "Internet Explorer", "Firefox"]
actionPath = '//*[@id="main"]/div/div/aside[1]/div/section/ul/li[13]/a/span'
actionSubpath = '//*[@id="main"]/div/div/aside[2]/div/section[2]/div/div/div[7]/a/span'
updateStartPath = '//*[@id="start]"'


root=Tk()
root.title("BMC Flash ROM Stress v0.3")
root.attributes("-topmost", True)
root.resizable(False, False)
var5 = StringVar()
var6 = StringVar()
stopFlag = 0
goROM1 = ""
goROM2 = ""

def countDown(sec):
    while sec != 0:
        sec -= 1
        print("Countdown ", sec)
        time.sleep(1)

def callThreading():
    t1 = threading.Thread(target=flashTest, name="StressTest")
    t1.start()

def flashTest():
    var6.set("Ongoing")
    flashDoneVer = ""

    timeFORMAT = '%Y-%m-%d %H:%M:%S'
    logTimeFormat = '%Y%m%d_%H%M%S'
    startTime = datetime.datetime.now().strftime(timeFORMAT)
    logTime = datetime.datetime.now().strftime(logTimeFormat)
    # Log name & create a log file
    logName = "BMC_ROMFlashTest_" + "_" + str(logTime) + ".txt"

    logFile = open(logName, "w", encoding="utf-8")
    logFile.write("\nStart Test from : " + str(startTime))

    # Record Test config
    logFile.write("\n ======== Test Setting ========")
    logFile.write("\n Test Browser : " + str(goBrowser))
    logFile.write("\n Test BMC IP: " + str(goUrl))
    logFile.write("\n Test Test loop: " +  str(goTotalloop))
    logFile.write("\n Test userID: " +  str(goUsrname))
    logFile.write("\n Test userPWD: " + str(goPasswd))
    logFile.write("\n Test ROM 1 version: " + str(goVer1))
    logFile.write("\n Test ROM 2 version: " + str(goVer2))
    logFile.write("\n ==============================")
    logFile.close()

    if goROM1 == "":
        messagebox.showerror("Error", "Please select Flash ROM 1" + "\n" + "If you selected ROM file, please click Set button to set.")
        return
    if goROM2 == "":
        messagebox.showerror("Error", "Please select Flash ROM 2" + "\n" + "If you selected ROM file, please click Set button to set.")
        return

    runLoop = 0
    print("StopFlag :", stopFlag)

    #if stopFlag == 0:
    for runLoop in range(int(goTotalloop)):
        if stopFlag == 0:
            # Open a file to log
            logFile = open(logName, "a", encoding="utf-8")

            runLoop = runLoop + 1
            print(" == Run Loop: ", runLoop)
            logFile.write("\n == Run Loop: " +  str(runLoop))
            print("  Start time :" + str(datetime.datetime.now().strftime(timeFORMAT)))
            logFile.write("\n  Start time :" + str(datetime.datetime.now().strftime(timeFORMAT)))

            var5.set(str(runLoop))
            if goBrowser == "Chrome":
                driver = webdriver.Chrome()
            if goBrowser == "Internet Explorer":
                driver = webdriver.Ie()
            if goBrowser == "Firefox":
                driver = webdriver.Firefox()
            if goBrowser == "Edge":
                driver  = webdriver.Edge()

            driver.maximize_window()
            driver.get('https://{}'.format(goUrl))
            time.sleep(5)

            ####################################################################################
            #    Login and check firmware for comfirm passed or failed
            ####################################################################################
            while TRUE:
                try:
                    # login
                    elem_usrid = WebDriverWait(driver, 30, 1).until(EC.presence_of_element_located((By.ID, "userid")))
                    elem_usrid.send_keys('{}'.format(goUsrname))
                    elem_pwd = WebDriverWait(driver, 30, 1).until(EC.presence_of_element_located((By.ID, "password")))
                    elem_pwd.send_keys('{}'.format(goPasswd))
                    elem_pwd.send_keys(Keys.RETURN)
                    print("...Button clicked!")
                    # get firmware version
                    elem_fw = WebDriverWait(driver, 30, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "fm-revision")))
                    sysFwver = elem_fw.text
                    print("...Firmware Got!")
                    break
                except TimeoutException:
                    driver.refresh()
                    print("*** Wait for login screen and Firmware got!")

            print(" Current BMC Version : " + sysFwver)
            logFile.write("\n  Current BMC Version : " + str(sysFwver))
            print("flashdonever :" + str(flashDoneVer))

            ## record flashed version in the loop for comparing in next loop
            flashDoneVer = sysFwver

            ##  Check Pass or Fail by version checking
            if runLoop != 1:
                if sysFwver == flashDoneVer:
                    print(" Flash loop " + str(runLoop) + " ... [ Passed ]")
                    logFile.write("\n  Flash loop " + str(runLoop) + " ... [ Passed ]")
                else:
                    print(" Flash loop " + str(runLoop) + " ... [ Failed ]")
                    logFile.write("\n  Flash loop " + str(runLoop) + " ... [ Failed ]")

            ## Detect Fw version and load BMC version which will be flashed
            if sysFwver == defVer1:
                runROM = goROM2
            else:
                runROM = goROM1

            print(" Flash ROM Version: " + runROM)
            logFile.write("\n  Flash ROM Version: " + str(runROM))

            ## go to Main menu - maintenance
            flashAct = driver.find_element_by_xpath(actionPath)
            actions = ActionChains(driver)
            actions.move_to_element(flashAct).perform()
            actions.click().perform()
            time.sleep(1)
            print("maintenance click!")

            ## go to sub main - firmware update
            flashAct1 = driver.find_element_by_xpath(actionSubpath)
            actions1 = ActionChains(driver)
            actions1.move_to_element(flashAct1).perform()
            actions1.click().perform()
            time.sleep(1)
            print("firmware update click!")

            ####################################################################################
            #    Start uploading
            ####################################################################################
            ## move to bottom of page for show the button
            targetElem = driver.find_element_by_id("filefirmware_image")
            driver.execute_script("arguments[0].focus();", targetElem)

            ## automatic load image file
            driver.find_element_by_id("filefirmware_image").send_keys(runROM)
            time.sleep(2)

            ## click button to upload
            print(" button text : " + driver.find_element_by_class_name("btn-success").text)
            driver.find_element_by_class_name("btn-success").click()
            time.sleep(2)

            ## press OK when pop a alert window
            all_handle = driver.window_handles
            print(all_handle)
            Alert(driver).accept()

            ## wait for upload
            print("... ROM start uploading...")
            time.sleep(3)
            while driver.find_element_by_class_name("progress-info").text != "Uploading 100%":
                print(driver.find_element_by_class_name("progress-info").text)
                time.sleep(3)

            ## dump and record update percetage
            print(driver.find_element_by_class_name("progress-info").text)
            logFile.write("\n" + driver.find_element_by_class_name("progress-info").text)
            print("ROM upload completed!")
            logFile.write("\n ROM upload completed!")

            ####################################################################################
            #    Start flashing
            ####################################################################################
            ## move to bottom of page for show the button again
            ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
            targetElem1 = driver.find_element_by_class_name("progress")
            driver.execute_script("arguments[0].focus();", targetElem1)
            time.sleep(3)

            ## make scroll to bottom
            while TRUE:
                ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                targetElem1 = driver.find_element_by_class_name("progress")
                driver.execute_script("arguments[0].focus();", targetElem1)
                try:
                    # Find start flash button
                    WebDriverWait(driver, 30, 1).until(EC.visibility_of_element_located((By.ID, "upload_progress")))
                    print("...Find upload_progress")
                    break
                except TimeoutException:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    ActionChains(driver).key_down(Keys.DOWN).perform()
                    print("Press DOWN")
                    time.sleep(2)
                    print("*** Wait for flash button")

            ## Check the button text for confirm the status. the text should be "Flash selected sections"
            while driver.find_element_by_class_name("btn-success").text != "Flash selected sections":
                print(" ...Button text : " + driver.find_element_by_class_name("btn-success").text)
                time.sleep(1)
            # Click button to flash
            driver.find_element_by_class_name("btn-success").click()

            print("*** Wait for ROM flashing")
            ## wait for another alert window which prompt session will resrt
            while TRUE:
                try:
                    WebDriverWait(driver, 30, 1).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    print("...Reset session Alert accepted")
                    break
                except TimeoutException:
                    print("*** Wait for session reset alert pop-up")

            ####################################################################################
            #    Flash completed, wait 120 secord and reset session
            ####################################################################################
            # Wait for BMC reset
            print("  Completed time :" + str(datetime.datetime.now().strftime(timeFORMAT)))
            print("...Wait for reseting - 120 secords")
            countDown(120)

            driver.refresh()
            driver.quit()
            print("...ROM update completed!")
            logFile.write("\n  ROM update completed!\n")

            # Log file close by each loop
            logFile.close()

            ## check loop count
            if runLoop >= int(goTotalloop):
                testFinish()
                return
        else:
            stopTest()


def testFinish():
    messagebox.showinfo("Test finish", "IP: " + goUrl + "\n" + goTotalloop + " loops test finished!")
    var6.set("Finished")

def stopLoop():
    var6.set("Stopping...")
    stopFlag = 1

def stopTest():
    testFinish()
    var6.set("Interrupt")

def configSet(var0, var1, var2, var3, var4, var5, var6, var7, var8):
    global goBrowser
    global goUrl
    global goTotalloop
    global goUsrname
    global goPasswd
    global goVer1
    global goVer2
    global goROM1
    global goROM2
    goBrowser = var0
    goUrl = var1
    goTotalloop = var2
    goUsrname = var3
    goPasswd = var4
    goVer1 = var5
    goVer2 = var6
    goROM1 = var7
    goROM2 = var8
    messagebox.showinfo("Setting is updated","Broswer: " + goBrowser + "\n" +
                                             "IP: " + goUrl + "\n" + "Testloops: " + goTotalloop +"\n" +
                                             "username: " + goUsrname + "\n" + "password: " + goPasswd + "\n" +
                                             "BMC version 1: " + goVer1 + "\n" +
                                             "BMC version 2: " + goVer2 + "\n" +
                                             "Flash ROM 1: " + goROM1 + "\n" +
                                             "Flash ROM 2: " + goROM2 + "\n" + "\n" +
                                             "Setting is updated, please click Ready to Go to start test.")
    print("==== config set =====")
    print("Browser : " + goBrowser)
    print("UrlSet : " + goUrl)
    print("TestloopSet : " + goTotalloop)
    print("UsernameSet : " + goUsrname)
    print("PasswordSet : " + goPasswd)
    print("Flash version 1 : " + goVer1)
    print("Flash version 2 : " + goVer2)
    print("Flash ROM 1 : " + goROM1)
    print("Flash ROM 2 : " + goROM2)

def loadFlash1():
    entry7_rom1_controlBar.delete(0, "end")
    fileName=filedialog.askopenfilename(initialdir=" ", title="Select a file", filetypes=(("Flash ROM File",".ima"),("All files","*.*")))
    entry7_rom1_controlBar.insert(END, fileName)
    logFName1 = fileName

def loadFlash2():
    entry8_rom2_controlBar.delete(0, "end")
    fileName=filedialog.askopenfilename(initialdir=" ", title="Select a file", filetypes=(("Flash ROM File",".ima"),("All files","*.*")))
    entry8_rom2_controlBar.insert(END, fileName)
    logFName2 = fileName


def appClose():
    root.quit()
    root.destroy()
    exit()


if __name__ == '__main__':
    # control frame
    controlBar = LabelFrame(root, text="Config Setting", font=12)
    controlBar.grid(row=0, column=0, padx=15, pady=10)
    lbl0_controlBar = Label(controlBar, text="Browser")
    lbl0_controlBar.grid(row=0, column=0, pady=5, sticky=E)
    browserList_controlBar= ttk.Combobox(controlBar, width=20, value=browserList)
    browserList_controlBar.grid(row=0, column=1, padx=10, sticky=W)
    browserList_controlBar.insert(1, browserList[0])

    lbl1_controlBar = Label(controlBar, text="SUT BMC IP")
    lbl1_controlBar.grid(row=1, column=0, pady=5, sticky=E)
    entry1_ip_controlBar = Entry(controlBar, width=20)
    entry1_ip_controlBar.grid(row=1, column=1, padx=10, sticky=W)
    entry1_ip_controlBar.insert(0, defUrl)

    lbl2_controlBar = Label(controlBar, text="Test loops")
    lbl2_controlBar.grid(row=2, column=0, pady=5, sticky=E)
    entry2_loop_controlBar = Entry(controlBar, width=5)
    entry2_loop_controlBar.grid(row=2, column=1, padx=10, sticky=W)
    entry2_loop_controlBar.insert(0, defTotalloop)

    lbl3_controlBar = Label(controlBar, text="username")
    lbl3_controlBar.grid(row=3, column=0, pady=5, sticky=E)
    entry3_id_controlBar = Entry(controlBar, width=20)
    entry3_id_controlBar.grid(row=3, column=1, padx=10, sticky=W)
    entry3_id_controlBar.insert(0, defUsrname)

    lbl4_controlBar = Label(controlBar, text="password")
    lbl4_controlBar.grid(row=4, column=0, pady=5, sticky=E)
    entry4_pwd_controlBar = Entry(controlBar, width=20)
    entry4_pwd_controlBar.grid(row=4, column=1, padx=10, sticky=W)
    entry4_pwd_controlBar.insert(0, defPasswd)

    lbl5_controlBar = Label(controlBar, text="BMC Version 1")
    lbl5_controlBar.grid(row=5, column=0, pady=5, sticky=E)
    entry5_ver1_controlBar = Entry(controlBar, width=10)
    entry5_ver1_controlBar.grid(row=5, column=1, padx=10, sticky=W)
    entry5_ver1_controlBar.insert(0, defVer1)

    lbl6_controlBar = Label(controlBar, text="BMC Version 2")
    lbl6_controlBar.grid(row=6, column=0, pady=5, sticky=E)
    entry6_ver2_controlBar = Entry(controlBar, width=10)
    entry6_ver2_controlBar.grid(row=6, column=1, padx=10, sticky=W)
    entry6_ver2_controlBar.insert(0, defVer2)

    lbl7_controlBar = Label(controlBar, text="BMC Flash ROM 1")
    lbl7_controlBar.grid(row=7, column=0, pady=5, sticky=W)
    entry7_rom1_controlBar = Entry(controlBar, width=40)
    entry7_rom1_controlBar.grid(row=7, column=1, padx=10, sticky=W)
    entry7_rom1_controlBar.insert(0, defROM1)
    loadFlash1_btn_controlBar = ttk.Button(controlBar, text="Load", command=lambda: loadFlash1())
    loadFlash1_btn_controlBar.grid(row=7, column=2, padx=5)

    lbl8_controlBar = Label(controlBar, text="BMC Flash ROM 2")
    lbl8_controlBar.grid(row=8, column=0, pady=5, sticky=W)
    entry8_rom2_controlBar = Entry(controlBar, width=40)
    entry8_rom2_controlBar.grid(row=8, column=1, padx=10, sticky=W)
    entry8_rom2_controlBar.insert(0, defROM2)
    loadFlash2_btn_controlBar = ttk.Button(controlBar, text="Load", command=lambda: loadFlash2())
    loadFlash2_btn_controlBar.grid(row=8, column=2, padx=5)
    # call config set to make config set.
    button_configSet = ttk.Button(controlBar, text="Config Set", command=lambda: configSet(browserList_controlBar.get(), entry1_ip_controlBar.get(),
                                                                                           entry2_loop_controlBar.get(), entry3_id_controlBar.get(),
                                                                                           entry4_pwd_controlBar.get(), entry5_ver1_controlBar.get(),
                                                                                           entry6_ver2_controlBar.get(), entry7_rom1_controlBar.get(),
                                                                                           entry8_rom2_controlBar.get()))

    button_configSet.grid(row=9, column=1, padx=90, pady=5, sticky=W)


    # Start and exit button
    startBar = LabelFrame(root, text="Start/Exit", font=12)
    startBar.grid(row=1, column=0, padx=15, pady=5, sticky=W)
    button1_controlBar = ttk.Button(startBar, text="Start", command=lambda: callThreading())
    button1_controlBar.grid(row=0, column=0, padx=40, pady=5, sticky=E)
    button3_controlBar = ttk.Button(startBar, text="Stop", command=lambda: stopLoop())
    button3_controlBar.grid(row=0, column=1, padx=30, pady=5, sticky=E)
    button2_controlBar = ttk.Button(startBar, text=" Exit ", command=lambda: appClose())
    button2_controlBar.grid(row=0, column=2, padx=40, sticky=W)


    # status frame
    var5.set(str(0))
    var6.set("Stopped")
    statusBar = LabelFrame(root, text="Test Status", font=12)
    statusBar.grid(row=2, column=0, padx=15, pady=5, sticky=W)

    lbl5_controlBar = Label(statusBar, text="Test status : ", font=(12))
    lbl5_controlBar.grid(row=0, column=0, padx=70, sticky=E)
    status1 = Label(statusBar, textvariable=var6, font=(14))
    status1.grid(row=0, column=1, padx=70, sticky=W)

    lbl4_controlBar = Label(statusBar, text="Test Loop : ",font=(12))
    lbl4_controlBar.grid(row=1, column=0, padx=70, sticky=E)
    status = Label(statusBar, textvariable=var5, font=(14))
    status.grid(row=1, column=1, padx=70, sticky=W)

    root.geometry("490x510+300+150")
    root.mainloop()
