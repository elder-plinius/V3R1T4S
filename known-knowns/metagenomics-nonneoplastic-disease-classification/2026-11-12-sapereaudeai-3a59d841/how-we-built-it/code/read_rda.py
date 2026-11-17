import sys
sys.stdout.reconfigure(encoding="utf-8")
import rdata
src, out = sys.argv[1], sys.argv[2]
conv = rdata.read_rda(src)
for k, v in conv.items():
    print(k, type(v), getattr(v, 'shape', None))
df = conv['sampleMetadata']
print(list(df.columns))
keep = ['study_name','sample_id','subject_id','number_reads','number_bases','minimum_read_length','median_read_length','age','BMI','country','gender','disease','study_condition','body_site']
keep = [c for c in keep if c in df.columns]
sub = df[df['study_name'].isin(['QinJ_2012','KarlssonFH_2013','QinN_2014','ZellerG_2014','HMP_2012','NielsenHB_2014'])][keep]
sub.to_csv(out, sep='\t', index=False)
print(sub.groupby('study_name').size())
print(sub.head())
