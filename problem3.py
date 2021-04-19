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
        "genome_fname" : "./test_genome.txt",
    }
    
    parser = argparse.ArgumentParser(
        description="""Finds the reverse complement of a nucleotide sequence""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--genome_fname", 
        type=str,
        default=defaults["genome_fname"],
        help="""File containing genome sequence"""
    )

    args = parser.parse_args()
    
    if as_dict:
        args = vars(args)
    return args

def reverse_complement(forward_sequence):
    """
    Generates the reverse complement of a nucleotide sequence
    
    Parameters:
        forward_sequence - str
            nucleotide sequence.
    Returns:
        rev_comp - str
            the reverse complement of the input nucleotide sequence
            
    """
    complement = forward_sequence.replace('A', '%temp%').replace('T', 'A').replace('%temp%', 'T')
    complement = complement.replace('G', '%temp%').replace('C', 'G').replace('%temp%', 'C')

    rev_comp = complement[::-1]

    return rev_comp

if __name__ == "__main__":
    args = parse_cmd_line(True)
    
    genome_file = args["genome_fname"]
    genome_file = open(genome_file)

    genome = genome_file.read().replace("\n", " ")
    genome_file.close()
    
    print('Original sequence : ', genome)
    print('Reverse complement sequence : ', reverse_complement(genome))