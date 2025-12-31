import re

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
    
