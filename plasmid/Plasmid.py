import re
from bcolors.bcolors import bcolors
from protein.Protein import Protein

class NotPichia(Exception):
    '''raise this exception if plasmid creation fails.'''
    pass


class Plasmid():
    '''
    Class that represents a single pPICZ or pGAPZ plasmid.
    '''
    def __init__(self, fasta_file, header, sequence):
        self.fasta_file = fasta_file
        self.header = header
        self.DNA = sequence
        self.promoter = self.get_promoter()
        self.coding_sequence = self.get_coding_DNA()
        self.secretion = self.secretion_check()
        self.mature_recombinant = self.get_mature_protein()
        self.protein = Protein(self.header, self.mature_recombinant)
        
    def get_promoter(self):
        '''
        Searches for methanol inducible aox1 promoter (pPICZ plasmids). If
        not found, looks for constitutive gap promoter (pGAPZ plasmids).
        '''
        aox1 = re.compile(r'AGATCTAACATC.{916}TTATTCGAAACG')
        gap = re.compile(r'AGATCTTTTTTG.{459}TTGAACAACTAT')
        if aox1.search(self.DNA):
            return 'aox1'
        if gap.search(self.DNA):
            return 'gap'
        raise NotPichia('Could not find aox1 or gap promoter')

    def get_coding_DNA(self):
        '''
        From plasmid sequence, returns DNA sequence of the recombinant
        protein coding region. Works with aox1 or gap promoters. 
        Assumes that protein is a fusion that ends after the plasmid-encoded 
        his tag, even if there is a stop codon.
        '''
        aox1_coding = re.compile(r'TTATTCGAAACG(.*)GTTTGTAGCCTT')
        gap_coding = re.compile(r'TATTTCGAAACG(.*)GTTTTAGCCTTA')
        if self.promoter == 'aox1':
            if match := aox1_coding.search(self.DNA):
                return match.group(1)
        if self.promoter == 'gap':
            if match := gap_coding.search(self.DNA):
                return match.group(1)
        raise NotPichia('Could not find coding sequence.')


    def secretion_check(self):
        '''
        Uses re to check for alpha factor secretion signal sequence
        and Ost1 variant. Returns 'alpha', 'ost1', or None.
        '''
        alpha = re.compile(r'ATGAGATTTCCT.*GAGGCTGAAGCT')
        ost1 = re.compile(r'ATGAGGCAGGTT.*GAGGCTGAAGCT')
        if alpha.search(self.DNA):
            return 'alpha'
        if ost1.search(self.DNA):
            return 'ost1'
        return 'cytoplasmic'

    
    def get_mature_protein(self):
        '''
        From the extracted coding sequence, which may contain unused
        C-terminal tag, and knowledge of the secretion signal 
        sequence (alpha, ost1, ''), return mature,recombinant 
        protein sequence.
        '''
        aa_to_stop = ''
        mature = ''
        genetic_code = {'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
                        'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
                        'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
                        'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
                        'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
                        'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
                        'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
                        'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
                        'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
                        'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
                        'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
                        'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
                        'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
                        'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
                        'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
                        'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
                        }

        if not self.coding_sequence:
            return None
        
        # Ensure in-frame start at ATG. some GAP cytoplasmic
        # sequences have extra nucleotides
        start_at_atg = re.compile(r'ATG.*')
        new_coding = start_at_atg.search(self.coding_sequence)
        self.coding_sequence = new_coding.group()
        for first, second, third in zip(
                self.coding_sequence[::3],
                self.coding_sequence[1::3],
                self.coding_sequence[2::3]
        ):
            codon = first + second + third
            codon = codon.upper()
            aa_to_stop = aa_to_stop + genetic_code[codon]
            if aa_to_stop.endswith('*'):
                break
        mature = aa_to_stop[:-1]
        if self.secretion == 'alpha':
            return mature[89:]
        if self.secretion == 'ost1':
            return mature[92:]
        return mature



    def print_fasta(self):
        '''
        Returns the mature recombinant protein in fasta format.
        '''
        printable = f'{bcolors.OKBLUE}>{self.header}{bcolors.ENDC}\n'
        sequence_string = ''
        for idx, aa in enumerate(self.mature_recombinant, start=1):
            sequence_string = sequence_string + aa
            if idx % 60 == 0:
                printable += sequence_string + '\n'
                sequence_string = ''
        printable += sequence_string + '\n'
        return printable

    
    def __repr__(self):
        return_str = ''
        return_str += f'name: {self.header}\n'
        return_str += f'promoter: {self.promoter}\n'
        return_str += f'coding sequence: {self.coding_sequence[:20]}'
        return_str += f'...{self.coding_sequence[-20:]}'
        return_str += f' ({len(self.coding_sequence)}bp)\n'
        return_str += self.print_fasta()
        return_str += '\n'
        return return_str
    
