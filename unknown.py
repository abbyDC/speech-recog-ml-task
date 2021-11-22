import os
import random
rootdir = '/home/abbydc/Downloads/speech_commands_v0.02'

subdirs = []
unknown_dir = "/home/abbydc/Downloads/speech_commands_v0.02/_unknown_"
for subdir, dirs, files in os.walk(rootdir):
    subdir = subdir.strip()
    if (subdir != "/home/abbydc/Downloads/speech_commands_v0.02/_unknown_") and (subdir != "/home/abbydc/Downloads/speech_commands_v0.02"):
        subdirs.append(subdir)

unknowns = []
for x in subdirs:
    for filename in os.listdir(x):
        if filename.endswith(".wav"):
            unknowns.append(os.path.join(x,filename))

random.shuffle(unknowns)
for i in range(0,5000):
    new_dir  = unknowns[i].split('/')
    new_dir[5] = '_unknown_'
    new_dir = '/'.join(new_dir)
    os.rename(unknowns[i],new_dir)