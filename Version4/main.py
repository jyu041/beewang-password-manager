# main.py - Version 4
# Login/register to store logins and passwords for websites
# Bee.Wang, 21 April 2020


import string, os, sys, hashlib, base64, time, random

# Variables to be declared at the start of the program when it runs for some default values
no_option_list = ['There is no such option avaliable, please enter again!','You have entered an invalid option, please try again!','Your option is invalid, please enter again!','There is no option for what you have entered, try again!']
user_access_granted = False
can_log_in = False

# Below here is the windows title, this can be changed anytime
windows_title = 'BeeWang Password Manager' 

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
    os.system(f'title {windows_title}' if os.name == 'nt' else '\n')


def exit_program():
    print(f'\n    Thank you for using {windows_title}, you can close this window now')
    sys.exit()


def restart_program():
    if os.name == 'nt':
        print('\n    Restarting program...')
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        clean()
        print('\n    Sorry but this function is currently only for windows users')


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
        print('    Your username must: \n    - only contain lower case letters and numbers\n    - no special characters allowed\n    - longer than 8 (eight) digits\n\n    You may type "!end" to cancel the register process')
        while True:
            login = str(input('    Enter your username here >> ')).lower()
            if encrypt(login) in f_register.read():
                print('\n    * There is already an account with this username!\n    Please login with it or make an account with a different username!')
            elif login == '!end':
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
        print(f'\n    Your account: "{login}" has been created! and you have been automatically logged in')
        global user_access_granted
        global login_username
        user_access_granted = True
        login_username = login
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
                        print('\n    Incorrect Password\n')
            
            if can_log_in == True:
                user_access_granted = True
                clean()
                print(f'\n    * You have been successfully logged in to "{login_username}"!')
            else:
                print('\n    FATAL ERROR: Login Unsucess')
        else:
            print(f'\n    * You have already logged in to "{login_username}", you do not need to login again')
            logout_func(user_access_granted)

        return login_username
    else:
        clean()
        print('\n    * Sorry but there are currently no accounts registered, please register an account first before coming')


# This encoding function encodes the user data in base64, and then returns it
def data_encode(encodedStr):
    for i in range(8):
        encodedStr = str(base64.b64encode(encodedStr.encode("utf-8")), "utf-8")
    return str(encodedStr)

# This decoding functions decodes the encrypted data and then returns it
def data_decode(decodedStr):
    for i in range(8):
        decodedStr = base64.b64decode(decodedStr).decode("utf-8")
    return str(decodedStr)


def store_details(auth_key):
    if auth_key:
        if os.path.isdir('./users') == False:
            os.mkdir('./users')
            print('\n    The program have detected that the folder that stores all \n    encrypted details has been deleted, all lost data cannot be\n    recovered using this program, but the missing files to run\n    this program has been re-created, please continue freely,\n    if you know what is happening you may ignore this message')

        f_account = open(f'./users/{encrypt(login_username)}','a+')
        written_amount = []
        print('\n    You can store your logins and passwords here!\n    Note that this process could be slow, because it is encrypting your data\n    Type "!end" to stop entering login details\n')
        while True:
            store_site = str(input('    Website to store for >> '))
            if store_site == '!end':
                break

            store_user = str(input('    Username to store for >> '))
            if store_user == '!end':
                break

            store_pwd = str(input('    Password to store for >> '))
            if store_pwd == '!end':
                break

            encoded_store_site = data_encode(store_site)
            encoded_store_user = data_encode(store_user)
            encoded_store_pwd = data_encode(store_pwd)
            f_account.write(f'{encoded_store_site}<>{encoded_store_user}<>{encoded_store_pwd}\n')
            written_amount.append('x')
            print('\n    Details Stored Successfuly\n')

        clean()
        if len(written_amount) == 0:
            print('\n    You have cancelled to store any login details')
        elif len(written_amount) == 1:
            print(f'\n    You have stored {len(written_amount)} login detail')
        else:
            print(f'\n    You have stored {len(written_amount)} login detail')

        f_account.close()
    else:
        clean()
        print('\n    * You are not logged in, you must log in to store login details privately!')


def del_line(line_item):
    written_lines = []
    with open(f'./users/{encrypt(login_username)}', "r") as f:
        lines = f.readlines()
    with open(f'./users/{encrypt(login_username)}', "w") as f:
        for line in lines:
            if len(written_lines) == 0:
                if not line.strip("\n").startswith(line_item):
                    f.write(line)
                else:
                    written_lines.append('x')
            else:
                f.write(line)


def read_details(auth_key):
    if auth_key:
        while True:
            if os.path.isdir('./users') == False:
                print('\n    The program have detected that the folder that stores all \n    encrypted details has been deleted, all lost data cannot be\n    recovered using this program, but the missing files to run\n    this program has been re-created, please continue freely,\n    if you know what is happening you may ignore this message')
            elif os.path.isfile(f'./users{encrypt(login_username)}') == False:
                print('\n    The file that stores the login details for current account\n    does not exist or has been deleted, information lost can not\n    be recovered, we are very sorry for what has happened to \n    your data, if you know what is happening you may ignore  \n    this message and continue, also that the missing file has been \nrecreated but will be empty until you start to store information inside it')
            else:
                clean()
                print('    Your login details are displayed below:')
                f_account = open(f'./users/{encrypt(login_username)}','r')
                full_details = []
                for lines in f_account:
                    line_info = lines.split('<>')
                    line_detail = []
                    for details in line_info:
                        line_detail.append(data_decode(details))
                    full_details.append(line_detail)

                if len(full_details) > 0:
                    print('\n        Websites:                 Username:            Password:')
                    for infos in range(len(full_details)):
                        print(f'    {str(int(infos) + 1)}.  ' + full_details[infos][0] + ' ' * (26 - len(full_details[infos][0])) + full_details[infos][1] + ' ' * (21 - len(full_details[infos][1])) + full_details[infos][2])

                    print('\n    Actions that can be performed:\n    1. Remove login details by line number, usage: "!a (number for website)"')
                    read_menu_commands = input('\n    Enter your command >> ')
                    if read_menu_commands.startswith('!a '):
                        numbers = read_menu_commands.replace('!a ','').strip(' ').split(' ')
                        temp_line = data_encode(str(full_details[int(numbers[0]) - 1][0]))
                        print(f'    Attempt to delete line "{int(numbers[0])}" gave a response of "{del_line(temp_line)}"')
                else:
                    f_account.close()
                    print('\n    You do not have stored login details in your files')

    else:
        clean()
        print('\n    * You are not logged in, you must log in to read stored login details!')
        

def menu():
    clean()
    print('\n                 <> Welcome to the BeeWang Password Manager <>')
    menu_text = """
    ========================= Available Options =========================

                      1.  Registering an account
                      2.  Logging in to an account
                      3.  Store login details (Requires Login)
                      4.  Retrieve login details (Requires Login)
                      5.  Log out from your account
                      6.  Close Program
                      7.  Restart Program

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
            store_details(user_access_granted)
        elif menu_choice == '4':
            read_details(user_access_granted)
        elif menu_choice == '5':
            logout_func(user_access_granted)
        elif menu_choice == '6':
            exit_program()
        elif menu_choice == '7':
            restart_program()
        else:
            clean()
            print(f'\n    * {random.choice(no_option_list)}')


try:
    change_title() # Change title function is only for windows user right now, this could change in the future
    menu()
except KeyboardInterrupt:
    print('\n\n    User Closed Program')