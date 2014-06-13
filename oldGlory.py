"""
OLD GLORY
By David Jonathan Ross <http://www.djr.com>

This drawbot script will draw the American Flag. 

It's also responsive! I made this to experiment with Drawbot Variables. 

For the most part, it follows the rules here:    
    http://en.wikipedia.org/wiki/Flag_of_the_United_States#Specifications
    
It does make some small allowances in order to get better results when the
variables are customized.

Wouldn't it be cool if the stars followed the historical patterns, starting with the ring of 13? Maybe next time.
"""

import random
from AppKit import NSColor

######
# SETTING GLOBAL VARIABLES
######
# define some of our key variables as special DrawBot variables, which can be manipulated with a simple UI

Variable([
    dict(
        name='flagSize', 
        ui='Slider', 
        args=dict(
            minValue=1, 
            maxValue=10, 
            value=5, 
            tickMarkCount=10, 
            stopOnTickMarks=True
            )
        ),
    dict(
        name='proportion', 
        ui='Slider', 
        args=dict(
            minValue=1, 
            maxValue=3, 
            value=1.9, 
            tickMarkCount=21, 
            stopOnTickMarks=True
            )
        ),
    dict(
        name='stripeCount', 
        ui='Slider', 
        args=dict(
            minValue=1, 
            maxValue=21, 
            value=13, 
            tickMarkCount=11, 
            stopOnTickMarks=True
            )
        ),
    dict(
        name='starRows', 
        ui='Slider', 
        args=dict(
            minValue=1, 
            maxValue=21, 
            value=9, 
            tickMarkCount=11, 
            stopOnTickMarks=True
            )
        ),
    dict(
        name='starCols', 
        ui='Slider', 
        args=dict(
            minValue=1, 
            maxValue=21, 
            value=11, 
            tickMarkCount=11, 
            stopOnTickMarks=True
            )
        ),
    dict(
        name='oddStripeColor', 
        ui='ColorWell', 
        args=dict(color=NSColor.redColor())
        ),
    dict(
        name='evenStripeColor', 
        ui='ColorWell', 
        args=dict(color=NSColor.whiteColor())
        ),
    dict(
        name='cantonColor', 
        ui='ColorWell', 
        args=dict(color=NSColor.blueColor())
        ),
    dict(
        name='starColor', 
        ui='ColorWell', 
        args=dict(color=NSColor.whiteColor())
        ),
    dict(
        name='jasperize', 
        ui='Slider', 
        args=dict(
            minValue=1, 
            maxValue=6, 
            value=1, 
            tickMarkCount=6, 
            stopOnTickMarks=True
            )
        ),
    ], globals())

# here are some other variables that will help us draw the flag

inch = 72
# our base unit, the height of the flag
unit = flagSize * inch

# some of the variables come out of the UI as floats, but I need them as ints
# since I intend to use them with the range() function
jasperize = int(round(jasperize))
stripeCount = int(round(stripeCount))
starRows = int(round(starRows))
starCols = int(round(starCols))

# flag dimensions
#proportion = 1.9 ###### this is now an adjustable variable
pageWidth = unit * proportion
pageHeight = unit 

# stripes
stripeHeight = pageHeight / int(round(stripeCount))

# canton
cantonHeight = stripeHeight * ( int(round(stripeCount)/2) + 1)
cantonWidth = (2 / 5) * pageWidth

# stars
starColWidth = cantonWidth / (starCols+1)
starRowWidth = cantonHeight / (starRows+1)
# starDiameter should be defined as (4 / 5) * stripeHeight, but this rule
# allows decent star sizing regardless of the number of starCols or starRows
starDiameter = min(starColWidth, starRowWidth)


# let's define the drawing of the star as a function, since we will be using it a lot
def star(x, y, d, b=None):
    # this is a hacky, non-mathematically correct star made from two polygons
    # if I were good at math, I would have drawn this a smarter way
    fill(starColor)
    r = d/2
    # an upside down triangle
    newPath()
    moveTo((x-r/1.1, y+r/3.5))
    lineTo((x+r/1.1, y+r/3.5))
    lineTo((x, y-r/2.6))
    closePath()
    drawPath()
    # a right side up triangle with a divet in the bottom
    newPath()
    moveTo((x, y+r))
    lineTo((x-r/1.6, y-r/1.3))
    lineTo((x, y-r/2.6))
    lineTo((x+r/1.6, y-r/1.3))
    closePath()
    drawPath()

######
# BUILD THE FLAG
######

# set page size
size(pageWidth, pageHeight)

# Loop through all the times we are going to draw the flag
for flag in range(jasperize):
    # Stripes
    # build the stripes up from the origin
    y = 0
    for stripe in range(stripeCount):
        if stripe % 2:
            fill(evenStripeColor)
        else:
            fill(oddStripeColor)
        rect(0, y, pageWidth, stripeHeight)
        # increment the y value so we travel up the page
        y += pageHeight/stripeCount

    # CANTON (that's the blue thing)
    # make a rectangle from the top left corner
    fill(cantonColor)
    rect(0, pageHeight-cantonHeight, cantonWidth, cantonHeight)

    # STARS
    # the american flag does not contain an even grid of stars
    # some rows have 6 stars, others have 5 
    # some columns have 5 stars, others have 4
    # but if we think of the canton as a checkerboard, there is a 9x11 grid 
    # where each position can have either a star or a gap.

    # let's define the position where we will start drawing the stars
    starOriginX = starColWidth
    starOriginY = pageHeight - cantonHeight + starRowWidth

    # now let's define some variables that we will change as we loop through
    starX = starOriginX
    starY = starOriginY

    # loop through all of the rows
    for y in range(starRows):
        # loop through all of the columns
        for x in range(starCols):
            # if both row and column are odd, draw the star
            if not x % 2 and not y % 2:
                star(starX, starY, starDiameter)
            # if both row and column are even, also draw the star:
            elif x % 2 and y % 2:
                star(starX, starY, starDiameter)
            # if the row is odd and the column is even, or vice versa
            # we should draw nothing
            # increment the x value to continue across the row
            starX += starColWidth
        # when we are done with the row, reset the x value and increment the y
        starX = starOriginX
        starY += starRowWidth
    
    # Draw the shadow as two rectangles
    shadowLength = height() / 30
    fill(0, 0, 0, .5)
    rect(shadowLength, -shadowLength*2, width()+shadowLength, shadowLength*2)
    rect(width(), 0, shadowLength*2, height()-shadowLength)
   
    # now that we are done drawing the flag 
    # scale the canvas, and relocate our canvas's position to the center
    # this way, all future drawing will happen at a new scale, for jasperization
    scaleFactor = .78
    widthDiff = width()-width()*scaleFactor
    heightDiff = height()-height()*scaleFactor
    translate(widthDiff/2, heightDiff/2)
    scale(scaleFactor)
    
# keep your eye on that grand old flag!
