class PrintColored:
    DEFAULT = '\033[0m'
    # Styles
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    UNDERLINE_THICK = '\033[21m'
    HIGHLIGHTED = '\033[7m'
    HIGHLIGHTED_BLACK = '\033[40m'
    HIGHLIGHTED_RED = '\033[41m'
    HIGHLIGHTED_GREEN = '\033[42m'
    HIGHLIGHTED_YELLOW = '\033[43m'
    HIGHLIGHTED_BLUE = '\033[44m'
    HIGHLIGHTED_PURPLE = '\033[45m'
    HIGHLIGHTED_CYAN = '\033[46m'
    HIGHLIGHTED_GREY = '\033[47m'

    HIGHLIGHTED_GREY_LIGHT = '\033[100m'
    HIGHLIGHTED_RED_LIGHT = '\033[101m'
    HIGHLIGHTED_GREEN_LIGHT = '\033[102m'
    HIGHLIGHTED_YELLOW_LIGHT = '\033[103m'
    HIGHLIGHTED_BLUE_LIGHT = '\033[104m'
    HIGHLIGHTED_PURPLE_LIGHT = '\033[105m'
    HIGHLIGHTED_CYAN_LIGHT = '\033[106m'
    HIGHLIGHTED_WHITE_LIGHT = '\033[107m'

    STRIKE_THROUGH = '\033[9m'
    MARGIN_1 = '\033[51m'
    MARGIN_2 = '\033[52m' # seems equal to MARGIN_1
    # colors
    BLACK = '\033[30m'
    RED_DARK = '\033[31m'
    GREEN_DARK = '\033[32m'
    YELLOW_DARK = '\033[33m'
    BLUE_DARK = '\033[34m'
    PURPLE_DARK = '\033[35m'
    CYAN_DARK = '\033[36m'
    GREY_DARK = '\033[37m'

    BLACK_LIGHT = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    def __init__(self):
        self.print_original = print # old value to the original print function
        self.current_color = self.DEFAULT

    def __call__(self,
                 *values: object, sep: str | None = None,
                 end: str | None = None,
                 file: str | None = None,
                 flush: bool = False,
                 color: str|None = None,
                 default_color: str|None = None,
    ):
        if default_color:
            self.current_color = default_color

        default = self.current_color
        if color:
            values = (color, *values, default)  # wrap the content within a selected color an a default
        else:
            values = (*values, default)  # wrap the content within a selected color an a default
        self.print_original(*values, end=end, file=file, flush=flush)

if __name__ == '__main__':
    print = PrintColored()

    print("Hello world - default")
    print("Hello world - Bold", color=print.BOLD)
    print("Hello world - Italic", color=print.ITALIC)
    print("Hello world - Underline", color=print.UNDERLINE)
    print("Hello world - UNDERLINE_THICK", color=print.UNDERLINE_THICK)
    print("Hello world - HighLithted", color=print.HIGHLIGHTED)
    print("Hello world - HIGHLIGHTED_BLACK", color=print.HIGHLIGHTED_BLACK)
    print("Hello world - HIGHLIGHTED_RED", color=print.HIGHLIGHTED_RED)
    print("Hello world - HIGHLIGHTED_GREEN", color=print.HIGHLIGHTED_GREEN)
    print("Hello world - HIGHLIGHTED_YELLOW", color=print.HIGHLIGHTED_YELLOW)
    print("Hello world - HIGHLIGHTED_BLUE", color=print.HIGHLIGHTED_BLUE)
    print("Hello world - HIGHLIGHTED_PURPLE", color=print.HIGHLIGHTED_PURPLE)
    print("Hello world - HIGHLIGHTED_CYAN", color=print.HIGHLIGHTED_CYAN)
    print("Hello world - HIGHLIGHTED_GREY", color=print.HIGHLIGHTED_GREY)
    print("Hello world - HIGHLIGHTED_GREY_LIGHT", color=print.HIGHLIGHTED_GREY_LIGHT)
    print("Hello world - HIGHLIGHTED_RED_LIGHT", color=print.HIGHLIGHTED_RED_LIGHT)
    print("Hello world - HIGHLIGHTED_GREEN_LIGHT", color=print.HIGHLIGHTED_GREEN_LIGHT)
    print("Hello world - HIGHLIGHTED_YELLOW_LIGHT", color=print.HIGHLIGHTED_YELLOW_LIGHT)
    print("Hello world - HIGHLIGHTED_BLUE_LIGHT", color=print.HIGHLIGHTED_BLUE_LIGHT)
    print("Hello world - HIGHLIGHTED_PURPLE_LIGHT", color=print.HIGHLIGHTED_PURPLE_LIGHT)
    print("Hello world - HIGHLIGHTED_CYAN_LIGHT", color=print.HIGHLIGHTED_CYAN_LIGHT)
    print("Hello world - HIGHLIGHTED_WHITE_LIGHT", color=print.HIGHLIGHTED_WHITE_LIGHT)
    print("Hello world - STRIKE_THROUGH", color=print.STRIKE_THROUGH)
    print("Hello world - MARGIN_1", color=print.MARGIN_1)
    print("Hello world - MARGIN_2", color=print.MARGIN_2)

    print("Hello world - BLACK", color=print.BLACK)
    print("Hello world - RED_DARK", color=print.RED_DARK)
    print("Hello world - GREEN_DARK", color=print.GREEN_DARK)
    print("Hello world - YELLOW_DARK", color=print.YELLOW_DARK)
    print("Hello world - BLUE_DARK", color=print.BLUE_DARK)
    print("Hello world - PURPLE_DARK", color=print.PURPLE_DARK)
    print("Hello world - CYAN_DARK", color=print.CYAN_DARK)
    print("Hello world - GREY_DARK", color=print.GREY_DARK)
    print("Hello world - BLACK_LIGHT", color=print.BLACK_LIGHT)
    print("Hello world - BLACK_LIGHT", color=print.BLACK_LIGHT)
    print("Hello world - RED", color=print.RED)
    print("Hello world - GREEN", color=print.GREEN)
    print("Hello world - YELLOW", color=print.YELLOW)
    print("Hello world - BLUE", color=print.BLUE)
    print("Hello world - PURPLE", color=print.PURPLE)
    print("Hello world - CYAN", color=print.CYAN)
    print("Hello world - WHITE", color=print.WHITE)

    # Back to normal
    print("", default_color=print.DEFAULT)
    print("Hello world - default")