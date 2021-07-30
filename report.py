from typing import List, Dict, Tuple

import console


# key: id, group of report
# value: a list of tuples of 2 values:
#        the first value is a title and the second value is a description
__report: Dict[str, List[Tuple[str, str]]] = {}


__report_titles: Dict[str, int] = {}
__max_id_len: int = 0


def add_id(id: str):
    global __informe, __max_id_len
    if id not in __report:
        __report[id] = []
        __max_id_len = max(__max_id_len, len(id))


def add_message_by_id(id: str, title: str, mensaje: str = ''):
    add_id(id)
    __report[id].append((title, mensaje))
    
    global __report_titles
    if id not in __report_titles:
        __report_titles[id] = 0
    __report_titles[id] = max(__report_titles[id], len(title))


def ge_val_per_id(id: str) -> list:
    return __report[id]


def num_total_values() -> int:
    n = 0
    for id in __report:
        n += num_errors_by_id(id)
    return n


def num_errors_by_id(id: str) -> int:
    try:    n = len(ge_val_per_id(id=id))
    except: n = 0
    return  n


@console.block(message_block='Informe general')
def print_general_report():
    for id in __report:
        n_errors = num_errors_by_id(id)
        color = console.RED if n_errors > 0 else console.GREEN
        tab = '.' * (__max_id_len - len(id))
        console.write(f'Total de < {id} > con error {tab} : {n_errors}', color=color)


@console.block(message_block='Informe detallado')
def print_detail_report():
    for id in __report:
        for title, message in __report[id]:
            console.warning(f'{id} : {title} | {message} ')


def general_report_string() -> str:
    report = ''
    for id in __report:
        n_errors = num_errors_by_id(id)
        tab = '.' * (__max_id_len - len(id))
        report += f'Total de < {id} > con error {tab} : {n_errors}\n'
    return report


def detail_report_string() -> str:
    report = ''
    for id in __report:
        for title, message in __report[id]:
            report += f'{id} : {title} | {message}\n'
    return report
