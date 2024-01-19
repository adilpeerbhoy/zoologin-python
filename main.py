'''
The is a local user authentication program for a zoo.
The program has the user provide a username and password
and checks those credentials to a file loaded in by the program.
If the credentials match, then the relevant information is
presented to the user based on their role.

First some libraries are imported that help with hashing
the password provided by the user and to work with json files
'''
import json
import hashlib

# This opens a json file containing the available credentials and roles
# for each user
with open('./credentials.json') as f:
    data = json.load(f)

'''
Here we are redefining the data in the json file so that the usernames
become keys and hashed passwords become values in a dictionary format.
We are also creating a dictionary for the user role in order to allow 
only certain information from being seen by the user.    
'''
auth = {}
groups = {}
for user in data['users']:
    auth[user['username']] = {'hash' : user['hash'], 'id' : user['id']}

for role in data['roles']:
    groups[role['user_id']] = {'role' : role['role'], 'id' : role['id']}

'''
These functions are what the user will see upon successful login based on 
their role. The user will be able to make a choice from a menu of options.
These include viewing all the data available to them and logging out to the 
main menu. More features can be added based on the type of information
each user would like to access most often. Data is stored in json files outside
the main program and are opened within their respective functions.
'''
def admin():
    print()
    print('Hello, System Admin!')
    print('As administrator, you have access to the zoo\'\s main computer system')
    print('This allows you to monitor users in the system and their roles.')
    print()
    print('1 - View Entire Staff')
    print('2 - Logout')
    print()

    with open('./staff.json') as f:
        data = json.load(f)

    while True:
        try:
            admin_select = int(input('Please select an option to continue (1-2): '))
            if admin_select == 1:
                print(json.dumps(data['staff'], indent=2))
                anykey=input("Enter anything to return to main menu")
                admin()
            if admin_select == 2:
                print()
                print()
                zoo_authentication()
        except ValueError:
            print("Invalid choice. Enter 1-2")
    exit

def veterinarian():
    print()
    print('Hello, Veterinarian!')
    print('As veterinarian, you have access to all of the animals\'\ health records')
    print('This allows you to view each animal\'\s medical history and current treatments/illnesses (if any), and to maintain a vaccination log.')
    print()
    print('1 - View all Animals')
    print('2 - View all Medical Reports')
    print('3 - Logout')
    print()

    with open('./animals.json') as f:
        animals = json.load(f)

    with open('./medical.json') as file:
        medicals = json.load(file)

    while True:
        try:
            vet_select = int(input('Please select an option to continue (1-3): '))
            if vet_select == 1:
                print(json.dumps(animals['animal'], indent=2))
                anykey=input("Enter anything to return to main menu")
                veterinarian()
            if vet_select == 2:
                print(json.dumps(medicals['record'], indent=2))
                anykey=input("Enter anything to return to main menu")
                veterinarian()
            if vet_select == 3:
                print()
                print()
                zoo_authentication()
        except ValueError:
            print("Invalid choice. Enter 1-3")
    exit

def zookeeper():
    print('Hello, Zookeeper!')
    print('As zookeeper, you have access to all of the animals\'\ information and their daily monitoring logs.')
    print('This allows you to track their feeding habits, habitat conditions, and general welfare.')
    print()
    print('1 - View all Animals')
    print('2 - View Monitoring Logs')
    print('3 - Logout')
    print()

    with open('./animals.json') as f:
        animals = json.load(f)
    
    with open('./logs.json') as file2:
        logs = json.load(file2)

    while True:
        try:
            zoo_select = int(input('Please select an option to continue (1-3): '))
            if zoo_select == 1:
                print(json.dumps(animals['animal'], indent=2))
                anykey=input("Enter anything to return to main menu")
                zookeeper()
            if zoo_select == 2:
                print(json.dumps(logs['log'], indent=2))
                anykey=input("Enter anything to return to main menu")
                zookeeper()
            if zoo_select == 3:
                print()
                print()
                zoo_authentication()
        except ValueError:
            print("Invalid choice. Enter 1-3")
    exit

'''
The main function. After greeting the user, asks for username and password (non-hashed).
Once the password is typed, it is hashed by the hexdigest function (performs MD5 hash).
Once hashed, the hashed password is compared to those stored on file. The user is allowed
to make three attempts to login before being booted out. After an unsuccessful attempt, the
user is asked if they would like to try again. If they select yes, they go back to the main menu.
If they choose not to retry, the program closes.
 '''
def zoo_authentication():
    attempts = 0
    quit = False
    while not quit:
        print('Hello, Welcome to the Zoo!')
        username = input('Enter Username: ')
        password = input('Enter Password: ')
        hash = hashlib.md5(password.encode())
        if hash.hexdigest() == auth[username]['hash']:
            print('Login Successful')
            role = groups[str(auth[username]['id'])]['role']
            if role == 'admin':
                admin()
                #return 0
            elif role == 'veterinarian':
                veterinarian()
                #return 0
            elif role == 'zookeeper':
                zookeeper()
                #return 0
            else:
                print('Role Not Found')
        else:
            attempts = attempts + 1
            resp = None
            while (resp != 'Y' and resp != 'N') and attempts < 3:
                resp = input('Authentication Failed! Would you like to try again (Y/N)? ')
            if attempts >= 3:
                print('Too many attempts - Goodbye')
                quit = True
            if resp.upper() == 'N':
                quit = True

# This allows the .py function to be called from the terminal window

if __name__ == '__main__':
    zoo_authentication()