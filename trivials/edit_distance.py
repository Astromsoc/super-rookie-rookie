"""
    Function to calculate and visualize edit distance 
        for string / blank-separated sentence comparison.

    Written by: 
        Astromsoc (schen4@andrew.cmu.edu)
    Last Updated at:
        Sep 1, 2022

    ---

    Featuring:
        - controllable layout loose level
        - controllable display automation

    Upcoming:
        - error path(s) reconstruction
"""


def get_edit_distance(
        hyp,                     # iterable, row-based, hypothesis
        ref,                     # iterable, col-based, reference
        verbose: bool=True,      # whether to display intermediate results
        loose_level: int=1       # how many blanks added in the table
    ):

    # set blank sepearators based on given loose level
    loose_level = max(1, loose_level)
    blanks = ' ' * loose_level

    # max length of words if inputs are lists
    if isinstance(hyp, list):
        hyp_maxlen = max(map(len, hyp))
        ref_maxlen = max(map(len, ref + ['[REF]\[HYP]']))
    else:
        hyp_maxlen, ref_maxlen = 1, len('[REF]\[HYP]')
    
    # consider both ref words' len & cnt len for horizontal alignment
    horizontal_maxlen = max(hyp_maxlen, len(str(max(len(hyp), len(ref)))))

    # print the inputs & formatted hypothesis header
    if verbose:
        hyp_str = hyp if isinstance(hyp, str) else ' '.join(hyp)
        ref_str = ref if isinstance(ref, str) else ' '.join(ref)
        print(
            f'\n[Reference]:  {ref_str}\n' +
            f'[Hypothesis]: {hyp_str}\n\n' +
            "[REF]\[HYP]".ljust(
                ref_maxlen +                                        # first col of ref units
                horizontal_maxlen + 2 +                             # added unit for hyp at the start (& " |")
                2 * loose_level                                     # 2 separator blanks in-between
            ) + 
            blanks.join([str(i).rjust(horizontal_maxlen) for i in hyp]) + '\n' +
            ' ' * (ref_maxlen + 2) +                                # first col of ref units & " |"
            '-' * (
                (len(hyp) + 1) * horizontal_maxlen +                # upcoming hyp units
                loose_level * (len(hyp) + 1)                        # seperator blanks
            )
        )

    # current row
    curr = list(range(len(hyp) + 1))

    # iterate over units in hypothesis
    for i in range(len(ref)):
        
        # update the previous row
        prev = curr

        # print the row if wanted
        if verbose:
            ref_unit = (
                str(ref[i - 1]).rjust(ref_maxlen) if i > 0          # ref units
                else " " * ref_maxlen                               # placeholder in row 0
            )
            print(
                f"{ref_unit} |{blanks}" +
                blanks.join([str(i).rjust(horizontal_maxlen) for i in prev])
            )

        # spare a new list for the current row
        curr = [0] * len(curr)

        # iterate over units in reference
        for j in range(len(curr)):
            
            # 3 scenarios
            curr[j] = min(
                (prev[j - 1] + int(hyp[j - 1] != ref[i]) 
                 if j > 0 else float('inf')),                   # substitution
                 prev[j] + 1,                                   # deletion
                 curr[j - 1] + 1 if j > 0 else float('inf')     # insertion
            )
    
    if verbose:
        print(
            f"{str(ref[i]).rjust(ref_maxlen)} |{blanks}" +
            blanks.join([str(i).rjust(horizontal_maxlen) for i in curr])
        )
    
    # print out the final edit distance
    print(f"\nEdit Distance: {curr[-1]}\n\n")
        
    return curr[-1]



if __name__ == '__main__':

    """
        String Comparisons, looser layout
    """

    ref1 = 'hdjakhdjks'
    hyp1 = 'dajdjksanjksa'

    get_edit_distance(
        ref=ref1, 
        hyp=hyp1, 
        loose_level=2
    )
    

    """
        (Blank-Separated) Sentence Comparisons, tighter layout
    """

    ref2 = 'I want to go to the CMU campus'.split(' ')
    hyp2 = 'I want to go to I want to go to I want to go to the CMU campus'.split(' ')

    get_edit_distance(
        ref=ref2, 
        hyp=hyp2, 
        loose_level=1
    )
    