#!/usr/bin/python

import os
import hashlib
import glob

# Delete the hashfile if it exists
for f in glob.glob(".src*"):
    os.remove(f)

for f in glob.glob(".dst*"):
    os.remove(f)

def hash_me_a_dir(func_hash_file, func_directory, func_dir_type):

    # Determine the number of total files recursively
    total_of_files = 0
    for root, dirs, files in os.walk(func_directory):
        total_of_files += len(files)

    current_file_count = 0
    # Analyzing the files recursively
    for root, directories, filenames in os.walk(func_directory):

        for filename in filenames:
            current_file_count += 1
            my_file_absolute = os.path.join(root, filename)
            #print "analyzing file "+my_file_absolute
            #print "processing file "+str(current_file_count)+" of "+str(total_of_files)+" => "+my_file_absolute
            print "processing file "+str(current_file_count)+" of "+str(total_of_files)+" [ \""+my_file_absolute+"\" ]"
            try:
                with open(my_file_absolute, 'rb') as fuck:
                    content = fuck.read()
                    currenthash = hashlib.sha256(content).hexdigest()
            except:
                print "file "+my_file_absolute+" is not readable - ignoring"
                pass

            with open(func_hash_file, "a") as my_hash_file:
                my_hash_file.write(currenthash+' ')
                my_hash_file.write('"'+filename+'" ')
                my_hash_file.write('"'+my_file_absolute+'"\n')

# Call the function
hash_me_a_dir(".src_hashfile.txt", "/tmp", "src")
hash_me_a_dir(".dst_hashfile.txt", "/pictures", "dst")

with open(".src_hashfile.txt") as f:
    for line in f:
        my_current_checksum = line.split()[0]
        with open(".dst_hashfile.txt") as dst_hash_file:
            found = (my_current_checksum in dst_hash_file.read().split())
        if found:
            print "file "+(line.split()[2])+" already exists - ignoring"
        else:
            print "file "+(line.split()[2])+" is new - will be copied"
