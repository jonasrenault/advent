from advent.utils import Advent

advent = Advent(4, 2020)

KEYS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


def main():
    lines = advent.get_input_lines()
    passports = get_passports(lines)
    c = [p for p in passports if all([k in p for k in KEYS])]
    advent.submit(1, len(c))

    c = len([p for p in passports if is_valid(p)])
    advent.submit(2, c)


def is_valid(p: dict[str, str]) -> bool:
    try:
        if not 1920 <= int(p["byr"]) <= 2002:
            return False
        if not 2010 <= int(p["iyr"]) <= 2020:
            return False
        if not 2020 <= int(p["eyr"]) <= 2030:
            return False
        if "cm" in p["hgt"]:
            if not 150 <= int(p["hgt"][:-2]) <= 193:
                return False
        elif "in" in p["hgt"]:
            if not 59 <= int(p["hgt"][:-2]) <= 76:
                return False
        else:
            return False
        if not (p["hcl"][0] == "#" and len(p["hcl"]) == 7):
            return False
        if not (p["hcl"].lower() == p["hcl"] and p["hcl"][1:].isalnum()):
            return False
        if p["ecl"] not in ("amb blu brn gry grn hzl oth".split(" ")):
            return False
        if not (len(p["pid"]) == 9 and all([c.isdigit() for c in p["pid"]])):
            return False
    except KeyError:
        return False
    return True


def get_passports(lines: list[str]) -> list[dict[str, str]]:
    passports = []
    passport: dict[str, str] = {}
    for line in lines:
        if not line:
            passports.append(passport)
            passport = {}
        else:
            kvs = [e.split(":") for e in line.split(" ")]
            for k, v in kvs:
                passport[k] = v
    passports.append(passport)
    return passports


if __name__ == "__main__":
    main()
