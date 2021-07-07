from mConsole import oConsole;

# Colors used in output for various types of information:
NORMAL =            0x0F07; # Light gray
DIM =               0x0F08; # Dark gray
INFO =              0x0F0D; # Bright purple
HILITE =            0x0F0F; # Bright white
OK =                0x0F02; # Green
OK_INFO =           0x0F0A; # Bright Green
ERROR =             0x0F04; # Red
ERROR_INFO =        0x0F0C; # Bright red
WARNING =           0x0F06; # Yellow
WARNING_INFO =      0x0F0E; # Bright yellow
UNDERLINE =        0x10000;

BAR =               0xFF5D; # Bright purple on Dark purple
PROGRESS =          0xFFD0; # Black on bright purple 

oConsole.uDefaultColor = NORMAL;
oConsole.uDefaultBarColor = BAR;
oConsole.uDefaultProgressColor = PROGRESS;
