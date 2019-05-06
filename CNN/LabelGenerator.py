import os

folder = "..\\Calgary_PS_DTI_Dataset\\"
labelfname = "Bad750Volumes.csv"
sliceStart = 96
sliceEnd = 160
niiFiles = []
for dirpaths, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.nii'):
            filePath = os.path.join(dirpaths, file)
            niiFiles.append(filePath)

#dict of bad volumes based on scan name
print("Getting bad volumes from csv")
badVols = dict()
with open(labelfname) as f:
    lines = f.readlines()
    for i in range(1, len(lines)):
        line = lines[i].split(',')
        vols = line[1].strip()
        vols = vols.split(';')
        #subtract one for 0 indexing
        vols = [int(vol)-1 for vol in vols if vol != '']
        sName = line[0].upper().strip().replace('-','')
        badVols[sName] = vols

print("Generating slice ids and labels")
#ID format: (filepath, volume, direction, slice number)
idList = list()
labels = dict()
for file in niiFiles:
    sStart = file.rfind('\\')
    sEnd = file.rfind('_')
    sName = file[sStart+1:sEnd]
    for volNum in range(35):
        label = 0
        if sName in badVols:
            if volNum in badVols[sName]:
                label = 1
        #64 slices centered around the middle assuming size 255
        for sliceNum in range(96,160):
            #sagittal
            tempId = (file, volNum, 1, sliceNum)
            idList.append(tempId)
            labels[tempId] = label
            #coronal
            tempId = (file, volNum, 2, sliceNum)
            idList.append(tempId)
            labels[tempId] = label
print("Done")