#!/usr/bin/env python3
"""Saved public positive control, signed-alias control, and corrupt negatives."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
CLAIM = HERE.parent.parent / 'claim'
CANDIDATE = json.loads((CLAIM / 'scheme.json').read_text())
controls = []

def add(name, scheme, expected_success, expected_additions, expected_error=None):
    path = HERE / (name + '.json')
    path.write_text(json.dumps(scheme,indent=2) + '\n')
    controls.append((name,path,expected_success,expected_additions,expected_error))

controls.append(('public153',CLAIM/'data/2x5x5_m40_cr153_cn283_ZT_reduced.json',True,153,None))

alias = deepcopy(CANDIDATE)
new_alias = 10 + len(alias['u_fresh'])
alias['u_fresh'].append([{'index':5,'value':-1}])
alias['u'][0] = [{'index':new_alias,'value':-1}]
add('positive_signed_alias',alias,True,148)

mutant = deepcopy(CANDIDATE)
mutant['u'][0][0]['value'] *= -1
add('negative_wrong_product_sign',mutant,False,148,'integer tensor mismatch')

mutant = deepcopy(CANDIDATE)
mutant['w'][0],mutant['w'][1] = mutant['w'][1],mutant['w'][0]
add('negative_wrong_output_order',mutant,False,148,'integer tensor mismatch')

mutant = deepcopy(CANDIDATE)
for rows in (mutant['u'],mutant['u_fresh']):
    for row in rows:
        for term in row:
            if term['index'] in (0,1):
                term['index'] = 1 - term['index']
add('negative_wrong_input_order',mutant,False,148,'integer tensor mismatch')

mutant = deepcopy(CANDIDATE)
mutant['u_fresh'][0][0]['index'] = 10
add('negative_forward_reference',mutant,False,148,'illegal or forward reference')

mutant = deepcopy(CANDIDATE)
mutant['v'][0][0]['value'] = 2
add('negative_forbidden_scalar',mutant,False,148,'scalar is not +/-1')

mutant = deepcopy(CANDIDATE)
new_alias = 10 + len(mutant['u_fresh'])
mutant['u_fresh'].append([{'index':5,'value':1}])
mutant['u'][0] = [{'index':5,'value':1},{'index':new_alias,'value':1}]
mutant['complexity']['reduced'] = 149
add('negative_expanded_nonternary',mutant,False,149,'expanded coefficients not ternary')

mutant = deepcopy(CANDIDATE)
new_alias = 10 + len(mutant['u_fresh'])
mutant['u_fresh'].append([{'index':5,'value':1}])
mutant['u'][0] = [{'index':5,'value':1},{'index':new_alias,'value':-1}]
mutant['complexity']['reduced'] = 149
add('negative_inactive_product',mutant,False,149,'inactive product 0')

mutant = deepcopy(CANDIDATE)
mutant['complexity']['reduced'] = 147
add('negative_wrong_cost',mutant,False,148,'declared reduced cost is wrong')

mutant = deepcopy(CANDIDATE)
mutant['complexity']['naive'] = 282
add('negative_wrong_naive_cost',mutant,False,148,'declared expanded naive cost is wrong')

mutant = deepcopy(CANDIDATE)
mutant['u'][0].append(deepcopy(mutant['u'][0][0]))
add('negative_duplicate_reference',mutant,False,148,'repeated sparse index')

mutant = deepcopy(CANDIDATE)
mutant['w'].pop()
add('negative_missing_output',mutant,False,148,'final-form count disagrees')

mutant = deepcopy(CANDIDATE)
mutant['z2'] = True
add('negative_wrong_field',mutant,False,148,'integer, not Z2, semantics required')

mutant = deepcopy(CANDIDATE)
mutant['u'][0][0]['value'] = True
add('negative_boolean_scalar',mutant,False,148,'scalar is not +/-1')

mutant = deepcopy(CANDIDATE)
mutant['m'] = 41
add('negative_wrong_rank',mutant,False,148,'rank must be 40')

mutant = deepcopy(CANDIDATE)
mutant['n'] = [5,2,5]
add('negative_wrong_format',mutant,False,148,'format must be (2,5,5)')

report = []
for name,path,success,additions,error in controls:
    command = [sys.executable,str(HERE/'check_independent.py'),str(path),
               '--expected-additions',str(additions)]
    if success:
        command += ['--audit',str(HERE/(name+'-audit.json'))]
    result = subprocess.run(command,text=True,capture_output=True)
    (HERE/(name+'-stdout.json')).write_text(result.stdout)
    (HERE/(name+'-stderr.txt')).write_text(result.stderr)
    output = json.loads(result.stdout)
    accepted = result.returncode == 0 and output.get('pass') is True
    expected_observed = accepted == success and (error is None or error in output.get('error',''))
    report.append({'control':name,'expected_acceptance':success,'actual_acceptance':accepted,
                   'exit_code':result.returncode,'expected_error':error,
                   'actual_error':output.get('error'),
                   'control_behaved_as_expected':expected_observed})
combined = {'pass':all(item['control_behaved_as_expected'] for item in report),
            'positive_controls':sum(item['expected_acceptance'] for item in report),
            'negative_controls':sum(not item['expected_acceptance'] for item in report),
            'controls':report}
(HERE/'controls-result.json').write_text(json.dumps(combined,indent=2)+'\n')
print(json.dumps(combined,indent=2))
if not combined['pass']:
    sys.exit(1)
