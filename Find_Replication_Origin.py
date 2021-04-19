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
        "genome_fname" : "./Salmonella_enterica.txt",
        "pattern_len" : 9,
        "mismatches" : 1,
        "window" : 500
    }
    
    parser = argparse.ArgumentParser(
        description="""Finds possible DNA bounding box at origin of replication""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--genome_fname", 
        type=str,
        default=defaults["genome_fname"],
        help="""File containing genome."""
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
    parser.add_argument("--window", 
        type=int,
        default=defaults["window"],
        help="""Value to subtract and add to min position found using skew method"""
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
        skew - list
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
        len(pattern_index) - int
            number of times approx pattern occurs in genome

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

def approx_pattern(genome, pattern_len, mismatches):
    """
    Finds most frequent pattern(s) (pattern_len long) with fewer than n number of mismatches. 
    Pattern reverse compliments are included in the count.
    
    Parameters:
        genome - str
            whole genome nucleotide sequence
        pattern_len - int
            length of nucleotide sequence
        mismatches - int
            max amount of mismatches between genome and pattern allowed
    Returns:
        max_key_list - list of str
             nucleotide seq n nucleotides long (pattern_len) that occur most frequently

    """

    counts_dict = {}
    for i in range(len(genome) - pattern_len-1):
        seq = genome[i:pattern_len+i]
        
        # counting how many times seq appears in genome, allowing n mismatches
        forward_count = pattern_mismatch(genome, seq, mismatches)
        
        # finding reverse compliment and counting how often it occurs, allowing n mismatches
        reverse_comp = reverse_complement(seq)
        reverse_count = pattern_mismatch(genome, reverse_comp, mismatches)

        count = forward_count + reverse_count

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
    window = args["window"]

    skew = tally(genome)
    
    min_value = min(skew)
    min_list = [i for i, x in enumerate(skew) if x == min_value]
    
    bounding_box = {}
    for i in range(len(min_list)):
        genome_copy = genome
        if min_list[i] - window < 0 or min_list[i] + window > len(genome):
            # report an error
            x=9
        else:
            start = min_list[i] - window
            stop = min_list[i] + window
            genome_copy = genome_copy[start:stop]

            max_approx_seq = approx_pattern(genome_copy, pattern_len, mismatches)

            bounding_box["ori" + str(i)] = max_approx_seq

    print('Possible DNA bounding boxes allowing {} mismatch(es) : '.format(mismatches), 
    bounding_box)