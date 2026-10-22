#!/usr/bin/python3

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
import sys, getopt
import scipy.stats as ss
import os
from pathlib import Path
import random


def rank_score(tcrdataframe, epitope):

    #print(tcrdataframe[['TCR','score','predicted','true']])

    # Calculate the rank for the right prediction
    rank = ss.rankdata(tcrdataframe.score)[tcrdataframe.predicted == epitope][0] - 1 # rank starts at 1

    #print(str(len(tcrdataframe) - rank))

    # Reverse rank so that lower is better
    return len(tcrdataframe) - rank

def main(argv):
   inputfolder = '' # Folder with scores
   truefolder = ''  # Ground truth file
   outputfile = '' # File where to output metrics
   negativelabel = 'HealthyControl' # The label corresponding to external negative data
   try:
      opts, args = getopt.getopt(argv,"hi:o:t:",["ifile=","ofile=","tfile="])
   except getopt.GetoptError:
      print ('evaluate.py -i <inputfolder> -t <groundtruthfolder> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('evaluate.py -i <inputfolder> -t <groundtruthfolder> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifolder"):
         inputfolder = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-t", "--tfolder"):
         truefolder = arg
   print ('Score folder is "' + inputfolder)

   print ('Groundtruth folder is "' + truefolder)

   if outputfile == '':
       outputfile = inputfolder + '_stats.txt'

   print ('Output file is "' + outputfile)

   #Read in score files
   testfiles = [file for file in os.listdir(inputfolder) if '.txt' in file]

   test_list = dict()

   print("Prediction files:")

   for file in testfiles:
      print(file)
      test_df = pd.read_csv(inputfolder + '/' + file,sep="[\t\s,]")

      epitope = Path(file).stem

      test_list[epitope] = test_df

   #Read in ground truth files
   truefiles = [file for file in os.listdir(truefolder) if '.txt' in file]

   true_list = dict()

   print("Ground truth files:")

   for file in truefiles:
      print(file)
      true_df = pd.read_csv(truefolder + '/' + file,sep="[\t\s,]")

      epitope = Path(file).stem

      true_list[epitope] = true_df

   micro_aucs = dict()
   micro_aucs_noneg = dict()
   average_rank = dict()

   for epitope in test_list:

       print(epitope)

       input = test_list[epitope]
       true = true_list[epitope]

       # Rename the columns for internal logic
       input = input.rename(columns={"Predicted": "score"})
       input = input.rename(columns={"epitope": "predicted"})
       input = input.rename(columns={"peptide": "predicted","Peptide": "predicted"})
       input = input.rename(columns={"Antigen": "predicted"})
       input = input.rename(columns={"prediction": "score"})
       input = input.rename(columns={"preds": "score"})
       input = input.rename(columns={"pred": "score"})
       input = input.rename(columns={"Scores": "score"})
       input = input.rename(columns={"Rank": "score"})
       input = input.rename(columns={"Predicted Binomial Values (0-1)": "score"})

       print(input)

       input = input.rename(columns={"TRB": "TRB_CDR3","TRA": "TRA_CDR3"})

       true = true.rename(columns={"Epitope_GroundTruth": "true"})
       true = true.rename(columns={"TCR_source": "true"})

       #Merge prediction file with ground truth
       merged = pd.merge(input, true,  how='left', left_on=['TRA_CDR3','TRB_CDR3'], right_on = ['TRA_CDR3','TRB_CDR3'])

       if epitope != "testSet_Global":

           #calculate the AUC for each epitope
           micro_aucs[epitope] = roc_auc_score(merged["Label"] == 1, merged["score"])

       else:

           if 'score' in merged:

               epitopes = merged.true.unique()

               # Merge alpha and beta so that we can filter based on unique TCRs later on
               merged['TCR'] = merged['TRA_CDR3'] + merged['TRB_CDR3']

               print(epitopes)

               #Calculate the average rank of the correct prediction (for each TCR and then summarise per eitope)
               average_rank = {epitope:np.average([rank_score(merged[merged['TCR'] == tcr],epitope) for tcr in merged[merged['true'] == epitope]["TCR"].unique()]) for epitope in epitopes}
               average_rank['_Average'] = np.average(list(average_rank.values()))

   if len(micro_aucs) > 0:
      micro_aucs['_Average'] = np.average(list(micro_aucs.values()))
   #micro_aucs_noneg['_Average'] = np.average(list(micro_aucs_noneg.values()))



   #Write the result to a file
   #output = pd.DataFrame({'MicroAUC':micro_aucs,'MicroAUCnoNeg':micro_aucs_noneg,'Average Rank':average_rank})
   if (len(average_rank) > 0 and len(micro_aucs) > 0):
       output = pd.DataFrame({'MicroAUC':micro_aucs,'Average Rank':average_rank})
   elif len(micro_aucs) > 0:
       output = pd.DataFrame({'MicroAUC':micro_aucs})
   elif len(average_rank) > 0:
       output = pd.DataFrame({'Average Rank':average_rank})

   output.to_csv(outputfile,sep="\t")

if __name__ == "__main__":
   main(sys.argv[1:])
