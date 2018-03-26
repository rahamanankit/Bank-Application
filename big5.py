import getpass
import cx_Oracle
con=cx_Oracle.connect('ankit123/ankit')
cur=con.cursor()
def check_user(email,password):
    cur.execute("SELECT EMAIL_ID FROM REGISTRATION")
    for i in cur.fetchall():
        if email in i:
            cur.execute("SELECT PASSWORD FROM REGISTRATION")
            for j in cur.fetchall():
                if password in j:
                    return True
            
def check_admin(email1,password1):
    cur.execute("SELECT EMAIL_ID,PASSWORD FROM NEW_ADMIN")
    for i in cur.fetchall():
        if email1 in i:
            cur.execute("SELECT PASSWORD FROM NEW_ADMIN")
            for j in cur.fetchall():
                if password1 in j:
                    return True 
            
def address_update(email,address):
    cur.execute("update registration set address='%s' where email_id='%s'"%(address,email))
    cur.execute("select address from registration where email_id='%s'"%(email))
    print("Your address has been updated to")
    for i in cur.fetchall():
        print(i[0])
    
        
def savings_account(custid,ac_no,bal):
    cur.execute("INSERT INTO NEW_USER VALUES('%d','%d','%f')"%(custid,ac_no,bal))
    
def current_account(custid,ac_no,bal):
    cur.execute("INSERT INTO NEW_USER1 VALUES('%d','%d','%f')"%(custid,ac_no,bal))

def fixed_account(custid,ac_no,t,bal):
    cur.execute("INSERT INTO FIXED_DEPOSIT VALUES('%d','%d','%d','%f')"%(custid,ac_no,t,bal))

def display_fd(ac_no):
    from tabulate import tabulate
    cur.execute("SELECT * FROM FIXED_DEPOSIT WHERE ACCOUNT_NUMBER='%d'"%(ac_no))
    print(tabulate(cur.fetchall(),headers=['CUSTOMER ID','ACCOUNT NUMBER','TERM','ACCOUNT_BALANCE']))
    
def deposit_account(ac_no,amt):
    cur.execute("UPDATE NEW_USER SET ACCOUNT_BALANCE = ACCOUNT_BALANCE + '%d' WHERE ACCOUNT_NUMBER = '%d'"%(amt,ac_no))
    cur.execute("INSERT INTO TRANSACTIONS VALUES ('%d',(SELECT SYSDATE FROM DUAL),'%s','%d',(SELECT ACCOUNT_BALANCE FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'))"%(ac_no,'CREDIT',amt,ac_no))
    cur.execute("SELECT ACCOUNT_BALANCE FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'"%(ac_no))
    for i in cur.fetchall():
        return(i[0])
        
def withdraw_account(ac_no,amt):
    cur.execute("UPDATE NEW_USER SET ACCOUNT_BALANCE = ACCOUNT_BALANCE - '%d' WHERE ACCOUNT_NUMBER = '%d'"%(amt,ac_no))
    cur.execute("INSERT INTO TRANSACTIONS VALUES ('%d',(SELECT SYSDATE FROM DUAL),'%s','%d',(SELECT ACCOUNT_BALANCE FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'))"%(ac_no,'DEBIT',amt,ac_no))
    cur.execute("SELECT ACCOUNT_BALANCE FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'"%(ac_no))
    for i in cur.fetchall():
        return(i[0])
        
def minimum_balance(ac_no):
    cur.execute("SELECT ACCOUNT_BALANCE FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'"%(ac_no))
    for i in cur.fetchall():
        return (i[0])
    
def close_account(ac_no):
    cur.execute("DELETE FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'"%(ac_no))
    
def print_detail(ac_no):
    from tabulate import tabulate
    cur.execute("SELECT * FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'"%(ac_no))
    print(tabulate(cur.fetchall(),headers=['Customer ID','Account Number','Account Balance']))
            
def transfer_closed_account(ac_no):
    cur.execute("INSERT INTO CLOSED_ACCOUNTS (CUST_ID,ACCOUNT_NUMBER,ACCOUNT_BALANCE) SELECT CUST_ID,ACCOUNT_NUMBER,ACCOUNT_BALANCE FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'"%(ac_no))
    cur.execute("UPDATE CLOSED_ACCOUNTS SET DATE_CLOSED=(SELECT SYSDATE FROM DUAL) WHERE ACCOUNT_NUMBER='%d'"%(ac_no))
        
def display_closed_accounts():
    from tabulate import tabulate
    cur.execute("SELECT * FROM CLOSED_ACCOUNTS")
    print(tabulate(cur.fetchall(),headers=['Customer ID', 'Account Number','Account Balance','Date closed']))

def transfer_money(ac_no1,ac_no2,amt1):
    cur.execute("UPDATE NEW_USER SET ACCOUNT_BALANCE = ACCOUNT_BALANCE - '%d' WHERE ACCOUNT_NUMBER = '%d'"%(amt1,ac_no1))
    cur.execute("UPDATE NEW_USER SET ACCOUNT_BALANCE = ACCOUNT_BALANCE + '%d' WHERE ACCOUNT_NUMBER = '%d'"%(amt1,ac_no2))
 
def transferrer(ac_no1):
    cur.execute("SELECT ACCOUNT_BALANCE FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'"%(ac_no1))
    for i in cur.fetchall():
        print("Account balance from which funds are send is =",i[0])
        
def transferred(ac_no2):
    cur.execute("SELECT ACCOUNT_BALANCE FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'"%(ac_no2))
    for i in cur.fetchall():
        print("Account balance to which funds are send is =",i[0])
        
def print_statement(ac_no,day1,day2):
    from tabulate import tabulate
    cur.execute("SELECT DATE_OF_TRANSACTION,TRANSACTION_TYPE,AMOUNT,ACCOUNT_BALANCE FROM TRANSACTIONS WHERE ACCOUNT_NUMBER='%d' AND TO_CHAR(DATE_OF_TRANSACTION,'YYYY-MM-DD')>='%s' AND TO_CHAR(DATE_OF_TRANSACTION,'YYYY-MM-DD')<='%s' "%(ac_no,day1,day2))
    print(tabulate(cur.fetchall(),headers=['DATE OF TRANSACTION','TRANSACTION TYPE','AMOUNT','BALANCE']))    

def display(ac_no):
    cur.execute("SELECT ACCOUNT_BALANCE FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'"%(ac_no))
    for i in cur.fetchall():
        return(i[0])
   
def loan(cust_id,ac_no,l_amt,terms):
          cur.execute("INSERT INTO LOAN VALUES('%d','%d','%d','%d')"%(cust_id,ac_no,l_amt,terms))
       
def display_loan(ac_no):
    from tabulate import tabulate
    cur.execute("SELECT * FROM LOAN WHERE ACCOUNT_NUMBER='%d'"%(ac_no))
    print(tabulate(cur.fetchall(),headers=['CUSTOMER ID','ACCOUNT NUMBER','LOAN_AMOUNT','REPAYMENT TERMS']))

def validate_loan(ac_no):
    cur.execute("SELECT ACCOUNT_BALANCE FROM NEW_USER WHERE ACCOUNT_NUMBER='%d'"%(ac_no))
    for i in cur.fetchall():
        return(i[0])
        
def fd_report(cust_id):
    from tabulate import tabulate
    cur.execute("SELECT ACCOUNT_NUMBER,TERM,ACCOUNT_BALANCE FROM FIXED_DEPOSIT WHERE CUST_ID='%d'"%(cust_id))    
    print(tabulate(cur.fetchall(),headers=['ACCOUNT_NUMBER','TERM','ACCOUNT_BALANCE']))

def fd_3(cust_id):
    from tabulate import tabulate
    cur.execute("SELECT * FROM FIXED_DEPOSIT WHERE ACCOUNT_BALANCE>=(SELECT SUM(ACCOUNT_BALANCE) FROM FIXED_DEPOSIT WHERE CUST_ID='%d')"%(cust_id))    
    print(tabulate(cur.fetchall(),headers=['CUSTOMER ID','ACCOUNT_NUMBER','TERM','ACCOUNT_BALANCE']))
 
def fd_4(amt):
    from tabulate import tabulate
    cur.execute("SELECT * FROM FIXED_DEPOSIT WHERE ACCOUNT_BALANCE>'%d'"%(amt))    
    print(tabulate(cur.fetchall(),headers=['CUSTOMER ID','ACCOUNT_NUMBER','TERM','ACCOUNT_BALANCE']))

def loan_report(cust_id):
    from tabulate import tabulate
    cur.execute("SELECT ACCOUNT_NUMBER,LOAN_AMOUNT,REPAYMENT_TERM FROM LOAN WHERE CUST_ID='%d'"%(cust_id))    
    print(tabulate(cur.fetchall(),headers=['LOAN_ACCOUNT_NUMBER','LOAN_AMOUNT','REPAYMENT_TERM']))
    
def loan_3(cust_id):
    from tabulate import tabulate
    cur.execute("SELECT * FROM LOAN WHERE LOAN_AMOUNT >= (SELECT SUM(LOAN_AMOUNT) FROM LOAN WHERE CUST_ID='%d')"%(cust_id))    
    print(tabulate(cur.fetchall(),headers=['CUSTOMER ID','LOAN_ACCOUNT_NUMBER','LOAN_AMOUNT','REPAYMENT_TERM']))
    
def loan_4(amt):
    from tabulate import tabulate
    cur.execute("SELECT * FROM LOAN WHERE LOAN_AMOUNT > '%d'"%(amt))    
    print(tabulate(cur.fetchall(),headers=['CUSTOMER ID','LOAN_ACCOUNT_NUMBER','LOAN_AMOUNT','REPAYMENT_TERM']))

flag = False
flag1 = False
choice = int(input("Press 1 to Sign Up \nPress 2 for Sign In \nPress 3 for admin login \nPress 0 to quit the application\n"))
if choice == 1:
    c = input("Enter Your Email_ID:")
    d = getpass.getpass("Enter Your 6 digit password:")
    flag = check_user(c,d)
    if (flag == True):
        print("Please sign in")
    else:
        print("Your account doesn't exist..Create an account")
        act_no = input("Enter your preferrable 4-8 digit account no:")
        name = input("Enter Your Name:")
        c_no = input("Enter Your 10 digit Contact Number:")
        address = input("Enter your address:")
        if (len(act_no) > 3 & len(act_no) < 9):
            if len(c_no) == 10:
                if len(d) == 6 :
                    cur.execute("INSERT INTO Registration VALUES('%d','%s','%d','%s','%s','%s')"%(int(act_no),name,int(c_no),c,d,address))
                    print("Your account has been created")
                else:
                    print("Your password is not in range")
            else:
                print("Your contact number is not in range")
        else:
            print("Your account number is not in range")
        
elif choice == 2:
        c = input("Enter your email id to sign in:")
        d = getpass.getpass("Enter your password:")
        flag = check_user(c,d)
        if (flag == True):
            print("You are signed in")
            choice2 = input("Press 1 to update address\nPress 2 to open a new account\nPress 3 to deposit money\nPress 4 to withdraw money\nPress 5 to print bank account statement\nPress 6 to transfer money\nPress 7 to close your account\nPress 8 to avail loan\nPress 9 to logout\n")                               
            if (choice2 == '1'):
                address_new = input("Enter your new address:")
                address_update(c,address_new)
            elif (choice2 == '2'):
                choice3 = input("Enter the type of account you want to open:\nSavings\nCurrent\nFD\n")
                act_no = int(input("Enter your account no:"))
                cust_id = int(input("Enter your customer id:"))
                balance = float(input("Enter the amount:"))
                if (choice3 == 'savings'):
                    cur.execute("Select account_number from registration")
                    for i in cur.fetchall():
                        if act_no in i:
                            savings_account(cust_id,act_no,balance)  
                            print("You have successfully opened a savings account!!")
                elif (choice3 == 'current'):
                    cur.execute("Select account_number from registration")
                    for i in cur.fetchall():
                        if act_no in i:
                            if (balance >= 5000):
                                current_account(cust_id,act_no,balance)  
                                print("You have successfully opened a current account!!")
                        else:
                            print("Not enough funds to open a current account")
                elif (choice3 == 'FD'):
                    term = int(input("Enter the number of months:"))
                    cur.execute("Select account_number from registration")
                    for i in cur.fetchall():
                        if act_no in i:
                            if (balance >= 1000 and balance % 1000 == 0 and term >= 12): 
                                fixed_account(cust_id,act_no,term,balance)  
                                print("You have successfully opened a fixed deposit account!!")
                                display_fd(act_no)
                            else:
                                print("You do not meet the criteria to open a FD Account")
            elif (choice2 == '3'):
                act_no = int(input("Enter your account no:"))
                l = display(act_no)
                print("Your current account balance is : ₹",l)
                amount = int(input("Enter the amount to be deposited:₹"));
                cur.execute("Select account_number from registration")
                for i in cur.fetchall():
                    if act_no in i:
                        if amount > 0:
                            u = deposit_account(act_no,amount)
                            print("Your updated account balance is = ₹",u)
                        else:
                            print("Please enter a valid amount")
            elif (choice2 == '4'):
                act_no = int(input("Enter your account no:"))
                l = display(act_no)
                print("Your current account balance is : ₹",l)
                amount = int(input("Enter the amount to be withdrawn:₹"));
                cur.execute("Select account_number from registration")
                for i in cur.fetchall():
                    if act_no in i:
                        k = minimum_balance(act_no)
                        if amount < k:
                            v = withdraw_account(act_no,amount)
                            print("Your updated account balance is = ₹",v)
                        else:
                            print("You don't have enough balance to withdraw")
            elif (choice2 == '5'):
                act_no = int(input("Enter your account no:"))
                date_from = input("Enter start date in YYYY-MM-DD Format:")
                date_to = input("Enter end date in YYYY-MM-DD Format:")
                print_statement(act_no,date_from,date_to)
                
            elif (choice2 == '6'):
                act_no1 = int(input("Enter your account no:"))
                act_no2 = int(input("enter the account no of the person whom you want to transfer:"))
                amount1 = int(input("Enter the amount to transfer:"))
                cur.execute("SELECT ACCOUNT_NUMBER FROM REGISTRATION")
                for i in cur.fetchall():
                    if act_no1 in i:
                        cur.execute("SELECT ACCOUNT_NUMBER FROM REGISTRATION")
                        for j in cur.fetchall():
                            if act_no2 in j:
                                transfer_money(act_no1,act_no2,amount1)
                                transferrer(act_no1)
                                transferred(act_no2)
                                
            elif (choice2 == '7'):
                act_no = int(input("Enter the account no that you want to close:"))
                print_detail(act_no)
                transfer_closed_account(act_no)
                close_account(act_no)
                print("Your bank account has been closed")
            
            elif (choice2 == '8'):
                loan_amt = int(input("Enter the loan amount:"))
                c_id = int(input("Enter your customer id:"))
                term = int(input("Enter the repayment term:"))
                act_no = int(input("Enter your account no:"))
                cur.execute("SELECT ACCOUNT_NUMBER FROM REGISTRATION")
                for i in cur.fetchall():
                    if act_no in i:
                        k = validate_loan(act_no)
                        if (loan_amt > 0 and loan_amt % 1000 == 0 and loan_amt <= (2 * k) and term > 0):
                            loan(c_id,act_no,loan_amt,term)
                            display_loan(act_no)
                        else:
                            print("You are not eligible for a loan")
                            
            elif (choice2 == '9'):
                print("You have been logged out")
            else:
                print("Sorry Wrong Choice")
        else:
            print("Incorrect credentials")
                     
elif choice == 3:
        a = input("Enter your admin login id:")
        b = getpass.getpass("Enter your password:")
        flag1 = check_admin(a,b)
        if (flag1 == True):
            print("You are signed in")
            choice1 = int(input("Press 1 to print closed account history\nPress 2 for FD report of a customer\nPress 3 for FD Report of Customers vis-à-vis another Customer\nPress 4 for FD Report of Customers w.r.t a particular FD Amount\nPress 5 for Loan Report of a Customer\nPress 6 for Loan Report of Customers vis-à-vis another Customer\nPress 7 for Loan Report of Customers w.r.t a particular Loan Amount\nPress 8 for Report of Customers who are yet to avail a loan\nPress 9 for Report of Customers who are yet to open a FD account\nPress 0 to Logout\n"))
            if (choice1 == 1):
                display_closed_accounts()
            elif (choice1 == 2):
                c_id = int(input("Enter the customer id:"))
                fd_report(c_id)
            elif (choice1 == 3):
                c_id = int(input("Enter the customer id:"))
                fd_3(c_id)
            elif (choice1 == 4):
                amount =int(input("Enter the amount:"))
                if (amount > 0 and amount % 1000 == 0):
                    fd_4(amount)
                else:
                    print("Not Applicable")
            elif (choice1 == 5):
                c_id = int(input("Enter the customer id:"))
                loan_report(c_id)
            elif (choice1 == 6):
                c_id = int(input("Enter the customer id:"))
                loan_3(c_id)
            elif (choice1 == 7):
                amount =int(input("Enter the amount:"))
                if (amount > 0 and amount % 1000 == 0):
                    loan_4(amount)
            elif (choice1 == 8):
                from tabulate import tabulate
                cur.execute("select registration.account_number,registration.full_name from registration full outer join loan on registration.account_number=loan.account_number where loan.account_number is null")
                print(tabulate(cur.fetchall(),['ACCOUNT_NUMBER','FULL_NAME']))
            elif (choice1 == 9):
                from tabulate import tabulate
                cur.execute("select registration.account_number,registration.full_name from registration full outer join fixed_deposit on registration.account_number=fixed_deposit.account_number where fixed_deposit.account_number is null")
                print(tabulate(cur.fetchall(),['ACCOUNT_NUMBER','FULL_NAME']))
            elif (choice1 == 0):
                print("You have been logged out")
        else:
            print("You are not an admin")
        
            
elif choice == 0:
        print("Quitting the application")
        
con.commit()
con.close()