"""Derive the Early 14 bound from the instance XML using only the standard library."""
import csv
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
INSTANCE = Path(sys.argv[1])
TEAMS = range(20)
ROUNDS = range(38)


def numbers(element, name):
    return tuple(map(int, filter(None, element.attrib[name].split(";"))))


def load():
    root = ET.parse(INSTANCE).getroot()
    assert [int(e.attrib["id"]) for e in root.findall("Resources/Teams/team")] == list(TEAMS)
    assert [int(e.attrib["id"]) for e in root.findall("Resources/Slots/slot")] == list(ROUNDS)
    assert root.findtext("Structure/Format/numberRoundRobin") == "2"
    assert root.findtext("Structure/Format/compactness") == "C"
    nodes = tuple(root.find("Constraints").iter())
    cap, = (e for e in nodes if e.tag == "BR2")
    assert (cap.get("type"), cap.get("mode2"), cap.get("homeMode")) == ("SOFT", "LEQ", "HA")
    assert (int(cap.attrib["intp"]), int(cap.attrib["penalty"])) == (18, 10)
    assert set(numbers(cap, "teams")) == set(TEAMS)
    assert set(numbers(cap, "slots")) == set(ROUNDS)
    result = {}
    for home, away, round_id in ((9, 0, 7), (10, 15, 4)):
        required, = (e for e in nodes if e.tag == "GA1"
                     and e.get("meetings") == f"{home},{away};"
                     and numbers(e, "slots") == (round_id,))
        assert (required.get("type"), required.get("min"), required.get("max")) == ("HARD", "1", "1")
        preferences = tuple(e for e in nodes if e.tag == "CA1" and e.get("type") == "SOFT"
                            and numbers(e, "teams") == (away,))
        assert preferences and all(e.get("mode") in ("H", "A") for e in preferences)
        result[away] = (round_id, preferences)
    return result


def patterns(required_away):
    for first in ("H", "A"):
        for repeat_slot in (None, *ROUNDS[1:]):
            seq = [first]
            for r in ROUNDS[1:]:
                if r == repeat_slot:
                    seq.append(seq[-1])
                else:
                    seq.append("A" if seq[-1] == "H" else "H")
            if seq.count("H") == 19 and seq[required_away] == "A":
                yield repeat_slot, seq


def charge(seq, rule):
    count = sum(seq[r] == rule.get("mode") for r in numbers(rule, "slots"))
    lo, hi, weight = (int(rule.attrib[k]) for k in ("min", "max", "penalty"))
    return weight * max(lo - count, count - hi, 0)


def main():
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(("team", "first_slot_venue", "repeat_slot", "pattern", "ca1_penalty"))
    lower_bound = 0
    for team, (mandatory_away, preferences) in load().items():
        costs = []
        for repeat, seq in patterns(mandatory_away):
            penalty = sum(charge(seq, rule) for rule in preferences)
            writer.writerow((team, seq[0], repeat, "".join(seq), penalty))
            costs.append(penalty)
        minimum = min(costs)
        print(f"# team {team}: {len(costs)} patterns, minimum {minimum}")
        lower_bound += minimum
    print(f"# Lower bound on Early 14: {lower_bound}")


if __name__ == "__main__":
    main()
