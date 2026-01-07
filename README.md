# komagataella

## Description

This package is for analyzing DNA sequence files from pPICZ and pGAPZ expression plasmids.
These plasmids are commonly used to express recombinant proteins in the yeast
*Komagataella phaffii* (*Pichia pastoris*). The program extracts the coding
sequence for the recombinant protein and produces a protein summary.

There are two major use cases:
1. Choosing a particular plasmid/protein from the DNA sequence database for detailed analysis.
2. Producing a nicely formated table that summarizes the entire DNA sequence database.


## Installation
Steps to install and run your project.

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

If the entire database is selected, a table is produced:

<img src="data/table.png">

