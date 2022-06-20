import os

# get source file
src = input("mkv file: ")

# get folder name
trgt = input("result folder name: ")

path = "open3d\\examples\\reconstruction_system\\"

# get color images and depth maps from mkv
os.system(path + "sensors\\azure_kinect_mkv_reader.py --input " + src + " --output " + trgt)

# 3D reconstruction
rec_command = "python " + path + "run_system.py " + trgt + "\\config.json"
os.system(rec_command + " --make")
os.system(rec_command + " --register")
os.system(rec_command + " --refine")
os.system(rec_command + " --integrate")
