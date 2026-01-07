# komagataella

## Description

This package is for analyzing DNA sequence files from pPICZ and pGAPZ expression plasmids.
These plasmids are commonly used to express recombinant proteins in the yeast
*Komagataella phaffii* (*Pichia pastoris*). The program extracts the coding
sequence for the recombinant protein and produces a protein summary.

There are two major use cases:
1. Choosing a particular plasmid/protein from the DNA sequence database for detailed analysis.
2. Producing a nicely formated table that summarizes the entire DNA sequence database.

### Science Background
If you have no idea what this is about, welcome! *Komagataella phaffii* is one of the most-used
microorganisms for recombinant protein expression (it is a single-celled yeast). This means
that pieces of DNA--chemically synthesized or PCR generated from another organism's DNA--can be inserted inside the organism to
produce large amounts of the protein that it encodes. Trying to express foreign proteins this way does not
always work. But, with advances in genomics and chemical DNA synthesis, this method can be theoretically used
to produce any protein.

### Motivation
I have a collection of about 200 engineered strains of *Komagataella phaffii*, each of which
expresses a different protein. `komagataella` makes analysis of specific recombinant proteins quick and easy, and also enables creation of a summary table for entire databases.

### How komagataella works
All of the information is computed from simple text files called `fasta` files. Each file has a single header row followed by a series of rows of DNA sequence. When analyzing a single plasmid/protein, a single fasta file is used. When analyzing the entire DNA sequence database, all fasta files are used.


## Installation
```
1. git clone https://github.com/tnaums/komagataella.git
2. pip install -r requirements.txt
```

`komatagaella` is mostly written in base python. `biopython` is used for both calculating the isoelectric point (pI) and performing and parsing remote blastp. `great-tables` is used to create html tables.

## Usage
Example files (DNA sequence files of expression plasmids in fasta format) are included in `data/`. Each file is placed inside of a unique folder; for example: `data/pTAN121/pTAN121.fa`. New files can be added similarly. The DNA sequence fasta files must end in either `*.fa` or `*.fasta`. While use of the `data/` folder is hard coded, it can be changed to point to another location by editing `root = "data/"` line near the top of the main function in main.py.

To run the program, type `python3 main.py`. This will launch an interactive menu.


If a single plasmid/protein is selected, text output is produced:

```name: pTAN160_Esorghi_lactamase
promoter: aox1
secretion: alpha
coding sequence: ATGAGATTTCCTTCAATTTT...ATCATCATCATCATCATTGA (2203bp)


>pTAN160_Esorghi_lactamase
EFFPANQQDLTFAKRNGTFEQSVFYGLTGPEVEAKLAKLKADGYRPTSLNIHGSTSDAKY
AGIWTKQTGDDFETILGANKTVYDAWLDSHKAQGYVSTHVSATGGSSDALFAGVMEKVPS
VANWIQVCGLDNPYAYANATIDEPMYIKGVSMYGAPNERQYCILGHENLVNYQQTVFYQT
DYFKKDYAKLLQSETSKRHWRPVFIDLSEDLLPTPIFDDTSVGQWVARTDLSASELEAEI
AAQKAKNLYAVHIAGAGSKGSKYAVLFAEHLSPLERKWTVTGEVTGFKTNDVVAKDMDAV
MEEFMKKNSVRQAQVAASVNGTVVAERSYTWAESDRAVVKPTDKFGLGSVSKMFTYAATT
NLLNEGLLNHTTRVYPFLGMNNPADNRSLDITVDHLLQHTAGYNRDIKPDIGFIFRNIAL
ERNQTTPVSLRELIEYVYEQPLDFTPGTDSVYSNYGTMLLSYLIANITGESFNSYIHKNV
LNGLDVELYPTSPELNANNPIVQETKYTFYPAQDPASTKQVSNANGGDGSIREEAIGAFG
LRASASTISQFLANHAAYDIGPRQAYTYRDGTIVGSRAFAQSQDLIDWSLILNTREYESE
QKWEQLVFGPISQWYKYALAE

Mass: 69.00 kDa
Length: 621 amino acids
Not tagged
pI: 5.18

Press Enter to continue...
```

In single protein/plasmid mode, an optional blastp search can be performed. Since submitting and retrieving results from NCBI is slow, the results are written to `data/plasmid/plasmid.fa_blast.xml`. When present, a summary is shown automatically. Whether the results file exists or not, a new search can optionally be performed.

```
Checking for existing blastp results...

Found existing blastp results file...


 gb      QIR83317.1   kilbournase [Stenocarpella maydis]                   0.0
 gb    KAL2209420.1   subtilisin-like protein [Sarocladium st              0.0
 gb    KAH8171103.1   subtilase family protein [Sarocladium i              0.0
 gb    KAH7317069.1   peptidase S                                          0.0
ref  XP_046006235.1   peptidase S                                          0.0


Would you like to run/re-run blastp at ncbi? (Y/N) y

Running remote blastp against nr database...
```

If the entire database is selected, an html table is produced:

<img src="data/table.png">

