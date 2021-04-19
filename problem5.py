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
        "sequence_len" : 5,
        "range" : 50,
        "occurances" : 4
    }
    
    parser = argparse.ArgumentParser(
        description="""Finds patterns forming clumps in a string.""",
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
    parser.add_argument("--range", 
        type=int,
        default=defaults["range"],
        help="""Desired length of sliding window"""
    )
    parser.add_argument("--occurances", 
        type=int,
        default=defaults["occurances"],
        help="""Number of times you want to see a pattern occur"""
    )
    args = parser.parse_args()
    
    if as_dict:
        args = vars(args)
    return args

def clump_finder(genome, pattern_len, window, occurances):
    """
    Finds patterns of n length (pattern_len) that are clumped together in a 
    given genome sequence (window) t number of times (occurances).
    
    Parameters:
        genome - str
            whole genome nucleotide sequence.
        pattern_len - int
            length of nucleotide sequence.
        window - int
            desired length of sliding window.
        occurances - int
            number of times you want to see a pattern occur.
    Returns:
        clumping_seq - list
            nucleotide sequences that appear at least t times (occurances) in a
            speficied window
    """

    # Describe at a high level what method was used to solve the problem below..

    count = {}
    clumping_seqs = []
    for i in range(len(genome)-(pattern_len-1)):
        pattern = genome[i:pattern_len+i]
        
        if pattern in count:
            count[pattern] = count[pattern] + 1
        else:
            count[pattern] = 1
        
        if i == window:
            max_key = max(count, key=count.get)
            if count[max_key] >= occurances:
                clumping_seqs.append(max_key)
            
            # need to delete first key value pair in count because when window
            # is moved the first entry is no longer in bounds of the next widnow.
            del count[list(count.keys())[0]]

            window = window + 1
    # Specific comment about how you're achieving what you described above..
    clumping_seqs = list(set(clumping_seqs))
    return clumping_seqs

if __name__ == "__main__":
    args = parse_cmd_line(True)
    
    genome_file = args["genome_fname"]
    genome_file = open(genome_file)

    genome = genome_file.read().replace("\n", " ")
    genome_file.close()
    
    pattern_len = args["sequence_len"]
    window = args["range"]
    occurances = args["occurances"]

    clumping_seqs = clump_finder(genome, pattern_len, window, occurances)
    print("Sequence(s) that clump : ", clumping_seqs)
    print("Number of sequence(s) that clump : ", len(clumping_seqs))