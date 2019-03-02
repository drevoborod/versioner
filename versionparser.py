#!/bin/env python3

from copy import deepcopy


class VersionParser:
    def __init__(self, version, separator=".", section_separator=None):
        self._initial_version_string = version
        self._sep = separator
        self._section_sep = section_separator
        self._initial_parsed_version = None
        self._parse()

    def _parse(self):
        if self._section_sep:
            prepared = self._initial_version_string.split(self._section_sep)
        else:
            prepared = [self._initial_version_string]
        prepared_splitted = [part.split(self._sep) for part in prepared]
        result = []
        for part in prepared_splitted:
            new_part = []
            for item in part:
                if new_part:
                    new_part.append(self._sep)
                if item.isdigit():
                    new_part.append(int(item))
                else:
                    [new_part.append(x) for x
                     in self._separate_types(item)]
            result.append(new_part)
        self._initial_parsed_version = result

    def incr(self, pos=-1, section=0, value=1):
        return self._calculate(pos, section, value, "+")

    def decr(self, pos=-1, section=0, value=1):
        return self._calculate(pos, section, value, "-")

    def _calculate(self, pos, section, value, operation):
        template = deepcopy(self._initial_parsed_version)
        digits_map = [n for n, x in enumerate(template[section])
                      if type(x) is int]
        index = digits_map[pos]
        if operation == "+":
            res = template[section].pop(index) + value
        elif operation == "-":
            res = template[section].pop(index) - value
            if res < 0:
                res = 0
        template[section].insert(index, res)
        result = ["".join(map(str, x)) for x in template]
        if self._section_sep:
            return self._section_sep.join(result)
        else:
            return result[0]

    @classmethod
    def increase(cls, version_string, separator=".", section_separator=None,
                 pos=-1, section=0, value=1):
        c = cls(version_string, separator, section_separator)
        return c.incr(pos, section, value)

    @classmethod
    def decrease(cls, version_string, separator=".", section_separator=None,
                 pos=-1, section=0, value=1):
        c = cls(version_string, separator, section_separator)
        return c.decr(pos, section, value)

    @property
    def parsed(self):
        if not self._initial_parsed_version:
            self._parse()
        return self._initial_parsed_version

    @staticmethod
    def _separate_types(string):
        all = []
        part = []
        prev_char = False
        for char in string:
            try:
                res = int(char)
            except ValueError:
                if prev_char:
                    part.append(char)
                else:
                    if part:
                        all.append(int("".join(map(str, part))))
                    part = [char]
                prev_char = True
            else:
                if prev_char:
                    all.append("".join(part))
                    part = [res]
                else:
                    part.append(res)
                prev_char = False
        if prev_char:
            all.append("".join(part))
        else:
            all.extend(part)
        return all


# Test
if __name__ == "__main__":
    s = "8aaa123abc222p,6,"

    print(VersionParser._separate_types(s))

    v = "1.2.3.%s" % s
    p = VersionParser(v)
    print(p.parsed)
    print(p.incr(pos=1))
    ver = "0.4.1-alpha6"
    print(VersionParser.increase(ver))
    print(VersionParser.decrease(ver, pos=-2, value=1))
    print(VersionParser.increase("1.0.3"))
    print(VersionParser.increase("great_release_4_0_1_RC", separator="_",
                                 pos=-2, value=3))
    print(VersionParser.decrease("beta8-0.99", pos=0))
    print(VersionParser.decrease("1.2.3alpha6+component0.2.5",
                                 section_separator="+", section=1))

