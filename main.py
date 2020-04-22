# main.py - Version 2
# Login/register to store logins and passwords for websites
# Bee.Wang, 21 April 2020


import string, os, sys, hashlib, base64, time, random

# Variables to be declared at the start of the program when it runs for some default values
no_option_list = ['There is no such option avaliable, please enter again!','You have entered an invalid option, please try again!','Your option is invalid, please enter again!','There is no option for what you have entered, try again!']
user_access_granted = False
can_log_in = False

# Uses world grade MD5 encryption to encrypt data througout the program
def encrypt(item_to_encrypt):
    for i in range(8):
        item_to_encrypt = hashlib.md5(item_to_encrypt.encode())
        item_to_encrypt = str(item_to_encrypt.hexdigest())
    return str(item_to_encrypt)


# Clear screen function
def clean():
    os.system('cls' if os.name=='nt' else 'clear')


# Changes Terminal title for windows users
def change_title():
    # This title can be changed by just editing it below here
    global windows_title
    windows_title = 'BeeWang Password Manager'
    try:
        os.system(f'title {windows_title}' if os.name == 'nt' else '\n')
    except:
        pass

def exit_program():
    #clean()
    print(f'\n    Thank you for using {windows_title}, you can close this window now')
    sys.exit()


def logout_func(auth_key):
    global user_access_granted
    global login_username
    if auth_key:
        while True:
            logout_choice = input('    Do you wish to logout (y/n): ').lower()
            if logout_choice == 'y':
                print('    You tried to log out')
                user_access_granted = False
                clean()
                print(f'\n    You have been logged out of "{login_username}"')
                login_username = '    Logged out'
                break
            elif logout_choice == 'n':
                clean()
                print('\n    You have cancelled to log out')
                break
            else:
                print('\n    That was an invalid choice! Please enter again!')
    else:
        clean()
        print('\n    You are not logged in!')


def register_func():
    # These two lines outside of the with is to create the file "accounts.txt" if it doesnt exist
    f_register = open('accounts.txt','a+')
    f_register.close()
    with open('accounts.txt','r+') as f_register:
        print('    Please enter information below:\n')
        print('    Your username must: \n    - only contain lower case letters and numbers\n    - no special characters allowed\n    - longer than 8 (eight) digits\n\n    You may type "end" to cancel the register process')
        while True:
            login = str(input('    Enter your username here >> ')).lower()
            if encrypt(login) in f_register.read():
                print('\n    * There is already an account with this username!\n    Please login with it or make an account with a different username!')
            elif login == 'end':
                clean()
                print('\n    * You have cancelled to register an acocunt!')
                return
            elif len(login) < 8:
                print(f'\n    * Your username is not long enough, it must be atleast 8 (eight) digits long\n    * You have entered {len(login)} digits')
            elif login.isalnum():
                break
            else:
                print('\n    Your username must only contain letters and numbers')
                
        while True:  
            password = str(input('    Enter your password here >> '))
            confirm_password = str(input('    Confirm your password here >> '))
            if password == confirm_password:
                break
            else:
                print('    Your entered password do not match! Please enter it correctly\n')

        f_register.write(f'{encrypt(login)}:{encrypt(password)}\n')
        print('\n    ==================================================\n    Checking for ./users folder...')
        if os.path.isdir('./users'):
            print('    Directory exists!')
        else:
            print('    Creating directory...')
            os.mkdir('./users')
            print('    Finished creating directory')
        print('    Checking if there are already files for current account...')
        if os.path.isfile(f'./users/{encrypt(login)}'):
            print('    Account already exists in file directories!')
        else:
            print('    Creating files for current user!')
            acc_f = open(f'./users/{encrypt(login)}','a+')
            if os.path.isfile(f'./users/{encrypt(login)}'):
                print('\n    Succesfully created')
            else:
                print('\n    FATAL ERROR: Failed to create file, this problem should not exist, but it just happened, so ah... idk help yourself')
            acc_f.close()
        print('    ==================================================\n')
        time.sleep(3)
        clean()
        print(f'\n    Your account: "{login}" has been created!')
        f_register.close()


def login_func():
    if os.path.isfile('accounts.txt'):
        global user_access_granted
        global login_username
        if user_access_granted == False:
            # Username Part of login below
            save_login_details_hashed = []
            while True:
                with open('accounts.txt','r') as f_login_files:
                    if len(save_login_details_hashed) == 0:
                        print('\n    Enter your login details below:')
                        login_username = str(input('    Username >> ')).lower()
                    
                        if len(save_login_details_hashed) == 0:
                            for lines in f_login_files:
                                if lines.startswith(f'{encrypt(login_username)}'):
                                    print('\n    Please enter your password:')
                                    save_login_details_hashed.append(lines)

                        if len(save_login_details_hashed) == 0:
                            print('\n    Unable to find username')
                    else:
                        break

            # Password Part of login below
            while True:
                with open('accounts.txt','r') as f_login_files:
                    login_password = str(input('    Password >> '))
                    extracted_password = str(save_login_details_hashed[0].split(':')[1].rstrip('\n'))
                    if encrypt(login_password) == extracted_password:
                        can_log_in = True
                        f_login_files.close()
                        break
                    else:
                        print('\n    The password you have entered does not match the one we have in our data base\n    Plase enter try again')
            
            if can_log_in == True:
                user_access_granted = True
                clean()
                print(f'\n    * You have been successfully logged in to "{login_username}"!')
            else:
                print('\n    FATAL ERROR: Login Unsucess')
        else:
            print(f'\n    * You have already logged in to "{login_username}", you do not need to login again')
            logout_func(user_access_granted)
    else:
        clean()
        print('\n    * Sorry but there are currently no accounts registered, please register an account first before coming')


def store_password(auth_key):
    if auth_key:
        print('    * WORKING *')
    else:
        clean()
        print('\n    * You are not logged in, you must log in to store passwords privately!')


def menu():
    clean()
    print('\n                 <> Welcome to the BeeWang Password Manager <>')
    menu_text = """
    ========================= Available Options =========================

                      1.  Registering an account
                      2.  Logging in to an account
                      3.  Store Password (Requires Login)
                      4.  Log out from your account
                      5.  Close Program

    =====================================================================
        (Please select an option by entering the corresponding number)
    """
    while True:
        print(menu_text)
        menu_choice = input('    Plase Enter number here >> ')
        if menu_choice == '1':
            register_func()
        elif menu_choice == '2':
            login_func()
        elif menu_choice == '3':
            store_password(user_access_granted)
        elif menu_choice == '4':
            logout_func(user_access_granted)
        elif menu_choice == '5':
            exit_program()
        else:
            clean()
            print(f'\n    * {random.choice(no_option_list)}')


try:
    change_title() # Change title function is only for windows user right now, this could change in the future
    menu()
except KeyboardInterrupt:
    print('\n    User Closed Program')