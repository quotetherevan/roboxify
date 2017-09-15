#!/usr/bin/env python

"""roboxify.py: alters gcode files for printing on CEL Robox 3D printer."""

import re
import sys
import math

commentCharRE = re.compile( r"\S*;" )
gRE = re.compile( r"G\S*" )
xRE = re.compile( r"X\S*" )
yRE = re.compile( r"Y\S*" )
eRE = re.compile( r"E\S*" )
bRE = re.compile( r"B\S*" )

line = "; none"

currentX = 0
currentY = 0
currentE = 0
currentB = 0
lineX = 0
lineY = 0
lineE = 0
lineB = 0
changeX = 0
changeY = 0
changeE = 0
changeB = 0
extrusion = []
retraction = []
bOn = []
bOff = []

if len(sys.argv) == 1:
	readfile = sys.argv[1]
	if ".gcode" in sys.argv[1]:
		cutLocation = readfile.find(".gcode")
		writefile = readfile[:cutLocation] + "_roboxified.gcode"
	else:
		print("Please enter a *.gcode file as the first argument")
		sys.exit()
else:
	print("usage: roboxify.py filename")
	sys.exit()
fr = open(readfile, 'r')
lines = [line.rstrip('\r\n') for line in fr]
fr.close()

for i, command in enumerate(lines):
	print( "line" + str(i) + ":" + command)
	commentMatch = commentCharRE.match( sampleString )
	if commentMatch:
		print("comment line detected")
	else:
		gMatch = gRE.match( command )
		xMatch = xRE.search( command )
		yMatch = yRE.search( command )
		eMatch = eRE.search( command )
		bMatch = bRE.search( command )
		
		if gMatch:
			gStr = str(gMatch.group())
			gStr = gStr[1:(len(gStr))]
			gDec = float(gStr)
			if gDec == 1 :
				print ("G1 line detected")			
				if bMatch:
					bStr = str(bMatch.group())
					bStr = bStr[1:(len(bStr))]
					bDec = float(bStr)
					if bDec == 0:
						print("WARNING: G1 line with B0 value")
						bOff.append(i)
					elif bdec > 0:
						print("G1 line with positive B value")
						bOn.append(i)
					lineB = bDec
					if currentB == lineB:
						changeB = 0
					else:
						changeB = currentB - lineB
						print("B value change: " + str(changeB) + " oldB: " + str(currentB) + " newB: " + str (lineB))
					currentB = lineB
				if xMatch:
					xStr = str(xMatch.group())
					xDec = float(xStr[1:(len(xStr))])
					lineX = xDec
					if xDec == currentX :
						changeX = 0
					else:
						changeX = currentX - lineX
				if yMatch:
					yStr = str(yMatch.group())
					yDec = float(yStr[1:(len(yStr))])
					lineY = yDec
					if yDec == currentY :
						changeY = 0
					else:
						changeY = currentY - lineY
				if eMatch:
					eStr = str(eMatch.group())
					eStr = eStr[1:(len(eStr))]
					eDec = float(eStr)
					lineE = eDec
					#relative e = any change in e is changeE
					changeE = eDec
				if changeE > 0 and (changeX > 0 or changeY > 0):
						extrusion.add(i)
						print ("extrusion line detected")
				elif changeE < 0:
						retraction.add(i)
						print ("retraction line detected")
				currentX = lineX
				currentY = lineY
				currentE = 0
				changeX = 0
				changeY = 0
				changeE = 0
				changeB = 0
				
for i, command in enumerate(lines):
	if i in bOn:
		currentB = 1
	elif i in bOff:
		currentB = 0
	if currentB == 0 and i in extrusion:
		#check for consecutive extrusions
		if (i + 1) in extrusion and (i+2) in extrusion and (i + 3) in extrusion:
			x1Match = xRE.search( command )
			if x1Match:
				x1Str = str(x1Match.group())
				x1 = float(x1Str[1:(len(x1Str))])
			else:
				x1 = 0
			y1Match = yRE.search( command )
			if y1Match:
				y1Str = str(y1Match.group())
				y1 = float(y1Str[1:(len(y1Str))])
			else:
				y1 = 0
			x2Match = xRE.search( lines[i+1] )
			if x2Match:
				x2Str = str(x2Match.group())
				x2 = float(x2Str[1:(len(x2Str))])
			else:
				x2 = 0
			y2Match = yRE.search( lines[i+1] )
			if y2Match:
				y2Str = str(y2Match.group())
				y2 = float(y2Str[1:(len(y2Str))])
			else:
				y2 = 0
			x3Match = xRE.search( lines[i+2] )
			if x3Match:
				x3Str = str(x3Match.group())
				x3 = float(x3Str[1:(len(x3Str))])
			else:
				x3 = 0
			y3Match = yRE.search( lines[i+2] )
			if y3Match:
				y3Str = str(y3Match.group())
				y3 = float(y3Str[1:(len(y3Str))])
			else:
				y3 = 0
			distTravelled = 0
			if y2 - y1 > 0 or y2 -y1 < 0 or x2 - x1 > 0 or x2 - x1 < 0:	
				distTravelled = distTravelled + math.hypot(x2 - x1, y2 - y1)
				#todo compare distace to 2mm and alter lines if close to 2mm
			if y3 - y2 > 0 or y3 -y2 < 0 or x3 - x2 > 0 or x2 - x2 < 0:
				distTravelled = distTravelled + math.hypot(x3 - x2, y3 - y2)
				#todo compare distace to 2mm and alter lines if close to 2mm
			if y4 - y3 > 0 or y4 -y3 < 0 or x4 - x3 > 0 or x4 - x3 < 0:
				distTravelled = distTravelled + math.hypot(x4 - x3, y4 - y3)
				#todo compare distace to 2mm and alter lines if close to 2mm

#todo find vlave closes and alter those to be done gradually
#todo write new file
