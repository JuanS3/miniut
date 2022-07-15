__ICONS = {
    (WARNING := 'warning') : '⚠',
    (ERROR   := 'error')   : '❌',
    (SUCCESS := 'success') : '✅',
    (INFO := 'info')    : '💡',
    (QUESTION := 'question') : '❓',
    (ANSWER := 'answer') : '💬',
    (HEART := 'heart') : '❤',
    (STAR := 'star') : '⭐',
    (CIRCLE := 'circle') : '⚪',
    (CROSS := 'cross') : '❌',
    (TRIANGLE_RIGHT := 'triangle_right') : '▶',
    (TRIANGLE_LEFT := 'triangle_left') : '◀',
    (TRIANGLE_UP := 'triangle_up') : '▲',
    (TRIANGLE_DOWN := 'triangle_down') : '▼',

    # ARROWS
    (ARROW_LEFT := 'arrow_left') : '⬅',
    (ARROW_RIGHT := 'arrow_right') : '➡',
    (ARROW_UP := 'arrow_up') : '⬆',
    (ARROW_DOWN := 'arrow_down') : '⬇',
    (ARROW_LEFT_RIGHT := 'arrow_left_right') : '↔',
    (ARROW_UP_DOWN := 'arrow_up_down') : '↕',
    (ARROW_UP_LEFT := 'arrow_up_left') : '⬅⬆',
    (ARROW_UP_RIGHT := 'arrow_up_right') : '➡⬆',
    (ARROW_DOWN_LEFT := 'arrow_down_left') : '⬅⬇',
    (ARROW_DOWN_RIGHT := 'arrow_down_right') : '➡⬇',
    (ARROW_LEFT_RIGHT_UP := 'arrow_left_right_up') : '↖',
    (ARROW_LEFT_RIGHT_DOWN := 'arrow_left_right_down') : '↘',
    (ARROW_UP_DOWN_LEFT := 'arrow_up_down_left') : '↗',
    (ARROW_UP_DOWN_RIGHT := 'arrow_up_down_right') : '↙',

}

ICONS_LIST = list(__ICONS.keys())


def icon(icon: str) -> str:
    """
    Return the icon of the given name

    Parameters
    ----------
    icon : str
        The name of the icon to return
    """
    return __ICONS[icon] if icon in ICONS_LIST else ''
