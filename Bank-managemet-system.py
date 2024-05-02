import random

# <-----------------------------------------------------------------Transaction Class start------------------------------------------------------------------------------->


class Transaction:
    def __init__(self,sender_account_number,receiver_account_number,amount,transaction_id) -> None:
        self.Transaction_id = transaction_id
        self.Sender_account_number = sender_account_number
        self.Receiver_account_number = receiver_account_number
        self.Amount = amount


# <-----------------------------------------------------------------Transaction Class end------------------------------------------------------------------------------->



# <-----------------------------------------------------------------Bank Class start------------------------------------------------------------------------------->
class Bank:
    def __init__(self,total_amount,bank_name) -> None:
        self.Bank_name = bank_name
        self.Total_amount = total_amount
        self.User_list = {} # It contains User Object and key is user Object's user_id and value is User Object.
        self.Admin_list = {} # It contains Admin Object and key is admin Object's user_id and value is Admin Object.
        self.Is_bankrupt = False
        self.Total_loan_amount = 0
    
    def Sign_Up(self,user):
        if isinstance(user,User)==True:
            for _,value in self.User_list.items():
                if value.Email == user.Email:
                    print(f"\nYOU HAVE ALREADY AN ACCOUNT WITH ACCOUNT NUMBER : {value.Account_number}.YOUR EMAIL ID IS : {value.Email}.PLEASE LOG IN.\n")
                    return
            self.User_list[user.User_id] = user
            print(f"\nYOU HAVE SUCCESSFULLY SIGN UP INTO {self.Bank_name} BANK.YOUR ACCOUNT NUMBER IS {user.Account_number}.YOUR USER ID IS : {user.User_id}.YOUR EMAIL ID IS : {user.Email}.NOW YOU ARE USER.\n")
        elif isinstance(user,Admin)==True:
            for _,value in self.Admin_list.items():
                if value.Email == user.Email:
                    print(f"\nYOU HAVE ALREADY AN ACCOUNT WITH USER ID : {value.User_id}.YOUR EMAIL ID IS :{value.Email}.PLEASE LOG IN.\n")
                    return
            self.Admin_list[user.User_id] = user
            print(f"\nYOU HAVE SUCCESSFULLY SIGN UP INTO {self.Bank_name} BANK.YOUR USER ID IS: {user.User_id}.YOUR EMAIL ID IS :{user.Email}. NOW YOU ARE ADMIN.\n")
        else:
            print("\nPLEASE ENTER CORRECT OBJECT OF 'Admin' or 'User' CLASS.\n")        
    
        
    def Login(self,email,password):
       
        for _,value in self.User_list.items():
            if value.Email==email and password == value.Password:
                print(f"\nWELCOME {value.Name}. YOU HAVE SUCCESSFULLY LOGGED IN INTO {self.Bank_name} BANK AS USER.YOUR USER ID IS : {value.User_id}.YOUR EMAIL ID IS : {value.Email}.\n")
                return value

        for _,value in self.Admin_list.items():
            if value.Email==email and password == value.Password:
                print(f"\nWELCOME {value.Name}. YOU HAVE SUCCESSFULLY LOGGED IN INTO {self.Bank_name} BANK AS ADMIN.YOUR USER ID IS : {value.User_id}.YOUR EMAIL ID IS : {value.Email}.\n")
                return value
        print(f"\nMAYBE THIS {email} ACCOUNT DOES NOT EXIST IN {self.Bank_name} BANK OR YOU HAVE GIVEN WRONG EMAIL OR PASSWORD.PLEASE CREATE A NEW ACCOUNT.\n")
        return None

# <-----------------------------------------------------------------Bank Class end------------------------------------------------------------------------------->

# <-----------------------------------------------------------------User Class start------------------------------------------------------------------------------->

class User:
    def __init__(self,name,email,address,account_type,password,role,user_id) -> None:
        self.Name = name
        self.Email = email
        self.Address = address
        self.Account_type = account_type
        self.Balance = 0
        self.Account_number = random.randint(10**14,10**15-1)
        self.Transaction_history = [] # It contains Transaction object 
        self.Take_loan_times = 0
        self.User_id = user_id
        self.Password = password
        self.Role = role
    def Deposit_balance(self,bank,amount):
        bank.Total_amount+=amount
        self.Balance+=amount
        for id,value in bank.User_list.items():
            if id==self.User_id:
                print(f"\n{value.Name}, YOU HAVE SUCCESSFULLY DEPOSIT {amount} TAKA\n")
                return
        print(f"\nYOUR ACCOUNT IS NOT EXIST IN {bank.Bank_name} BANK.YOUR EMAIL ID : {self.Email}\n")
        return
    def Withdraw_balance(self,bank,amount):
        if self.Balance < amount:
            print(f"\nINSUFFICIENT BALANCE! YOU HAVE ONLY {self.Balance} TAKA LEFT IN YOUR ACCOUNT\n")
        else:
            if bank.Total_amount < amount:
                print(f"\nCURRENTLY,{bank.Bank_name} BANK DOES NOT HAVE {amount} TAKA IN VAULT.PLEASE WAIT SOME TIMES\n")
            else:
                for id,_ in bank.User_list.items():
                    if self.User_id == id:
                        bank.Total_amount-=amount
                        self.Balance-=amount
                        print(f"\nYOU HAVE SUCCESSFULLY WITHDRAW {amount} TAKA IN YOUR BALANCE FROM {bank.Bank_name} BANK.\n")
                        return
                print(f"\n{self.Email} ID DOES NOT HAVE ANY ACCOUNT IN {bank.Bank_name} BANK\n")

    def Available_balance(self):
        print(f"\nYOUR BALANCE IS {self.Balance} TAKA\n")
    def Transaction_history_check(self):
        if not self.Transaction_history:
            print(f"\nYOUR TRANSACTION HISTORY IS EMPTY.PLEASE DO A TRANSACTION AFTER THAT CHECK IT.\n")
        else:
            for value in self.Transaction_history:
                print(f"\nSENDER ACCOUNT NUMBER : {value.Sender_account_number}\nRECEIVER ACCOUNT NUMBER : {value.Receiver_account_number}\nAMOUNT:{value.Amount}\nTRANSACTION ID:{value.Transaction_id}\n")
                print("<------------------------------------------------>")
    def Take_loan(self,bank,amount):
        if bank.Is_bankrupt==False:
            if bank.Total_amount > amount:
                if self.Take_loan_times>=2:
                    print(f"\nYOU CAN NOT TAKE LOAN MORE THAN TWICE.YOU HAVE ALREADY TAKEN LOAN {self.Take_loan_times} TIMES.\n")
                else:
                    for id,_ in bank.User_list.items():
                        if id==self.User_id:
                            self.Balance+=amount
                            bank.Total_loan_amount+=amount
                            self.Take_loan_times+=1
                            print(f"\nYOU HAVE SUCCESSFULLY TAKE LOAN {amount} TAKA FROM {bank.Bank_name} BANK.\n")
                            return
                    print(f"\nTHIS USER DOES NOT EXIST IN {bank.Bank_name} BANK.EMAIL ID OF THIS ACCOUNT IS : {self.Email}\n")
                    return 
            else:
                print(f"\nCURRENTLY,{bank.Bank_name} BANK DOES NOT HAVE {amount} TAKA IN VAULT.PLEASE WAIT SOME TIMES\n")
        else:
            print(f"\nTHIS {bank.Bank_name} BANK DECLARED BANKRUPTCY.SO, YOU CAN'T TAKE LOAN.\n")
    def Transfer_balance(self,account_number,bank,amount,transaction_id):
        for _,value in bank.User_list.items():
            if value.Account_number == account_number:
                if self.Balance >= amount:
                    for us_id,_ in bank.User_list.items():
                        if us_id == self.User_id:
                           self.Balance-=amount
                           value.Balance+=amount
                           new_transaction = Transaction(sender_account_number=self.Account_number,receiver_account_number=value.Account_number,amount=amount,transaction_id=transaction_id)
                           self.Transaction_history.append(new_transaction)
                           print(f"\nYOU HAVE SUCCESSFULLY TRANSFERRED {amount} TAKA TO {value.Account_number} ACCOUNT\n")
                           return 
                    print(f"\nYOUR EMAIL : {self.Email}.THIS ACCOUNT DOES NOT EXIST.\n")
                else:
                    print(f"\nTHIS TIME ONLY {self.Balance} TAKA AVAILABLE IN YOUR ACCOUNT. YOU CAN'T TRANSFER {amount} TAKA TO {value.Account_number} ACCOUNT\n")
                    return
        print(f"\nTHIS {account_number} ACCOUNT DOES NOT EXIST IN {bank.Bank_name} BANK\n")

# <-----------------------------------------------------------------User Class end------------------------------------------------------------------------------->



# <-----------------------------------------------------------------Admin Class start------------------------------------------------------------------------------->

class Admin:
    def __init__(self,name,email,password,address,role,user_id) -> None:
        self.Name = name
        self.Email = email
        self.Password = password
        self.Address = address
        self.Role = role
        self.User_id = user_id

    def Delete_user_account(self,bank,email):
        for id,value in bank.User_list.items():
            if value.Email == email:
                del bank.User_list[id]
                print(f"\nTHIS {email} ACCOUNT IS SUCCESSFULLY DELETED.\n")
                return 
        print(f"\nTHIS {email} ACCOUNT DOES NOT EXIST IN {bank.Bank_name} BANK.\n")
    def See_all_user_account(self,bank):
        if not bank.User_list:
            print("\nUSER LIST IS EMPTY.\n")
        else:
            for id,value in bank.User_list.items():
                print(f"\nNAME:{value.Name}\nEMAIL ADDRESS:{value.Email}\nACCOUNT NUMBER:{value.Account_number}\nID:{id}\n")
                print("<------------------------->")
        
    def See_total_balance(self,bank):
        print(f"\n{bank.Total_amount} TAKA.\n")
    def See_total_loan_amount(self,bank):
        print(f"\n{bank.Total_loan_amount} TAKA.\n")
    def Stop_loan_feature(self,bank):
        bank.Is_bankrupt = True
        print("\nSUCCESSFULLY STOPPED BANK LOAN FEATURE.\n")
    def Enable_loan_feature(self,bank):
        bank.Is_bankrupt = False
        print("\nSUCCESSFULLY ENABLED BANK LOAN FEATURE.\n")
    def Create_an_user_account(self,user,bank):
        for _,value in bank.User_list.items():
            if user.Email == value.Email:
                print(f"\nYOU HAVE ALREADY AN ACCOUNT IN THIS BANK.HERE IS YOUR ACCOUNT NUMBER : {value.Account_number} AND EMAIL ID : {value.Email} .PLEASE LOGIN.\n")
                return
        bank.User_list[user.User_id]=user
        print(f"\nYOU HAVE SUCCESSFULLY CREATED AN ACCOUNT.HERE IS YOUR ACCOUNT NUMBER : {user.Account_number} AND EMAIL ID : {user.Email}.\n")


# <-----------------------------------------------------------------Admin Class end------------------------------------------------------------------------------->





# <-----------------------------------------------------------------While loop start------------------------------------------------------------------------------->


Phitron = Bank(100000,"Phitron")
while True:
        print("1 For create an account. ")
        print("2 For log in an account. ")
        print("3 For exit.")
        choose = int(input("Please enter a number: "))
        if  choose==1:
            while True:
                print("1 For create an admin account. ")
                print("2 For create a user account. ")
                print("3 For exit.")
                press = int(input("Please enter a number : "))
                if press==1:
                    admin_name = input("Please enter your name : ")
                    admin_email = input("Please enter your email address : ")
                    admin_password = input("Please enter your password : ")
                    admin_address = input("Please enter your address : ")
                    admin_role = input("Please enter your role (Example: admin) : ")
                    admin_id = random.randint(10**3,10**4-1)
                    new_admin = Admin(name=admin_name,email=admin_email,password=admin_password,address=admin_address,role=admin_role,user_id=admin_id)
                    Phitron.Sign_Up(new_admin)     
                elif press==2:
                    user_name = input("Please enter your name : ")
                    user_email = input("Please enter your email address : ")
                    user_password = input("Please enter your password : ")
                    user_address = input("Please enter your address : ")
                    user_account_type = input("Please enter your account type (Saving or Current) : ")
                    user_role = input("Please enter your role (Example: user) : ")
                    user_id = random.randint(10**3,10**4-1)
                    new_user = User(name=user_name,email=user_email,address=user_address,account_type=user_account_type,password=user_password,role=user_role,user_id=user_id)
                    Phitron.Sign_Up(new_user)
                elif press==3:
                    break
                else:
                    print("\nPlease enter correct number 1 or 2 or 3\n")         
        elif choose==2:
            while True:
                print("1 For admin login")
                print("2 For user login")
                print("3 For exit")
                press = int(input("Please enter a number : "))
                if press==1:
                    admin_email_id = input("Please enter your email id : ")
                    admin_password = input("Please enter your password : ")
                    admin = Phitron.Login(email=admin_email_id,password=admin_password)
                    while True:
                        if admin!=None:
                            print("1 For delete user account ")
                            print("2 For see all user account ")
                            print("3 For see total balance ")
                            print("4 For total loan amount ")
                            print("5 For stop loan feature ")
                            print("6 For enable loan feature ")
                            print("7 For create an user account ")
                            print("8 For exit ")
                            press = int(input("Please Enter a number : "))
                            if press==1:
                                del_user_email = input("Please enter user email id : ")
                                admin.Delete_user_account(bank=Phitron,email=del_user_email)
                            elif press==2:
                                admin.See_all_user_account(Phitron)
                            elif press==3:
                                admin.See_total_balance(Phitron)
                            elif press==4:
                                admin.See_total_loan_amount(Phitron)
                            elif press==5:
                                admin.Stop_loan_feature(Phitron)
                            elif press==6:
                                admin.Enable_loan_feature(Phitron)
                            elif press==7:
                                ad_user_name = input("Please enter user name : ")
                                ad_user_email = input("Please enter user email address : ")
                                ad_user_password = input("Please enter user password : ")
                                ad_user_address = input("Please enter user address : ")
                                ad_user_account_type = input("Please enter user account type (Saving or Current) : ")
                                ad_user_role = input("Please enter user role (Example: user) : ")
                                ad_user_id = random.randint(10**3,10**4-1)
                                if ad_user_role!='user':
                                    print("\nPlease write the correct spelling (Example: user)\n")
                                else:
                                    ad_user = User(name=ad_user_name,email=ad_user_email,address=ad_user_address,account_type=ad_user_account_type,password=ad_user_password,role=ad_user_role,user_id=ad_user_id)
                                    admin.Create_an_user_account(ad_user,Phitron)    
                            elif press==8:
                                break
                            else:
                                print("Please enter a valid number from 1 to 6")
                        else:
                            print(f"This account does not exist on {Phitron.Bank_name} bank.\n")
                            break
                elif press==2:
                    user_email_id = input("Please enter your email id : ")
                    user_password = input("Please enter your password : ")
                    user = Phitron.Login(email=user_email_id,password=user_password)
                    while True:
                        if user!=None:
                            print("1 For deposit balance")
                            print("2 For withdraw balance")
                            print("3 For check balance")
                            print("4 For check transaction history")
                            print("5 For take loan")
                            print("6 For transfer balance")
                            print("7 For exit")
                            select = int(input("Please select a number : "))
                            if select==1:
                                amount = int(input("Please enter amount : "))
                                user.Deposit_balance(Phitron,amount)
                            elif select==2:
                                self_amount = int(input("Please enter amount : "))
                                user.Withdraw_balance(Phitron,self_amount)
                            elif select==3:
                                user.Available_balance()
                            elif select==4:
                                user.Transaction_history_check()                           
                            elif select==5:
                                selfs_amount = int(input("Please enter amount : "))
                                user.Take_loan(Phitron,selfs_amount)                           
                            elif select==6:
                                ss_account_number = int(input("Please enter account number : "))
                                ss_amount = int(input("Please enter amount : "))
                                ss_transaction_id = random.randint(10**9,10**10-1)
                                user.Transfer_balance(ss_account_number,Phitron,ss_amount,ss_transaction_id)                       
                            elif select==7:
                                break
                            else:
                                print("\nInvalid input ! Please enter number from 1 to 7\n")
                        else:
                            print(f"\nThis account does not exist on {Phitron.Bank_name} bank.\n")
                            break
                elif press==3:
                    break
                else:
                    print("\nInvalid input ! Please enter number from 1 to 3.\n")
        elif choose==3:
            break
        else:
            print("\nInvalid input ! Please enter number from 1 to 3\n")
    

# <-----------------------------------------------------------------While loop end------------------------------------------------------------------------------->

