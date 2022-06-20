import os

# get source file
source = input("mkv file: ")

# get folder name
target = input("result folder name: ")

# refining iterations
iterations = input("number of refining iteration: ")

path = "open3d\\examples\\reconstruction_system\\"

# get color images and depth maps from mkv
os.system(path + "sensors\\azure_kinect_mkv_reader.py --input " + source + " --output " + target)

# 3D reconstruction
reconstruction_command = "python " + path + "run_system.py " + target + "\\config.json"
os.system(reconstruction_command + " --make")
os.system(reconstruction_command + " --register")

for i in range(iterations):
    os.system(reconstruction_command + " --refine")
os.system(reconstruction_command + " --integrate")
