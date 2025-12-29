import os
from bcolors.bcolors import bcolors

def greeting():
    '''
    Prints a greeting at the top of the page.
    '''
    # Prepare to print at the top of the page
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print the menu
    print()
    print(f'{bcolors.OKGREEN}Welcome to the expression plasmid', end='')
    print(f' analyzer!{bcolors.ENDC}')

def goodbye():
    '''
    Prints a goodbye message.
    '''
    print()
    print(f'{bcolors.OKGREEN}Thank you for using the expression ', end='')
    print(f'plasmid analyzer!{bcolors.ENDC}')
    print()

def menu():
    '''
    Prints a menu and returns the selection as an integer.
    '''
    print()
    print('=======================================')
    print('1 - Make an object from a plasmid in')
    print(f'   {bcolors.OKBLUE}data{bcolors.ENDC} folder.')
    print('9 - Quit.')
    print('=======================================')
    print()
    while True:
        try:
            return int(input('What would you like to do? '))
        except ValueError:
            print('Not a valid selection. Please enter an integer.')
    
def main():
    greeting()
    root = "data"
    while True:
        selection = menu()
        if selection == 1:
            print(f"That is an interesting choice...")
        elif selection == 9:
            goodbye()
            break
        else:
            print('Not a valid choice. Please try again.')


if __name__ == "__main__":
    main()
