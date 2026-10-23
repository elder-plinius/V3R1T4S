#!/usr/bin/env python3
"""Spell out every primitive signed addition, free alias, and product, then
execute the resulting tape exactly on all 250 pairs of input basis vectors."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
scheme = json.loads((HERE.parent.parent/'claim/scheme.json').read_text())
tape = []

def signed(name, sign):
    return {'name':name,'sign':sign}

def emit_stage(key, input_names, output_names):
    pool = list(input_names)
    def emit_row(row,destination,tag):
        terms = [signed(pool[term['index']],term['value']) for term in row]
        if len(terms) == 1:
            tape.append({'destination':destination,'operation':'alias','operands':terms,
                         'addition_cost':0,'product_cost':0,'source_form':tag})
            return
        left = terms[0]
        for k in range(1,len(terms)):
            last = k == len(terms)-1
            dest = destination if last else destination+'_fold'+str(k)
            tape.append({'destination':dest,'operation':'add','operands':[left,terms[k]],
                         'addition_cost':1,'product_cost':0,'source_form':tag})
            left = signed(dest,1)
    for i,row in enumerate(scheme[key+'_fresh']):
        dest = key.upper()+str(len(pool))
        emit_row(row,dest,key+'_fresh['+str(i)+']')
        pool.append(dest)
    for i,row in enumerate(scheme[key]):
        emit_row(row,output_names[i],key+'['+str(i)+']')

emit_stage('u',['A'+str(i) for i in range(10)],['L'+str(k) for k in range(40)])
emit_stage('v',['B'+str(i) for i in range(25)],['R'+str(k) for k in range(40)])
for k in range(40):
    tape.append({'destination':'P'+str(k),'operation':'product',
                 'operands':[signed('L'+str(k),1),signed('R'+str(k),1)],
                 'addition_cost':0,'product_cost':1,'source_form':'product['+str(k)+']'})
emit_stage('w',['P'+str(k) for k in range(40)],['C'+str(i) for i in range(10)])

available = {'A'+str(i) for i in range(10)} | {'B'+str(i) for i in range(25)}
for instruction in tape:
    assert instruction['destination'] not in available
    assert all(operand['name'] in available and operand['sign'] in (-1,1)
               for operand in instruction['operands'])
    available.add(instruction['destination'])
assert sum(row['addition_cost'] for row in tape) == 148
assert sum(row['product_cost'] for row in tape) == 40

executed = 0
for ai in range(10):
    for bi in range(25):
        values = {'A'+str(i):int(i==ai) for i in range(10)}
        values.update({'B'+str(i):int(i==bi) for i in range(25)})
        for row in tape:
            operands = [values[term['name']] if term['sign']==1 else -values[term['name']]
                        for term in row['operands']]
            if row['operation'] == 'alias':
                value = operands[0]
            elif row['operation'] == 'add':
                value = operands[0] + operands[1]
            else:
                assert row['operation'] == 'product'
                value = operands[0] * operands[1]
            values[row['destination']] = value
            executed += 1
        for i in range(2):
            for j in range(5):
                assert values['C'+str(j*2+i)] == int(ai//5==i and bi%5==j and ai%5==bi//5)

(HERE/'candidate-primitive-tape.json').write_text(json.dumps(tape,indent=2)+'\n')
result = {'pass':True,'primitive_instructions':len(tape),
          'additions':sum(row['addition_cost'] for row in tape),
          'multiplications':sum(row['product_cost'] for row in tape),
          'free_alias_or_sign_instructions':sum(row['operation']=='alias' for row in tape),
          'basis_pairs':250,'output_values_checked':2500,
          'primitive_instructions_executed':executed,'all_references_sequential':True}
(HERE/'tape-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
