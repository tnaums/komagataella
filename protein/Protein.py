import re
import os
from Bio.SeqUtils.IsoelectricPoint import IsoelectricPoint as IP
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

class Protein():
    """Protein object from header and sequence."""

    def __init__(self, path, fasta_file, header, amino_acids):
        self.path = path
        self.fasta_file = fasta_file
        self.header = header
        self.amino_acids = amino_acids
        self.length = len(amino_acids)
        self.mw = self.mass(amino_acids)
        self.tag = self.check_tag_anywhere()
        self.pI = self.get_pI()
        self.blast = False
        self.identifier = ""
        self.description = ""
        self.organism = ""
        self.evalue = ""
        
    def mass(self, amino_acids):
        """
        Returns the monoisotopic mass for a protein or peptide.
        """
        CONSTANT = 18.000
        mass_dict = {
            'A': 71.03711,
            'R': 156.10111,
            'N': 114.04293,
            'D': 115.02694,
            'C': 103.00919,
            'Q': 128.05858,
            'E': 129.04259,
            'G': 57.02146,
            'H': 137.05891,
            'I': 113.08406,
            'L': 113.08406,
            'K': 128.09496,
            'M': 131.04049,
            'F': 147.06841,
            'P': 97.05276,
            'S': 87.03203,
            'T': 101.04768,
            'W': 186.07931,
            'Y': 163.06333,
            'V': 99.06841,
            }
        protein_mass = CONSTANT
        for residue in amino_acids:
            protein_mass = protein_mass + mass_dict[residue]
        return protein_mass / 1000
        
    def check_tag_anywhere(self):
        '''
        Checks protein sequence for a His tag.
        '''
        tag_re = re.compile(r'HHHHHH')
        if not self.amino_acids:
            return False
        if tag_re.search(self.amino_acids):
            return True
        else:
            return False


    def get_pI(self):
        '''
        Uses biopython method to calculate and return the pI of
        self.mature_recombinant.
        '''
        protein = IP(self.amino_acids)
        return protein.pi()


    def check_blast(self):
        '''
        Check if blast output file exists for a plasmid. If it does,
        set values for self.identifier, self.description, self.organism
        from the top hit by calling self.parse_blast(). Returns True or 
        False.
        '''
        blast_file_out = f'{self.path}/{self.fasta_file}_blast.xml'
        if os.path.isfile(blast_file_out):
            self.parse_blast()
            return True
        else:
            print('Blast file not found.')
        return False


    
    def parse_blast(self):
        '''
        Extracts and returns identifier, description, and organism for the top
        blastp hit.
        '''
        alignment_parser = re.compile(r'\|([A-Z_.0-9]*)\|[ ]{0,1}(.*?)\[(.*?)\]')
        blast_file_out = f'{self.path}/{self.fasta_file}_blast.xml'
        result_handle = open(blast_file_out)
        blast_record = NCBIXML.read(result_handle)
        if blast_record.alignments:
            top_alignment = blast_record.alignments[0]
            title_match =  alignment_parser.search(top_alignment.title)
            identifier, description, organism = title_match.groups()
            self.identifier = identifier.strip()
            self.description = description.strip()
            self.organism = organism.strip()
        else:
            print('No alignments found in {blast_file_out}.')

    def print_blast(self):
        '''
        Print summary for top blastp hits.
        '''
        description_parser = re.compile(r'^(\w{2,4})\|([\S]*)\|([^>0-9]*).+\s([0-9.]*)$')
        blast_file_out = f'{self.path}/{self.fasta_file}_blast.xml'
        result_handle = open(blast_file_out)
        blast_record = NCBIXML.read(result_handle) # <class 'Bio.Blast.NCBIXML.Blast'>
        for idx, description in enumerate(blast_record.descriptions):
            desc_str = str(description)
            evalue_match = description_parser.search(desc_str)
            try:
                groups = evalue_match.groups()
                print(f'{groups[0]:>3} {groups[1].strip():>15}   {groups[2][:40].strip():<40} {groups[3].strip():>15}')
            except AttributeError:
                print(description)
            if idx == 4:
                break
        # if blast_record.alignments:
        #     for idx, alignment in enumerate(blast_record.alignments):
        #         print(f'{idx:>3} {alignment}')
        #         title_match = alignment_parser.search(alignment.title)
        #         identifier, description, organism = title_match.groups()
        #         print(f'{idx + 1:>3}. {identifier:>15}\t{description[:40]:<40}\t{organism:<35}\t')
        #         if idx == 5:
        #             break

    def run_blast(self):
        '''
        Run blastp with self.amino_acids as query against the
        refseq_protein database.
        '''
        print()
        print('Running remote blastp against nr database...')
        print()
        result_handle = NCBIWWW.qblast('blastp', 'nr', self.amino_acids)
        blast_file_out = f'{self.path}/{self.fasta_file}_blast.xml'

        with open(blast_file_out, 'w') as out_handle:
            out_handle.write(result_handle.read())
            print(f'Wrote blast_file_out: {blast_file_out}')            
        result_handle.close()

    
    def __repr__(self):
        return f'Protein: {self.header}\nSequence: {self.amino_acids}\nMass: {self.mw/1000:>5.2f} kDa'

    def __str__(self):
        '''Print header and sequence in fasta format'''
        return_str = f'>{self.header}\n'
        for idx, residue in enumerate(self.amino_acids, start=1):
            return_str += residue
            if idx % 60 == 0:
                return_str = return_str + '\n'
        return_str += '\n\n'
        return_str += f'Mass: {self.mw:>5.2f} kDa\n'
        return_str += f'Length: {self.length} amino acids\n'
        if self.tag:
            return_str += 'His tag is present\n'
        else:
            return_str += 'Not tagged\n'
        return_str += f'pI: {self.pI:.2f}'
        return return_str
        
