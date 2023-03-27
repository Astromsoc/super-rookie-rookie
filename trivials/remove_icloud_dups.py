"""
    Script to clear up duplicate files due to iCloud Archive backup merging.

    Written by: 
        Astromsoc (schen4@andrew.cmu.edu)
    Last Updated at:
        Mar 27, 2023

    ---

    Assertion:
        - each duplicate file has the fixed automatically added suffix: "* 2.*"
    
    Upcoming:
        - allow customized input of anti-duplicate suffixes

"""

import os
import re
import filecmp
import argparse


SPECIAL_CASE_I = "\n[   TWIN FILE MISSING  ] Twin file ({}) does not exist."
SPECIAL_CASE_II = "\n[    TWIN FILE DIFF    ] Twin file ({}) is not the same as {{}}."
DELETED_MSG = "\n[ SUCCESSFULLY DELETED ] File ({}) has been deleted. Twin file ({}) is kept."
GLOBAL_COUNT = 0


def clear_files_in_one_folder(folder: str):
    global GLOBAL_COUNT
    print(f"\n\n### NOW CLEARING UP DIRECTORY: [{folder}] ###")
    assert os.path.isdir(folder)
    for root, dirs, files in os.walk(folder):
        full_fps = [os.path.join(root, f) for f in files]
        for fp in full_fps:
            # skipping the I-don't-know-what-it-is file
            if fp.endswith('.icloud'): continue
            if re.match(r"^.+ 2(\.)?.*$", fp):
                # check if the corresponding original file exists
                twin = re.sub(" 2\.", ".", fp)
                if not os.path.exists(twin): print(SPECIAL_CASE_I.format(twin)); continue
                elif not filecmp.cmp(fp, twin): print(SPECIAL_CASE_II.format(twin, fp)); continue
                else: print(DELETED_MSG.format(fp, twin)); GLOBAL_COUNT += 1; os.remove(fp)
            else: continue
    if dirs: clear_files_in_one_folder(dirs)


def main(args):
    # root call
    clear_files_in_one_folder(args.r)
    # report
    print(f"\n\nA total of [{GLOBAL_COUNT}] file(s) have been deleted.")



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Clear up duplicate files due to iCloud Archive backup merging.")

    parser.add_argument(
        '-r',
        type=str,
        help='(str) Absolute path to the root folder to start scouting & cleaning.'
    )

    args = parser.parse_args()
    # check folder existence
    assert os.path.exists(args.r), f"[FOLDER NOT EXISTED] Input folder ({args.r}) does not exist."
    assert os.path.isdir(args.r), f"[NOT A FOLDER] Input path ({args.r}) does not direct to a folder."
    main(args)