# LC-3 Obfuscatron
# Converts all LC3 operations to FILL commands for the assembler
# Written by Michael Kersting Jr.
import sys

# Returns a 2-position hex representation of a character
def cleanHex(data):
    data = hex(ord(data))
    data = data.replace("0x", "")
    if len(data) == 1:
        data = "0"+data
    return data.upper()

# Returns an 8-bit binary representation of a character
def cleanBinary(data):
    data = bin(ord(data))
    data = data.replace("0b", "")
    zeroes = 8 - len(data)
    data = ("0"*zeroes) + data
    return data

# Prints the help menu
def printHelp():
    helpMenu = """
LC-3 Obfuscatron
Converts an LC-3 .obj file to a .asm file with nothing but .FILL

Usage: obfuscatron.py <objfile> -<x|b>

-x | Use hex values
-b | Use binary values
"""
    print(helpMenu)

# Load the data from the OBJ file
if (len(sys.argv) != 3 or sys.argv[1] == "-h" or sys.argv[2] == "-h"):
    printHelp()
    sys.exit(0)

if (sys.argv[2] == "-h"):
    printHelp()
    sys.exit(0)

filename = sys.argv[1]
resultType = sys.argv[2]
filein = open(filename, "rb")
filedata = filein.read()
filein.close()

# Convert each pair of bytes to the specified type
results = list()
labelCounter = 0
for i in range(2, len(filedata), 2):
    byte1 = filedata[i]
    byte2 = filedata[i+1]

    if (resultType == "-x"):
        results.append(".FILL x" + cleanHex(byte1) + cleanHex(byte2) + "\n")
    elif (resultType == "-b"):
        results.append(".FILL b" + cleanBinary(byte1) + cleanBinary(byte2) + "\n")
    else:
        print "Unknown output type \"%s\"" % resultType
        sys.exit(0)

# Save the results to a file
fileout = open(filename.replace(".obj", ".asm"), "w")
fileout.write(".ORIG x3000\n")
for i in results:
    fileout.write(i)
fileout.close()
print "Completed"
