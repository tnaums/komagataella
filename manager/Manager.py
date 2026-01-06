import os
import re
import pandas as pd
from great_tables import GT, style, loc, md
from bcolors.bcolors import bcolors
from plasmid.Plasmid import Plasmid
from plasmid.Plasmid import NotPichia

class Manager():

    def __init__(self):
        '''
        Manager class object that manages Plasmid objects. Stores
        them in a dictionary with integer keys, starting at zero.
        '''
        # This is a hack; single analysis uses a dict with key always
        # set to 0. Only one object exists in dict
        self.plasmids_dict = {}
        self.next_number = 0
        # List is for analysis of all plasmids in the library. Plasmid
        # objects are created and inserted
        self.plasmids_list = []
        # A list of lists that assembles data needed for pandas df
        # from the plasmid objects. Used to create great-tables table.
        self.pandas_list = []

    def create_object(self, root):
        '''
        Creates Plasmid objects and inserts them into the Manager dictionary.
        '''
        while True:
            # Interactively decide which plasmid to use.
            subfolder = select_subfolder(root)
            # Find the fasta file for the expression plasmid.
            fasta_file = select_file(f'{root}{subfolder}')
            if fasta_file == None:
                print(f'No fasta files found for {subfolder}')
                input('\nPress Enter to continue.')
            else:
                break
        chosen_file = f'{root}{subfolder}/{fasta_file}'
        # Open file, get header and sequence
        header, sequence = single_fasta_parser(chosen_file)
        # Create plasmid object
        try:
            oPlasmid = Plasmid(fasta_file, header, sequence)
            self.plasmids_dict[self.next_number] = oPlasmid            
        except NotPichia:
            print('Not a pichia expression plasmid.')
            input('Press Enter to continue...')
            self.create_object(root)

    def print_object(self):
        '''
        Prints analysis summary for object
        '''
        os.system('cls' if os.name == 'nt' else 'clear')        
        print(self.plasmids_dict[0])
        print(self.plasmids_dict[0].protein)
        input('\nPress Enter to continue...')

    def create_all_objects(self, root):
        '''
        Creates Plasmid objects for the entire database in root folder.
        '''
        # Reset the list, in case it was used previously
        self.plasmids_list = []
        self.pandas_list = []
        folders = get_folders(root)
        print(folders)
        for folder in folders:
            fasta_file = select_file_automatic(f'{root}{folder}')
            if not fasta_file:
                continue
            chosen_file = f'{root}{folder}/{fasta_file}'
 #           name = chosen_file[30:37]
            # Open file, get header and sequence
            header, sequence = single_fasta_parser(chosen_file)
            # Create the object
            try:
                oPlasmid = Plasmid(chosen_file, header, sequence)
                self.plasmids_list.append(oPlasmid)                
            except NotPichia:
                continue


    def prepare_for_pandas(self, chosen_list):
        self.pandas_list = []    # Clear any previous list
        for plasmid in chosen_list:
            if plasmid.protein.tag:
                tag = '+'
            else:
                tag = ''
            self.pandas_list.append([plasmid.header, plasmid.promoter, plasmid.secretion, tag, plasmid.protein.mw, plasmid.protein.pI])
        return

    def create_df(self):
        self.plasmids_df = pd.DataFrame(self.pandas_list, columns=['plasmid', 'promoter', 'SSS', 'tag', 'kDa', 'pI'])
        return


    def create_table(self):
        self.table = (
            GT(self.plasmids_df, rowname_col='plasmid')
            .tab_header(
                title=md('**Expression Plasmids**'),
            )
            .fmt_number(columns=['kDa', 'pI'], decimals=1)
            .tab_spanner(
                label='',
                columns=['plasmid', 'promoter', 'SSS', 'tag', 'kDa', 'pI']
            )
            .tab_style(
                style=style.text(size='22px', align='center'),
                locations=loc.body(
                    columns='tag',
                    )
                )
            .tab_style(
                style=style.fill(color='lightblue'),
                locations=loc.body(
                    columns='SSS',
                    rows=lambda frame: frame['SSS'] == 'cytoplasmic',
                )
            )
            .data_color(
                columns=['kDa'],
                palette=['rebeccapurple', 'white', 'orange'],
                na_color='white',
                domain=[116, 8],
            )
            .tab_style(
                style=style.text(color='green', weight='bold'),
                locations=loc.body(
                columns='tag',
                rows=lambda frame: frame['tag'] == True,
                )
            )
            .tab_style(
                style=style.fill(color='#F9E3D6'),
                locations=loc.body(
                columns='promoter',
                rows=lambda frame: frame['promoter'] == 'gap',
                )
            )
#        .opt_stylize(style=1)# color='blue') 6,3,1
        )
        self.table.show()
    
            

def select_subfolder(root_directory):
    '''
    Takes a folder, sorts and prints subfolders, then allows user
    selection. Returns the chosen subfolder.
    '''
            
    # Prepare to print at the top of the page    
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print(f'Entering {root_directory}')
    print()
    walker = os.walk(root_directory)
    root_dirs_files = next(walker)
    subfolders = root_dirs_files[1]
    subfolders.sort()
    for idx, subfolder in enumerate(subfolders):
        print(f'{idx:>3}. {subfolder}')
    folder_choice = int(input('Choose a folder. (input integer) '))
    return subfolders[folder_choice]        


def select_file(root_directory):
    '''
    Prints files from a given folder. Initially tries to find
    and return expected file ending in `fa` or `fasta`
    '''
    # Prepare to print at the top of the page
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{bcolors.OKGREEN}Entering {root_directory}{bcolors.ENDC}')
    print()
    fasta_files = []
    for file in os.listdir(root_directory):
        if file.endswith('fa') or file.endswith('fasta'):
            fasta_files.append(file)

    if len(fasta_files) > 0:
        print('=======================================')
        for idx, file in enumerate(fasta_files):
            print(f'{idx:>3}. {file}')
        print('=======================================')
    else:
        print('Fasta file not found.')
        return None
    while True:
        try:
            file_choice = int(input('What file do you want to analyze? (input integer) '))
            break
        except ValueError:
            print('Please try again.')
    return fasta_files[file_choice]

def select_file_automatic(root_directory):
    '''
    Initially tries to find and return a single file ending in `fa` 
    or `fasta`. If no file is found, returns None. If more than one file,
    asks user for manual selection.
    '''
    # Prepare to print at the top of the page
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{bcolors.OKGREEN}Entering {root_directory}{bcolors.ENDC}')
    print()
    fasta_files = []
    for file in os.listdir(root_directory):
        if file.endswith('fa') or file.endswith('fasta'):
            fasta_files.append(file)
    if len(fasta_files) == 1:
        return fasta_files[0]
    elif len(fasta_files) == 0:
        print('Fasta file not found.')
        return None
    else:
        print('=======================================')
        for idx, file in enumerate(fasta_files):
            print(f'{idx:>3}. {file}')
        print('=======================================')
    while True:
        try:
            file_choice = int(input('What file do you want to analyze? (input integer) '))
            break
        except ValueError:
            print('Please try again.')
    return fasta_files[file_choice]


def single_fasta_parser(fasta_file):
    '''
    Opens a file with a single fasta sequence, parses the header and
    sequence, then returns both as strings.
    '''
    sequence = ''
    with open(fasta_file, 'rt', encoding='utf-8') as fastafile:
        first_line = fastafile.readline().rstrip()
        header = first_line[1:]
        for line in fastafile.readlines():
            sequence = sequence + line.rstrip()
    return (header, sequence)

def get_folders(root_directory):
    '''
    Given root folder with plasmid files, returns a list of plasmid 
    folders named pTAN___.
    '''
    # Prepare to print at the top of the page
    os.system('cls' if os.name == 'nt' else 'clear')
#    pTAN_finder = re.compile(r'^pTAN\d{3}')
    print()
    print(f'Entering {root_directory}')
    print()
    walker = os.walk(root_directory)
    root_dirs_files = next(walker)
    subfolders = []
    for folder in root_dirs_files[1]:
        subfolders.append(folder)
    subfolders.sort()
    return subfolders


