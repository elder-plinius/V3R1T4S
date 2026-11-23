"""A fixed family of categorical forecasters evaluated by nested grouped CV."""
from collections import defaultdict
from dataclasses import dataclass, replace
from pathlib import Path
import argparse
import csv
import json
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ALPHAS = (.01, .03, .1, .3, 1.)
STRENGTHS = (1., 4., 16., 64.)
FAMILIES = {
    'dialogues': ('order2', 'order3', 'repetition', 'timing'),
    'dominica': ('order2', 'order3', 'repetition'),
    'turns': ('order2', 'order3', 'repetition', 'timing'),
}


@dataclass
class Sequence:
    group: str
    fold: int
    row: np.ndarray
    count: np.ndarray
    duration: np.ndarray
    onset: np.ndarray
    speaker: np.ndarray


def load_sequences(task):
    source = 'DominicaCodas.csv' if task == 'dominica' else 'sperm-whale-dialogues.csv'
    streams = defaultdict(list)
    with (ROOT / 'data' / source).open(encoding='utf-8-sig', newline='') as handle:
        for i, row in enumerate(csv.DictReader(handle)):
            if task == 'dominica':
                key = (row['Date'].replace('-', '/'), row['Unit'])
                entry = (int(row['codaNUM2018']), i, row['CodaType'], float(row['Duration']), 0)
            else:
                key = (row['REC'], '')
                entry = (float(row['TsTo']), i, min(int(row['nClicks']), 10), float(row['Duration']), int(row['Whale']))
            streams[key].append(entry)
    folds = {name: i % 5 for i, name in enumerate(sorted({key[0] for key in streams}))}
    output = []
    for (group, unit), records in sorted(streams.items()):
        onset, row, count, dur, speaker = map(np.array, zip(*sorted(records)))
        output.append(Sequence(group, folds[group], row, count, dur, onset, speaker))
    return output


def contexts(codes, sequence, kind, width, edges):
    """Build each target's features using prefixes only. A zero code denotes unavailable input."""
    last = np.r_[0, codes[:-1] + 1]
    lag2 = np.r_[0, last[:-1]] if width > 1 else np.zeros_like(last)
    lag3 = np.r_[0, lag2[:-1]] if width > 1 else np.zeros_like(last)
    run = np.zeros_like(last)
    distinct = np.zeros_like(last)
    if width > 1:
        length = 0
        before_run = 0
        for j in range(1, len(last)):
            if last[j] != last[j - 1]:
                length = 0
                before_run = last[j - 1]
            length += 1
            run[j] = min(6, length)
            distinct[j] = before_run
    if kind == 'dominica':
        return {'order2': (last, lag2), 'order3': (last, lag2, lag3), 'repetition': (last, run, distinct)}
    duration = sequence.duration
    frac = np.zeros_like(last)
    if len(edges):
        bins = np.r_[0., edges, max(2., edges[-1] * 2)]
        index = np.searchsorted(edges, duration, side='right')
        relative = (duration - bins[index]) / np.maximum(bins[index + 1] - bins[index], 1e-8)
        frac[1:] = np.clip(np.floor(3 * relative[:-1]), 0, 2).astype(int) + 1
    previous_count = np.r_[0, sequence.count[:-1]]
    gap = np.zeros_like(last)
    slope = np.zeros_like(last)
    speaker = np.zeros_like(last)
    if width > 1:
        gap[2:] = np.searchsorted([.4, .9, 1.8, 4., 12.], np.diff(sequence.onset)[:-1], side='right') + 1
        dur_change = np.diff(np.log(np.maximum(.01, duration)))
        slope[2:] = np.searchsorted([-.25, -.08, .08, .25], dur_change[:-1], side='right') + 1
        speaker[2:] = 1 + (sequence.speaker[:-2] == sequence.speaker[1:-1])
    return {'order2': (last, lag2), 'order3': (last, lag2, lag3), 'repetition': (last, run, distinct),
            'timing': (last, frac if kind == 'dialogues' else previous_count, gap, slope, speaker)}


def prepare(training, validation, task):
    if task == 'dominica':
        vocabulary = sorted({code for seq in training for code in seq.count})
        lookup = {code: i for i, code in enumerate(vocabulary)}
        k = len(lookup) + 1
        edges = []
        def encode(seq):
            return np.array([lookup.get(c, k - 1) for c in seq.count], dtype=int)
    else:
        vocabulary = [str(i) for i in range(50 if task == 'dialogues' else 2)]
        k = len(vocabulary)
        edges = np.quantile(np.concatenate([seq.duration for seq in training]), [.2,.4,.6,.8], method='linear')
        def encode(seq):
            if task == 'turns':
                return np.r_[-1, (seq.speaker[1:] == seq.speaker[:-1]).astype(int)]
            return (seq.count - 1) * 5 + np.searchsorted(edges, seq.duration, side='right')

    def materialize(sequences, include_twin):
        targets, prev, reference_pairs, labels, rows, unknown = [], [], [], [], [], []
        parts = {width: defaultdict(list) for width in (1, 3) if width == 3 or include_twin}
        for seq in sequences:
            codes = encode(seq)
            base_start = 2 if task == 'turns' else 1
            reference_pairs.append((codes[base_start-1:-1], codes[base_start:]))
            if len(codes) < 3:
                continue
            targets.extend(codes[2:])
            prev.extend(codes[1:-1])
            labels.extend([seq.group] * (len(codes)-2))
            rows.extend(seq.row[2:])
            unknown.extend((codes[2:] == k - 1) if task == 'dominica' else [False] * (len(codes)-2))
            for width, store in parts.items():
                for name, feature_columns in contexts(codes, seq, task, width, edges).items():
                    store[name].append(np.stack(feature_columns, axis=1)[2:])
        return (np.array(targets), np.array(prev), np.concatenate([a for a,b in reference_pairs]),
                np.concatenate([b for a,b in reference_pairs]), np.array(labels), np.array(rows),
                {width: {name: np.concatenate(parts) for name, parts in store.items()} for width,store in parts.items()},
                int(sum(unknown)))

    return k, edges, vocabulary, materialize(training, True), materialize(validation, True)


def reference_probs(k, cases, test, alpha):
    counts = np.bincount(cases[2]*k + cases[3], minlength=k*k).reshape(k,k)
    matrix = counts + alpha
    matrix /= matrix.sum(axis=1, keepdims=True)
    return matrix[test[1]]


def fit_tables(training_features, evaluation_features, labels, k):
    tables = []
    train_keys = np.zeros(len(training_features),dtype=np.int64)
    test_keys = np.zeros(len(evaluation_features),dtype=np.int64)
    for training_col, test_col in zip(training_features.T, evaluation_features.T):
        train_keys = train_keys * 128 + training_col
        test_keys = test_keys * 128 + test_col
        keys, indexes = np.unique(train_keys, return_inverse=True)
        counts = np.bincount(indexes*k+labels, minlength=len(keys)*k).reshape(len(keys),k)
        index = np.minimum(np.searchsorted(keys, test_keys),len(keys)-1)
        tables.append(counts[index] * (keys[index] == test_keys)[:,None])
    return tables


def table_probs(k, counts, label_counts, strength):
    posterior = np.broadcast_to((label_counts+.5)/(label_counts.sum()+.5*k), counts[0].shape)
    for step in counts:
        posterior = (step+strength*posterior)/(step.sum(axis=1,keepdims=True)+strength)
    return posterior


def losses(probabilities, targets):
    return -np.log2(probabilities[np.arange(len(targets)), targets])


def evaluate(sequences, task, retain=False):
    names = FAMILIES[task]
    rows, deltas, groups, fold_ids = [], defaultdict(list), [], []
    total_unknown = 0
    for outer in range(5):
        cross = defaultdict(float)
        train = [seq for seq in sequences if seq.fold != outer]
        test = [seq for seq in sequences if seq.fold == outer]
        for inner in range(5):
            if inner == outer:
                continue
            k, _, _, tr, va = prepare([s for s in train if s.fold != inner], [s for s in train if s.fold == inner], task)
            label_counts = np.bincount(tr[0], minlength=k)
            for alpha in ALPHAS:
                cross['R1', alpha] += losses(reference_probs(k,tr,va,alpha), va[0]).sum()
            for width in (1,3):
                for name in names:
                    tables = fit_tables(tr[6][width][name],va[6][width][name],tr[0],k)
                    for h in STRENGTHS:
                        cross[width, name, h] += losses(table_probs(k,tables,label_counts,h), va[0]).sum()
        best_alpha = min(ALPHAS,key=lambda a:cross['R1',a])
        chosen = {width:{name:min(STRENGTHS,key=lambda h:cross[width,name,h]) for name in names} for width in (1,3)}
        family = min(names,key=lambda name:cross[3,name,chosen[3][name]])
        k, edges, vocab, tr, va = prepare(train,test,task)
        total_unknown += va[7]
        label_counts = np.bincount(tr[0],minlength=k)
        predictions = {'R1':reference_probs(k,tr,va,best_alpha)}
        for name in names:
            for width in (1,3):
                width_name = 'twin' if width == 1 else 'full'
                tables = fit_tables(tr[6][width][name],va[6][width][name],tr[0],k)
                predictions[name+'_'+width_name] = table_probs(k,tables,label_counts,chosen[width][name])
        predictions['selected_full'] = predictions[family+'_full']
        predictions['selected_twin'] = predictions[family+'_twin']
        for key, p in predictions.items():
            assert np.all(p > 0) and np.allclose(p.sum(axis=1),1, rtol=0,atol=1e-12)
            deltas[key].append(losses(p,va[0]))
        groups.extend(va[4])
        fold_ids.extend([outer]*len(va[0]))
        if retain:
            rows.append(dict(fold=outer,selected=family,alpha=best_alpha,hyperparameters=chosen,edges=list(edges),vocabulary=vocab,
                             row=va[5],group=va[4],target=va[0],predictions=predictions))
    return {key:np.concatenate(v) for key,v in deltas.items()},np.array(groups),np.array(fold_ids),rows,total_unknown


def group_ci(values, groups):
    _, indexes = np.unique(groups,return_inverse=True)
    totals = np.bincount(indexes,weights=values)
    counts = np.bincount(indexes)
    boot = np.random.default_rng(20261118).integers(0,len(totals),size=(10000,len(totals)))
    draws = totals[boot].sum(axis=1)/counts[boot].sum(axis=1)
    return np.quantile(draws,[.025,.975]).tolist()


def summarize(loss, groups, fold_ids, task, bootstrap=True):
    metrics = {}
    for name in ('selected', *FAMILIES[task]):
        full = loss[name+'_full']
        comparisons = {'baseline':loss['R1']-full,'twin':loss[name+'_twin']-full}
        metrics[name] = {'bits':float(full.mean()),
                         'gain':{c:float(v.mean()) for c,v in comparisons.items()}}
        if bootstrap:
            metrics[name]['CI95'] = {c:group_ci(v,groups) for c,v in comparisons.items()}
            metrics[name]['fold_gains'] = {c:[float(v[fold_ids == f].mean()) for f in range(5)] for c,v in comparisons.items()}
    return dict(task=task, baseline_bits=float(loss['R1'].mean()), targets=len(groups), groups=len(set(groups)), models=metrics)


def shuffle(sequences, seed):
    rng = np.random.default_rng(seed)
    shuffled = []
    for seq in sequences:
        order = rng.permutation(len(seq.row))
        shuffled.append(replace(seq,count=seq.count[order],duration=seq.duration[order],speaker=seq.speaker[order]))
    return shuffled


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('task', choices=FAMILIES)
    parser.add_argument('--controls', type=int, default=0)
    args = parser.parse_args()
    seqs = load_sequences(args.task)
    start = time.monotonic()
    output = ROOT/'output'
    if args.controls:
        path = output / (args.task+'-shuffles.jsonl')
        done = {json.loads(line)['seed'] for line in path.read_text().splitlines()} if path.exists() else set()
        with path.open('a') as file:
            for seed in range(310000, 310000+args.controls):
                if seed in done:
                    continue
                result = summarize(*evaluate(shuffle(seqs,seed),args.task)[:3],args.task,bootstrap=False)
                file.write(json.dumps(dict(seed=seed, **result))+'\n')
                file.flush()
        return
    loss, groups, fold_ids, rows, unknown = evaluate(seqs,args.task,retain=True)
    result = summarize(loss,groups,fold_ids,args.task)
    result['unknown_targets'] = unknown
    result['elapsed_seconds'] = time.monotonic()-start
    for row in rows:
        f = row['fold']
        np.savez_compressed(output/f'{args.task}-fold{f}.npz', row=row['row'], group=row['group'],
                            target=row['target'], **row['predictions'])
    result['folds'] = [{k:r[k] for k in ('fold','selected','alpha','hyperparameters','edges','vocabulary')} for r in rows]
    (output/f'{args.task}-result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'folds'},indent=2))


if __name__ == '__main__':
    main()
