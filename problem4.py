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
        "specified_seq" : "ATG"
    }
    
    parser = argparse.ArgumentParser(
        description="""Identifies position(s) of specific nucleotide sequence in genome.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--genome_fname", 
        type=str,
        default=defaults["genome_fname"],
        help="""File containing genome"""
    )
    parser.add_argument("--specified_seq", 
        type=str,
        default=defaults["specified_seq"],
        help="""Sample specified nucleotide sequence"""
    )

    args = parser.parse_args()
    
    if as_dict:
        args = vars(args)
    return args

def seq_position(genome, specified_seq):
    """
    Identifies position(s) of specific nucleotide sequence in genome

    Parameters:
        genome - str
            whole genome nucleotide sequence. case sensitive
        specified_seq - str
            specified nucleotide sequence. case sensitive
    Returns:
        pos - list
            list of positions specified nucleotide sequence occures in genome
    """
    pos = []
    for i in range(len(genome)-(len(specified_seq)-1)):
        if genome[i:(len(specified_seq)+i)] == specified_seq:
            pos.append(i)
    return pos

if __name__ == "__main__":
    args = parse_cmd_line(True)
    
    genome_file = args["genome_fname"]
    genome_file = open(genome_file)

    genome = genome_file.read().replace("\n", " ")
    genome_file.close()

    specified_seq = args["specified_seq"]

    print('Looking for : ', specified_seq)
    print('Found in position(s) : ', seq_position(genome, specified_seq))