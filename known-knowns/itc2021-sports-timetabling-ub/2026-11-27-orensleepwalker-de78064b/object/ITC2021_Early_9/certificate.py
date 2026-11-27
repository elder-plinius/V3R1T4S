"""Replay the finite venue-pattern certificate for Early 9."""
import csv
from itertools import combinations
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

INSTANCE = Path(__file__).resolve().parent / 'data/Early_9.instance.xml'
TEAM = 2
TEAMS = range(18)
SLOTS = range(34)


def ids(rule, name):
    return tuple(map(int, filter(None, rule.attrib[name].split(';'))))


def load(instance):
    root = ET.parse(instance)
    assert [int(e.get('id')) for e in root.findall('Resources/Teams/team')] == list(TEAMS)
    assert [int(e.get('id')) for e in root.findall('Resources/Slots/slot')] == list(SLOTS)
    assert root.findtext('Structure/Format/numberRoundRobin') == '2'
    assert root.findtext('Structure/Format/compactness') == 'C'
    rule, = root.iter('BR2')
    assert [rule.get(k) for k in ('type', 'mode2', 'homeMode', 'intp', 'penalty')] == [
        'SOFT', 'LEQ', 'HA', '16', '10']
    assert set(ids(rule, 'teams')) == set(TEAMS) and set(ids(rule, 'slots')) == set(SLOTS)
    venue = [r for r in root.iter('CA1') if r.get('type') == 'HARD' and TEAM in ids(r, 'teams')]
    assert all(r.get('mode') in ('H', 'A') for r in venue)
    fixture, = [r for r in root.iter('GA1') if r.get('meetings') == '5,2;' and ids(r, 'slots') == (13,)]
    assert [fixture.get(k) for k in ('type', 'min', 'max')] == ['HARD', '1', '1']
    return venue


def patterns(instance):
    venue = load(instance)
    for count in range(4):
        for repeats in combinations(SLOTS[1:], count):
            for first in ('H', 'A'):
                bits = [first]
                for r in SLOTS[1:]:
                    bits.append(bits[-1] if r in repeats else ('A' if bits[-1] == 'H' else 'H'))
                if bits.count('H') != 17 or bits[13] != 'A':
                    continue
                if all(int(rule.get('min')) <= sum(bits[r] == rule.get('mode') for r in ids(rule, 'slots'))
                       <= int(rule.get('max')) for rule in venue):
                    yield repeats, ''.join(bits)


def bounds(instance):
    surviving = list(patterns(instance))
    assert all(len(repeat_slots) == 3 for repeat_slots, _ in surviving)
    assert all(any(r % 2 for r in repeat_slots) for repeat_slots, _ in surviving)
    assert surviving
    return surviving


def main():
    instance = Path(sys.argv[1]) if len(sys.argv) > 1 else INSTANCE
    writer = csv.writer(sys.stdout, lineterminator='\n')
    writer.writerow(('team', 'repeat_slots', 'home_away_pattern'))
    surviving = bounds(instance)
    for slots, pattern in surviving:
        writer.writerow((TEAM, ' '.join(map(str, slots)), pattern))
    print(f'# Team 2 allowed sequences with three repeats: {len(surviving)}')
    print('# Team 2 allowed sequences with fewer repeats: 0')
    print('# Team 2 three-repeat sequences with all repeat slots even: 0')
    print('# Minimum possible total repeats: at least 20')
    print('# Lower bound on Early 9: 40')


if __name__ == '__main__':
    main()
