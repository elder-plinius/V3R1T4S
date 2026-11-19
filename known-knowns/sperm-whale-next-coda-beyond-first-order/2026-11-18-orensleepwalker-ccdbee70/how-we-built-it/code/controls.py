"""Checkpointed ordinary and transition-preserving controls."""
from collections import Counter, defaultdict
from dataclasses import replace
import argparse
import fcntl
import json
import time
import numpy as np

from campaign import ROOT, evaluate, load_sequences, shuffle, summarize


def random_trail(tokens, rng):
    graph = defaultdict(list)
    for first, second in zip(tokens, tokens[1:]):
        graph[first].append(second)
    for edges in graph.values():
        rng.shuffle(edges)
    path = [tokens[0]]
    reverse = []
    while path:
        if graph[path[-1]]:
            path.append(graph[path[-1]].pop())
        else:
            reverse.append(path.pop())
    output = np.array(reverse[::-1])
    assert len(output) == len(tokens) and output[0] == tokens[0]
    assert Counter(zip(tokens,tokens[1:])) == Counter(zip(output,output[1:]))
    return output


def grouped_transform(sequences, task):
    boundaries = {f: np.quantile(np.concatenate([s.duration for s in sequences if s.fold != f]),
                                  [.2,.4,.6,.8], method='linear') for f in range(5)}

    def transform(seed):
        rng = np.random.default_rng(seed)
        transformed = []
        for seq in sequences:
            if len(seq.row) < 2:
                transformed.append(seq)
                continue
            if task == 'dialogues':
                tokens = (seq.count-1)*5 + np.searchsorted(boundaries[seq.fold],seq.duration,side='right')
                trail = random_trail(tokens,rng)
                groups = {x: rng.permutation(np.flatnonzero(tokens == x)).tolist() for x in set(tokens)}
                order = [groups[x].pop() for x in trail]
                transformed.append(replace(seq,count=seq.count[order],duration=seq.duration[order],speaker=seq.speaker[order]))
            elif task == 'turns':
                switches = (seq.speaker[1:] != seq.speaker[:-1]).astype(int)
                trail = random_trail(switches,rng)
                speakers = 1 + (np.r_[0, np.cumsum(trail)] % 2)
                order = rng.permutation(len(speakers))
                transformed.append(replace(seq,count=seq.count[order],duration=seq.duration[order],speaker=speakers))
            else:
                assert task == 'dominica'
                trail = random_trail(seq.count,rng)
                transformed.append(replace(seq,count=trail))
        return transformed
    return transform


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('task', choices=('dialogues','turns','dominica'))
    parser.add_argument('mode', choices=('payload','first_order'))
    parser.add_argument('--n', type=int, default=400)
    args = parser.parse_args()
    import campaign
    from fast_prepare import prepare
    campaign.prepare = prepare
    sequences = load_sequences(args.task)
    transform = grouped_transform(sequences,args.task) if args.mode == 'first_order' else lambda seed:shuffle(sequences,seed)
    path = ROOT/'output'/f'{args.task}-{args.mode}-controls.jsonl'
    with path.open('a+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        seen = {json.loads(line)['seed'] for line in f}
        start = time.monotonic()
        for offset, seed in enumerate(range(310000,310000+args.n),1):
            if seed in seen:
                continue
            surrogate = transform(seed)
            changed = sum(np.count_nonzero(a.count != b.count)+np.count_nonzero(a.duration != b.duration)
                          +np.count_nonzero(a.speaker != b.speaker) for a,b in zip(sequences,surrogate))
            report = summarize(*evaluate(surrogate,args.task)[:3],args.task,bootstrap=False)
            f.write(json.dumps(dict(seed=seed, changed_fields=int(changed), **report))+'\n')
            f.flush()
            if offset in (1,10) or offset % 25 == 0:
                print(args.task,args.mode,offset,'controls checkpointed',round(time.monotonic()-start,1),flush=True)


if __name__ == '__main__':
    main()
