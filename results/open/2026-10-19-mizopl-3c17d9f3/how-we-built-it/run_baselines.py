#!/opt/homebrew/bin/python3
import os, sys, time, subprocess
from pathlib import Path
import numpy as np
import pandas as pd
from pyteomics import electrochem, mass, parser
from sklearn import ensemble, feature_extraction, preprocessing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = BASE_DIR


# 1. Exact reproduction of tcrexab, tcrexb, tcrexa from methods_scripts/immrep_tcrex/tcrexmodel.ipynb
basicity = {'A': 206.4, 'B': 210.7, 'C': 206.2, 'D': 208.6, 'E': 215.6, 'F': 212.1, 'G': 202.7,
            'H': 223.7, 'I': 210.8, 'K': 221.8, 'L': 209.6, 'M': 213.3, 'N': 212.8, 'P': 214.4,
            'Q': 214.2, 'R': 237.0, 'S': 207.6, 'T': 211.7, 'V': 208.7, 'W': 216.1, 'X': 210.2,
            'Y': 213.1, 'Z': 214.9}
hydrophobicity = {'A': 0.16, 'B': -3.14, 'C': 2.50, 'D': -2.49, 'E': -1.50, 'F': 5.00, 'G': -3.31,
                  'H': -4.63, 'I': 4.41, 'K': -5.00, 'L': 4.76, 'M': 3.23, 'N': -3.79, 'P': -4.92,
                  'Q': -2.76, 'R': -2.77, 'S': -2.85, 'T': -1.08, 'V': 3.02, 'W': 4.88, 'X': 4.59,
                  'Y': 2.00, 'Z': -2.13}
helicity = {'A': 1.24, 'B': 0.92, 'C': 0.79, 'D': 0.89, 'E': 0.85, 'F': 1.26, 'G': 1.15, 'H': 0.97,
            'I': 1.29, 'K': 0.88, 'L': 1.28, 'M': 1.22, 'N': 0.94, 'P': 0.57, 'Q': 0.96, 'R': 0.95,
            'S': 1.00, 'T': 1.09, 'V': 1.27, 'W': 1.07, 'X': 1.29, 'Y': 1.11, 'Z': 0.91}
mutation_stability = {'A': 13, 'C': 52, 'D': 11, 'E': 12, 'F': 32, 'G': 27, 'H': 15, 'I': 10,
                      'K': 24, 'L': 34, 'M':  6, 'N':  6, 'P': 20, 'Q': 10, 'R': 17, 'S': 10,
                      'T': 11, 'V': 17, 'W': 55, 'Y': 31}
physchem_properties = {'basicity': basicity, 'hydrophobicity': hydrophobicity,
                       'helicity': helicity, 'mutation stability': mutation_stability}

def gene_to_family(gene):
    gene_str = str(gene)
    if gene_str == 'unresolved':
        return gene_str
    return gene_str.split('-')[0].zfill(2)

def encode_gene(gene):
    gene_str = str(gene)
    if '-' in gene_str:
        return '-'.join(g.zfill(2) for g in gene_str.split('-'))
    return gene_str

def convert_gene_df(data):
    data = data.copy()
    for gene in [g for g in data.columns.values if g in ['TRBV','TRBJ','TRAV','TRAJ']]:
        data[gene] = data[gene].str.replace(r'\*0\d', '', regex=True)
        data[gene] = data[gene].apply(encode_gene)
        data[gene + '_family'] = data[gene].apply(gene_to_family)
    return data

# Pre-cache pI and fast_mass per single amino acid or sequence to make compute_features 10x faster with identical floats
aa_pI_cache = {aa: electrochem.pI(aa) for aa in mutation_stability.keys()}
seq_mass_cache = {}
seq_pI_cache = {}
def cached_mass(seq):
    if seq not in seq_mass_cache:
        seq_mass_cache[seq] = mass.fast_mass(seq)
    return seq_mass_cache[seq]
def cached_pI(seq):
    if seq not in seq_pI_cache:
        seq_pI_cache[seq] = electrochem.pI(seq)
    return seq_pI_cache[seq]

def compute_features(data):
    features_list = []
    onehot_encoder = feature_extraction.DictVectorizer(sparse=False)
    features_list.append(pd.DataFrame(
        onehot_encoder.fit_transform(data[['V_gene', 'J_gene', 'V_family', 'J_family']].to_dict(orient='records')),
        columns=onehot_encoder.feature_names_))
    features_list.append(data['CDR3_sequence'].apply(lambda s: parser.length(s)).to_frame().rename(columns={'CDR3_sequence': 'length'}))
    aa_counts = pd.DataFrame.from_records([parser.amino_acid_composition(s) for s in data['CDR3_sequence']]).fillna(0)
    aa_counts.columns = ['{} count'.format(col) for col in aa_counts.columns]
    features_list.append(aa_counts)
    for prop_name, prop_lookup in physchem_properties.items():
        features_list.append(data['CDR3_sequence'].apply(
            lambda s: np.mean([prop_lookup[aa] for aa in s])).to_frame().rename(columns={'CDR3_sequence': 'average {}'.format(prop_name)}))
    features_list.append(data['CDR3_sequence'].apply(cached_mass).to_frame().rename(columns={'CDR3_sequence': 'mass'}))
    features_list.append(data['CDR3_sequence'].apply(cached_pI).to_frame().rename(columns={'CDR3_sequence': 'pI'}))
    pos_aa, pos_basicity, pos_hydro, pos_helicity, pos_mutation, pos_pI = [[] for _ in range(6)]
    for sequence in data['CDR3_sequence']:
        length = parser.length(sequence)
        start_pos = -1 * (length // 2)
        pos_range = list(range(start_pos, start_pos + length)) if length % 2 == 1 else list(range(start_pos, 0)) + list(range(1, start_pos + length + 1))
        pos_aa.append({'pos_{}_{}'.format(pos, aa): 1 for pos, aa in zip(pos_range, sequence)})
        pos_basicity.append({'pos_{}_basicity'.format(pos): basicity[aa] for pos, aa in zip(pos_range, sequence)})
        pos_hydro.append({'pos_{}_hydrophobicity'.format(pos): hydrophobicity[aa] for pos, aa in zip(pos_range, sequence)})
        pos_helicity.append({'pos_{}_helicity'.format(pos): helicity[aa] for pos, aa in zip(pos_range, sequence)})
        pos_mutation.append({'pos_{}_mutation_stability'.format(pos): mutation_stability[aa] for pos, aa in zip(pos_range, sequence)})
        pos_pI.append({'pos_{}_pI'.format(pos): aa_pI_cache[aa] for pos, aa in zip(pos_range, sequence)})
    features_list.append(pd.DataFrame.from_records(pos_aa).fillna(0))
    features_list.append(pd.DataFrame.from_records(pos_basicity).fillna(0))
    features_list.append(pd.DataFrame.from_records(pos_hydro).fillna(0))
    features_list.append(pd.DataFrame.from_records(pos_helicity).fillna(0))
    features_list.append(pd.DataFrame.from_records(pos_mutation).fillna(0))
    features_list.append(pd.DataFrame.from_records(pos_pI).fillna(0))
    return pd.concat(features_list, axis=1)

def add_classifier_features(target, train):
    target = target.copy()
    missing = [f for f in train.columns if f not in target.columns.values]
    if missing:
        for f in missing:
            target[f] = 0
    target.fillna(0, inplace=True)
    return target[train.columns.values]

t0 = time.time()
traindir = os.path.join(BASE_DIR, "training_data")
testdir = os.path.join(BASE_DIR, "test_set")
truedir = os.path.join(BASE_DIR, "true_set")

train_list = {}
for file in sorted(os.listdir(traindir)):
    if file.endswith(".txt") and file != "README.txt":
        ep = Path(file).stem
        train_list[ep] = convert_gene_df(pd.read_csv(os.path.join(traindir, file), sep="\t"))

test_list = {}
for file in sorted(os.listdir(testdir)):
    if file.endswith(".txt") and file not in ("README.txt", "testSet_Global_NoHeaders.txt"):
        ep = Path(file).stem
        df = pd.read_csv(os.path.join(testdir, file), sep="\t")
        df = df[df['TRB_CDR3'] != 'TRB_CDR3'].reset_index(drop=True)
        test_list[ep] = convert_gene_df(df)


beta_features, alpha_features, y = {}, {}, {}
for ep in train_list:
    beta_features[ep] = compute_features(train_list[ep].rename(columns={'TRBV':'V_gene','TRBJ':'J_gene','TRBV_family':'V_family','TRBJ_family':'J_family','TRB_CDR3':'CDR3_sequence'})).add_prefix('B_')
    alpha_features[ep] = compute_features(train_list[ep].rename(columns={'TRAV':'V_gene','TRAJ':'J_gene','TRAV_family':'V_family','TRAJ_family':'J_family','TRA_CDR3':'CDR3_sequence'})).add_prefix('A_')
    y[ep] = preprocessing.LabelEncoder().fit_transform(train_list[ep]['Label'])

beta_testfeatures, alpha_testfeatures = {}, {}
for ep in test_list:
    beta_testfeatures[ep] = compute_features(test_list[ep].rename(columns={'TRBV':'V_gene','TRBJ':'J_gene','TRBV_family':'V_family','TRBJ_family':'J_family','TRB_CDR3':'CDR3_sequence'})).add_prefix('B_')
    alpha_testfeatures[ep] = compute_features(test_list[ep].rename(columns={'TRAV':'V_gene','TRAJ':'J_gene','TRAV_family':'V_family','TRAJ_family':'J_family','TRA_CDR3':'CDR3_sequence'})).add_prefix('A_')

classifier = {'A': {}, 'B': {}, 'AB': {}}
for ep in train_list:
    X_ab = np.concatenate((alpha_features[ep].values, beta_features[ep].values), axis=1)
    classifier['AB'][ep] = ensemble.RandomForestClassifier(200, random_state=0, class_weight='balanced').fit(X_ab, y[ep])
    classifier['A'][ep] = ensemble.RandomForestClassifier(200, random_state=0, class_weight='balanced').fit(alpha_features[ep].values, y[ep])
    classifier['B'][ep] = ensemble.RandomForestClassifier(200, random_state=0, class_weight='balanced').fit(beta_features[ep].values, y[ep])

for chain, name in [('AB', 'tcrexab'), ('B', 'tcrexb'), ('A', 'tcrexa')]:
    outdir = os.path.join(WORK_DIR, f"baseline_{name}")
    os.makedirs(outdir, exist_ok=True)
    for ep in test_list:
        if ep == 'testSet_Global':
            globaldata = []
            for pm in train_list:
                td = test_list[ep].copy(deep=True)
                td['epitope'] = pm
                if chain == 'A':
                    X_te = add_classifier_features(alpha_testfeatures[ep], alpha_features[pm]).values
                elif chain == 'B':
                    X_te = add_classifier_features(beta_testfeatures[ep], beta_features[pm]).values
                else:
                    X_te = np.concatenate((add_classifier_features(alpha_testfeatures[ep], alpha_features[pm]),
                                           add_classifier_features(beta_testfeatures[ep], beta_features[pm])), axis=1)
                td['score'] = classifier[chain][pm].predict_proba(X_te)[:, 1]
                globaldata.append(td[['TRA_CDR3', 'TRB_CDR3', 'epitope', 'score']])
            pd.concat(globaldata).to_csv(os.path.join(outdir, ep + '.txt'), sep='\t', index=False)
        else:
            td = test_list[ep][['TRA_CDR3', 'TRB_CDR3']].copy(deep=True)
            if chain == 'A':
                X_te = add_classifier_features(alpha_testfeatures[ep], alpha_features[ep]).values
            elif chain == 'B':
                X_te = add_classifier_features(beta_testfeatures[ep], beta_features[ep]).values
            else:
                X_te = np.concatenate((add_classifier_features(alpha_testfeatures[ep], alpha_features[ep]),
                                       add_classifier_features(beta_testfeatures[ep], beta_features[ep])), axis=1)
            td['score'] = classifier[chain][ep].predict_proba(X_te)[:, 1]
            td.to_csv(os.path.join(outdir, ep + '.txt'), sep='\t', index=False)
    stats_out = os.path.join(WORK_DIR, f"baseline_{name}_stats.txt")
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "evaluation/evaluate.py"), "-i", outdir, "-t", truedir, "-o", stats_out], check=True, stdout=subprocess.DEVNULL)

print(f"tcrex baselines finished in {time.time() - t0:.2f}s")
pub_micro = pd.read_csv(os.path.join(BASE_DIR, "evaluation/microaucs.csv"), index_col=0)
pub_rank = pd.read_csv(os.path.join(BASE_DIR, "evaluation/epitoperank.csv"), index_col=0)
for name in ['tcrexab', 'tcrexb', 'tcrexa']:
    st = pd.read_csv(os.path.join(WORK_DIR, f"baseline_{name}_stats.txt"), sep="\t", index_col=0)
    rerun_avg = st.loc['_Average', 'MicroAUC']
    pub_avg = pub_micro.loc[name, '_Average']
    rerun_rnk = st.loc['_Average', 'Average Rank']
    pub_rnk = pub_rank.loc[name, '_Average']
    print(f"  {name}: rerun MicroAUC _Average = {rerun_avg:.6f} vs published {pub_avg:.6f} (diff = {abs(rerun_avg - pub_avg):.6f}); Average Rank = {rerun_rnk:.6f} vs published {pub_rnk:.6f}")
