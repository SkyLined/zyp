# COMMONLY USED COLOR NAMES
COLOR_DIM                               = 0x0F08; # Dark gray
COLOR_NORMAL                            = 0x0F07; # Light gray
COLOR_HILITE                            = 0x0F0F; # White

COLOR_INFO                              = 0x0F0D; # Bright purple
COLOR_LIST                              = 0x0F0D; # Bright purple

COLOR_BUSY                              = 0x0F03; # Cyan
COLOR_OK                                = 0x0F02; # Green
COLOR_WARNING                           = 0x0F06; # Brown
COLOR_ERROR                             = 0x0F04; # Red

COLOR_SELECT_YES                        = 0x0F0D; # Bright purple
COLOR_SELECT_MAYBE                      = 0x0F05; # Dark purple
COLOR_SELECT_NO                         = 0x0F05; # Dark purple

COLOR_INPUT                             = 0x0F0B; #
COLOR_OUTPUT                            = 0x0F07; #

COLOR_ADD                               = 0x0F0A; # Bright green
COLOR_MODIFY                            = 0x0F0B; # Bright cyan
COLOR_REMOVE                            = 0x0F0C; # Bright red

COLOR_PROGRESS_BAR                      = 0xFF85; # Dark purple on dark gray
COLOR_PROGRESS_BAR_HILITE               = 0xFF5D; # bright purple on dark purple 
COLOR_PROGRESS_BAR_SUBPROGRESS          = 0xFFD0; # Black on bright purple

CONSOLE_UNDERLINE                       = 0x10000;

# COMMONLY USED CHARS
CHAR_INFO                               = "→";
CHAR_LIST                               = "•";

CHAR_BUSY                               = "»";
CHAR_OK                                 = "√";
CHAR_WARNING                            = "▲";
CHAR_ERROR                              = "×";

CHAR_SELECT_YES                         = "●";
CHAR_SELECT_MAYBE                       = "•";
CHAR_SELECT_NO                          = "·";

CHAR_INPUT                              = "◄";
CHAR_OUTPUT                             = "►";

CHAR_ADD                                = "+";
CHAR_MODIFY                             = "±";
CHAR_REMOVE                             = "-";
CHAR_IGNORE                             = "·";

# DEFAULTS
from mConsole import oConsole;
oConsole.uDefaultColor = COLOR_NORMAL;
oConsole.uDefaultBarColor = COLOR_PROGRESS_BAR;
oConsole.uDefaultProgressColor = COLOR_PROGRESS_BAR_HILITE;
oConsole.uDefaultSubProgressColor = COLOR_PROGRESS_BAR_SUBPROGRESS;
