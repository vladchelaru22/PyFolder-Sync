import os
import shutil
import sys
import time
from pathlib import Path
from datetime import datetime

#defining every command line argument:
psource=sys.argv[1]
pcopy=sys.argv[2]
synctime=int(sys.argv[3])
plog=sys.argv[4]

#use command: 
#python main.py 'source_path' 'copy_path' 'time_interval'(in seconds) 'logfile_path'

#function that compares the two folder trees
def compare_trees(psource,pcopy,synctime):
    #we have 4 operations: file/folder copying, file/folder deletion
    #(if a folder/file is renamed, it will first be deleted and then recreated to match Source)
    
    #for each case I iterated through every folder/file and 
    #logged the operations in a log file and command line
                
        # walking the source folder tree
        for root,dirs,files in os.walk(psource):
            current=os.path.relpath(root,psource) #keeping track of current path relative to source
            copy_root=os.path.join(pcopy,current) #root where the copy is made
            
            for dir in dirs:
                source_dir=os.path.join(root,dir)
                copy_dir=os.path.join(copy_root,dir)
                if not os.path.exists(copy_dir):
                    os.makedirs(copy_dir, exist_ok=True)
                    log_file = open(plog, 'a')
                    log_file.write(
                        f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Created folder: {copy_dir}\n')
                    print(
                        f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Created folder: {copy_dir}')
            
            for file in files:
                source_file=os.path.join(root,file)
                copy_file=os.path.join(copy_root,file)
                if not os.path.exists(copy_file):
                    shutil.copy2(source_file, copy_file)
                    log_file=open(plog, 'a')
                    log_file.write(
                        f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Copied file: {copy_file}\n')
                    print(
                        f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Copied file: {copy_file}')
        
        # checking if any files/folders need to be deleted in the copy folder
        for root,dirs,files in os.walk(pcopy):
            current=os.path.relpath(root,pcopy)
            source_root=os.path.join(psource,current)
            
            for dir in dirs:
                source_dir=os.path.join(source_root,dir)
                copy_dir=os.path.join(root,dir)
                if not os.path.exists(source_dir):
                    shutil.rmtree(copy_dir)
                    log_file=open(plog, 'a')
                    log_file.write(
                        f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Deleted folder: {copy_dir}\n')
                    print(
                        f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Deleted folder: {copy_dir}')
            
            for file in files:
                source_file=os.path.join(source_root,file)
                copy_file=os.path.join(root,file)
                if not os.path.exists(source_file):
                    os.remove(copy_file)
                    log_file=open(plog, 'a')
                    log_file.write(
                        f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Deleted file: {copy_file}\n')
                    print(
                        f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Deleted file: {copy_file}')
        time.sleep(synctime)  # introduce specified interval between syncs

while True:
    compare_trees(psource,pcopy,synctime)
