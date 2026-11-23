"""Independently verify the FD001 profile and official archive correspondence."""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import re
from statistics import mean
from zipfile import ZipFile


def check(condition, label):
    if not condition:
        raise ValueError(f"verification failed: {label}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument("profile", type=Path)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    files = json.loads(args.profile.read_bytes())["files"]

    with ZipFile(args.archive) as archive:
        print("NASA archive SHA-256:", sha256(args.archive.read_bytes()).hexdigest())
        print("NASA readme.txt SHA-256:", sha256(archive.read("readme.txt")).hexdigest())
        for name in (*files, "Damage Propagation Modeling.pdf"):
            raw = (args.data / name).read_bytes()
            digest = sha256(raw).hexdigest()
            check(raw == archive.read(name), f"archive bytes {name}")
            print(f"Official archive bytes match: {name}, {len(raw)} bytes, {digest}")
            if name not in files:
                continue
            info = files[name]
            physical = raw.splitlines()
            records = [(line, re.findall(rb"[^ \t]+", data))
                       for line, data in enumerate(physical, 1) if data.strip()]
            width = 1 if name.startswith("RUL") else 26
            check(len(records) == info["rows"] and width == info["columns"]
                  and all(len(tokens) == width for _, tokens in records), f"shape {name}")
            check(digest == info["sha256"] and len(raw) == info["bytes"], f"integrity {name}")
            check([line for line, data in enumerate(physical, 1) if not data.strip()]
                  == info["blank_lines"], f"blank lines {name}")
            duplicates = sum(count - 1 for count in Counter(tuple(t) for _, t in records).values())
            check(duplicates == info["duplicates"], f"duplicates {name}")
            expected_fields = (["endpoint_rul"] if width == 1 else
                               ["unit", "cycle", "setting_1", "setting_2", "setting_3"] +
                               [f"sensor_{i:02}" for i in range(1, 22)])
            check(expected_fields == info["field_order"], f"column order {name}")
            check(info["missing_by_column"] == dict.fromkeys(expected_fields, 0)
                  and all(info[field] == 0 for field in
                          ("missing_total", "non_finite", "excluded_records", "parse_errors")),
                  f"missing/non-finite/exclusions {name}")
            values = [(line, [Fraction(token.decode("ascii")) for token in tokens])
                      for line, tokens in records]
            for field, column in zip(expected_fields, zip(*(v for _, v in values))):
                stats = info["summaries"][field]
                check((len(column), 0, min(column), max(column), mean(column), min(column) == max(column))
                      == (stats["valid"], stats["excluded"], Fraction(stats["minimum"]),
                          Fraction(stats["maximum"]), Fraction(stats["mean_exact"]), stats["constant"]),
                      f"stats {name}/{field}")
            print(f"PASS {name}: shape, field order, hashes, blanks, duplicates, missing, and all exact summaries")
            if width == 1:
                continue

            groups = {}
            keys = []
            for line, vals in values:
                unit, cycle = vals[:2]
                check(unit.denominator == cycle.denominator == 1 and min(unit, cycle) >= 1,
                      f"integer Unit/Cycle {name}")
                groups.setdefault(int(unit), []).append((int(cycle), line, vals))
                keys.append((unit, cycle))
            check(len(groups) == info["unit_count"] == len(info["units"]) == 100,
                  f"unit count {name}")
            check(len(keys) - len(set(keys)) == info["duplicate_unit_cycle"]
                  and sum(b < a for a, b in zip(keys, keys[1:])) == info["order_anomalies"],
                  f"keys and order {name}")
            gaps = 0
            for unit, rows in groups.items():
                cycles = {row[0] for row in rows}
                missing = sorted(set(range(1, max(cycles) + 1)).difference(cycles))
                constant = [expected_fields[index] for index in range(5, width)
                            if len({item[2][index] for item in rows}) == 1]
                check(info["units"][str(unit)] == dict(rows=len(rows), cycle_min=min(cycles),
                      cycle_max=max(cycles), missing_cycles=missing, constant_sensors=constant),
                      f"unit profile {name}/{unit}")
                gaps += len(missing)
            check(gaps == info["cycle_gaps"], f"gap total {name}")
            check(info["constant_sensors"] == [field for field in expected_fields[5:]
                  if info["summaries"][field]["constant"]], f"whole-file constants {name}")
            ordering = sorted(groups)
            for unit, sensor in zip((ordering[0], ordering[len(ordering)//2], ordering[-1]), (2, 9, 21)):
                ordered = sorted(groups[unit])
                profiled = info["units"][str(unit)]
                for bound, (cycle, line, vals) in zip(("min", "max"), (ordered[0], ordered[-1])):
                    position = sensor + 5
                    raw_token = physical[line - 1].split()[position - 1].decode("ascii")
                    check(cycle == profiled[f"cycle_{bound}"] and
                          Fraction(raw_token) == vals[position - 1], f"sample {name}/{unit}/{cycle}")
                    print(f"PASS sample {name}: Unit={unit} Cycle={cycle} line={line} "
                          f"Sensor={sensor} position={position} raw_value={raw_token}")
            print(f"PASS {name}: all Unit ranges, keys, order, gaps and constant classifications")


if __name__ == "__main__":
    main()
