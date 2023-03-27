"""
    Function to calculate and visualize edit distance 
        for string / blank-separated sentence comparison.

    Written by: 
        Astromsoc (schen4@andrew.cmu.edu)
    Last Updated at:
        Mar 27, 2023

    ---

    Featuring:
        - controllable layout loose level
        - controllable display automation
        - error path(s) reconstruction
"""

import re
from string import punctuation
ADDITIONAL_PUNCTUATIONS = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."


def prep(
        raw: str
    ):
    """
        Function to preprocess the input string
    """
    # remove punctuations & down to lower case
    raw = re.sub(f"[{punctuation}{ADDITIONAL_PUNCTUATIONS}]", ' ', raw).lower()
    # handle repetitive white spaces
    cooked, i = '', 0
    while i < len(raw):
        cooked += raw[i]
        if raw[i] != ' ':
            i += 1
        else:
            j = i + 1
            while j < len(raw) and raw[j] == ' ':
                j += 1
            i = j
    return cooked.strip()
    


def get_edit_distance(
        hyp,                     # str, row-based, hypothesis
        ref,                     # str, col-based, reference
        verbose: bool=True,      # whether to display intermediate results
        loose_level: int=1,      # how many blanks added in the table
        use_cer: bool=False,     # treat the inputs as characters (white spaces considered)
        use_ser: bool=False,     # treat the inputs as a unity
        preprocess: bool=True,   # whether to remove punctuations & unify cases
        show_trace: bool=False   # whether to show potential error paths
    ):

    # set blank sepearators based on given loose level
    loose_level = max(1, loose_level)
    blanks = ' ' * loose_level

    # modify inputs based on given flags
    if preprocess:
        ref, hyp = prep(ref), prep(hyp)
    if use_ser:
        refs, hyps = [ref], [hyp]
    else:
        refs, hyps = (
            (list(ref), list(hyp)) if use_cer else 
            (ref.split(' '), hyp.split(' '))
        )

    # max length of words if inputs are lists
    hyp_maxlen = max(map(len, hyps))
    ref_maxword = max(map(len, refs))
    ref_maxlen = max(ref_maxword, len('[REF]\[HYP]'))
    
    # consider both ref words' len & cnt len for horizontal alignment
    horizontal_maxlen = max(hyp_maxlen, len(str(max(len(hyps), len(refs)))))

    # print the inputs & formatted hypothesis header
    if verbose:
        print(
            f'\n[Reference]:  {ref}\n' +
            f'[Hypothesis]: {hyp}\n\n' +
            "[REF]\[HYP]".ljust(
                ref_maxlen +                                                        # first col of ref units
                horizontal_maxlen + 2 +                                             # added unit for hyp at the start (& " |")
                2 * loose_level                                                     # 2 separator blanks in-between
            ) + 
            blanks.join([str(i).rjust(horizontal_maxlen) for i in hyps]) + '\n' +
            ' ' * (ref_maxlen + 2) +                                                # first col of ref units & " |"
            '-' * (
                (len(hyps) + 1) * horizontal_maxlen +                               # upcoming hyp units
                loose_level * (len(hyps) + 1)                                       # seperator blanks
            )
        )

    if show_trace:

        edit_matrix = [list(range(len(hyps) + 1)) for _ in range(len(refs) + 1)]

        # show first row
        print(
            f"{' '.rjust(ref_maxlen)} |{blanks}" +
            blanks.join([str(k).rjust(horizontal_maxlen) for k in edit_matrix[0]])
            )

        # iterate over units in hypothesis
        for i in range(1, len(refs) + 1):
            
            # iterate over units in reference
            for j in range(len(hyps) + 1):
                edit_matrix[i][j] = min(
                        (edit_matrix[i - 1][j - 1] + int(hyps[j - 1] != refs[i - 1]) 
                            if j > 0 else float('inf')),                                # substitution
                        edit_matrix[i - 1][j] + 1,                                      # deletion
                        edit_matrix[i][j - 1] + 1 if j > 0 else float('inf')            # insertion
                    )
            
            # print the row if wanted
            if verbose:
                ref_unit = str(refs[i - 1]).rjust(ref_maxlen)                 
                print(
                    f"{ref_unit} |{blanks}" +
                    blanks.join([str(k).rjust(horizontal_maxlen) for k in edit_matrix[i]])
                )
        
        # print out the final edit distance
        print(f"\nEdit Distance: {edit_matrix[-1][-1]}")

        # print out WER / CER / SER
        prefix = 'Sentence' if use_ser else 'Character' if use_cer else 'Word'
        print(f"{prefix} Error Rate: {(edit_matrix[-1][-1] / len(refs)) * 100:.4f}%\n")

        # backtrace to obtain error paths
        error_paths = list()

        # function to backtrace & reconstruct error paths
        def trace_back(
                i: int,
                j: int,
                later_errors: str
            ):
            if i == 0 and j == 0:
                # value conversion dictionary
                vals = {'I': 1, 'S': 0, 'D': -1, ' ': 0}
                assert len(refs) + sum([vals[u] for u in later_errors]) == len(hyps)
                error_paths.append(list(later_errors))
            if i > 0:
                # deletion
                if edit_matrix[i][j] == edit_matrix[i - 1][j] + 1:
                    trace_back(i - 1, j, f"D{later_errors}")
            if j > 0:
                # insertion
                if edit_matrix[i][j] == edit_matrix[i][j - 1] + 1:
                    trace_back(i, j - 1, f"I{later_errors}")
            if i > 0 and j > 0:
                # substitution
                if edit_matrix[i][j] == edit_matrix[i - 1][j - 1] + int(hyps[j - 1] != refs[i - 1]):
                    mark = 'S' if hyps[j - 1] != refs[i - 1] else ' '
                    trace_back(i - 1, j - 1, f"{mark}{later_errors}")
            
        # run the back tracing
        trace_back(len(refs), len(hyps), '')

        # display the result 
        for i, u in enumerate(error_paths):
            new_refs, new_hyps = list(), list()
            new_error_path = list()
            idx_refs, idx_hyps = 0, 0
            for j, uu in enumerate(u):
                longer_len = -1                         # initiation
                if uu in {'S', ' '}:
                    longer_len = max(
                        len(refs[idx_refs]),
                        len(hyps[idx_hyps])
                    )
                    new_refs.append(refs[idx_refs].rjust(longer_len))
                    new_hyps.append(hyps[idx_hyps].rjust(longer_len))
                    idx_refs += 1
                    idx_hyps += 1
                elif uu == 'I':
                    longer_len = len(hyps[idx_hyps])
                    new_refs.append('#' * longer_len)
                    new_hyps.append(hyps[idx_hyps])
                    idx_hyps += 1
                elif uu == 'D':
                    longer_len = len(refs[idx_refs])
                    new_refs.append(refs[idx_refs])
                    new_hyps.append('#' * longer_len)
                    idx_refs += 1
                new_error_path.append(str(uu).rjust(longer_len))

            print(
                "Error Path #" + f"{i + 1}:".rjust(3) + 
                "\n[REF]: " + "   ".join(new_refs) +
                "\n[HYP]: " + "   ".join(new_hyps) +
                "\n[ERR]: " + "   ".join(new_error_path) +
                "\n"
            )

        return edit_matrix[-1][-1]


    else:

        curr = list(range(len(hyps) + 1))

        # iterate over units in hypothesis
        for i in range(len(refs)):
            
            # update the previous row
            prev = curr

            # print the row if wanted
            if verbose:
                ref_unit = (
                    str(refs[i - 1]).rjust(ref_maxlen) if i > 0                     # ref units
                    else " " * ref_maxlen                                           # placeholder in row 0
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
                    (prev[j - 1] + int(hyps[j - 1] != refs[i]) 
                    if j > 0 else float('inf')),                                    # substitution
                    prev[j] + 1,                                                    # deletion
                    curr[j - 1] + 1 if j > 0 else float('inf')                      # insertion
                )
        
        if verbose:
            print(
                f"{str(refs[-1]).rjust(ref_maxlen)} |{blanks}" +
                blanks.join([str(k).rjust(horizontal_maxlen) for k in curr])
            )
        
        # print out the final edit distance
        print(f"\nEdit Distance: {curr[-1]}")

        # print out WER / CER / SER
        prefix = 'Sentence' if use_ser else 'Character' if use_cer else 'Word'
        print(f"{prefix} Error Rate: {(curr[-1] / len(refs)) * 100:.4f}%\n\n")

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
        use_cer=True,
        loose_level=2,
        show_trace=True
    )
    

    """
        (Blank-Separated) Sentence Comparisons, tighter layout
    """

    ref2 = 'I want to go to the CMU campus'
    hyp2 = 'I want to go to I want to go to I want to go to the CMU campus'

    get_edit_distance(
        ref=ref2, 
        hyp=hyp2, 
        loose_level=1,
        show_trace=True
    )


    """
        Evaluation of Real-Life ASR Results
    """
    
    refs = [
        # "I want to go to the CMU campus",
        # "I went to see Bullet Train and it's definitely worth the ticket.",
        # "Det finns flera anledningar att inte äta kyckling."
        "S AE M . IH Z . M AY . D AO G .",
        "S AE M . IH Z . M AY . D AO G ."
    ]
    hyps = [
        # "I want to go to the gym you can",
        # "I went to Sybil and Trey and it's definitely worth the ticket.",
        # "Det finns flera anledningar att du inte äta kyckling."
        "S AE M . IH Z . M AY . G AA D .",
        "S AE M . Z . M AY . D AO G ."
    ]


    for i, ref in enumerate(refs):
        hyp = hyps[i]
        # CER
        print("\n[CER]")
        get_edit_distance(ref=ref, hyp=hyp, use_cer=True, verbose=False)
        # WER
        print("\n[WER]")
        get_edit_distance(ref=ref, hyp=hyp, use_cer=False, show_trace=True)
        # SER
        print("\n[SER]")
        get_edit_distance(ref=ref, hyp=hyp, use_ser=True, verbose=False)
        # finished
        print("\n\n")