import os#information about library and syntax for clearing screen from https://www.geeksforgeeks.org/clear-screen-python/
import pickle#syntax, method for reading and writing objects from a file, information about library from
#https://cbse.nic.in/ePub/webcbse/webcbse/Computer%20Science%20with%20Python%20(Class-XII)/index.html

class savings_account:#class that generates objects that represent savings accounts
    interestrate=0.06#constant for all onjects
    def __init__(self,no):#constructor
            print("Enter the Following Details: ")
            self.account_holder=input("Account Holder: ")
            self.amount_held=int(input("Initial Deposit Amount: "))
            self.accountid="sacc"+str(no)
    def deposit(self):#deposits money into account
        x=int(input("Enter amount: "))
        self.amount_held+=x
        return self.amount_held
    def withdraw(self):#withdraws money from account, prints error message if there isn't enough money in the account
        x=int(input("Enter amount: "))
        if(x>self.amount_held):
            print("Denied, not enough money in account.")
            return False
        else:
            self.amount_held-=x
            return self.amount_held
    def display(self):# displays details of account
        print("Account Holder:",self.account_holder)
        print("Account ID:",self.accountid)
        print("Balance:",self.amount_held)
    def increment(self,t):#calculates total amount in account after applying interest (simple interest formula)
        if (t>0):
            self.amount_held+=(self.amount_held)*(self.interestrate)*(t/12)
        return self.amount_held

class checking_account(savings_account):#class that generates objects that represent checking accounts
#this class is inheriting from savings accounts as some member functions (like deposit and withdraw) are common
    interestrate=0.04
    def __init__(self,no):#constructor
            print("Enter the Following Details: ")
            self.account_holder=input("Account Holder: ")
            self.amount_held=int(input("Initial Deposit Amount: "))
            self.accountid="cacc"+str(no)
class CD(savings_account):#class that generates objects that represent CD accounts
#this class is inheriting from savings accounts as some member functions (like deposit and display) are common
    interestrate=0.08
    def __init__(self,no):#constructor
            print("Enter the Following Details: ")
            self.account_holder=input("Account Holder: ")
            self.holding_duration=int(input("Holding Duration (in months): "))
            self.amount_held=int(input("Initial Deposit Amount: "))
            self.accountid="CD"+str(no)
    def withdraw(self):#withdraws from account, but prints a warning if it's before the holding duration has elapsed
        if self.amount_held==0:
            self.amount_held=False
            print("Account Empty")
        else:
            t=int(input("How long has it been since the account was opened? (in months) "))
            if (t<self.holding_duration):
                ans=input("Holding duration has not elapsed yet. Are you sure you want to withdraw anyway? (Answering 'yes' will incur a fine) ")
                if ("ES" in ans or "es" in ans):
                    self.amount_held=self.amount_held//12
                else:
                    self.amount_held=False
            else:
                self.amount_held=0
        return self.amount_held #the return value is 1 so that the value of amount_held gets updated in the file outside the function
    def display(self):# displays details of account
        print("Account Holder:",self.account_holder)
        print("Account ID:",self.accountid)
        print("Balance:",self.amount_held)
        print("Holding Duration:",self.holding_duration//12,"year(s)",self.holding_duration%12,"month(s)")


class joint_account(savings_account):#class that generates objects that represent joint accounts
#this class is inheriting from savings accounts as some functionalities (like deposit and withdraw) are common
    interestrate=0.06
    def __init__(self,no):#constructor
            print("Enter the Following Details: ")
            self.prim_acc_holder=input("Primary Account Holder: ")
            self.sec_acc_holder=input("Secondary Account Holder: ")
            self.amount_held=int(input("Initial Deposit Amount: "))
            self.accountid="jacc"+str(no)
    def display(self):#displays details of account - is different because this type of account has two holders
        print("Primary Account Holder:",self.prim_acc_holder)
        print("Secondary Account Holder:", self.sec_acc_holder)
        print("Account ID:",self.accountid)
        print("Balance:",self.amount_held)
class loanprofile:# Creates objects that are stored in a file to help record loans given out by the bank. These objects can be thought of as "loan accounts"
    interestrate=0.05
    def __init__(self,name):
        self.credit_score=0
        self.debt=0
        self.name=name
    def increment(self,t):#Increments debt by applying interest. Time is decided by the amount of time after which the user visits the bank
        if (t>0):
            self.debt+=(self.debt)*(self.interestrate)*(t)
        return self.debt
    def display(self):
        print("Name:",self.name)
        print("Credit Score:",self.credit_score)
        print("Debt:",self.debt)
def loan():#Goes through process to take out loan:
    needtowrite=False
    name=input("Enter Name: ")#Asks for name to check whether the user has already taken out a loan, and to make a new "loan account" if they haven't
    file=open("loan.dat","rb+")#opens file with "loan" accounts
    flag=True
    try:
        while True:
            pos=file.tell()
            d=pickle.load(file)
            if d.name==name:#user has taken out a loan, new debt will be added to their "loan account"
                debt=d
                flag=False
                break
    except (EOFError,pickle.UnpicklingError):#handles error that occurs when end of file is reached
        pass
    if flag:
        debt=loanprofile(name)
    debt.credit_score=0
    f=open("accounts.dat","rb+")
    try:
        while True:
            ac=pickle.load(f)
            if(ac.account_holder==name):
                debt.credit_score+=1
    except (EOFError,pickle.UnpicklingError):
        pass
    f.close()
    amount=int(input("Requested Loan Amount: "))
    #for approval for loan amounts above 10,000 credit score should be>=2, else creditscore>=1
    if debt.credit_score>=2 and amount>=10000:
        debt.debt+=amount
        print("Loan Approved!")
    elif debt.credit_score>=1 and amount<10000:
        debt.debt+=amount
        print("Loan Approved!")
    else:
        print("Loan Not Approved.")
    if flag:
        file.seek(pos)
    pickle.dump(debt,file)
    file.close()


def counting(x):#counts the number of existing accounts of a particular type then returns the (count)+1 to be used to generate unique account IDs
    try:
        f=open("accounts.dat","rb")#opens file with data of all accounts
    except:
        return 1
    try:
        c=1
        lis=[]
        while True:
            ac=pickle.load(f)
            if ac is not None:
                if ac.accountid.startswith("s") and x==1:
                    lis.append(int(ac.accountid[4:]))
                elif ac.accountid.startswith("c") and x==2:
                    lis.append(int(ac.accountid[4:]))
                elif ac.accountid.startswith("CD") and x==3:
                    lis.append(int(ac.accountid[2:]))
                elif ac.accountid.startswith("j") and x==4:
                    lis.append(int(ac.accountid[4:]))
    except (EOFError, pickle.UnpicklingError):
        pass
    f.close()
    try:
        return c+max(lis)
    except:
        return c

def modify(nac,accid): # to modify/ update account information in the file
    f=open("accounts.dat","rb+")#opens file with data of all accounts
    try:
        while True:
            pos=f.tell()#records position of start of object
            ac=pickle.load(f)#reads object from file
            if (ac.accountid)==accid:
                f.seek(pos)#moves to start position of object in file
                pickle.dump(nac,f)#overwrites object with updated information
                break#breaks after modifying correct object
    except (EOFError,pickle.UnpicklingError):#handles error when end of file is reached
        pass
    f.close()#closes file

def show(name):# displays details of all accounts held by user
    f=open("accounts.dat","rb+")
    file=open("loan.dat","ab+")
    #this value is used to calculate interest (both on deposited money and loans held) and update the amount accordingly in the file
    t=int(input("How long has it been since your last visit?(Enter your answer in months) "))
    print("\n")
    print("Accounts:\n")
    a=0
    try:
        while True:#searching for accounts held by user
            ac=pickle.load(f)
            try:
                if (ac.account_holder==name):
                    a+=1
                    if not ac.accountid.startswith("j"):
                        #updating amount according to interest
                        ac.amount_held=ac.increment(t)
                        modify(ac,ac.accountid)
                        #displaying account details
                        ac.display()
                        print("\n")
                    else:#separate case for joint accounts to check if user is a primary account holder or a secondary account holder
                        if (ac.prim_acc_holder)==name or (ac.sec_acc_holder)==name:
                            ac.amount_held=ac.increment(t)
                            modify(ac,ac.accountid)
                            ac.display()
                            print("\n")
            except:
                pass

    except (EOFError,pickle.UnpicklingError):#handles error when end of file is reached and UnpicklingError
        pass
    if a==0:
        print("NA\n")
    print("Loans:\n")
    l=0
    try:
        while True:
            loanobj=pickle.load(file)
            pos=file.tell()
            if loanobj.name==name:
                l+=1
                loanobj.debt=loanobj.increment(t)#incrementing amount owed by user to bank
                loanobj.display()
                print("\n")
    except EOFError:#handles error when end of file is reached
        pass
    if l==0:
        print("NA\n")
    else:
        file.seek(pos)
        pickle.dump(loanobj,file)
    f.close()
    file.close()

def close_account(accid): # to close an account - it does this by deleting the appropriate object from the file
    f=open("accounts.dat","rb+")#opens file with data of all accounts
    file=open("temp.dat","wb+")
    try:
        while True:
            ac=pickle.load(f)#reads object from file
            if (ac.accountid!=accid):
                pickle.dump(ac,file)#overwrites data held by object with "None" i.e., erases it
                break#breaks after deleting the appropriate objects
    except (EOFError,pickle.UnpicklingError):#handles error when end of file is reached
        pass
    f.close()
    file.close()
    os.remove("accounts.dat")
    os.rename("temp.dat","accounts.dat")

def create_account(x): # to create an account
    accno=counting(x)#generating ID
    if (x==1):
        ac=savings_account(accno)
    elif(x==2):
        ac=checking_account(accno)
    elif(x==3):
        ac=CD(accno)
    elif(x==4):
        ac=joint_account(accno)
    f=open("accounts.dat","ab")#opening file with accounts
    pickle.dump(ac,f)# storing new account info in the file
    f.close()#close file with accounts

def cheque():# to deposit a cheque
    yaccid=input("Enter account ID of payee: ")#accept user's account ID
    oaccid=input("Enter account ID of payer: ")#enter account id of person that wrote the cheque
    if oaccid.accountid.startswith("CD"):
        print("Cheques from CD accounts cannot be deposited.")
        return None
    f=open("accounts.dat","rb+")
    try:
        flag=0
        while True:
            ac=pickle.load(f)
            if (ac is not None) and ac.accountid==yaccid:
                yac=ac#retrieving user account ("your" account)
            if (ac is not None)and ac.accountid==oaccid:
                flag=1
                oac=ac#retrieving account of person who wrote the cheque("other" account)
    except (EOFError,pickle.UnpicklingError):#handles error when end of file is reached
        pass
    if (flag==1):#if person's account id is in the accounts file, withdraw from their account, deposit in user's account
        temp=oac.amount_held
        oac.amount_held=oac.withdraw()
        if not oac.amount_held:
            return None
        else:
            yac.amount_held+=(temp-oac.amount_held)
            modify(oac,oaccid)
            modify(yac,yaccid)
            print("Cheque Deposited Successfully")
    else:#if person's account id not in file, deposit in user's account
        yac.amount_held=yac.deposit()
        modify(yac,yaccid)
        print("Cheque Deposited Successfully")
    f.close()

def transfer():#to transfer money to another account
    yaccid=input("Enter your account ID: ")#enter user's account id
    if yaccid.accountid.startswith("CD"):
        print("Tranfers cannot be made from CD accounts.")
        return None
    oaccid=input("Enter account ID that money has to be transfered to: ")#enter account id of person user wants to transfer money to
    f=open("accounts.dat","rb+")
    try:
        flag=0
        while True:
            ac=pickle.load(f)
            if ac is not None:
                if ac.accountid==yaccid:
                    yac=ac #retrieving account of user ("your" account)
                if ac.accountid==oaccid:
                    flag=1
                    oac=ac#retrieving account that money is being transfered to ("other" account)
    except (EOFError,pickle.UnpicklingError):#handles error when end of file is reached
        pass
    if (flag==1):#if person's account id is in the accounts file, withdraw from user's account, deposit in theirs
        temp=yac.amount_held
        yac.amount_held=yac.withdraw()
        if not yac.amount_held:
            print("Transaction Unsuccessful")
            return None
        else:
            oac.amount_held+=(temp-yac.amount_held)
            modify(oac,oaccid)
            modify(yac,yaccid)
            print("Transaction Successful!")
    else:#if person's account id is not in the accounts file, withdraw from user account
        yac.amount_held=yac.withdraw()
        if yac.amount_held:
            modify(yac,yaccid)
            print("Transaction Successful!")
    f.close()

def payloan():#to pay back loans
    accno=input("Enter account ID: ")#choose account
    file=open("accounts.dat","ab+")#opens file with account data
    f=open("loan.dat","ab+")#opens file with "loan" accounts
    try:
        flag=True
        while True:
            a=pickle.load(file)#reads object from file
            pos1=file.tell()#position of account object
            if (a.accountid)==accno:
                    flag=False
                    if not (a.accountid.startwith(j)):
                        ac=a
                        name=ac.account_holder
                        ac.display()
                        print("\n")
                    else:
                        ac=a
                        p_or_s=input("Primary Account Holder or Secondary Account Holder? (p/s) ")
                        if(p_or_s)=="p":
                            name=ac.prim_acc_holder
                            ac.display()
                            print("\n")
                        if(p_or_s)=="s":
                            name=ac.sec_acc_holder
                            ac.display()
                            print("\n")
                    break
    except (EOFError,pickle.UnpicklingError):#handles error when end of file is reached
        pass
    if flag:
        print("Account does not exist.")
        return None
    try:
        flag2=True
        while True:
            d=pickle.load(f)#reads a loan object from the file
            pos2=f.tell()#position of loan object
            if(d.name)==name:
                flag2=False
                loanobj=d
                break
    except (EOFError,pickle.UnpicklingError):#handles error when end of file is reached
        pass
    if flag2:
        print("No loan has been taken out in this name.")
        return None
    amount=int(input("Enter Amount: "))#specify amount to be paid to bank
    #to take care of accidental overpaying by user
    if amount>loanobj.debt:
        amount=loanobj.debt
    #subtract amount from debt, withdraw from accounts
    ac.amount_held=ac.withdraw()
    if ac.amount_held:
        loanobj.debt-=amount
        file.seek(pos1)
        pickle.dump(ac)
        f.seek(pos2)
        pickle.dump(loanobj)
    file.close()
    f.close()

def creation():#function creates a menu that displays the different types of accounts a user can open and allows them to do that
        while True:
            print("What kind of account do you want to open?")
            print("1. Savings Account")
            print("2. Checking Account")
            print("3. CD Account")
            print("4. Joint Account")
            print("5. Recommendations")
            try:
                x=int(input())
            except:
                _=os.system("cls")
                continue
            if(x==5):
                _=os.system("cls")
                f=open("Recommendations.txt","r")#reads from file with information about different accounts
                whole=f.read()
                print(whole)
                f.close()
                y=input("Ok? ")
                if ("ES" in y or "es" in y):#not including the "y" removes extra checking for variations like "Yes" and "yes"
                    _=os.system("cls")
                    continue
            else:
                create_account(x)
                break

def continuation():#to ask the user if they wish to continue operations on the account
    y=input("Do you wish to continue?(yes/no)")
    if (y=="yes"):
        main()
    else:
        _=os.system("cls")
        print("Have a Nice Day!")
        exit()

def transaction(ac,accid,option):#to carry out transactions (deposit/withdraw) on bank accounts
    if (option==1):
        ac.deposit()
        modify(ac,accid)
        print("Deposit successful.\nCurrent Balance:",ac.amount_held)
    elif (option==2):
        ac.amount_held=ac.withdraw()
        if (ac.amount_held==0):
            print("Withdraw successful.\nCurrent Balance:",ac.amount_held)
            modify(ac,accid)
        elif(ac.amount_held):
            print("Withdraw successful.\nCurrent Balance:",ac.amount_held)
            modify(ac,accid)

def accessing():#allows the user to access money held in their account and carry out transactions
    name=input("Enter your name: ")
    show(name)
    accid=input("Which account would you like to access? ")
    file=open("accounts.dat","rb+")
    try:
        flag=True
        while True:
            ac=pickle.load(file)
            if ac.accountid==accid:#searches for appropriate account in file using unique account ID
                account=ac
                flag=False
                break
    except (EOFError,pickle.UnpicklingError):#for handling End of File Error
        pass
    file.close()
    if flag:
        print("Account does not exist.")
        return None
    option=int(input("What would you like to do?\n1. Deposit\n2. Withdraw\n"))
    transaction(account,accid,option)

def main():
    _=os.system("cls")
    print("Welcome to ABC Bank")
    print("New or Old Customer?")
    customer=input()
    if "ew" in customer:
        creation()
        continuation()
    elif "ld" in customer:
        _=os.system("cls")
        print("Welcome Back! How can we help you today?")
        print("1. View Account Details")
        print("2. Access Old Account ")
        print("3. Create New Account ")
        print("4. Close Account ")
        print("5. Request Loan ")
        print("6. Pay Back Loan ")
        print("7. Transfer ")
        print("8. Deposit Cheque ")
        x=int(input())
        _=os.system("cls")
        if (x==1):
            name=input("Enter your name: ")
            show(name)
        elif (x==2):
            accessing()
        elif(x==3):
            creation()
        elif(x==4):
            accountid=input("Enter Account ID: ")
            close_account(accountid)
            print("Account Closed\n")
        elif(x==5):
            loan()
        elif(x==6):
            payloan()
        elif(x==7):
            transfer()
        elif(x==8):
            cheque()
        continuation()
    else:
        exit()

main()#calling the main function
