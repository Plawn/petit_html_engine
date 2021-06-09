from enum import Flag
import re
from typing import List

local_funcs = [
    'centered_button',
    'student_fullname',
]


def extract_variable(var: str):
    # remove the '(' and ')'
    r = var.split('+')
    r = [
        i
        .replace('(', "")
        .replace(')', "")
        .strip()
        for i in r if '"' not in i
    ]

    # print(var, r)
    return r


def get_placeholder(text: str, local_funcs: List[str]) -> List[str]:
    for name in local_funcs:
        text = text.replace(name, '')
    # finding between {{ }}
    res: List[str] = re.findall(
        r"\{{(.*?)\}}", text, re.MULTILINE
    )
    # finding between {% %}
    res2 = []
    for i in res:
        res2.extend(extract_variable(i.strip()))
    # extract variables
    return res2


if __name__ == "__main__":
    with open('t.html', 'r') as f:
        content = f.read()
    res = get_placeholder(content, local_funcs)
    print(res)
