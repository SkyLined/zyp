from oConsole import oConsole;
from mColors import *;

asLogo = [s.rstrip() for s in """
                                                                                
        .dSSSSSSSP' YSb   ,dSP' iSSSSSSb                                        
            ,dSP'    YSb,dSP'  iSP` _7SP     Python zip compression utility     
          ,dSP'       )dSP'   iSSSSSS*'                                         
        ,dSP'       ,dSP'    iSP`          http://github.com/SkyLined/zyp       
      .dSSSSSSP'  .dSP'     iSP`                                                
                                                                                """.split("""
""")];

# We can now add color to console output, so let's create a second version of
# the above logo, but with color information (" " = default terminal color, hex
# digit = color number.
asLogoColors = [s.rstrip() for s in """
                                                                                
        DD5555555DD D5D   DD5DD D555555D                                        
            DD5DD    D5DDD5DD  D5DD DD5D     777777 777 77777777777 7777777     
          DD5DD       DD5DD   D555555DD                                         
        DD5DD       DD5DD    D5DD          555555555555555555555555555555       
      D5555555DD  DD5DD     D5DD                                                
                                                                                """.split("""
""")];

def fPrintLogo():
  # We will use the above ASCII and color data to create a list of arguments
  # that can be passed to oConsole.fPrint in order to output the logo in color:
  oConsole.fLock();
  try:
    for uLineIndex in xrange(len(asLogo)):
      uCurrentColor = NORMAL;
      bUnderlined = False;
      asLogoPrintArguments = [""];
      sCharsLine = asLogo[uLineIndex];
      sColorsLine = asLogoColors[uLineIndex];
      uColorIndex = 0;
      for uColumnIndex in xrange(len(sCharsLine)):
        sColor = sColorsLine[uColorIndex];
        uColorIndex += 1;
        if sColor == "_":
          bUnderlined = not bUnderlined;
          sColor = sColorsLine[uColorIndex];
          uColorIndex += 1;
        uColor = (sColor != " " and (0x0F00 + long(sColor, 16)) or NORMAL) + (bUnderlined and UNDERLINE or 0);
        if uColor != uCurrentColor:
          asLogoPrintArguments.extend([uColor, ""]);
          uCurrentColor = uColor;
        sChar = sCharsLine[uColumnIndex];
        asLogoPrintArguments[-1] += sChar;
      oConsole.fPrint(*asLogoPrintArguments);
  finally:
    oConsole.fUnlock();
