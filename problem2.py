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
        "genome_fname" : "./Vibrio_cholerae.txt",
        "sequence_len" : 3
    }
    
    parser = argparse.ArgumentParser(
        description="""Finds the most frequent nucleotide sequence 
        (n letters long) in a genome.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--genome_fname", 
        type=str,
        default=defaults["genome_fname"],
        help="""File containing genome"""
    )
    parser.add_argument("--sequence_len", 
        type=int,
        default=defaults["sequence_len"],
        help="""Desired length of nucleotide sequence to look for"""
    )

    args = parser.parse_args()
    
    if as_dict:
        args = vars(args)
    return args

def pattern_frequency(genome, pattern_len):
    """
    Counts frequency of every nucleotide sequence (n letters long) in a genome.
    
    Parameters:
        genome - str
            whole genome nucleotide sequence.
        pattern_len - int
            length of nucleotide sequence.
    Returns:
        count - dict
            keys - sequence (str) n letters long (pattern_len) 
            values - number of times pattern found in genome
    """
    count = {}

    for i in range(len(genome)-(pattern_len-1)):
        pattern = genome[i:pattern_len+i]
        
        if pattern in count:
            count[pattern] = count[pattern] + 1
        else:
            count[pattern] = 1
        
    return count

if __name__ == "__main__":
    args = parse_cmd_line(True)
    
    genome_file = args["genome_fname"]
    genome_file = open(genome_file)

    genome = genome_file.read().replace("\n", " ")
    genome_file.close()
    
    pattern_len = args["sequence_len"]

    counts_dict = pattern_frequency(genome, pattern_len)
    max_key = max(counts_dict, key=counts_dict.get)

    max_key_list = []

    for key, value in counts_dict.items():
        if value == counts_dict[max_key]:
            max_key_list.append(key)
    
    # print(counts_dict)
    print('Most frequent sequence(s) in genome : ', max_key_list)
    print('Number of occurances : ', counts_dict[max_key])


    
