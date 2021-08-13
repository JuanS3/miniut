import functools
import platform
import os
import colorama

from miniut import config as cfg


COLORS_LIST = [RED     := 'RED',
               GREEN   := 'GREEN',
               YELLOW  := 'YELLOW',
               BLUE    := 'BLUE',
               MAGENTA := 'MAGENTA',
               CYAN    := 'CYAN',
               ]

__COLORS = {RED     : colorama.Fore.RED,
            GREEN   : colorama.Fore.GREEN,
            YELLOW  : colorama.Fore.YELLOW,
            BLUE    : colorama.Fore.BLUE,
            MAGENTA : colorama.Fore.MAGENTA,
            CYAN    : colorama.Fore.CYAN
            }

__indentation_basic = ' '
__lvl = ''
__LVL_SIZE = 2
__init = False


_START_LANGS = {cfg.ENG : 'START',
                cfg.ESP : 'INICIA',
                }

_END_LANGS = {cfg.ENG : 'END',
              cfg.ESP : 'TERMINA',
              }


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                         decorators                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def block(message_block: str or dict, color: str = BLUE):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            message = message_block
            if isinstance(message_block, dict):
                message = message_block[cfg.lang()]

            start_block(message, color)
            new_line()
            value = func(*args, **kwargs)
            new_line()
            end_block(message, color)
            return value
        return wrapped
    return decorator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                          functions                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def _init():
    """
    If the console still doesn't start, then start the console without
    clearing the screen, but do nothing if the console is started
    """
    if not __init:
        init(False)


def init(clear: bool = True):
    """
    Initialize the console, and resert the indentation level

    Parameters
    ----------
    clear : bool, optional
        True to clear the screen and False is not, by default True
    """
    global __init, __lvl
    __lvl = ''

    colorama.init(autoreset=True)
    if clear:
        clear_console()
    __init = True


def clear_console():
    """
    Clear the console screen
    """
    os.system('clear' if platform.system() != 'Windows' else 'cls')


def add_lvl():
    """
    Add one level (indentation)
    """
    global __lvl
    __lvl += (__indentation_basic * __LVL_SIZE)


def del_lvl():
    """
    Substract one level (indentation)
    """
    global __lvl
    __lvl = __lvl[:-__LVL_SIZE]


def __send_msg(message: str,
               endl: str = '\n',
               withlvl: bool = True,
               color: str = ''
               ) -> None:
    """
    Print the message to the console, the `endl` is the same as `end` in print function
    and is necessary print the message with the current indentation level and the color
    indicate.

    Parameters
    ----------
    message : [type]
        Message to print to console
    endl : str, optional
        The end of line, by default `\\n`
    withlvl : bool, optional
        True if the message should be printed with the current indentation
        False is not necessary, by default `True`
    color : str, optional
        The color of the message, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color
    """
    _init()
    message = message
    if withlvl: message = __lvl + message

    if color in COLORS_LIST: msg_col = f'{colorama.Style.BRIGHT}{__COLORS[color]}'
    else: msg_col = ''

    print(f'{msg_col}{message}', end=endl)


def start_block(message: str, color: str = BLUE):
    """
    Start a block of messages

    Parameters
    ----------
    message : str
        The title of the block
    color : str, optional
        The color of the title block, by default BLUE
    """
    __send_msg(f'{colorama.Style.BRIGHT}{__COLORS[color]}{_START_LANGS[cfg.lang()]} {message.upper()}')
    add_lvl()


def end_block(message: str, color: str = BLUE):
    """
    End a block of messages

    Parameters
    ----------
    message : str
        The title of the block
    color : str, optional
        The color of the title block, by default BLUE
    """
    del_lvl()
    __send_msg(f'{colorama.Style.BRIGHT}{__COLORS[color]}{_END_LANGS[cfg.lang()]} {message.upper()}')
    new_line()


def println(message: str,
            endl='\n',
            withlvl=True,
            color: str = ''
            ):
    """
    Print the message to the console, ending with the specified endl, by default `\\n`,
    color and indentation.

    Parameters
    ----------
    message : str
        The message to display in the console
    endl : str, optional
        The end of line, by default `\\n`
    withlvl : bool, optional
        True if the message should be printed with the current indent
        False is not necessary, by default True
    color : str, optional
        The color of the message, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color
    """
    __send_msg(message, endl=endl, withlvl=withlvl, color=color)


def warning(message: str):
    """
    Warning message starts with 'warning: {message}'

    Parameters
    ----------
    message : str
        The message to display in the log
    """
    __send_msg(f'{colorama.Style.BRIGHT}{__COLORS[YELLOW]}warning: {message}')


def error(message: str):
    """
    Error message is displayed like `error: >>> {message} <<<`

    Parameters
    ----------
    message : str
        The message to display in the log
    """
    __send_msg(f'{colorama.Style.BRIGHT}{__COLORS[RED]}error: >>> {message} <<<')


def new_line():
    """
    Display a blank line in the console
    """
    __send_msg('')


def line(size: int = 30):
    """
    Display a line in the console like this `-- -- -- -- -- -- --`
    whit the indicated size

    Parameters
    ----------
    size : int, optional
        The size of the line to display, by display 30
    """
    __send_msg(f'{("-- " * size)[:-1]}')
    new_line()
