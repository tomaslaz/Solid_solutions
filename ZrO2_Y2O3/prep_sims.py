"""
A script to prepare solid solution directories for ZrO2 -> Y2O3, 4x4x4 supercell

"""

import os
import shutil

totalSubstitutions = 128
NAtoms = totalSubstitutions * 6
outputDir = "output/"
dataDir = "data"
masterginFile = "Master.gin"
jobSubmissionFile = "jobSubmit.sh"

def substituteAtoms(targetFile, nSubs):
    """
    A script to substitute ZrO2 with Y2O3 atoms

    The function assumes that Zr atoms are listed starting with 5th line and ends
    at 4 + 2 * totalSubstitutions and O atoms are from 5 + 2 * totalSubstitutions
    and ends 4 + 6 * totalSubstitutions

    targetFile - target file for substitution
    nSubs - total number of substitutions: 2 Zr atoms are replaced with 2 Y atoms,
        1 O atom is replaced with a vacancy.
    """

    targetFileTemp = "%s.tmp" % targetFile

    fileIn = open(targetFile, 'r')
    fileOut = open(targetFileTemp, 'w')

    lineNo = 0
    for line in fileIn:

        # these lines are for atom coordinates
        if (lineNo > 3 and lineNo < 4+NAtoms):

            atomNo = lineNo-3

            # replacing Zr atoms
            if (atomNo <= (2 * nSubs)):
                atomsLineList = line.split()
                atomsLineList[0] = "Y"
                fileOut.write(" ".join(atomsLineList) + "\n")
            # replacing O atoms
            elif ((atomNo > totalSubstitutions*2) and
                  (atomNo <= (totalSubstitutions*2 + nSubs*4)) and
                  ((atomNo % 4) == 0)):

                    atomsLineList = line.split()
                    atomsLineList[1] = "x2"
                    fileOut.write(" ".join(atomsLineList) + "\n")
            # adding other atoms
            else:
                fileOut.write(line)

        else:
            fileOut.write(line)

        lineNo += 1

    fileIn.close()
    fileOut.close()

    shutil.move(targetFileTemp, targetFile)

    return

if __name__ == "__main__":

    # deletes output directory if it exists
    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)

    os.makedirs(outputDir)

    for i in range(totalSubstitutions+1):
        print("Preparing directory %d/%d" % (i+1, totalSubstitutions+1))

        # creating simulation directory
        newDir = os.path.join(outputDir, "simulation%d/data" % (i))

        # copying files from the data directory
        shutil.copytree(dataDir, newDir)

        targetFile = os.path.join(newDir, masterginFile)

        # substitute atoms
        if i > 0:
            substituteAtoms(targetFile, i)

        # copy job submission file
        shutil.copy2(jobSubmissionFile,
            os.path.join(outputDir, "simulation%d/%s" % (i, jobSubmissionFile)))

    print("Finished.")
