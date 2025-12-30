import os
import re
from bcolors.bcolors import bcolors

class Manager():

    def __init__(self):
        '''
        Manager class object that manages Plasmid objects. Stores
        them in a dictionary with integer keys, starting at zero.
        '''
        self.plasmids_dict = {}
        self.next_number = 0


    def create_object(self, root):
        '''
        Creates Plasmid objects and inserts them in the Manager dictionary.
        '''
        # Interactively decide which plasmid to use.
        subfolder = select_subfolder(root)
        # Find the fasta file for the expression plasmid.
        fasta_file = select_file(f'{root}{subfolder}')
        chosen_file = f'{root}{subfolder}/{fasta_file}'
        # Open file, get header and sequence
        header, sequence = single_fasta_parser(chosen_file)
        print(f'Header: {header}')
        print(f'Sequence: {sequence}')
        # Search sequence for promoter
        promoter = get_promoter(sequence)
        print(f'\n\nThe promoter is: {promoter}')
        # # Create specific plasmid object type that depends on above analysis
        # if promoter == 'aox1' or promoter == 'gap':
        #     oPlasmid = pichia_plasmid(name,header, sequence, promoter)
        #     self.pichia_list.append(oPlasmid)
        #     self.combined_list.append(oPlasmid)
        #     print(oPlasmid)
        # elif promoter == 'T7' or promoter == 'ara':
        #     oPlasmid = ecoli_plasmid(name,header, sequence, promoter)
        #     self.ecoli_list.append(oPlasmid)
        #     self.combined_list.append(oPlasmid)
        #     print(oPlasmid)
        # else:
        #     None


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
    and return expected file like 'pTAN167.fa'. If not, the 
    fasta files that end with 'fa' are displayed for manual
    selection. 
    '''
    # Prepare to print at the top of the page
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{bcolors.OKGREEN}Entering {root_directory}{bcolors.ENDC}')
    print()
    fasta_files = []
    for file in os.listdir(root_directory):
        if file.endswith('fa') or file.endswith('fasta'):
            fasta_files.append(file)
    print('=======================================')
    if fasta_files:
        for idx, file in enumerate(fasta_files):
            print(f'{idx:>3}. {file}')
    else:
        print('No fasta files found (*.fa)')
        return None
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

def get_promoter(sequence):
    '''
    Searches for methanol inducible aox1 promoter (pPIC plasmids). If
    not found, looks for constitutive gap promoter (pGAP plasmids).
    '''
    aox1 = re.compile(r'AGATCTAACATC.{916}TTATTCGAAACG')
    gap = re.compile(r'AGATCTTTTTTG.{459}TTGAACAACTAT')
    if aox1.search(sequence):
        return 'aox1'
    if gap.search(sequence):
        return 'gap'
    return None
