# FontMaker

### ABSTRACT
A simple python script that converts a directory of SVGs to a working TTF or OTF file using the Fontforge module.  Fontforge must be installed via Homebrew (or its' equivalent on other OSs) or compiled by the user in order to gain access to the module and command line functions.

This script is currently slightly speciffic to the font I was creating, but can easily be modified for any font.  You can theoretically do everything in Python, but the main purpose of this script is to eliminate the process of importing and manually setting the kerning/spacing of glyphs.  Then, you can make minor tweaks withing the Fontforge GUI editor. 

### METHODS
The script first cleans the SVGs using [Scour](https://github.com/scour-project/scour), using multithreading to speed up the process (though it is still slow).  It also logs this activity so it only cleans new or modified files, and thus allows you to make slight modifications to the fontforge portion of the script and see the results rapidly.  In my case, this process reduced the SVG file size by an average of ~30% without sacrificing quality.

The script then creates a font object, imports the outlines from the SVG files, and sets the default spacing to be 1/4 of the width of the lowercase "i" glyph from your font set.  This spacing can easily be modified by changing the `spacing` variable in the main function.

It is important that the SVGs are named according to their corresponding character. IE, the capital "A" glyph should be named `A.svg`.  The correct character names can be found in the Fontforge GUI editor by clicking on the glyph and looking for the name in quotes at the top of the application.  Most are named as you would expect, but some are unique.  Because I used Affinity Designer to create my SVGs, I had to name the lowercase char SVGs prefixed with a hyphen (eg. `-a.svg`) as AFD auto-capitalizes them on export for some reason.  If your design software doesn't cause this issue, you should be fine omitting the hyphen.

### NOTES
I dont plan on maintaining this much, but wanted to make it public as I had so much trouble finding a way to do this.  Feel free to create an issue if you have any questions though and I will try and respond when I have time.
