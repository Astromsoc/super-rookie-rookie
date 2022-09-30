import argparse



def get_trellis(labels, num_frames):
    trellis = list()

    # first scan: check what can be passed
    nexts = dict()
    for i, l in enumerate(labels):
        nexts[i] = [i]
        if i < len(labels) - 1:
            nexts[i].append(i + 1)
            if labels[i + 1] == '<b>':
                if i < len(labels) - 2:
                    if labels[i + 2] != l:
                        nexts[i].append(i + 2)
    
    def unit_add(i, prefix):
        if len(prefix) >= num_frames:
            return
        if len(prefix) == num_frames - 1:
            if i >= len(labels) - 2:
                trellis.append(prefix + [labels[i]])
        else:
            for j in nexts[i]:
                unit_add(j, prefix + [labels[i]])
                
    # start from <b>
    unit_add(0, [])
    # start from first char
    unit_add(1, [])

    return trellis
    



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='trellis building - CTC style')

    parser.add_argument(
        '--labels', 
        type=str, 
        default='<b> s <b> e <b> e <b>', 
        help='string of expanded labels, separated by space'
    )

    parser.add_argument(
        '--frames',
        type=int,
        default=6,
        help='number of frames to expand the label sequence to'
    )

    args = parser.parse_args()

    ts = get_trellis(args.labels.split(), args.frames)
    for i, t in enumerate(ts):
        print(f'trellis #{i + 1:<3} ' +
              ' '.join(tt if tt == '<b>' else f' {tt} ' for tt in t))