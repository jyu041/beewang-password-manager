# main.py - Version9
# Login/register to store logins and passwords for websites
# Bee.Wang, 24 April 2020


# CUSTOMIZABLE SETTINGS ========================================================================================
encoding_power_low = 8 # ONLY CHANGE THIS WHEN THERE ARENT ACCOUNTS REGISTERED, THIS VALUE MUST NOT EXCEED 62
encoding_power = 16 # ONLY CHANGE THIS WHEN THERE ARENT ACCOUNTS REGISTERED
# Changing the above two values would result in old login details and accounts not being able to work properly

# Default settings for some visuals and support functions
auto_login_after_register = True # Change this to false if you would want to disable auto login after register
console_color = '0b' # Windows Only, you may play around with this color code to get different color themes in your console
windows_title = 'BeeWang-Password-Manager' # Windows Only
# ==============================================================================================================


import os, sys, hashlib, base64, time, random

# Useless thing just to make the restart look cooler
print('    ' + str(sys.argv))

# Variables to be declared at the start of the program when it runs for some default values
no_option_list = ['There is no such option avaliable, please enter again!','You have entered an invalid option, please try again!','Your option is invalid, please enter again!','There is no option for what you have entered, try again!']
user_access_granted = False
can_log_in = False
encyrption_salt = 'mysuperdupercantbeguessedsecretsaltkey' # A salt key for the encryption process


# Uses world grade SHA512 encryption to encrypt data througout the program
def encrypt(item_to_encrypt):
    item_to_encrypt = item_to_encrypt + encyrption_salt
    for i in range(encoding_power):
        item_to_encrypt = str(hashlib.sha512(item_to_encrypt.encode()).hexdigest())
    return str(item_to_encrypt)


# Clear screen function
def clean():
    os.system('cls' if os.name=='nt' else 'clear')


def exit_program():
    print(f'\n    Thank you for using {windows_title}, you can close this window now')
    sys.exit()


def restart_program():
    print("\n    argv was", sys.argv)
    print("    sys.executable was", sys.executable)
    print("    restarting now")
    os.execv(sys.executable, ['python'] + sys.argv)


def auto_settings():
    # title settings
    os.system(f'title {windows_title}' if os.name == 'nt' else '\n')
    # color settings:
    os.system(f'color {console_color}')


# This encoding function encodes the user data in base64, and then returns it
def data_encode(encodedStr):
    for i in range(encoding_power_low):
        print(f'    Encoding process : {str(((i+1) / encoding_power_low) * 100)}%', end='\r')
        encodedStr = str(base64.b64encode(encodedStr.encode("utf-8")), "utf-8")
    print('                                             ', end='\r')
    return str(encodedStr)


# This decoding functions decodes the encrypted data and then returns it
def data_decode(decodedStr):
    for i in range(encoding_power_low):
        print(f'    Decoding process : {str(((i+1) / encoding_power_low) * 100)}%', end='\r')
        decodedStr = base64.b64decode(decodedStr).decode("utf-8")
    print('                                             ', end='\r')
    return str(decodedStr)


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
    with open('accounts.txt','a+') as f_register:
        f_register.close()
    with open('accounts.txt','r+') as f_register:
        print('    Please enter information below:\n')
        print('    Your username must: \n    - only contain lower case letters and numbers\n    - no special characters allowed\n    - longer than 5 (five) digits\n\n    You may type "!end" to cancel the register process')
        while True:
            login = str(input('    Enter your username here >> ')).lower()
            if encrypt(login) in f_register.read():
                print('\n    * There is already an account with this username!\n    Please login with it or make an account with a different username!')
            elif login == '!end':
                clean()
                print('\n    * You have cancelled to register an acocunt!')
                return
            elif len(login) < 5:
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
            with open(f'./users/{encrypt(login)}','a+') as acc_f:
                if os.path.isfile(f'./users/{encrypt(login)}'):
                    print('\n    Succesfully created')
                else:
                    print('\n    FATAL ERROR: Failed to create file, this problem should not exist, but it just happened, so ah... idk help yourself')
                acc_f.close()
        print('    ==================================================\n')
        time.sleep(2)
        clean()
        
        global user_access_granted
        global login_username
        if auto_login_after_register:
            user_access_granted = True
            login_username = login
            print(f'\n    Your account: "{login}" has been created! and you have been automatically logged in')
        else:
            user_access_granted = False
            print('\n    Auto login has been disabled, you may change this in the settings options')
        f_register.close()


def login_func():
    if os.path.isfile('accounts.txt') and os.stat('accounts.txt').st_size != 0:
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
                        if login_username == '!end':
                            clean()
                            print('\n    User cancelled login process')
                            return 
                    
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


def delete_acc(auth_key):
    if auth_key:
        global user_access_granted
        clean()
        print('\n    Are you sure you want to delete your account?!\n    All stored data for your account will be un-recoverable after current action!')
        confirm_del = input('\n    Confirm by entering your password: ')
        with open('accounts.txt','r') as check_account:
            for lines in check_account:
                if lines.startswith(f'{encrypt(login_username)}'):
                    if encrypt(confirm_del) == str(lines.split(':')[1].rstrip('\n')):
                        with open('accounts.txt','w') as del_account:
                            for lines in check_account:
                                if lines.startswith(f'{encrypt(login_username)}'):
                                    pass
                                else:
                                    del_account.write(lines)
                        if os.path.isfile(f'./users/{encrypt(login_username)}'):
                            os.remove(f'./users/{encrypt(login_username)}')
                            clean()
                            user_access_granted = False
                            print(f'\n    Your account, [{login_username}], and data associated with has been removed')
                    else:
                        clean()
                        print('\n    INCORRECT PASSWORD, RETURNING TO HOMESCREEN')
                        return
                


    else:
        clean()
        print('\n    You cannot delete any accounts without being logged in')
        return


def store_details(auth_key):
    if auth_key:
        if os.path.isdir('./users') == False:
            os.mkdir('./users')
            print('\n    The program have detected that the folder that stores all \n    encrypted details has been deleted, all lost data cannot be\n    recovered using this program, but the missing files to run\n    this program has been re-created, please continue freely,\n    if you know what is happening you may ignore this message')

        with open(f'./users/{encrypt(login_username)}','a+') as f_account:
            with open(f'./users/{encrypt(login_username)}','r') as f_detail_len:
                lines_of_details = f_detail_len.read()
                if len(lines_of_details) > 9999:
                    clean()
                    time.sleep(4)
                    print('\n    FATAL ISSUE: You have reached the maximum login details that one account can store!\n    Please remove unwanted login details from "view login details"\n    Or create a new account!')
                    return

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
            print(f'\n    You have stored {len(written_amount)} login details')

        f_account.close()
    else:
        clean()
        print('\n    * You are not logged in, you must log in to store login details privately!')


def del_line(line_item):
    with open(f'./users/{encrypt(login_username)}', "r") as f_read:
        lines = f_read.readlines()
    with open(f'./users/{encrypt(login_username)}', "w") as f_write:
        for i, line in enumerate(lines):
            if i not in line_item:
                f_write.write(line)


def change_line(item_list):
    file_read = open(f'./users/{encrypt(login_username)}', "r")
    lines = file_read.readlines()
    file_read.close()
    with open(f'./users/{encrypt(login_username)}', "w") as file_write:
        num_sum = item_list[0].strip(' ').replace(' ','')
        for i, line_data in enumerate(lines):
            if i + 1 != int(num_sum):
                file_write.write(line_data)
            else:
                file_write.write(f'{data_encode(item_list[1])}<>{data_encode(item_list[2])}<>{data_encode(item_list[3])}\n')


def clear_line():
    print('\n    Are you sure you want to clear all your logins?!')
    clear_choice = input('    Please confirm (Y/N) >> ').lower()
    if clear_choice == 'y':
        with open(f'./users/{encrypt(login_username)}','w') as clean_file:
            print()
            for i in range(1,101):
                print(f'    Clearing Progress: {i}%', end='\r')
                time.sleep(0.01)

            print('\n    Finished Clearning...')
            time.sleep(1.5)
            print('    ' + str(clean_file))#this print here is only to remove the yellow under lines of not used variables in visual studio code, this line does not need to exist
            return
    else:
        print('\n    Cancelled to clear all logins, returning...')
        time.sleep(1)


def read_details(auth_key):
    if auth_key:
        while True:
            if os.path.isfile(f'./users/{encrypt(login_username)}') == False:
                if os.path.isdir('./users') == False:
                    os.mkdir('./users')
                print('\n    The file that stores the login details for current account\n    does not exist or has been deleted, information lost can not\n    be recovered, we are very sorry for what has happened to \n    your data, if you know what is happening you may ignore  \n    this message and continue, also that the missing file has been \n    recreated but will be empty until you start to store \n    information inside it')
                f_create = open(f'./users/{encrypt(login_username)}','a+')
                f_create.close()
                time.sleep(4)
                clean()
                print('\n    * Your files were corrupted, but now has been fixed!')
                return
            else:
                clean()
                print('\n    Your login details are displayed below:')
                with open(f'./users/{encrypt(login_username)}','r') as f_account:
                    full_details = []
                    for lines in f_account:
                        line_info = lines.split('<>')
                        line_detail = []
                        for details in line_info:
                            line_detail.append(data_decode(details))
                        full_details.append(line_detail)

                    if len(full_details) > 0:
                        print('\n           Websites:                 Username:            Password:\n')
                        for infos in range(len(full_details)):
                            print(' ' * (8 - len(str(infos + 1))) + f'{str(int(infos + 1))}.  ' + full_details[infos][0] + ' ' * (26 - len(full_details[infos][0])) + full_details[infos][1] + ' ' * (21 - len(full_details[infos][1])) + full_details[infos][2])
                        print("""

    Actions that can be performed, without the brackets:
    Commands:                                            Usages:

    !end                                                 1. To leave this page     
    !del (number for website)                            2. Remove login details by line number
    !change (number) (website) (username) (password)     3. Change login details by line number
    !clear                                               4. Clear all login details

                        """)
                        read_menu_commands = input('\n    Enter your command >> ')
                        if '!end' in read_menu_commands:
                            clean()
                            print('\n    User closed login details view')
                            return

                        # Bulk delete items in login details:
                        elif read_menu_commands.startswith('!del '):
                            numbers = read_menu_commands.replace('!del ','').strip(' ').split(' ')
                            for i in range(len(numbers)):
                                numbers[i] = int(numbers[i]) - 1
                            
                            del_line(numbers)
                        
                        # change login details by line number:
                        elif read_menu_commands.startswith('!change '):
                            inform = read_menu_commands.replace('!change ','').strip(' ').split(' ')
                            if len(inform) == 4:
                                change_line(inform)
                            else:
                                print('\n    You need to enter at least three values!\n    Example: !change (number) (website) (username) (password)')

                        elif read_menu_commands.startswith('!clear'):
                            clear_line()

                        else:
                            clean()
                            print('\n    That was an invalid command!')
                            time.sleep(1)
                    else:
                        f_account.close()
                        clean()
                        print('\n    * You do not have stored login details in your files')
                        break

    else:
        clean()
        print('\n    * You are not logged in, you must log in to read stored login details!')


def store_public():
    print('\n    WARNING: You are about to store information that is visible to all users that uses this program\n    All information in this file can be removed by anyone\n    do not keep important information here!\n')
    with open('./users/publiclogins','a+') as public_write:
        written_amount = []
        print('    Type "!end" to stop entering login details\n')
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
            public_write.write(f'{encoded_store_site}<>{encoded_store_user}<>{encoded_store_pwd}\n')
            written_amount.append('x')
            print('\n    Details Stored Successfuly\n')

    clean()
    if len(written_amount) == 0:
        print('\n    You have cancelled to store any login details')
    elif len(written_amount) == 1:
        print(f'\n    You have stored {len(written_amount)} login detail')
    else:
        print(f'\n    You have stored {len(written_amount)} login details')


def view_public():
    if os.path.isfile('./users/publiclogins') == False:
        clean()
        print('\n    No public login details available')
        return
    else:
        clean()
        print('\n    Your login details are displayed below:')
        with open(f'./users/publiclogins','r') as f_account:
            full_details = []
            for lines in f_account:
                line_info = lines.split('<>')
                line_detail = []
                for details in line_info:
                    line_detail.append(data_decode(details))
                full_details.append(line_detail)

            if len(full_details) > 0:
                print('\n           Websites:                 Username:            Password:\n')
                for infos in range(len(full_details)):
                    print(' ' * (8 - len(str(infos + 1))) + f'{str(int(infos + 1))}.  ' + full_details[infos][0] + ' ' * (26 - len(full_details[infos][0])) + full_details[infos][1] + ' ' * (21 - len(full_details[infos][1])) + full_details[infos][2])
        
        print(input('\n    Press Enter to return to home screen'))
        clean()


def del_public(auth_key):
    if auth_key:
        if os.path.isfile('./users/publiclogins'):
            print('\n    You are about to delete the file the stores public keys, are you sure you want to delete them all!?')
            del_pub_con = input('    Please confirm (Y:N) >> ').lower()
            if del_pub_con == 'y':
                os.remove('./users/publiclogins')
                clean()
                print('\n    All Publicly stored Login details have been removed!')
            else:
                clean()
                print('\n    Cancelled to delete publicly stored login details, returned to main menu')
        else:
            clean()
            print('\n    There are currently no stored public login details')
    else:
        clean()
        print('\n    You must login first before being able to remove public login details')


def menu():
    clean()
    print('\n                 <> Welcome to the BeeWang Password Manager <>')
    menu_text = """
    ========================= Available Options =========================

                      1.  Logging in to an account
                      2.  Registering an account
                      3.  Log out from your account
                      4.  Delete Account (CAUTION)

                      5.  Store login details (Requires Login)
                      6.  Retrieve login details (Requires Login)

                      7.  Store login details publicly (Anyone Can See!)
                      8.  View publicly stored login details
                      9.  Remove publicly stored login details

                     10.  Close Program
                     11.  Restart Program

    =====================================================================
        (Please select an option by entering the corresponding number)
    """
    while True:
        print(menu_text)
        menu_choice = input('    Plase Enter number here >> ')
        # Sorted to different categories
        if menu_choice == '1':
            login_func()
        elif menu_choice == '2':
            register_func()
        elif menu_choice == '3':
            logout_func(user_access_granted)
        elif menu_choice == '4':
            delete_acc(user_access_granted)

        elif menu_choice == '5':
            store_details(user_access_granted)
        elif menu_choice == '6':
            read_details(user_access_granted)

        elif menu_choice == '7':
            store_public()
        elif menu_choice == '8':
            view_public()
        elif menu_choice == '9':
            del_public(user_access_granted)

        elif menu_choice == '10':
            exit_program()
        elif menu_choice == '11':
            restart_program()
        
        else:
            clean()
            print(f'\n    * {random.choice(no_option_list)}')


try:
    auto_settings()
    menu()
except KeyboardInterrupt:
    print('\n\n    User Closed Program')