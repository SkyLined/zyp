from mConsole import oConsole;

from mColors import *;

asLogo = [s.rstrip() for s in """
                                                                                
        .dSSSSSSSP' YSb   ,dSP' iSSSSSSb,                                       
            ,dSP'    YSb,dSP'  iSP` _7SP`   Python zip (de-)compression utility 
          ,dSP'       )dSP'   iSSSSSS*'                                         
        ,dSP'       ,dSP'    iSP`          http://github.com/SkyLined/zyp       
      .dSSSSSSP'  .dSP'     iSP`                                                
                                                                                """.split("""
""")];

# We can now add color to console output, so let's create a second version of
# the above logo, but with color information (" " = default terminal color, hex
# digit = color number.
asLogoColors = [s.rstrip() for s in """
                                                                                
        5DDDDDDDDD5 5DD   5DDD5 5DDDDDDD5                                       
            5DDD5    5DD5DDD5  5DD5 5DDD5   777777 777 7777777777777777 7777777 
          5DDD5       5DDD5   5DDDDDD55                                         
        5DDD5       5DDD5    5DD5          777777777777777777777777777777       
      5DDDDDDDD5  5DDD5     5DD5                                                
                                                                                """.split("""
""")];

def fPrintLogo():
  # We will use the above ASCII and color data to create a list of arguments
  # that can be passed to oConsole.fOutput in order to output the logo in color:
  for uLineIndex in range(len(asLogo)):
    uCurrentColor = NORMAL;
    bUnderlined = False;
    asLogoPrintArguments = [""];
    sCharsLine = asLogo[uLineIndex];
    sColorsLine = asLogoColors[uLineIndex];
    uColorIndex = 0;
    for uColumnIndex in range(len(sCharsLine)):
      sColor = sColorsLine[uColorIndex];
      uColorIndex += 1;
      if sColor == "_":
        bUnderlined = not bUnderlined;
        sColor = sColorsLine[uColorIndex];
        uColorIndex += 1;
      uColor = (sColor != " " and (0x0F00 + int(sColor, 16)) or NORMAL) + (bUnderlined and UNDERLINE or 0);
      if uColor != uCurrentColor:
        asLogoPrintArguments.extend([uColor, ""]);
        uCurrentColor = uColor;
      sChar = sCharsLine[uColumnIndex];
      asLogoPrintArguments[-1] += sChar;
    oConsole.fOutput(*asLogoPrintArguments);
