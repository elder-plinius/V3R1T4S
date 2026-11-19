"""Vectorized implementation of campaign.prepare, with paired equivalence checks."""
import json
import time
import numpy as np
import campaign
from controls import grouped_transform

SLOW = campaign.prepare


def materialize(sequences, task, edges, lookup, k):
    lengths = np.array([len(s.row) for s in sequences])
    start = np.r_[0,np.cumsum(lengths)[:-1]]
    row = np.concatenate([s.row for s in sequences])
    index = np.arange(len(row))
    prefix = np.repeat(start,lengths)
    position = index-prefix
    targets = index[position>=2]
    duration = np.concatenate([s.duration for s in sequences])
    count = np.concatenate([s.count for s in sequences])
    onset = np.concatenate([s.onset for s in sequences])
    speaker = np.concatenate([s.speaker for s in sequences])

    if task == 'dominica':
        code = np.fromiter((lookup.get(x,k-1) for x in count),dtype=int,count=len(row))
    elif task == 'dialogues':
        code = (count-1)*5 + np.searchsorted(edges,duration,side='right')
    else:
        code = (speaker == np.r_[speaker[0],speaker[:-1]]).astype(int)
        code[start] = -1
    binary = task == 'turns'
    eligible = index[position >= (2 if binary else 1)]
    last = code[targets-1]+1
    lag2 = code[targets-2]+1
    lag3 = np.where(position[targets]>=3,code[targets-3]+1,0)
    changed = np.r_[True, code[1:] != code[:-1]]
    changed[start] = True
    run_start = np.maximum.accumulate(np.where(changed,index,0))[targets-1]
    run = np.minimum(6,targets-run_start)
    distinct = np.where(run_start==prefix[targets],0,code[run_start-1]+1)
    zero = np.zeros_like(last)
    cols = {3:{'order2':(last,lag2),'order3':(last,lag2,lag3),'repetition':(last,run,distinct)},
            1:{'order2':(last,zero),'order3':(last,zero,zero),'repetition':(last,zero,zero)}}
    if task != 'dominica':
        if task == 'dialogues':
            bins = np.r_[0.,edges,max(2.,edges[-1]*2)]
            previous = duration[targets-1]
            bin_index = np.searchsorted(edges,previous,side='right')
            fraction = (previous-bins[bin_index])/np.maximum(bins[bin_index+1]-bins[bin_index],1e-8)
            within = np.clip(np.floor(3*fraction),0,2).astype(int)+1
        else:
            within = count[targets-1]
        gap = np.searchsorted([.4,.9,1.8,4.,12.],onset[targets-1]-onset[targets-2],side='right')+1
        log_duration = np.log(np.maximum(.01,duration))
        change = log_duration[targets-1]-log_duration[targets-2]
        slope = np.searchsorted([-.25,-.08,.08,.25],change,side='right')+1
        identity = 1+(speaker[targets-1]==speaker[targets-2])
        cols[3]['timing']=(last,within,gap,slope,identity)
        cols[1]['timing']=(last,within,zero,zero,zero)
    contexts = {width:{name:np.stack(columns,axis=1) for name,columns in tables.items()}
                for width,tables in cols.items()}
    group = np.repeat([s.group for s in sequences],lengths)[targets]
    unknown = int(np.count_nonzero(code[targets] == k-1)) if task == 'dominica' else 0
    return code[targets],last-1,code[eligible-1],code[eligible],group,row[targets],contexts,unknown


def prepare(training,validation,task):
    if task == 'dominica':
        vocabulary = sorted({code for seq in training for code in seq.count})
        lookup = {code:i for i,code in enumerate(vocabulary)}
        k = len(vocabulary)+1
        edges = []
    else:
        k = 50 if task == 'dialogues' else 2
        vocabulary = [str(i) for i in range(k)]
        lookup = {}
        edges = np.quantile(np.concatenate([seq.duration for seq in training]),
                            [.2,.4,.6,.8],method='linear')
    return k,edges,vocabulary,materialize(training,task,edges,lookup,k),materialize(validation,task,edges,lookup,k)


def verify():
    def checked(train,test,task):
        a,b = SLOW(train,test,task),prepare(train,test,task)
        assert a[0] == b[0] and a[2] == b[2] and np.array_equal(a[1],b[1])
        for reference,candidate in zip(a[3:],b[3:]):
            assert all(np.array_equal(x,y) for x,y in zip(reference[:6],candidate[:6]))
            for width,tables in reference[6].items():
                for key, features in tables.items():
                    assert np.array_equal(features,candidate[6][width][key]),(task,width,key)
            assert reference[7]==candidate[7]
        return b

    results = []
    for task in ('dialogues','turns','dominica'):
        data = campaign.load_sequences(task)
        inputs = [('real',data),('payload',campaign.shuffle(data,310000)),
                      ('first_order',grouped_transform(data,task)(310000))]
        for mode,seqs in inputs:
            campaign.prepare=checked
            t=time.monotonic()
            reference=campaign.evaluate(seqs,task)[0]
            slow=time.monotonic()-t
            campaign.prepare=prepare
            t=time.monotonic()
            fast=campaign.evaluate(seqs,task)[0]
            elapsed=time.monotonic()-t
            assert all(np.array_equal(reference[key],fast[key]) for key in reference)
            results.append(dict(task=task,mode=mode,checked_seconds=slow,fast_seconds=elapsed,status='PASS'))
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    verify()
