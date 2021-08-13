import os
import logging
import functools
from datetime import datetime as dt
import re

from miniut.exceptions import RestoreLog
from miniut import config as cfg


FOLDER_LOGS_DEFAULT = 'Logs'

_folder_logs = FOLDER_LOGS_DEFAULT
_log_name = 'logging.log'
_log: logging.Logger = None
_log_ok: bool = True
_log_aux: str = ''

_lvl = ''
_STANDARD_LVL = ' '
_LVL_INDENT = 2


_START_LANGS = {cfg.ENG : 'START',
                cfg.ESP : 'INICIA',
                }

_END_LANGS = {cfg.ENG : 'END',
              cfg.ESP : 'TERMINA',
              }

_RESTORED_LOG_LANGS = {cfg.ENG : 'RESTORED',
                       cfg.ESP : 'RECONSTRUIDO',
                       }

_RESTORE_EXCEPT_LANGS = {cfg.ENG : 'Impossible to restore log',
                         cfg.ESP : 'No ha sido posible reconstruir el log',
                         }

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                         decorators                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def block(message_block: str or dict):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            message = message_block
            if isinstance(message_block, dict):
                message = message_block[cfg.lang()]
            start_block(message)
            value = func(*args, **kwargs)
            end_block(message)
            return value
        return wrapped
    return decorator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                          functions                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def init(log_name: str,
         folder_log: str = FOLDER_LOGS_DEFAULT,
         time: bool = True
         ) -> None:
    """
    Initialize the logging module

    Parameters
    ----------
    log_name : str
        Name of logging file
    folder_log : str, optional
        Folder where the logging file should be stored, by default 'Logs'
    time : bool, optional
        True in case the logging file name has the time with format '%Y%m%d-%H%M%S'
        False in case the time in the name is not necessary, by default True
    """
    global _log_name, _folder_logs, _log
    time_log: str = dt.now().strftime('%Y%m%d-%H%M%S') if time else ''
    _log_name: str = f'{log_name} - {time_log}.log'
    _folder_logs: str = folder_log

    if not os.path.exists(_folder_logs):
        os.makedirs(_folder_logs)

    format = logging.Formatter('%(asctime)-8s - %(levelname)-8s - %(message)s')
    heandler = logging.FileHandler(f'{_folder_logs}/{_log_name}', encoding='UTF-8')
    heandler.setFormatter(format)
    _log = logging.getLogger(_log_name)
    _log.setLevel(logging.DEBUG)
    _log.addHandler(heandler)


def get_folder_log() -> str:
    return _folder_logs


def get_log_name() -> str:
    return _log_name


def _add_lvl() -> None:
    global _lvl
    _lvl += (_STANDARD_LVL * _LVL_INDENT)


def _sub_lvl() -> None:
    global _lvl
    _lvl = _lvl[:-_LVL_INDENT]


def _bad_log() -> None:
    global _log_ok
    _log_ok = False


def start_block(message: str) -> None:
    info(f'# {_START_LANGS[cfg.lang()]} {message.upper()} #', False)
    _add_lvl()


def end_block(message: str):
    _sub_lvl()
    info(f'# {_END_LANGS[cfg.lang()]} {message.upper()} #', False)


def _define_log_aux(type_message: str, msg: str) -> None:
    global _log_aux
    log_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    _log_aux += f'{log_time} - {type_message:<10} - {msg}\n'


def info(message: str, sublvl=True) -> None:
    lvl = _lvl + '' if sublvl else _lvl
    msg = f'{lvl}{message}'
    try:
        _log.info(msg)
    except:
        _bad_log()
    finally:
        _define_log_aux(type_message='INFO', msg=msg)


def warning(message: str) -> None:
    msg = f'{_lvl}{message}'
    try:
        _log.warning(msg)
    except:
        _bad_log()
    finally:
        _define_log_aux(type_message='WARNING', msg=msg)


def critical(message: str) -> None:
    msg = f'{_lvl}{message}'
    try:
        _log.critical(msg)
    except:
        _bad_log()
    finally:
        _define_log_aux(type_message='CRITICAL', msg=msg)


def error(message: str) -> None:
    msg = f'{_lvl}>>> {message} <<<'
    try:
        _log.error(msg)
    except:
       _bad_log()
    finally:
        _define_log_aux(type_message='ERROR', msg=msg)


def _generar_log_auxiliar() -> None:
    log_file_name = f'{_log_name[:-4]} - {_RESTORED_LOG_LANGS[cfg.lang()]}.log'

    try:
        with open(f'{_folder_logs}/{log_file_name}', 'w', encoding='UTF-8') as f:
            f.write(_log_aux)
    except Exception as e:
        raise RestoreLog(message=_RESTORE_EXCEPT_LANGS[cfg.lang()],
                            error=str(e)  
                            )


def close() -> None:
    if not _log_ok:
        _generar_log_auxiliar()
