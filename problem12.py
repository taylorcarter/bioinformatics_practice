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
        "pattern" : "ACG",
        "mismatches" : 1
    }
    
    parser = argparse.ArgumentParser(
        description="""Generates patterns (using 'pattern') with n mismatches allowed""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--pattern", 
        type=str,
        default=defaults["pattern"],
        help="""Sample specified nucleotide sequence"""
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

def generator(pattern, mismatches):
    """
    Generates all possible patterns with n mismatches allowed using 'pattern'
    
    Parameters:
        pattern - str
            specified nucleotide sequence. case sensitive
        mismatches - int
            max amount of mismatches between pattern and generated pattern allowed
    Returns:
         - list
            all patterns possible with n mismatches allowed

    """
    bases = [ "A", "C", "T", "G"]
    pattern = list(pattern)
    poss_patterns = []
    for i in range(len(pattern)):
        pattern_copy = pattern.copy()
        for b in range(len(bases)):
            if bases[b] != pattern[i]:
                pattern_copy[i] = bases[b]
                new_pattern = "".join(pattern_copy)
                poss_patterns.append(new_pattern)
    return poss_patterns

if __name__ == "__main__":
    args = parse_cmd_line(True)
    pattern = args["pattern"]
    mismatches = args["mismatches"]

    poss_patterns = generator(pattern, mismatches)

    print("All possible patterns allowing {} mismatch(es) of {} : ".format(mismatches, pattern) , poss_patterns)