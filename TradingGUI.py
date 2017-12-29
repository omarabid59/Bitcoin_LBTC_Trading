from Tkinter import *
import APICalls as api_calls
import json
from tkMessageBox import *
import time
from VerticalScrolledFrame import VerticalScrolledFrame

def refresh_quadriga_open_orders():
    global quadriga_open_orders
    quadriga_open_orders = api_calls.getQuadrigaOpenOrders(api_calls.qkey, api_calls.qsecret,
                                                                api_calls.qclientID)
    
def refresh_account_balances():
    global balance
    global lbtc_balance
    balance = api_calls.getBalance(api_calls.qkey, api_calls.qsecret, api_calls.qclientID)
    lbtc_balance = api_calls.get_lbtc_balance()
def refresh_sending_address():
    global lbtc_sending_address
    global quadriga_sending_address
    lbtc_sending_address = api_calls.getRecievingLBTCAddress()
    quadriga_sending_address = api_calls.getQuadrigaDepositAddress(api_calls.qkey, api_calls.qsecret,
                                                                api_calls.qclientID)

def refresh_lbtc_open_orders():
    global all_data
    global quadrigaBTCPerDollar
    quadrigaData = api_calls.getBTCMarketData()
    quadrigaBTCPerDollar = float(quadrigaData['last'])
    all_data = api_calls.getOpenOrders(api_calls.getLBTCData(), api_calls.getLBTCUserName(), quadrigaBTCPerDollar)
def refresh_quadriga_market_data():
    global quadrigaData
    global quadrigaBTCPerDollar
    quadrigaData = api_calls.getMarketData()
    quadrigaBTCPerDollar = float(quadrigaData['last'])



def refresh_network_data():
    # Get the open orders
    refresh_quadriga_open_orders()
    refresh_account_balances()
    refresh_sending_address()
    refresh_lbtc_open_orders()
    global quadriga_portion_book_orders
    quadriga_portion_book_orders = api_calls.getOrderBook(1)
    print('Sucess. Retrieved Data')
    return TRUE

def refresh_network_data_dialog():
    refresh_network_data()
    showinfo("Success","Data Refreshed")

def transfer_btc_to_localbitcoins_dialog(key, secret, clientID, amount, pin):
       # Check if pin's match
       if (pin == api_calls.SECURITY_PIN):
              # First show ask question dialog
              questionStr = 'You are about to withdraw ' + str(amount) + ' BTC to address: '
              questionStr += str(lbtc_sending_address)
              questionStr += '\nAre you sure?'
              question_result = askquestion("Confirm Withdrawal",questionStr)
              if question_result == 'yes':
                  out = api_calls.sendBTC(key, secret, clientID, amount, lbtc_sending_address)
                  out = json.loads(out)
                  if 'error' in out:
                      error_code = out['error']['code']
                      if (error_code == 21):
                        showerror("Error", "Insufficient funds")
                      else:
                          showerror("Error", 'Unknown error')
                  else:
                      textStr = 'Valid pin. Sending ' + str(amount) + ' to  address ' + str(
                          lbtc_sending_address) + " Result: " + str(out)
                      showinfo("Success!",textStr)

       else:
              showerror("Error", "Please enter a valid pin.")


def transfer_localbitcoins_to_quadriga_dialog(key, secret, clientID, amount, pin,sending_address):
    # Check if pin's match
    if (pin == api_calls.SECURITY_PIN):
        # First show ask question dialog
        questionStr = 'You are about to withdraw ' + str(amount) + ' BTC to address: '
        questionStr += str(lbtc_sending_address)
        questionStr += '\nAre you sure?'
        question_result = askquestion("Confirm Withdrawal", questionStr)
        if question_result == 'yes':
            out = api_calls.sendBTC(key, secret, clientID, amount, lbtc_sending_address)
            out = json.loads(out)
            if 'error' in out:
                error_code = out['error']['code']
                if (error_code == 21):
                    showerror("Error", "Insufficient funds")
                else:
                    showerror("Error", 'Unknown error')
            else:
                textStr = 'Valid pin. Sending ' + str(amount) + ' to  address ' + str(
                    lbtc_sending_address) + " Result: " + str(out)
                showinfo("Success!", textStr)

    else:
        showerror("Error", "Please enter a valid pin.")

def buy_btc_dialog(name, amount_cad, buy_price, pin,master):
   amount_btc = str(round(float(amount_cad)/float(buy_price),6))
   # SPECIFY THE CORRECT KEY, SECRET, CLIENT ID
   key = api_calls.qkey
   secret = api_calls.qsecret
   clientID = api_calls.qclientID

   # Check if pin's match
   if (pin == api_calls.SECURITY_PIN):
       # First show ask question dialog
       questionStr = 'You are about to buy $' + str(amount_cad) + ' @ $'
       questionStr += str(buy_price)
       questionStr += '\nExact BTC Amount: ' + amount_btc
       questionStr += '\nAre you sure?'
       question_result = askquestion("Confirm Purchase", questionStr)
       if question_result == 'yes':
           out = api_calls.buyBTC(key, secret, clientID, amount_btc, buy_price)
           out = json.loads(out)
           if 'error' in out:
               textStr = str(out['error']['message'])
               print(textStr)
               showerror("Error", textStr)
           else:
               textStr = 'Valid pin. Buying $' + str(amount_cad) + " Result: " + str(out)
               showinfo("Success!", textStr)
               # REFRESH THE DATA!
               refresh_quadriga_open_orders()
               quadriga_open_orders_frame(master)

   else:
       showerror("Error", "Please enter a valid pin.")
def sell_btc_dialog(name, amount_cad, buy_price, pin,master):
   amount_btc = str(round(float(amount_cad)/float(buy_price),6))
   # SPECIFY THE CORRECT KEY, SECRET, CLIENT ID
   key = api_calls.qkey
   secret = api_calls.qsecret
   clientID = api_calls.qclientID

   # Check if pin's match
   if (pin == api_calls.SECURITY_PIN):
       # First show ask question dialog
       questionStr = 'You are about to sell $' + str(amount_cad) + ' @ $'
       questionStr += str(buy_price)
       questionStr += '\nExact BTC Amount: ' + amount_btc
       questionStr += '\nAre you sure?'
       question_result = askquestion("Confirm Purchase", questionStr)
       if question_result == 'yes':
           out = api_calls.sellBTC(key, secret, clientID, amount_btc, buy_price)
           out = json.loads(out)
           if 'error' in out:
               textStr = str(out['error']['message'])
               print(textStr)
               showerror("Error", textStr)
           else:
               textStr = 'Valid pin. Buying $' + str(amount_cad) + " Result: " + str(out)
               showinfo("Success!", textStr)
               # REFRESH THE DATA!
               refresh_quadriga_open_orders()
               quadriga_open_orders_frame(master)

   else:
       showerror("Error", "Please enter a valid pin.")

def cancel_order_dialog( tid, datetime, price, amount, master):
    account = 'Account Name'
    key = api_calls.qkey
    secret = api_calls.qsecret
    clientID = api_calls.qclientID
    # First show ask question dialog
    questionStr = 'You are about to cancel order with info:\n'
    questionStr += 'Account: ' + str(account) + '\n'
    questionStr += 'ID: ' + str(tid) + '\n'
    questionStr += 'Date: ' + str(datetime) + '\n'
    questionStr += 'Price $: ' + str(price) + '\n'
    questionStr += 'Amount (BTC): ' + str(amount) + '\n'
    questionStr += 'Are you sure?'
    question_result = askquestion("Confirm Cancellation", questionStr)
    if question_result == 'yes':
       out = api_calls.cancelTrade(key, secret, clientID, tid)
       out = json.loads(out)
       if (isinstance(out,bool)):
           textStr = 'Order with ID: ' + str(tid) + " Canceled! " + " Result: " + str(out)
           showinfo("Success!", textStr)
           # REFRESH THE DATA!
           refresh_quadriga_open_orders()
           quadriga_open_orders_frame(master)
       else:
           if 'error' in out:
               textStr = str(out['error']['message'])
               print(textStr)
               showerror("Error", textStr)

# Show's the Left frame summarizing current balances.
def account_summary_frame(master):
    main_frame = Frame(master,bg="yellow")
    main_frame.grid()

    balance_cad = round(float(balance['cad_balance']),2)
    balance_btc = round(float(balance['eth_available']),4)
    lbtc_rounded_balance = round(float(lbtc_balance),4)



    for r in range(7):
        main_frame.rowconfigure(r, weight=1)
    for c in range(4):
        main_frame.columnconfigure(c, weight=1)

    l1 = Label(main_frame,text = "-")
    l1.grid(row=0,column=0,sticky=E+W)
    l2 = Label(main_frame, text="   Your Name   ", fg="red")
    l2.grid(row=0, column=1, sticky=E + W)
    l3 = Label(main_frame, text="    LocalBitcoins", fg="red")
    l3.grid(row=0, column=2, sticky=E + W)
    l4 = Label(main_frame, text="    Total", fg="red")
    l4.grid(row=0, column=3, sticky=E + W)
    l5 = Label(main_frame, text="BTC", fg="red")
    l5.grid(row=1, column=0, sticky=E + W)
    l6 = Label(main_frame, text="CAD", fg="red")
    l6.grid(row=2, column=0, sticky=E + W)

    # Display the data...
    l1 = Label(main_frame, text=str(balance_btc))
    l1.grid(row=1, column=1, sticky=E + W)
    l1 = Label(main_frame, text=str(balance_cad))
    l1.grid(row=2, column=1, sticky=E + W)


    l1 = Label(main_frame, text=str(lbtc_rounded_balance))
    l1.grid(row=1, column=2, sticky=E + W)
    l1 = Label(main_frame, text="N/A")
    l1.grid(row=2, column=2, sticky=E + W)

    l1 = Label(main_frame, text=str(balance_btc+lbtc_rounded_balance))
    l1.grid(row=1, column=3, sticky=E + W)
    l1 = Label(main_frame, text=str(balance_cad))
    l1.grid(row=2, column=3, sticky=E + W)

    l1 = Label(main_frame, text="Withdrawal Amount (BTC)")
    l1.grid(row=3, column=0, rowspan=1, columnspan=2,  sticky=E + W)
    withdraw_amount = Entry(main_frame, text="0.0")
    withdraw_amount.grid(row=3, column=2, rowspan=1, columnspan=2, sticky=E + W)
    withdraw_amount.delete(0,END)
    withdraw_amount.insert(0,"0.0")


    e1 = Entry(master, fg="black")
    e1.insert(0, 'PIN')
    e1.grid(row=4, column=0, rowspan=1, columnspan=4, sticky=W + E + N + S)


    b1 = Button(master, text='Transfer Quadiga -> LocalBitcoins', command=lambda:
             transfer_btc_to_localbitcoins_dialog(api_calls.qkey, api_calls.qsecret,
                                                  api_calls.qclientID,
                                                  withdraw_amount.get(), e1.get()),
                    fg="black")
    b1.grid(row=5, column=0, rowspan=1, columnspan=4, sticky=W + E + N + S)


    b1 = Button(master, text='Transfer LocalBitcoins -> Quadriga', command=lambda:
    transfer_localbitcoins_to_quadriga_dialog(api_calls.qkey, api_calls.qsecret,
                                                  api_calls.qclientID,
                                         withdraw_amount.get(), e1.get()),
                fg="black")
    b1.grid(row=7, column=0, rowspan=1, columnspan=4, sticky=W + E + N + S)



def lbtc_open_orders_frame(master):
    frame = VerticalScrolledFrame(master)
    frame.pack(fill=X)

    if (not all_data['data']):
        l1 = Label(frame.interior, text='### NO OPEN ORDERS! ###', fg="black")
        l1.pack(side=TOP, fill=X)
    else:
        for data in all_data['data']:
            this_data = all_data['data'][data]
            #print (this_data)
            client_username = this_data['client']
            amount_cad = str(this_data['deposit_amount_cad'])
            e_transfer_fee = str(max(api_calls.depositFee * float(amount_cad), 5))
            btc_bought = str(round(this_data['bitcoins_bought'],2))
            btc_sold = str(round(this_data['bitcoins_sold'],2))
            usable_dollar_amount = str(this_data['usable_dollar_amount'])
            btc_profit = str(round(this_data['btc_profit'],2))
            cad_profit = str(round(this_data['cad_profit'],2))
            l1 = Label(frame.interior, text='##########Trading with client ' + client_username
                       + ' ###########', fg="black")
            l1.pack(side=TOP, fill=X)
            l2 = Label(frame.interior, text='Deposit this much into Quadriga $' + amount_cad, fg="red")
            l2.pack(side=TOP, fill=X)
            l3 = Label(frame.interior, text='Interac E-Transfer Fee $' + e_transfer_fee, fg="red")
            l3.pack(side=TOP, fill=X)
            l4 = Label(frame.interior, text='Bitcoins Bought  ' + btc_bought
                       + ' BTC (on Quadriga @ $' + str(quadrigaBTCPerDollar), fg="red")
            l4.pack(side=TOP, fill=X)
            l5 = Label(frame.interior, text='Bitcoins Sold  ' + btc_sold
                                            + ' BTC ', fg="red")
            l5.pack(side=TOP, fill=X)
            l6 = Label(frame.interior, text='Using $  ' + usable_dollar_amount
                                            , fg="red")
            l6.pack(side=TOP, fill=X)
            l7 = Label(frame.interior, text='Profit $' + cad_profit + ' (' + btc_profit + ' BTC)'
                       , fg="red")
            l7.pack(side=TOP, fill=X)

        l8 = Label(master, text='Net Profit $' + str(round(all_data['net_revenue_cad'],2))
                   + ' (' + str(round(all_data['net_revenue_btc'],3)) + ' BTC)'
                   , fg="black")
        l8.pack(side=LEFT, fill=X)



def quadriga_open_orders_frame(master):
    # Destroy all previous children in this frame
    for widget in master.winfo_children():
        widget.destroy()
    frame = Frame(master, bg="pink")
    frame.grid()

    rows = 2 # Initially you have this many rows (Title, Headers)
    cols = 8 #Fixed

    pad_size = 10


    #Manual configuration of the first 2 rows

    '''
    for r in range(10):
        frame.rowconfigure(r, weight=1)
    for c in range(7):
        frame.columnconfigure(c, weight=1)
    '''

    l1 = Label(frame, text="QUADRIGA OPEN ORDERS ")
    l1.grid(row=0, column=0, columnspan=8, rowspan=1, sticky=E + W)



    l_account = Label(frame, text="Account", bg="orange", fg="black", borderwidth=2, relief="solid", padx = pad_size)
    l_account.grid(row=1, column=0, sticky=E + W)

    #l_tid = Label(frame, text="Transaction ID", bg="orange", fg="black", borderwidth=2, relief="solid",padx = pad_size)
    #l_tid.grid(row=1, column=1, sticky=E + W)

    l_datetime = Label(frame, text="Date and Time", bg="orange", fg="black", borderwidth=2,relief="solid", padx = pad_size)
    l_datetime.grid(row=1, column=1, sticky=E + W)

    l_type = Label(frame, text="Type", bg="orange", fg="black", borderwidth=2, relief="solid",padx = pad_size)
    l_type.grid(row=1, column=2, sticky=E + W)

    l_price = Label(frame, text="Price", bg="orange", fg="black", borderwidth=2, relief="solid",padx = pad_size)
    l_price.grid(row=1, column=3, sticky=E + W)

    l_amount = Label(frame, text="Amount (BTC)", bg="orange", fg="black", borderwidth=2, relief="solid",padx = pad_size)
    l_amount.grid(row=1, column=4, sticky=E + W)

    l_status = Label(frame, text="Status", bg="orange", fg="black", borderwidth=2, relief="solid",padx = pad_size)
    l_status.grid(row=1, column=5, sticky=E + W)

    l_cancel = Label(frame, text="Cancel Order", bg="red", fg="black", borderwidth=2, relief="solid", padx=pad_size)
    l_cancel.grid(row=1, column=6, sticky=E + W)


    if (not  quadriga_open_orders):
        pass
    else:

        num_orders = 0 #get the total number of orders
        for open_order in quadriga_open_orders:
            num_orders = num_orders + 1

        rows = rows + num_orders #total number of rows


        row_num=2



        # get all open transactions from quadriga account
        for open_order in quadriga_open_orders:
            account = "Account User Name"
            tid = str(open_order["id"])  # order id
            datetime = str(open_order["datetime"])
            type = "sell" if open_order["type"] == 0 else "buy"
            price = str(round(float(open_order["price"]), 2))
            amount = str(round(float(open_order["amount"]), 8))  # in BTC
            status = "partially filled" if open_order["status"] == 0 else "active"  # status of order

            #Fill the table
            l_account = Label(frame, text=account, bg="white", fg="black", borderwidth=2, relief="solid", padx=pad_size)
            l_account.grid(row=row_num, column=0, sticky=E + W)

            #l_tid = Label(frame, text=tid, bg="white", fg="black", borderwidth=2, relief="solid", padx=pad_size)
            #l_tid.grid(row=row_num, column=1, sticky=E + W)

            l_datetime = Label(frame, text=datetime, bg="white", fg="black", borderwidth=2, relief="solid",
                               padx=pad_size)
            l_datetime.grid(row=row_num, column=1, sticky=E + W)

            l_type = Label(frame, text=type, bg="white", fg="black", borderwidth=2, relief="solid", padx=pad_size)
            l_type.grid(row=row_num, column=2, sticky=E + W)

            l_price = Label(frame, text=price, bg="white", fg="black", borderwidth=2, relief="solid", padx=pad_size)
            l_price.grid(row=row_num, column=3, sticky=E + W)

            l_amount = Label(frame, text=amount, bg="white", fg="black", borderwidth=2, relief="solid", padx=pad_size)
            l_amount.grid(row=row_num, column=4, sticky=E + W)

            l_status = Label(frame, text=status, bg="white", fg="black", borderwidth=2, relief="solid", padx=pad_size)
            l_status.grid(row=row_num, column=5, sticky=E + W)

            #cancelation button
            Button(frame, text="Cancel",
                   command=lambda tid=tid, datetime=datetime, price=price,
                                  amount=amount: cancel_order_dialog(tid, datetime, price, amount,master),
                   borderwidth=2,
                   relief="solid", fg="red"
                   ).grid(row=row_num, column=6, sticky=E + W)

            row_num = row_num + 1


###############  ------------ TESTING OPEN ORDERS FRAME. NOT IN USE ###############
def open_orders_frame2(master):
    #frame = VerticalScrolledFrame(master)
    #frame.pack(fill=X)

    frame = Frame(master, bg="yellow")
    frame.grid()

    for r in range(6):
        frame.rowconfigure(r, weight=1)
    for c in range(8):
        frame.columnconfigure(c, weight=1)
    l1 = Label(frame,text = "Client ")
    l1.grid(row=0,column=0,sticky=E+W)
    l2 = Label(frame, text="Deposit $ ")
    l2.grid(row=0, column=1, sticky=E + W)
    l3 = Label(frame, text="E-Transfer Fee ")
    l3.grid(row=0, column=2, sticky=E + W)
    l4 = Label(frame, text="BTC Bought ")
    l4.grid(row=0, column=3, sticky=E + W)
    l5 = Label(frame, text="BTC Sold ")
    l5.grid(row=0, column=4, sticky=E + W)
    l6 = Label(frame, text="$ Amount ")
    l6.grid(row=0, column=5, sticky=E + W)
    l7 = Label(frame, text="Profit $ ")
    l7.grid(row=0, column=6, sticky=E + W)
    l8 = Label(frame, text="Profit (BTC) ")
    l8.grid(row=0, column=7, sticky=E + W)


    if (not all_data['data']):
        print('No Data!')
        #l1 = Label(frame.interior, text='### NO OPEN ORDERS! ###', fg="black")
        #l1.pack(side=TOP, fill=X)
    else:
        for data in all_data['data']:
            this_data = all_data['data'][data]
            #print (this_data)
            client_username = this_data['client']
            amount_cad = str(this_data['deposit_amount_cad'])
            e_transfer_fee = str(max(api_calls.depositFee * float(amount_cad), 5))
            btc_bought = str(round(this_data['bitcoins_bought'],2))
            btc_sold = str(round(this_data['bitcoins_sold'],2))
            usable_dollar_amount = str(this_data['usable_dollar_amount'])
            btc_profit = str(round(this_data['btc_profit'],2))
            cad_profit = str(round(this_data['cad_profit'],2))

            l1 = Label(frame, text=client_username)
            l1.grid(row=data, column=0, sticky=E + W)
            l2 = Label(frame, text=amount_cad)
            l2.grid(row=data, column=1, sticky=E + W)
            l3 = Label(frame, text=e_transfer_fee)
            l3.grid(row=data, column=2, sticky=E + W)
            l4 = Label(frame, text=btc_bought)
            l4.grid(row=data, column=3, sticky=E + W)
            l5 = Label(frame, text=btc_sold)
            l5.grid(row=data, column=4, sticky=E + W)
            l6 = Label(frame, text=usable_dollar_amount)
            l6.grid(row=data, column=5, sticky=E + W)
            l7 = Label(frame, text=cad_profit)
            l7.grid(row=data, column=6, sticky=E + W)
            l8 = Label(frame, text=btc_profit)
            l8.grid(row=data, column=6, sticky=E + W)



        l8 = Label(master, text='Net Profit $' + str(round(all_data['net_revenue_cad'],2))
                   + ' (' + str(round(all_data['net_revenue_btc'],3)) + ' BTC)'
                   , fg="black")
        l8.pack(side=LEFT, fill=X)

def purchase_frame(master):
    global quadrigaOpenOrdersFrame
    main_frame = Frame(master,bg="yellow")
    main_frame.grid()

    for r in range(6):
        main_frame.rowconfigure(r, weight=1)
    for c in range(2):
        main_frame.columnconfigure(c, weight=1)
    l1 = Label(main_frame,text = "Total Purchase from Quadriga $")
    l1.grid(row=0,column=0,sticky=E+W)
    l2 = Entry(main_frame, text="$ ")
    l2.grid(row=0, column=1, sticky=E + W)
    l2.delete(0,END)
    l2.insert(0,str(all_data['total_purchase_amount']))

    l3 = Label(main_frame, text="Account ")
    l3.grid(row=1, column=0, sticky=E + W)
    l4 = Entry(main_frame, text=" Omar ")
    l4.grid(row=1, column=1, sticky=E + W)
    l4.delete(0,END)
    l4.insert(0, "Omar")

    l5 = Label(main_frame, text="Net Profit ")
    l5.grid(row=2, column=0, sticky=E + W)
    l6 = Entry(main_frame, text="  ")
    l6.grid(row=2, column=1, sticky=E + W)
    l6.delete(0, END)
    out = str(all_data['net_revenue_btc']) + " BTC"
    l6.insert(0, out)

    l7 = Label(main_frame, text="Buy Price $")
    l7.grid(row=3, column=0, sticky=E + W)
    l8 = Entry(main_frame, text=" $ ")
    l8.grid(row=3, column=1, sticky=E + W)
    l8.delete(0, END)
    l8.insert(0, str(quadrigaBTCPerDollar))

    l9 = Label(main_frame, text="Enter PIN ")
    l9.grid(row=4, column=0, sticky=E + W)
    l10 = Entry(main_frame, text="")
    l10.grid(row=4, column=1, sticky=E + W)
    l10.delete(0, END)
    l10.insert(0, "")


    Button(main_frame, text="Place Buy Order".format(c),
           command=lambda: buy_btc_dialog(l4.get(),
                                          l2.get(), l8.get(), l10.get(),quadrigaOpenOrdersFrame),
           ).grid(row=5, column=1, sticky=E + W)
    Button(main_frame, text="Place Sell Order".format(c),
           command=lambda: sell_btc_dialog(l4.get(),
                                          l2.get(), l8.get(), l10.get(), quadrigaOpenOrdersFrame),
           ).grid(row=6, column=1, sticky=E + W)


def market_order_frame(master):
    frame = VerticalScrolledFrame(master)
    frame.pack(fill=X)

    if (not all_data['data']):
        l1 = Label(frame.interior, text='### NO OPEN ORDERS! ###', fg="black")
        l1.pack(side=TOP, fill=X)
    else:
        for data in all_data['data']:
            this_data = all_data['data'][data]
            #print (this_data)
            client_username = this_data['client']
            amount_cad = str(this_data['deposit_amount_cad'])
            e_transfer_fee = str(max(api_calls.depositFee * float(amount_cad), 5))
            btc_bought = str(round(this_data['bitcoins_bought'],2))
            btc_sold = str(round(this_data['bitcoins_sold'],2))
            usable_dollar_amount = str(this_data['usable_dollar_amount'])
            btc_profit = str(round(this_data['btc_profit'],2))
            cad_profit = str(round(this_data['cad_profit'],2))
            l1 = Label(frame.interior, text='##########Trading with client ' + client_username
                       + ' ###########', fg="black")
            l1.pack(side=TOP, fill=X)
            l2 = Label(frame.interior, text='Deposit this much into Quadriga $' + amount_cad, fg="red")
            l2.pack(side=TOP, fill=X)
            l3 = Label(frame.interior, text='Interac E-Transfer Fee $' + e_transfer_fee, fg="red")
            l3.pack(side=TOP, fill=X)
            l4 = Label(frame.interior, text='Bitcoins Bought  ' + btc_bought
                       + ' BTC (on Quadriga @ $' + str(quadrigaBTCPerDollar), fg="red")
            l4.pack(side=TOP, fill=X)
            l5 = Label(frame.interior, text='Bitcoins Sold  ' + btc_sold
                                            + ' BTC ', fg="red")
            l5.pack(side=TOP, fill=X)
            l6 = Label(frame.interior, text='Using $  ' + usable_dollar_amount
                                            , fg="red")
            l6.pack(side=TOP, fill=X)
            l7 = Label(frame.interior, text='Profit $' + cad_profit + ' (' + btc_profit + ' BTC)'
                       , fg="red")
            l7.pack(side=TOP, fill=X)

        l8 = Label(master, text='Net Profit $' + str(round(all_data['net_revenue_cad'],2))
                   + ' (' + str(round(all_data['net_revenue_btc'],3)) + ' BTC)'
                   , fg="black")
        l8.pack(side=LEFT, fill=X)

def market_order_frame(master):
    frame = Frame(master, bg="grey")
    frame.grid()

    rows = 3  # Initially you have this many rows (Time, Title, Headers)
    cols = 6  # Fixed ((price + amount + value) x 2

    pad_size = 2
    bw = 1 # border width


    #NOTE: Assumption we have exact same number of 'bid' and 'ask' portion of open book orders selected from all open book orders
    num_open_orders = 0  # get the total number of open book orders
    for open_book_order in quadriga_portion_book_orders['bids']:
        num_open_orders = num_open_orders + 1



    for r in range(rows + num_open_orders):
        frame.rowconfigure(r, weight=1)
    for c in range(cols):
        frame.columnconfigure(c, weight=1)

    #Time when order book was retrieved
    l_buy_title = Label(frame, text="Order Book:  " + str(quadriga_portion_book_orders['dt']), borderwidth=bw,
                        relief="solid", padx=pad_size, bg="light grey")
    l_buy_title.grid(row=0, column=0, columnspan=6, rowspan=1, sticky=E + W)

    #Titles
    l_buy_title = Label(frame, text="Top  " + str(num_open_orders) +  "  Buy/Bid Orders  ", borderwidth=bw, relief="solid", padx=pad_size, bg="green")
    l_buy_title.grid(row=1, column=0, columnspan=3, rowspan=1, sticky=E + W)

    l_sell_title = Label(frame, text="Top  " + str(num_open_orders) + "  Sell/Ask Orders  ", borderwidth=bw, relief="solid", padx=pad_size, bg="red")
    l_sell_title.grid(row=1, column=3, columnspan=3, rowspan=1, sticky=E + W)

    #Headers
    l__b_header_price = Label(frame, text="Price (CAD $)", borderwidth=bw, relief="solid", padx=pad_size)
    l__b_header_price.grid(row=2, column=0, columnspan=1, rowspan=1, sticky=E + W)

    l__s_header_price = Label(frame, text="Price (CAD $)", borderwidth=bw, relief="solid", padx=pad_size)
    l__s_header_price.grid(row=2, column=3, columnspan=1, rowspan=1, sticky=E + W)

    l_b_header_amount = Label(frame, text="Amount (BTC)", borderwidth=bw, relief="solid", padx=pad_size)
    l_b_header_amount.grid(row=2, column=1, columnspan=1, rowspan=1, sticky=E + W)

    l_s_header_amount = Label(frame, text="Amount (BTC)", borderwidth=bw, relief="solid", padx=pad_size)
    l_s_header_amount.grid(row=2, column=4, columnspan=1, rowspan=1, sticky=E + W)

    l_b_header_value = Label(frame, text="Value (CAD $)", borderwidth=bw, relief="solid", padx=pad_size)
    l_b_header_value.grid(row=2, column=2, columnspan=1, rowspan=1, sticky=E + W)

    l_s_header_value = Label(frame, text="Value (CAD $)", borderwidth=bw, relief="solid", padx=pad_size)
    l_s_header_value.grid(row=2, column=5, columnspan=1, rowspan=1, sticky=E + W)

    # start from this row (we had Time+Title+Header)
    row_num = 3
    #Note: Assumption size of 'bids' and 'asks' is same in the 'quadriga_portion_book_orders'
    #Get 'bids' and 'asks'
    bids = quadriga_portion_book_orders['bids']
    asks = quadriga_portion_book_orders['asks']
    for i in range(num_open_orders):

        #Buy order
        buy_book_order = bids[i]

        price_b = round(float(buy_book_order[0]),2)
        amount_b = float(buy_book_order[1])
        value_b = round(price_b * amount_b,2)

        l = Label(frame, text=str(price_b), bg="white", fg="black", borderwidth=2, relief="solid",
                  padx=pad_size)
        l.grid(row=row_num, column=0, sticky=E + W)

        l = Label(frame, text=str(amount_b), bg="white", fg="black", borderwidth=2, relief="solid",
                  padx=pad_size)
        l.grid(row=row_num, column=1, sticky=E + W)

        l = Label(frame, text=str(value_b), bg="white", fg="black", borderwidth=2, relief="solid",
                  padx=pad_size)
        l.grid(row=row_num, column=2, sticky=E + W)



        #Sell order
        sell_book_order = asks[i]

        price_s = round(float(sell_book_order[0]),2)
        amount_s = float(sell_book_order[1])
        value_s = round(price_s * amount_s,2)

        l = Label(frame, text=str(price_s), bg="white", fg="black", borderwidth=2, relief="solid",
                  padx=pad_size)
        l.grid(row=row_num, column=3, sticky=E + W)

        l = Label(frame, text=str(amount_s), bg="white", fg="black", borderwidth=2, relief="solid",
                  padx=pad_size)
        l.grid(row=row_num, column=4, sticky=E + W)

        l = Label(frame, text=str(value_s), bg="white", fg="black", borderwidth=2, relief="solid",
                  padx=pad_size)
        l.grid(row=row_num, column=5, sticky=E + W)

        row_num = row_num + 1


def main_prog_frame(master):
       global quadrigaOpenOrdersFrame
       master.grid()
       master.title("Grid Manager")
       for r in range(6):
              master.rowconfigure(r, weight=1)
       for c in range(5):
              master.columnconfigure(c, weight=1)

       Button(master, text="Refresh".format(c),
              command=refresh_network_data_dialog,
              ).grid(row=6, column=c, sticky=E + W)


       # LEFT SUMMARY FRAME (3x2)
       summary_frame = Frame(master, bg="red")
       summary_frame.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
       account_summary_frame(summary_frame)

       # LBTC OPEN ORDERS FRAME (3x3)
       lbtcOpenOrdersFrame = Frame(master, bg="green")
       lbtcOpenOrdersFrame.grid(row = 0, column = 2, rowspan = 1, columnspan = 3, sticky = W+E+N+S)
       lbtc_open_orders_frame(lbtcOpenOrdersFrame)

       # Quadriga OPEN ORDERS FRAME (3x3)
       quadrigaOpenOrdersFrame = Frame(master, bg="purple")
       quadrigaOpenOrdersFrame.grid(row=1, column=2, rowspan=2, columnspan=3, sticky=W + E + N + S)
       quadriga_open_orders_frame(quadrigaOpenOrdersFrame)






       # PURCHASE SUMMARY FRAME (3x3)
       PurchaseSummaryFrame = Frame(master, bg="yellow")
       PurchaseSummaryFrame.grid(row=3, column=2, rowspan=3, columnspan=3, sticky=W + E + N + S)
       purchase_frame(PurchaseSummaryFrame)

       # Market Order FRAME  (3x2)
       MarketOrderFrame = Frame(master, bg="blue")
       MarketOrderFrame.grid(row=3, column=0, rowspan=3, columnspan=2, sticky=W + E + N + S)
       market_order_frame(MarketOrderFrame)


       # TODO: Output profit to text file (comma delimitted)
       # TODO: List last few trades from Quadriga.
       # account_name, amount_cad, btc_price, profit, date
       # TODO: List the daily, weekly, monthly E-Transfer
       # TODO: Ensure network data is loaded before calling the main frame as it crashes otherwise.


# Global variables
global quadrigaData,quadrigaBTCPerDollar, lbtc_balance, all_data, \
    balance,lbtc_sending_address,\
    quadriga_open_orders
refresh_network_data()
root = Tk()
main_prog_frame(root)
root.mainloop()
