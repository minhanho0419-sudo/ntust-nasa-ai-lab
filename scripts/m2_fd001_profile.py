"""Profile local C-MAPSS FD001 files without changing the inputs."""
import argparse
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re

FILES = {"train_FD001.txt": 26, "test_FD001.txt": 26, "RUL_FD001.txt": 1}
FIELDS = ["unit", "cycle", "setting_1", "setting_2", "setting_3"] + [
    f"sensor_{index:02}" for index in range(1, 22)
]
NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[Ee][+-]?[0-9]+)?")


def summarize(values):
    if not values:
        return dict(valid=0, excluded=0, minimum=None, maximum=None, mean=None, constant=None)
    low, high = min(values), max(values)
    mean = Fraction(sum(values)) / len(values)
    with localcontext() as context:
        context.prec = 40
        display = Decimal(mean.numerator) / Decimal(mean.denominator)
    return dict(valid=len(values), excluded=0, minimum=str(low), maximum=str(high),
                mean=str(display), mean_exact=str(mean), constant=low == high)


def parse(path, width):
    raw = path.read_bytes()
    rows, blanks, errors = [], [], []
    for line_number, line in enumerate(raw.decode("ascii", errors="strict").splitlines(), 1):
        tokens = line.split()
        if not tokens:
            blanks.append(line_number)
            continue
        if len(tokens) != width or any(not NUMBER.fullmatch(token) for token in tokens):
            errors.append(line_number)
            continue
        values = tuple(map(Decimal, tokens))
        integers = values[:2] if width == 26 else values
        minimum = 1 if width == 26 else 0
        if any(value < minimum or value != value.to_integral_value() for value in integers):
            errors.append(line_number)
            continue
        rows.append((line_number, tuple(tokens), values))
    if errors or not rows:
        raise ValueError(f"{path.name}: {len(errors)} malformed/missing/non-finite records; "
                         f"physical lines={errors[:20]}; valid records={len(rows)}")
    return raw, rows, blanks


def profile(path, width):
    raw, rows, blanks = parse(path, width)
    fields = FIELDS if width == 26 else ["endpoint_rul"]
    columns = list(zip(*(values for _, _, values in rows)))
    result = dict(
        bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), rows=len(rows), columns=width,
        field_order=fields, blank_lines=blanks, duplicates=len(rows) - len({tokens for _, tokens, _ in rows}),
        missing_by_column={name: 0 for name in fields}, missing_total=0,
        non_finite=0, excluded_records=0, parse_errors=0,
        summaries={name: summarize(values) for name, values in zip(fields, columns)},
    )
    if width == 1:
        return result

    by_unit = defaultdict(list)
    key_counts = Counter()
    order_anomalies = 0
    previous = (0, 0)
    for line, _, values in rows:
        unit, cycle = map(int, values[:2])
        order_anomalies += (unit, cycle) < previous
        previous = (unit, cycle)
        by_unit[unit].append((cycle, line, values[5:]))
        key_counts[unit, cycle] += 1

    units = {}
    for unit, records in sorted(by_unit.items()):
        cycles = {cycle for cycle, _, _ in records}
        first, last = min(cycles), max(cycles)
        sensors = list(zip(*(values for _, _, values in records)))
        units[unit] = dict(rows=len(records), cycle_min=first, cycle_max=last,
                           missing_cycles=sorted(set(range(1, last + 1)) - cycles),
                           constant_sensors=[field for field, values in zip(FIELDS[5:], sensors)
                                             if min(values) == max(values)])
    result.update(unit_count=len(units), units=units, order_anomalies=order_anomalies,
                  duplicate_unit_cycle=sum(count - 1 for count in key_counts.values()),
                  cycle_gaps=sum(len(unit["missing_cycles"]) for unit in units.values()),
                  constant_sensors=[name for name in FIELDS[5:] if result["summaries"][name]["constant"]])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    inputs = [args.data_dir / name for name in FILES]
    if args.output.resolve() in {path.resolve() for path in inputs}:
        parser.error("output must be distinct from inputs")
    try:
        with localcontext() as context:
            context.prec = 80  # FD001 tokens have modest precision; see source and rules report.
            files = {name: profile(args.data_dir / name, width) for name, width in FILES.items()}
        test = files["test_FD001.txt"]
        if set(test["units"]) != set(range(1, files["RUL_FD001.txt"]["rows"] + 1)):
            raise ValueError("test unit IDs do not align with the RUL vector")
        payload = dict(dataset="NASA C-MAPSS FD001", files=files)
        args.output.write_bytes((json.dumps(payload, indent=2, allow_nan=False) + "\n").encode("utf-8"))
    except (OSError, ValueError, ArithmeticError) as error:
        parser.exit(1, f"FD001 profile failed: {error}\n")
    for name, info in files.items():
        print(f"{name}: rows={info['rows']} columns={info['columns']} sha256={info['sha256']}")


if __name__ == "__main__":
    main()
