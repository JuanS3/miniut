from typing import Any, List, Union
import functools
import platform
import os

from miniut import config as cfg
from miniut.term import *


__indentation_type  : str = ' '
__indentation_lvl   : str = ''
__indentantion_size : int = 2
__is_init : bool = False
__autoreset_colors: bool = True

__START_LANGS = {
    cfg.ENG : 'START',
    cfg.ESP : 'INICIA',
}

__END_LANGS = {
    cfg.ENG : 'END',
    cfg.ESP : 'TERMINA',
}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                         decorators                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def block(message_block: Union[str, dict],
          color: str = BLUE,
          bg_color: str = ''
          ) -> callable:
    """
    Decorator to create a block of text.

    Parameters
    ----------
    message_block : Union[str, dict]
        if is a str, then is the title of the block, if is a dict, then is the
        title is taken according to the language selected in the config file,
        e.g. {'en': 'Title', 'es': 'Título'} the title is printed is Title if the
        language is `en`, and Título if the language is `es`.

    color : str, optional
        The color of the message, by default BLUE

    bg_color : str, optional
        The background color of the message, by default has no color
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            message = message_block
            if isinstance(message_block, dict):
                message = message_block[cfg.lang()]

            start_block(message, color=color, bg_color=bg_color)
            new_line()
            value = func(*args, **kwargs)
            new_line()
            end_block(message, color=color, bg_color=bg_color)
            return value
        return wrapped
    return decorator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                          functions                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def __init():
    """
    If the console still doesn't start, then start the console without
    clearing the screen, but do nothing if the console is started
    """
    if not __is_init:
        init(False)


def init(clear: bool = True,
         indentation_type: str = ' ',
         indentation_size: int = 2,
         autoreset_colors: bool = True
         ) -> None:
    """
    Initialize the console, and resert the indentation level

    Parameters
    ----------
    clear : bool, optional
        True to clear the screen and False is not, by default True
    """
    global __is_init, __indentation_lvl, __indentantion_size, __indentation_type, __autoreset_colors
    __indentation_lvl = ''
    __indentantion_size = indentation_size
    __indentation_type  = indentation_type
    __autoreset_colors  = autoreset_colors

    if clear:
        clear_screen()
    __is_init = True


def clear_screen():
    """
    Clear the console screen
    """
    os.system('clear' if platform.system() != 'Windows' else 'cls')


def add_lvl():
    """
    Add one level (indentation)
    """
    global __indentation_lvl
    __indentation_lvl += (__indentation_type * __indentantion_size)


def del_lvl():
    """
    Substract one level (indentation)
    """
    global __indentation_lvl
    __indentation_lvl = __indentation_lvl[:-__indentantion_size]


def _colorize(text: str,
              color: str,
              bg_color: str,
              style: str,
              reset_console_colors: bool,
              ) -> str:
    """
    Colorize the text

    Parameters
    ----------
    text : str
        The text to colorize

    color : str
        The color of the text, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    bg_color : str
        The background color of the text, the color must be one of the `BACKGROUNS_LIST`
        or `COLORS_LIST` for all colors available; by default has no color

    style : str
        The style of the text, the style must be one of the `STYLES_LIST`,
        by default has no style

    reset_console_colors : bool
        True to reset all colors, False is not necessary, by default `True`

    Returns
    -------
    str
        The colorized text
    """
    colorized_text = get_color(color) + \
                     get_background(bg_color) + \
                     get_style(style) + \
                     text
    if reset_console_colors:
        colorized_text += reset_colors()

    return colorized_text


def println(*message: Any,
            endl: str = '\n',
            withlvl: bool = True,
            color: str = '',
            bg_color: str = '',
            reset_all_colors: bool = True,
            style: str = '',
            sep: str = ' '
            ) -> None:
    """
    Print the message to the console, the `endl` is the same as `end` in print function
    and is necessary print the message with the current indentation level and the color
    indicate.

    Parameters
    ----------
    message : Any
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

    bg_color : str, optional
        The background color of the message, the color must be one of the `BACKGROUNS_LIST`
        or `COLORS_LIST` for all colors available; by default has no color

    reset_all_colors : bool, optional
        True to reset all colors, False is not necessary, by default `True`

    style : str, optional
        The style of the message, the style must be one of the `STYLES_LIST`,
        by default has no style

    sep : str, optional
        The separator between the values, by default is a space
    """
    __init()
    message = __to_string(*message, sep=sep)

    if withlvl:
        message = __indentation_lvl + message

    reset_console_colors: str = reset_colors() if reset_all_colors or __autoreset_colors else ''
    colorized_text: str = _colorize(text=message,
                                    color=color,
                                    bg_color=bg_color,
                                    style=style,
                                    reset_console_colors=reset_console_colors
                                    )
    print(colorized_text, end=endl)


def __to_string(*values: Any, sep: str = ' ') -> str:
    return sep.join([str(m) for m in values])


def start_block(*message: Any, color: str = BLUE, bg_color: str = '') -> None:
    """
    Start a block of messages

    Parameters
    ----------
    message : Any
        The title of the block

    color : str, optional
        The color of the title block, by default BLUE

    bg_color : str, optional
        The background color of the title block, by default has no color
    """
    message = __to_string(*message)
    println(f'{__START_LANGS[cfg.lang()]} {message.upper()}',
            color=color,
            bg_color=bg_color
            )
    add_lvl()


def end_block(*message: Any,
              color: str = BLUE,
              bg_color: str = '',
              style: str = ''
              ) -> None:
    """
    End a block of messages

    Parameters
    ----------
    message : Any
        The title of the block

    color : str, optional
        The color of the title block, by default BLUE

    bg_color : str, optional
        The background color of the title block, by default has no color

    style : str, optional
        The style of the title block, by default has no style
    """
    message = __to_string(*message)
    del_lvl()
    println(f'{__END_LANGS[cfg.lang()]} {message.upper()}',
            color=color,
            bg_color=bg_color,
            style=style
            )
    new_line()


def warning(*message: Any,
            color: str = BLUE,
            bg_color: str = '',
            style: str = ''
            ) -> None:
    """
    Warning message starts with 'warning: {message}'

    Parameters
    ----------
    message : Any
        The message to display in the log

    color : str, optional
        The color of the message, by default YELLOW

    bg_color : str, optional
        The background color of the message, by default has no color

    style : str, optional
        The style of the message, by default has no style
    """
    message = __to_string(*message)
    println(f'warning: {message}', color=color, bg_color=bg_color, style=style)


def error(*message: Any,
          color: str = RED,
          bg_color: str = '',
          style: str = ''
          ) -> None:
    """
    Error message is displayed like `error: >>> {message} <<<`

    Parameters
    ----------
    message : Any
        The message to display in the log

    color : str, optional
        The color of the message, by default RED

    bg_color : str, optional
        The background color of the message, by default has no color

    style : str, optional
        The style of the message, by default has no style
    """
    message = __to_string(*message)
    println(f'error: >>> {message} <<<', color=color, bg_color=bg_color, style=style)


def new_line():
    """
    Display a blank line in the console
    """
    println('', withlvl=False)


def line(size: int = 30,
         style: str = '-- ',
         color: str = '',
         bg_color: str = '',
         style_text: str = ''
         ) -> None:
    """
    Display a line in the console like this `-- -- -- -- -- -- --`
    whit the indicated size

    Parameters
    ----------
    size : int, optional
        The size of the line to display, by display 30

    style : str, optional
        The style of the line, by default is '-- '

    color : str, optional
        The color of the line, by default has no color

    bg_color : str, optional
        The background color of the line, by default has no color

    style_text : str, optional
        The style of the line, by default has no style
    """
    line: str = style * size
    if line[:-1] == ' ':
        line = line[:-1]
    println(line, color=color, bg_color=bg_color, style=style_text)
    new_line()


def print_emoji_list() -> None:
    """
    Print the list of emojis available
    """
    println('Emojis available:')
    add_lvl()
    for e in EMOJIS_LIST:
        println(f'{emoji(e):2} : {e}')
    del_lvl()


def print_color_list() -> None:
    """
    Print the list of colors available in the console
    """
    println('Colors available:')
    add_lvl()
    for e in COLORS_LIST:
        println(f'{e:7} : ', endl='')
        println('Miniut', color=e, withlvl=False)
    del_lvl()
    new_line()

    print('Background colors available:')
    add_lvl()
    for e in BACKGROUNDS_LIST:
        println(f'{e:10} : ', endl='')
        println('Miniut', bg_color=e, withlvl=False)
    del_lvl()

def print_style_list() -> None:
    """
    Print the list of styles available in the console
    """
    println('Styles available:')
    add_lvl()
    for e in STYLES_LIST:
        println(f'{e:10} : ', endl='')
        println('Miniut', style=e, withlvl=False)
    del_lvl()


def __max_len_value(matrix, nan_format) -> int:

    def max_value(cell) -> int:
        cellstr = str(cell)
        if cellstr in ('None', 'nan', 'NaN'):
            cellstr = nan_format
        return max(max_len, len(cellstr))

    max_len = 0
    for row in matrix:
        if isinstance(row, list):
            for col in row:
                max_len = max_value(col)
        else:
            max_len = max_value(row)
    return max_len


def __print_matrix_header(header: List[str],
                          len_index: int,
                          color_index: str,
                          extra_spacing: str,
                          withlvl: bool,
                          max_len_value: int,
                          lvl_space: int = 3
                          ) -> None:
    """
    Print the header of the matrix

    Parameters
    ----------
    header : List[str]
        If the matrix has a header to print with them, by default None

    len_index : int
        Longest value size index of the indexes

    color_index : str
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available

    extra_spacing : str
        The extra spacing befote printing the header

    withlvl : bool
        True if the matrix should be printed with the current indentation False in otherwise

    max_len_value : int
        Longest value size in the matrix

    lvl_space : int
        Number of aditional spaces based on the style
    """
    spaces: str = ' ' * (len_index + lvl_space)
    indentation: str = __indentation_lvl if withlvl else ''

    println(f'{indentation}{spaces}{extra_spacing}', endl='', withlvl=False)
    for h in header:
        println(f' {h : ^{max_len_value}} ', color=color_index, endl='', withlvl=False)
    new_line()


def __print_matrix_row(row: list,
                       max_len_value: int,
                       color: str,
                       nan_format: str,
                       color_style: str,
                       color_index: str,
                       end_line: str,
                       start_line: str,
                       index_name: str,
                       indentation: str
                       ) -> None:
    """
    Printed the row of the matrix.

    Parameters
    ----------
    row : list
        The row of the matrix to be printed

    max_len_value : int
        Longest value size in the matrix

    color : str
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available

    nan_format : str
        The formatted string to print a NaN/None value

    color_style : str
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available

    color_index : str
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available

    end_line : str
        The end of line to be printed

    start_line : str
        The beginning of line to be printed

    index_name : str
        The name of the index to be printed

    indentation : str
        The indentation of the line
    """
    println(indentation, endl='', withlvl=False)
    println(index_name,  endl='', color=color_index, withlvl=False)
    println(start_line,  endl='', color=color_style, withlvl=False)

    for cell in row:
        cellstr = str(cell) if str(cell) not in ('None', 'nan', 'NaN', '') else nan_format
        println(f' {cellstr : ^{max_len_value}} ', color=color, endl='', withlvl=False)
    println(end_line, color=color_style, withlvl=False)


def __print_matrix_box_style(matrix,
                             header: List[str],
                             indexes: Union[List[str], str],
                             nan_format: str,
                             color: str,
                             color_index: str,
                             color_style: str,
                             max_len_value: int,
                             len_index: int,
                             style : str,
                             withlvl: bool
                             ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    div: str = '-' * (len(matrix[0]) * max_len_value) + '-' * (len(matrix[0]) * 2)
    spaces: str = ' ' * (len_index + 3)
    indentation: str = __indentation_lvl if withlvl else ''

    if header is not None:
        __print_matrix_header(header = header,
                              len_index = len_index,
                              color_index = color_index,
                              extra_spacing = '',
                              withlvl = withlvl,
                              max_len_value = max_len_value
                              )

    bar_div = lambda: println(f'{indentation}{spaces}{div}', color=color_style, withlvl=False)

    bar_div()

    for index_row_id, row in enumerate(matrix):
        __print_matrix_row(row = row,
                           max_len_value = max_len_value,
                           color = color,
                           nan_format = nan_format,
                           color_style = color_style,
                           color_index = color_index,
                           end_line = ' | ' if style == 'box' else '',
                           start_line = ' | ',
                           index_name = f'{indexes[index_row_id]: >{len_index}}' if indexes is not None else '',
                           indentation = indentation
                           )

    bar_div() if style == 'box' else new_line()



def __print_matrix_numpy_style(matrix,
                               header: List[str],
                               indexes: Union[List[str], str],
                               style: str,
                               nan_format: str,
                               color: str,
                               color_index: str,
                               color_style: str,
                               max_len_value: int,
                               len_index: int,
                               withlvl: bool
                               ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    indentation: str = __indentation_lvl if withlvl else ''

    if header is not None:
        __print_matrix_header(header = header,
                              len_index = len_index,
                              color_index = color_index,
                              extra_spacing = '   ',
                              withlvl = withlvl,
                              max_len_value = max_len_value
                              )

    max_rows: int = len(matrix)

    for index_row_id, row in enumerate(matrix):
        # string line
        if index_row_id == 0:
            println(indentation, '[ ', endl='', color=color_style, withlvl=False)
        else:
            println('  ', indentation, endl='', withlvl=False)

        __print_matrix_row(row = row,
                           max_len_value = max_len_value,
                           color = color,
                           nan_format = nan_format,
                           color_style = color_style,
                           color_index = color_index,
                           end_line = ' ]' if max_rows != index_row_id + 1 else ' ]  ]',
                           start_line = ' [ ',
                           index_name = f'{indexes[index_row_id]: >{len_index}}' if indexes is not None else '',
                           indentation = indentation
                           )


def __print_matrix_without_style(matrix,
                                 header: List[str],
                                 indexes: Union[List[str], str],
                                 style: str,
                                 nan_format: str,
                                 color: str,
                                 color_index: str,
                                 color_style: str,
                                 max_len_value: int,
                                 len_index: int,
                                 withlvl: bool
                                 ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    indentation: str = __indentation_lvl if withlvl else ''

    if header is not None:
        __print_matrix_header(header = header,
                              len_index = len_index,
                              color_index = color_index,
                              extra_spacing = '',
                              withlvl = withlvl,
                              max_len_value = max_len_value,
                              lvl_space = 0
                              )

    for index_row_id, row in enumerate(matrix):
        __print_matrix_row(row = row,
                           max_len_value = max_len_value,
                           color = color,
                           nan_format = nan_format,
                           color_style = color_style,
                           color_index = color_index,
                           end_line = '',
                           start_line = '',
                           index_name = f'{indexes[index_row_id]: >{len_index}}' if indexes is not None else '',
                           indentation = indentation
                           )



def print_matrix(matrix,
                 header: Union[List[str], str] = 'all',
                 indexes: Union[List[str], str] = 'all',
                 style: str = 'box',
                 nan_format: str = '',
                 color: str = None,
                 color_index: str = '',
                 color_style: str = '',
                 withlvl: bool = True
                 ) -> None:
    """
    Print a matrix in a pretty formatted

    >>> matrix = [[1, 2, 3], [4, 5, 6]]
    >>> print_matrix(matrix)
    ...
    ...     0  1  2
    ...     -------
    ... 0 | 1  2  3 |
    ... 1 | 4  5  6 |
    ...     -------

    >>> print_matrix(matrix,
    >>>              header=['one', 'two', 'three'],
    >>>              indexes=['row1', 'row2'],
    >>>              style='semibox'
    >>>              )
    ...
    ...          one     two    three
    ...        -----------------------
    ... row1 |    1       2       3
    ... row2 |    4       5       6

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str] | str, optional
        A list of strings if is a presonalized column name
        - `all` to show the index of the column,
        - `None` do not show any index, by default `all`

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name
        - `all` to show the index of the row,
        - `None` do not show any index, by default `all`

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix
        - `numpy` or `np` Has been printed like a NumPy matrix
        - `None` Without borders, only show the values

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    if indexes == 'all':
        indexes = [str(i) for i in range(len(matrix))]

    if header == 'all':
        header = [str(i) for i in range(len(matrix[0]))]


    max_len_value = __max_len_value(matrix, nan_format)
    max_len_value = max(max_len_value, __max_len_value([] if header is None else header, nan_format))

    len_index = 0

    if isinstance(indexes, list):
        len_index: int = __max_len_value(indexes, nan_format)

    kwargs = {'matrix' : matrix,
              'header' : header,
              'indexes' : indexes,
              'nan_format' : nan_format,
              'color' : color,
              'color_index' : color_index,
              'color_style' : color_style,
              'max_len_value' : max_len_value,
              'len_index' : len_index,
              'style' : style,
              'withlvl' : withlvl
              }

    if style is None:
        __print_matrix_without_style(**kwargs)
    elif style in ('box', 'semibox'):
        __print_matrix_box_style(**kwargs)
    elif style in ('numpy', 'np'):
        __print_matrix_numpy_style(**kwargs)
