#!/usr/bin/env python

"""roboxify.py: alters gcode files for printing on CEL Robox 3D printer."""

import re
import sys
import math

commentCharRE = re.compile( r"\S*;" )
gRE = re.compile( r"G\S*" )
xRE = re.compile( r"X\S*" )
yRE = re.compile( r"Y\S*" )
#zRE = re.compile( r"Z\S*" )
eRE = re.compile( r"E\S*" )
#fRE = re.compile( r"F\S*" )
bRE = re.compile( r"B\S*" )

line = "; none"

currentX = 0
currentY = 0
#currentZ = 0
currentE = 0
#currentF = 0
currentB = 0
lineX = 0
lineY = 0
#lineZ = 0
lineE = 0
#lineF = 0
lineB = 0
changeX = 0
changeY = 0
#changeZ = 0
changeE = 0
#changeF = 0
changeB = 0
existingB0 = []
existingB1 = []
extrusionLine = []
retraction = []

readFile_lines = 0

if len(sys.argv) == 1:
	readfile = sys.argv[1]
	if ".gcode" in sys.argv[1]:
		cutLocation = readfile.find(".gcode")
		writefile = readfile[:cutLocation] + "_roboxified.gcode"
	else:
		print("Please enter a *.gcode file as the first argument")
		sys.exit()
	fr = open(readfile, 'r')
	readFile_lines = fr.read().count('\n')
	fr.close()
	fr = open(readfile, 'r')
else:
	print("usage: roboxify.py filename")
	sys.exit()
for i, command in enumerate(fr):
	line = command
	print( "line" + str(i) + ":" + line)
	commentMatch = commentCharRE.match( sampleString )
	if commentMatch:
		print("comment line detected")
	else:
		gMatch = gRE.match( line )
		xMatch = xRE.search( line )
		yMatch = yRE.search( line )
		#zMatch = zRE.search( line )
		eMatch = eRE.search( line )
		#fMatch = fRE.search( line )
		bMatch = bRE.search( line )
		
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
						existingB0.append(i)
					elif bdec > 0:
						print("G1 line with positive B value")
						existingB1.append(i)
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
				#if zMatch:
					#zStr = str(zMatch.group())
					#zStr = zStr[1:(len(zStr))]
					#zDec = float(zStr)
					#lineZ = zDec
					#if zDec == currentZ :
					#	changeZ = 0
					#else:
					#	changeZ = currentZ - lineZ
				if eMatch:
					eStr = str(eMatch.group())
					eStr = eStr[1:(len(eStr))]
					eDec = float(eStr)
					lineE = eDec
					#relative e = any change in e is changeE
					changeE = eDec
				#if fMatch:
					#fStr = str(fMatch.group())
					#fStr = fStr[1:(len(fStr))]
					#fDec = float(fStr)
					#lineF = fDec
					#if fDec == currentF :
						#changeF = 0
					#else:
						#changeF = currentF - lineF
				if changeE > 0 and (changeX > 0 or changeY > 0):
						extrusionLine.add(i)
						print ("extrusion line detected")
				elif changeE < 0:
						retraction.add(i)
						print ("retraction line detected")
				currentX = lineX
				currentY = lineY
				#currentZ = lineZ
				currentE = 0
				#currentF = lineF
				changeX = 0
				changeY = 0
				#changeZ = 0
				changeE = 0
				#changeF = 0
				changeB = 0
fr.close()
