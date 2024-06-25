import tkinter as tk            
import time
from datetime import datetime
from DB_manager import DB_manager

'''
TODO:
- Hook up to database
- Implement Cash Dispenser Functionality
- Implement pages:
    - withdraw
    - dispense
    - check balance
- Bug test
- Give PIN PAD more functions [Partially Done]
- Display the pin somewhere when its being entered [DONE]
- Make the cancel option work
'''

'''
This should be changed in the future
Card #: Pin
1: 1234
2: 2121
3: 3333
'''


# ----------------- COLOR VARIABLES -------------------------------------------
color_header_section = "#737373"

color_side_section = "#b1b1b1"
color_side_component =  "#d9d9d9"

color_screen = "#7fb554"
color_text_light = "#ffffff"
color_text_dark = "#272727"

color_red = "#ff0000"
color_yellow = "#f9e300"
color_green = "#31ff00"

color_selected = "#e6ffe6"
color_notSelected = "#ffb3b3"
color_card = "#f2f2f2"


# ----------------- GLOBAL VARIABLES ------------------------------------------
current_pinpad_val = ""
current_msg = "Please select a card"
current_card = ""
current_page = "StartPage"
current_access = False


# ----------------- ROOT WINDOW -----------------------------------------------
class ATMApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("ATM")
        # ---------  APP LAYOUT -----------------------------------------------
        self.geometry("1200x800")
        self.resizable(0,0)
        self.config(bg=color_text_light)

        pages = [StartPage, MenuPage, WithdrawPage, DepositPage, BalancePage]

        # --------- MESSAGE OPTIONS -------------------------------------------
        message_default = "Please select a card"
        message_pin_prompt = "Please enter your PIN"
        message_pin_success = "Successful PIN Entry \n-- BUG CHECKING MESSAGE"
        message_pin_failure = "Incorrect PIN \nPlease try again"
        self.message_Withdraw_above_Max = "Withdraw Exceeds \nLimit"
        self.message_Withdraw_above_Balance = "Withdraw Exceeds\nAccount Balance"


        # --------- HEADER ----------------------------------------------------
        self.frame_header = tk.Frame(self, bg=color_header_section)
        self.frame_header.place(relx = 0, rely=0, relwidth=1, relheight=0.1)

        label_header = tk.Label(self.frame_header,
                               text="ATM",
                               font=("Arial", 60, "bold"),
                               fg=color_text_dark,
                               bg=color_header_section)
        label_header.pack()
        
    







        # --------- LEFT SECTION ----------------------------------------------
        self.frame_left_section = tk.Frame(self, bg=color_side_section)
        self.frame_left_section.place(relx = 0, rely=0.1, relwidth=0.3, relheight=0.9)
        # ========= PINPAD ====================================================
        frame_pinpad = tk.Frame(self, bg=color_side_component, highlightthickness=3, highlightbackground=color_text_dark)
        frame_pinpad_display = tk.Frame(self,bg=color_side_component,highlightthickness=3, highlightbackground=color_text_dark)
        frame_pinpad.place(relx=0.05, rely=0.2, relwidth=0.2, relheight=0.55)
        frame_pinpad_display.place(relx=0.05, rely=0.12, relwidth=0.2, relheight=0.08)
        pinpad_label = tk.Label(frame_pinpad_display, 
                            text = current_pinpad_val,
                            font=("Arial", 30, "bold"),
                            bg=color_side_component,
                            fg=color_text_dark)
        pinpad_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ========= FUNCTIONS =================================================
        def quickRemoveAdd(): #General
            for F in pages:
                page_name = F.__name__
                frame = F(frame_container, self)
                self.frames[page_name] = frame
                frame.place(relx=0, rely=0, relwidth=1, relheight=1)


        def setCurrentMessage(text): #General
            global current_msg, current_page
            current_msg = text
            clear_value()
            quickRemoveAdd()
            self.show_frame(current_page)


        def correctPIN():
            global current_msg, current_page
            current_msg = message_pin_success
            clear_value()
            current_page = "MenuPage"
            quickRemoveAdd()
            self.show_frame("MenuPage")
        
    
        def confirm_value(): #Needs to become more general
            global current_pinpad_val, current_card, current_access
            if current_access == False:
                if current_card == "":
                    setCurrentMessage(message_default + "!")
                    return
                if current_card == 1:
                    pin = str(DB_manager.get_pin(1))
                    if current_pinpad_val == pin: 
                        current_access = True
                        correctPIN()
                        return
                if current_card == 2:
                    pin = str(DB_manager.get_pin(2))
                    if current_pinpad_val == pin: 
                        current_access = True
                        correctPIN()
                        return
                if current_card == 3:
                    pin = str(DB_manager.get_pin(3))
                    if current_pinpad_val == pin: 
                        current_access = True
                        correctPIN()
                        return
                setCurrentMessage(message_pin_failure)
            if current_access == True:
                #give submit button different function once the card has been granted access
                return


        def updatePinVisual():
            global current_pinpad_val,current_page
            if current_page == "StartPage":
                pin = ''
                for i in range(len(current_pinpad_val)):
                    pin += '*'
                pinpad_label.config(text=pin)
                pinpad_label.place(y=6)#place(relx=0, rely=0.1, relwidth=1, relheight=1)
            else:
                pinpad_label.config(text=current_pinpad_val)


        def click(number):
            global current_pinpad_val
            current_pinpad_val+=str(number)
            updatePinVisual()


        def clear_value():
            global current_pinpad_val
            current_pinpad_val = ""
            updatePinVisual()


        def cancel_transaction(): #General
            global current_card, current_access, current_page
            if current_card != "":
                current_card = ""
                current_access = False
                current_page = "StartPage"
                button_card_1.config(state=tk.NORMAL, bg=color_card)
                button_card_2.config(state=tk.NORMAL, bg=color_card)
                button_card_3.config(state=tk.NORMAL, bg=color_card)
                self.button_confirm.config(command=confirm_value)
                my_label = tk.Label(self, 
                            text = "Ejecting card...",
                            font=("Arial", 30, "bold"),
                            bg=color_screen,
                            fg=color_text_light)
                my_label.place(relx=0.33, rely=0.25, relwidth=0.33, relheight=0.2)
                my_label.after(2000,lambda:my_label.destroy())
                setCurrentMessage(message_default)

        self.updatePin = updatePinVisual
        self.clearPin = clear_value
        self.canceltransaction = cancel_transaction
        self.message = setCurrentMessage

        # ========= BUTTONS ===================================================
        button_1 = tk.Button(frame_pinpad, text="1", command=lambda: click(1))
        button_2 = tk.Button(frame_pinpad, text="2", command=lambda: click(2))
        button_3 = tk.Button(frame_pinpad, text="3", command=lambda: click(3))
        button_4 = tk.Button(frame_pinpad, text="4", command=lambda: click(4))
        button_5 = tk.Button(frame_pinpad, text="5", command=lambda: click(5))
        button_6 = tk.Button(frame_pinpad, text="6", command=lambda: click(6))
        button_7 = tk.Button(frame_pinpad, text="7", command=lambda: click(7))
        button_8 = tk.Button(frame_pinpad, text="8", command=lambda: click(8))
        button_9 = tk.Button(frame_pinpad, text="9", command=lambda: click(9))
        button_0 = tk.Button(frame_pinpad, text="0", command=lambda: click(0))

        self.button_cancel = tk.Button(frame_pinpad, text="Cancel", bg=color_red, command=cancel_transaction)
        button_clear = tk.Button(frame_pinpad, text="Clear", bg=color_yellow, command=clear_value)
        self.button_confirm = tk.Button(frame_pinpad, text="Confirm", bg=color_green, command=confirm_value)

        button_1.place(relx=0/3, rely=2/5, relwidth=1/3, relheight=1/5)
        button_2.place(relx=1/3, rely=2/5, relwidth=1/3, relheight=1/5)
        button_3.place(relx=2/3, rely=2/5, relwidth=1/3, relheight=1/5)
        button_4.place(relx=0/3, rely=1/5, relwidth=1/3, relheight=1/5)
        button_5.place(relx=1/3, rely=1/5, relwidth=1/3, relheight=1/5)
        button_6.place(relx=2/3, rely=1/5, relwidth=1/3, relheight=1/5)
        button_7.place(relx=0/3, rely=0/5, relwidth=1/3, relheight=1/5)
        button_8.place(relx=1/3, rely=0/5, relwidth=1/3, relheight=1/5)
        button_9.place(relx=2/3, rely=0/5, relwidth=1/3, relheight=1/5)
        button_0.place(relx=0/3, rely=3/5, relwidth=3/3, relheight=1/5)
        
        self.button_cancel.place(relx=0/3, rely=4/5, relwidth=1/3, relheight=1/5)
        button_clear.place(relx=1/3, rely=4/5, relwidth=1/3, relheight=1/5)
        self.button_confirm.place(relx=2/3, rely=4/5, relwidth=1/3, relheight=1/5)


        # --------- RIGHT SECTION ---------------------------------------------
        self.frame_right_section = tk.Frame(self, bg=color_side_section)
        self.frame_right_section.place(relx = 0.7, rely=0.1, relwidth=0.3, relheight=0.9)

        # ========= CARD SCANNER ==============================================
        frame_card_scanner = tk.Frame(self, bg=color_side_component, highlightthickness=3, highlightbackground=color_text_dark)
        frame_card_scanner.place(relx=0.75, rely=0.2, relwidth=0.2, relheight=0.5)

        # ========= FUNCTIONS =================================================
        def insertCard(number):
            global current_card, current_msg
            current_card = number
            if current_card == 1:
                button_card_1.config(bg=color_selected)
                button_card_2.config(bg=color_notSelected, state=tk.DISABLED)
                button_card_3.config(bg=color_notSelected, state=tk.DISABLED)
            if current_card == 2:
                button_card_2.config(bg=color_selected)
                button_card_1.config(bg=color_notSelected, state=tk.DISABLED)
                button_card_3.config(bg=color_notSelected, state=tk.DISABLED)
            if current_card == 3:
                button_card_3.config(bg=color_selected)
                button_card_1.config(bg=color_notSelected, state=tk.DISABLED)
                button_card_2.config(bg=color_notSelected, state=tk.DISABLED)
            setCurrentMessage(message_pin_prompt)
                
        # ========= BUTTONS ===================================================
        cardWidth = 32
        cardHeight = 8
        button_card_1 = tk.Button(frame_card_scanner, text="card 1", bg=color_card, command=lambda: insertCard(1))
        button_card_2 = tk.Button(frame_card_scanner, text="card 2", bg=color_card, command=lambda: insertCard(2))
        button_card_3 = tk.Button(frame_card_scanner, text="card 3", bg=color_card, command=lambda: insertCard(3))
        
        button_card_1.place(relx=0, rely=0/3, relwidth=1, relheight=1/3)
        button_card_2.place(relx=0, rely=1/3, relwidth=1, relheight=1/3)
        button_card_3.place(relx=0, rely=2/3, relwidth=1, relheight=1/3)

        frame_cash_dispenser = tk.Frame(self, bg=color_side_component, highlightthickness=3, highlightbackground=color_text_dark)
        frame_cash_dispenser.place(relx=0.75, rely=0.8, relwidth=0.2, relheight=0.15)

        label_cash_dispenser = tk.Label(frame_cash_dispenser,
                                        text="Cash Dispenser",
                                        font=("Arial", 20, "bold"),
                                        bg=color_side_component,
                                        fg=color_text_dark)
        label_cash_dispenser.place(relx=0, rely=0.1, relwidth=1, relheight=0.3)








        # --------- MIDDLE SECTION --------------------------------------------
        frame_container = tk.Frame(self, highlightthickness=3, highlightbackground=color_text_dark)
        frame_container.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.9)

        self.frames = {}

        quickRemoveAdd()
        self.show_frame("StartPage")

    # ------------- SHOW FRAMES -----------------------------------------------
    #Check account balance
    def validWithdrawl(self):
            global current_pinpad_val,current_card,current_msg
            maxWithdraw = DB_manager.get_maxWithdraw(current_card)
            current_allowable_withdraw = maxWithdraw - DB_manager.get_currentWithdraw(current_card)
            last_withdraw_time_str = DB_manager.get_last_withdraw_time_str_by_id(current_card)
            
            if last_withdraw_time_str is not None:
                last_withdraw_time = datetime.strptime(last_withdraw_time_str,"%d/%m/%y %H:%M:%S")
                time_since_last_withdraw_seconds = (datetime.now() - last_withdraw_time).seconds
                if time_since_last_withdraw_seconds>60:
                    DB_manager.resetCurrentWithdraw(current_card)
                    current_allowable_withdraw = maxWithdraw

            if current_pinpad_val != '':
                if (float(current_pinpad_val) > DB_manager.get_balance_by_id_query(current_card)):
                    self.clearPin()
                    self.updatePin()
                    self.update_withdraw_low_funds("WithdrawPage")
                    self.canceltransaction()
                    my_label = tk.Label(self, 
                            text = "Insufficient account \n funds ejecting card...",
                            font=("Arial", 30, "bold"),
                            bg=color_screen,
                            fg=color_text_light)
                    my_label.place(relx=0.33, rely=0.25, relwidth=0.33, relheight=0.2)
                    my_label.after(2000,lambda:my_label.destroy())
                elif (float(current_pinpad_val) > current_allowable_withdraw):
                    self.clearPin()
                    self.updatePin()
                    self.update_withdraw_above_max("WithdrawPage")
                    self.canceltransaction()
                    my_label = tk.Label(self, 
                            text = "Max withdraw limit \n reached ejecting card...",
                            font=("Arial", 30, "bold"),
                            bg=color_screen,
                            fg=color_text_light)
                    my_label.place(relx=0.33, rely=0.25, relwidth=0.33, relheight=0.2)
                    my_label.after(2000,lambda:my_label.destroy())
                else:
                    self.sufficientATMFunds()
    
    def sufficientATMFunds(self):
        global current_pinpad_val,current_card
        if(float(current_pinpad_val) > DB_manager.get_AtmBalance()):
            self.clearPin()
            self.updatePin()
            self.update_withdraw_ATM_max("WithdrawPage")
            self.canceltransaction()
            my_label = tk.Label(self, 
                text = "Insufficient ATM \n funds ejecting card...",
                font=("Arial", 30, "bold"),
                bg=color_screen,
                fg=color_text_light)
            my_label.place(relx=0.33, rely=0.25, relwidth=0.33, relheight=0.2)
            my_label.after(2000,lambda:my_label.destroy())
        else:
            withdraw_time_str = datetime.now().strftime("%d/%m/%y %H:%M:%S")
            
            DB_manager.WithdrawMoney_ATM(float(current_pinpad_val))
            DB_manager.WithdrawMoney(float(current_pinpad_val),withdraw_time_str,current_card) 
            DB_manager.setCurrentWithdraw(float(current_pinpad_val),current_card)
            self.clearPin()
            self.updatePin()
            self.update_and_show_balance_frame("WithdrawPage")
            frame_cash_dispenser = tk.Frame(self, bg='green', highlightthickness=3, highlightbackground=color_text_dark)
            frame_cash_dispenser.place(relx=0.75, rely=0.8, relwidth=0.2, relheight=0.15)
            frame_cash_dispenser.after(2000,lambda:frame_cash_dispenser.destroy())
            self.canceltransaction()
            my_label = tk.Label(self, 
                text = "Disbursing Cash \n please take cash \n and card...",
                font=("Arial", 30, "bold"),
                bg=color_screen,
                fg=color_text_light)
            my_label.place(relx=0.33, rely=0.25, relwidth=0.33, relheight=0.2)
            my_label.after(2000,lambda:my_label.destroy())
            

    def DepositMoney(self):
        global current_pinpad_val,current_card

        if current_pinpad_val != '':
            DB_manager.DepositMoney(float(current_pinpad_val),current_card)
            DB_manager.DepositMoneyATM(float(current_pinpad_val))
            self.clearPin()
            self.updatePin()
            self.update_and_show_balance_frame("DepositPage")


    def changeButtons(self,page):
        global current_page, current_msg
        current_page = page
        self.button_cancel.config(command=self.canceltransaction)
        match page:
            case "WithdrawPage":
                self.button_confirm.config(command= self.validWithdrawl)
            case "DepositPage":
                self.button_confirm.config(command= self.DepositMoney)
        
    def Go_home(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.changeButtons(cont)

    def show_frame(self, cont):
        global current_msg
        frame = self.frames[cont]
        frame.tkraise()
        self.changeButtons(cont)

    def update_and_show_balance_frame(self,cont):
        frame = self.frames[cont]
        frame.refresh()
        self.show_frame(cont)

    def clear_frame(self,cont):
        frame = self.frames[cont]
        frame.clear()
        self.show_frame(cont)

    def update_withdraw_low_funds(self,cont):
        frame = self.frames[cont]
        frame.badWithdraw()
        self.show_frame(cont)

    def update_withdraw_above_max(self,cont):
        frame = self.frames[cont]
        frame.maxWithdraw()
        self.show_frame(cont)

    def update_withdraw_ATM_max(self,cont):
        frame = self.frames[cont]
        frame.atmMax()
        self.show_frame(cont)


















# ----------------- START WINDOW ----------------------------------------------
class StartPage(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=color_screen)
        
        # ========= LABELS ====================================================
        label_title = tk.Label(self, 
                         text="START PAGE",
                         font=("Arial", 30, "bold"),
                         bg=color_screen,
                         fg=color_text_light)
        label_title.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.2)

        my_label = tk.Label(self, 
                            text = current_msg,
                            font=("Arial", 30, "bold"),
                            bg=color_screen,
                            fg=color_text_light)
        my_label.place(relx=0, rely=0.2, relwidth=1, relheight=0.2)
















# ----------------- MAIN MENU WINDOW ------------------------------------------
class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=color_screen)
        heightLabel = 0.1

        # ========= LABELS ====================================================
        label_title = tk.Label(self, 
                         text="MAIN MENU PAGE",
                         font=("Arial", 30, "bold"),
                         bg=color_screen,
                         fg=color_text_light)
        label_title.place(relx=0, rely=0, relwidth=1, relheight=heightLabel)


        # ========= BUTTONS ===================================================
        heightButton = 0.15
        widthButton = 0.5 
        YoffsetButton = 0.2 #Y indentation
        XoffsetButton = 0.25 #X indentation
        labelOffset = heightLabel #Account for label size
        spacingOffset = 0.05 #Additional spacing


        button_withdraw = tk.Button(self,
                                    text="1. Withdraw Money",
                                    command=lambda: controller.clear_frame("WithdrawPage"))
        button_withdraw.place(relx=XoffsetButton, 
                              rely=(YoffsetButton*0+labelOffset+spacingOffset), 
                              relwidth=widthButton, 
                              relheight=heightButton)

        button_desposit = tk.Button(self,
                                    text="2. Deposit Money",
                                    command=lambda: controller.clear_frame("DepositPage"))
        button_desposit.place(relx=XoffsetButton, 
                              rely=(YoffsetButton*1+labelOffset+spacingOffset), 
                              relwidth=widthButton, 
                              relheight=heightButton)

        button_balance = tk.Button(self,
                                    text="3. Check Balance",
                                    command=lambda: controller.update_and_show_balance_frame("BalancePage"))
        button_balance.place(relx=XoffsetButton, 
                             rely=(YoffsetButton*2+labelOffset+spacingOffset), 
                             relwidth=widthButton, 
                             relheight=heightButton)

        button_cancel = tk.Button(self,
                                    text="4. Cancel",
                                    command=None)
        button_cancel.place(relx=XoffsetButton, 
                            rely=(YoffsetButton*3+labelOffset+spacingOffset), 
                            relwidth=widthButton, 
                            relheight=heightButton)


        
    












# ----------------- WITHDRAW WINDOW -------------------------------------------
class WithdrawPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=color_screen)

        self.xOffsetLabel = 0
        self.yOffsetLabel = 0.1
        self.widthLabel = 1
        self.heightLabel = 0.2
        
        
        # ========= LABELS ====================================================
        label_title = tk.Label(self, 
                         text="WITHDRAW PAGE",
                         font=("Arial", 30, "bold"),
                         bg=color_screen,
                         fg=color_text_light)
        label_title.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        self.label_withdraw_balance = tk.Label(self, 
            text="",
            font=("Arial", 20, "bold"),
            bg=color_screen,
            fg=color_text_light)
        self.label_withdraw_balance.place(relx=self.xOffsetLabel, 
                                          rely=self.yOffsetLabel, 
                                          relwidth=self.widthLabel, 
                                          relheight=self.heightLabel)
        heightButton = 0.08
        widthButton = 0.25 
        YoffsetButton = 1 - heightButton - 0.04
        XoffsetButton = 0.7 
        button_withdraw = tk.Button(self,
                                    text="Done",
                                    command=lambda: controller.show_frame("MenuPage"))
        button_withdraw.place(relx=XoffsetButton, 
                              rely=YoffsetButton, 
                              relwidth=widthButton, 
                              relheight=heightButton)

    def refresh(self):
        self.label_withdraw_balance.destroy()
        self.label_withdraw_balance = tk.Label(self, 
            text="New Balance: " +str(DB_manager.get_balance_by_id_query(current_card)),
            font=("Arial", 20, "bold"),
            bg=color_screen,
            fg=color_text_light)
        self.label_withdraw_balance.place(relx=self.xOffsetLabel, 
                                          rely=self.yOffsetLabel, 
                                          relwidth=self.widthLabel, 
                                          relheight=self.heightLabel)

    def clear(self):
        self.label_withdraw_balance.destroy()
        self.label_withdraw_balance = tk.Label(self, 
            text="Current Balance: "+str(DB_manager.get_balance_by_id_query(current_card)),
            font=("Arial", 20, "bold"),
            bg=color_screen,
            fg=color_text_light)
        self.label_withdraw_balance.place(relx=self.xOffsetLabel, 
                                          rely=self.yOffsetLabel, 
                                          relwidth=self.widthLabel, 
                                          relheight=self.heightLabel)

    def badWithdraw(self):
        self.label_withdraw_balance.destroy()
        self.label_withdraw_balance = tk.Label(self, 
            text="Insufficient Funds",
            font=("Arial", 20, "bold"),
            bg=color_screen,
            fg=color_text_light)
        self.label_withdraw_balance.place(relx=self.xOffsetLabel, 
                                          rely=self.yOffsetLabel, 
                                          relwidth=self.widthLabel, 
                                          relheight=self.heightLabel)

    def maxWithdraw(self):
        self.label_withdraw_balance.destroy()
        self.label_withdraw_balance = tk.Label(self, 
            text="Withdraw request is greater \n then allowable max",
            font=("Arial", 20, "bold"),
            bg=color_screen,
            fg=color_text_light)
        self.label_withdraw_balance.place(relx=self.xOffsetLabel, 
                                          rely=self.yOffsetLabel, 
                                          relwidth=self.widthLabel, 
                                          relheight=self.heightLabel)
    
    def atmMax(self):
        self.label_withdraw_balance.destroy()
        self.label_withdraw_balance = tk.Label(self, 
            text="Withdraw request is greater \n then ATM funds",
            font=("Arial", 20, "bold"),
            bg=color_screen,
            fg=color_text_light)
        self.label_withdraw_balance.place(relx=self.xOffsetLabel, 
                                          rely=self.yOffsetLabel, 
                                          relwidth=self.widthLabel, 
                                          relheight=self.heightLabel)










# ----------------- DEPOSIT WINDOW --------------------------------------------
class DepositPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=color_screen)

        self.xOffsetLabel = 0
        self.yOffsetLabel = 0.1
        self.widthLabel = 1
        self.heightLabel = 0.2
        
        # ========= LABELS ====================================================
        label_title = tk.Label(self, 
                         text="DEPOSIT PAGE",
                         font=("Arial", 30, "bold"),
                         bg=color_screen,
                         fg=color_text_light)
        label_title.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        self.label_deposit_balance = tk.Label(self, 
            text="",
            font=("Arial", 20, "bold"),
            bg=color_screen,
            fg=color_text_light)
        self.label_deposit_balance.place(relx=self.xOffsetLabel, 
                                          rely=self.yOffsetLabel, 
                                          relwidth=self.widthLabel, 
                                          relheight=self.heightLabel)
        heightButton = 0.08
        widthButton = 0.25 
        YoffsetButton = 1 - heightButton - 0.04
        XoffsetButton = 0.7 
        button_withdraw = tk.Button(self,
                                    text="Done",
                                    command=lambda: controller.show_frame("MenuPage"))
        button_withdraw.place(relx=XoffsetButton, 
                              rely=YoffsetButton, 
                              relwidth=widthButton, 
                              relheight=heightButton)

    def refresh(self):
        self.label_deposit_balance.destroy()
        self.label_deposit_balance = tk.Label(self, 
            text="New Balance: " +str(DB_manager.get_balance_by_id_query(current_card)),
            font=("Arial", 20, "bold"),
            bg=color_screen,
            fg=color_text_light)
        self.label_deposit_balance.place(relx=self.xOffsetLabel, 
                                          rely=self.yOffsetLabel, 
                                          relwidth=self.widthLabel, 
                                          relheight=self.heightLabel)

    def clear(self):
        self.label_deposit_balance.destroy()
        















# ----------------- BALANCE WINDOW --------------------------------------------
class BalancePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=color_screen)

        self.xOffsetLabel = 0
        self.yOffsetLabel = 0.1
        self.widthLabel = 1
        self.heightLabel = 0.2
        # ========= LABELS ====================================================
        label_title = tk.Label(self, 
                            text="BALANCE PAGE",
                            font=("Arial", 30, "bold"),
                            bg=color_screen,
                            fg=color_text_light)
        label_title.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        if current_card!="":
            curr_balance = str(DB_manager.get_balance_by_id_query(current_card))
            self.label_balance = tk.Label(self, 
            text="Current Balance: " +curr_balance,
            font=("Arial", 20, "bold"),
            bg=color_screen,
            fg=color_text_light)
            self.label_balance.place(relx=self.xOffsetLabel, 
                                 rely=self.yOffsetLabel, 
                                 relwidth=self.widthLabel, 
                                 relheight=self.heightLabel)

        # ========= LABELS ====================================================
        heightButton = 0.08
        widthButton = 0.25 
        YoffsetButton = 1 - heightButton - 0.04
        XoffsetButton = 0.7 

        button_withdraw = tk.Button(self,
                                    text="Done",
                                    command=lambda: controller.show_frame("MenuPage"))
        button_withdraw.place(relx=XoffsetButton, 
                              rely=YoffsetButton, 
                              relwidth=widthButton, 
                              relheight=heightButton)

    def refresh(self):
        self.label_balance.destroy()
        if current_card!="":
            curr_balance = str(DB_manager.get_balance_by_id_query(current_card))
            self.label_balance = tk.Label(self, 
            text="Current Balance: " +curr_balance,
            font=("Arial", 20, "bold"),
            bg=color_screen,
            fg=color_text_light)
            self.label_balance.place(relx=self.xOffsetLabel, 
                                 rely=self.yOffsetLabel, 
                                 relwidth=self.widthLabel, 
                                 relheight=self.heightLabel)
        
        

