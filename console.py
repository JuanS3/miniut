import functools
import platform
import os
import colorama


_COLORS_LIST = [RED     := 'RED',
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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                         decorators                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def block(message_block: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapped():
            start_block(message_block)
            new_line()
            func()
            new_line()
            end_block(message_block)
        return wrapped
    return decorator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                          functions                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def _init():
    """
    If the console still doesn't start, then start the console without
    clearing the screen, but do nothing if the console is started.
    """    
    if not __init:
        init(False)


def init(clear: bool = True):
    global __init

    colorama.init(autoreset=True)
    if clear:
        clear_console()
    __init = True


def clear_console():
    os.system('clear' if platform.system() != 'Windows' else 'cls')


def add_lvl():
    global __lvl
    __lvl += (__indentation_basic * __LVL_SIZE)


def del_lvl():
    global __lvl
    __lvl = __lvl[:-__LVL_SIZE]


def __send_msg(message,
               endl='\n',
               withlvl=True,
               color: str = ''
               ) -> None:
    _init()
    message = message
    if withlvl: message = __lvl + message

    if color in _COLORS_LIST: msg_col = f'{colorama.Style.BRIGHT}{__COLORS[color]}'
    else: msg_col = ''

    print(f'{msg_col}{message}', end=endl)


def start_block(message):
    __send_msg(f'{colorama.Style.BRIGHT}{__COLORS[BLUE]}INICIA {message.upper()}')
    add_lvl()


def end_block(message):
    del_lvl()
    __send_msg(f'{colorama.Style.BRIGHT}{__COLORS[BLUE]}TERMINA {message.upper()}')
    new_line()


def write(message: str,
          endl='\n',
          withlvl=True,
          color: str = ''
          ):
    __send_msg(message, endl=endl, withlvl=withlvl, color=color)


def warning(message: str):
    __send_msg(f'{colorama.Style.BRIGHT}{__COLORS[YELLOW]}warning: {message}')


def error(message: str):
    __send_msg(f'{colorama.Style.BRIGHT}{__COLORS[RED]}error: >>> {message} <<<')


def new_line():
    __send_msg('')


def line(size: int = 30):
    __send_msg(f'{("-- " * size)[:-1]}')
    new_line()
