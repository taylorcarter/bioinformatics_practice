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
        description="""Finds 'skew' of a nucleotide sequence""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--genome_fname", 
        type=str,
        default=defaults["genome_fname"],
        help="""File containing genome"""
    )

    args = parser.parse_args()
    
    if as_dict:
        args = vars(args)
    return args

def tally(genome):
    """
    Finds skew of nucleuotide sequence.
    
    Parameters:
        genome - str
            whole genome nucleotide sequence.
    Returns:
         - list
            ints
    """
    skew = [0]
    for i in range(len(genome)):
        if genome[i] == 'C':
            count = skew[i] - 1
        elif genome[i] == 'G':
            count = skew[i] + 1
        else:
            count = skew[i] + 0

        skew.append(count)
    return skew

if __name__ == "__main__":
    args = parse_cmd_line(True)
    
    genome_file = args["genome_fname"]
    genome_file = open(genome_file)

    genome = genome_file.read().replace("\n", " ")
    genome_file.close()

    skew = tally(genome)

    print(skew)