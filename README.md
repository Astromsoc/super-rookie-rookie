# super-rookie-rookie

Collage of some functional codes used when needed (personally) for trivial stuff.

## Novel Scraper

Simple script to sracpe texts embedded within a certain tag and concatenate them into one joint `.txt` file.

## Matplotlib Utils

Several script templates I find useful in daily use to plot good-looking figures that satiate basic needs.

## Trivials

Other hard-to-categorize codes I write for fun or to assist understanding of course contents or significant algorithms.

- `ctc_trellis.py`: build all potential CTC outputs given a groundtruth label sequence and the number of frames to fill in ([sample results](trivials/sample-output-ctc-trellis.txt))

- `edit_distance.py`: compute edit distance, construct full 2D matrix, and rebuilt error paths for a pair of reference and hypothesis strings ([sample results](trivials/sample-output-edit-distance.txt))

- `remove_icloud_dups.py`: input the absolute folder filepath (in iCloud Drive) to clear up all duplicated iCloud backups (fixed format: `"### 2(.)(##)"`, or with regex: `r".+ 2(\.).+"`) ([sample results](trivials/sample-output-remove-icloud-dups.txt))
  