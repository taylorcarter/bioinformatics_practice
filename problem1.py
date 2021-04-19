import argparse
import os

def parse_cmd_line(as_dict=False):
    """
    Description:
        Parses the command line arguments for the program
    Parameters:
        as_dict - bool
            Returns the args as a dict. Default=False
    Returns:
        The command line arguments as a dictionary or a Namespace object and the
        parser used to parse the command line.
    """

    defaults = {
        "vibrio_genome_fname" : "./Vibrio_cholerae.txt",
        "promoter" : "ATG"
    }
    
    parser = argparse.ArgumentParser(
        description="""Counts user specified nucleotide sequence in genome""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--vibrio_genome_fname", 
        type=str,
        default=defaults["vibrio_genome_fname"],
        help="""File containing vibrio genome"""
    )
    parser.add_argument("--promoter", 
        type=str,
        default=defaults["promoter"],
        help="""Sample specified nucleotide sequence"""
    )

    args = parser.parse_args()
    
    if as_dict:
        args = vars(args)
    return args

def pattern_count(genome, pattern):
    """
    Counts number of times specfied nucleotide sequence is observed in 
    genome.
    
    Parameters:
        genome - str
            whole genome nucleotide sequence. case sensitive
        pattern - str
            specified nucleotide sequence. case sensitive
    Returns:
        count - int
            Number of times pattern is observed in genome
    """
    count = 0
    for i in range(len(genome)):
        if len(genome[i:(len(pattern)+i)]) < len(pattern):
            break

        if genome[i:(len(pattern)+i)] == pattern:
            count = count + 1
    return count

if __name__ == "__main__":
    args = parse_cmd_line(True)
    
    genome_file = args["vibrio_genome_fname"]
    genome_file = open(genome_file)

    genome = genome_file.read().replace("\n", " ")
    genome_file.close()

    promoter = args["promoter"]

    print(pattern_count(genome, promoter))
    
