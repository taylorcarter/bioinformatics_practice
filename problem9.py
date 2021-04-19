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
        "pattern_len" : 4,
        "mismatches" : 1
    }
    
    parser = argparse.ArgumentParser(
        description="""Finds the most frequent pattern(s) with approx the same seq""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--genome_fname", 
        type=str,
        default=defaults["genome_fname"],
        help="""File containing genome"""
    )
    parser.add_argument("--pattern_len", 
        type=int,
        default=defaults["pattern_len"],
        help="""Sample length of specified nucleotide sequence"""
    )
    parser.add_argument("--mismatches", 
        type=int,
        default=defaults["mismatches"],
        help="""Max amount of mismatches allowed"""
    )

    args = parser.parse_args()
    
    if as_dict:
        args = vars(args)
    return args

def pattern_mismatch(genome, pattern, mismatches):
    """
    Counts the number of times the approximate pattern is observed in genome.
    
    Parameters:
        genome - str
            whole genome nucleotide sequence. case sensitive
        pattern - str
            specified nucleotide sequence. case sensitive
        mismatches - int
            max amount of mismatches between genome and pattern allowed
    Returns:
        pattern_index - list
            positon(s) in genome where approx pattern is found

    """
    pattern_index = []
    
    for i in range(len(genome) - (len(pattern)-1)):
        j = 0
        count = 0
        while j < len(pattern):
            if genome[j] != pattern[j]:
                count += 1
            j += 1

        if count <= mismatches:
            pattern_index.append(i)

        genome = genome[1:]
    
    return len(pattern_index)

def approx_pattern(genome, pattern_len, mismatches):
    """
    Finds most frequent pattern(s) with fewer than n number of mismatches.
    
    Parameters:
        genome - str
            whole genome nucleotide sequence
        pattern_len - int
            length of nucleotide sequence
        mismatches - int
            max amount of mismatches between genome and pattern allowed
    Returns:
        frequent_patterns - list of str
             nucleotide seq n nucleotides long (pattern_len) that occur most frequently

    """
    
    counts_dict = {}
    for i in range(len(genome) - pattern_len-1):
        seq = genome[i:pattern_len+i]
        
        # counting how many times seq appears in genome, allowing n mismatches
        count = pattern_mismatch(genome, seq, mismatches)

        if seq not in counts_dict:
            counts_dict[seq] = count
    
    max_key = max(counts_dict, key=counts_dict.get)

    max_key_list = []

    for key, value in counts_dict.items():
        if value == counts_dict[max_key]:
            max_key_list.append(key)

    return max_key_list

if __name__ == "__main__":
    args = parse_cmd_line(True)
    
    genome_file = args["genome_fname"]
    genome_file = open(genome_file)

    genome = genome_file.read().replace("\n", " ")
    genome_file.close()

    pattern_len = args["pattern_len"]
    mismatches = args["mismatches"]

    max_approx_seq = approx_pattern(genome, pattern_len, mismatches)

    print('Most frequent sequence(s) in genome allowing {} mismatch(es) : '.format(mismatches), max_approx_seq)
