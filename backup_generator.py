import os
import shutil
import time
import hashlib
from datetime import datetime


class Log:

    def create_backup(self, logg_location):
        log = open(logg_location + f"\log.txt", 'a')
        log.write('The backup was created \n')
        log.close()

    def dir_added(self, filepath, logg_location):
        log = open(logg_location + f"\log.txt", 'a')
        log.write(f"{filepath} was created in the source, "
                          f"adding it to backup also @ {datetime.now()} \n")
        log.close()

    def file_added(self, filepath, logg_location):
        log = open(logg_location + f"\log.txt", 'a')
        log.write(f"{filepath} was created in the source, "
                  f"adding it to backup also @ {datetime.now()} \n")
        log.close()

    def file_updated(self, filepath, logg_location):
        log = open(logg_location + f"\log.txt", 'a')
        log.write(f"{filepath} was updated in the source, "
                  f"updating it to backup also @ {datetime.now()} \n")
        log.close()

    def deleted(self, filepath, logg_location):
        log = open(logg_location + f"\log.txt", 'a')
        log.write(f"{filepath} was deleted from the source, "
                  f"deleting it from backup also @ {datetime.now()} \n")
        log.close()


writing_log = Log()

source_location = input("Enter the absolute path of the file you want to create a backup to: ")
backup_location = input("Enter the absolute path to the location where you want the backup: ")
log_location = input("Enter the absolute path to where you want the log file: ")
time_sync = int(input("Please specify the time (in minutes) you want to sync the file with the backup file: "))

shutil.copytree(source_location, f"{backup_location}", dirs_exist_ok=True)
log = open(log_location+f"\log.txt", 'a')
log.write('The backup was created \n')
log.close()


def backup_generator(source_filepath: str, backup_filepath: str):
    for i in os.listdir(source_filepath):
        i_loc = str(source_filepath + f"\{i}")
        if os.path.isdir(os.path.join(source_filepath, i)):
            if not os.path.exists(os.path.join(backup_filepath, i)):
                shutil.copytree(i_loc, os.path.join(backup_filepath, i))
                writing_log.dir_added(os.path.join(source_filepath, i), log_location)
                print(f"{i} was not in backup, added it")
            else:
                backup_generator(os.path.join(source_filepath, i), os.path.join(backup_filepath, i))

        elif os.path.isfile(os.path.join(source_filepath, i)):
            if not os.path.exists(os.path.join(backup_filepath, i)):
                try:
                    shutil.copy2(i_loc, os.path.join(backup_filepath, i), follow_symlinks=False)
                    print(f"{i} was not in backup, added it")
                    writing_log.file_added(os.path.join(source_filepath, i), log_location)
                except PermissionError:
                    print("Permision err")
            else:
                hash_source = hashlib.md5(open(os.path.join(source_filepath, i), 'rb').read()).hexdigest()
                hash_backup = hashlib.md5(open(os.path.join(backup_filepath, i), 'rb').read()).hexdigest()
                if hash_backup != hash_source:
                    shutil.copy2(i_loc, os.path.join(backup_filepath, i), follow_symlinks=False)
                    print("hashul md5 nu era acelasi, asa ca am facut overwrite la fisier")
                    writing_log.file_updated(os.path.join(source_filepath, i), log_location)



def removing_files(source_filepath: str, backup_filepath: str):
    for i in os.listdir(source_filepath):
        if os.path.isdir(os.path.join(source_filepath, i)):
            if not os.path.exists(os.path.join(backup_filepath, i)):
                try:
                    os.rmdir(path=os.path.join(source_filepath, i))
                    writing_log.deleted(os.path.join(source_filepath, i), log_location)
                    print(f"{os.path.join(source_filepath, i)} was deleted from the source, "
                          f"deleting it from backup also")
                except OSError:
                    shutil.rmtree(path=os.path.join(source_filepath, i))
                    writing_log.deleted(os.path.join(source_filepath, i), log_location)
                    print(f"{os.path.join(source_filepath, i)} was deleted from the source, "
                          f"deleting it from backup also")
            else:
                removing_files(os.path.join(source_filepath, i), os.path.join(backup_filepath, i))

        elif os.path.isfile(os.path.join(source_filepath, i)):
            if not os.path.exists(os.path.join(backup_filepath, i)):
                os.remove(path=os.path.join(source_filepath, i))
                writing_log.deleted(os.path.join(source_filepath, i), log_location)
                print(f"{os.path.join(source_filepath, i)} was deleted from the source, deleting it from backup also")


while True:
    backup_generator(source_location, backup_location)
    removing_files(backup_location, source_location)
    time.sleep(time_sync*60)

#Another implementation using os.walk

# Source and Backup directories
# source_dir = r'PATH'
# backup_dir = r'PATH'
#
# while True:
#     # Recursively traverse the Source directory
#     for dirpath, dirnames, filenames in os.walk(source_dir):
#         # Check if the current directory is in Backup
#
#
#         if dirpath.replace(source_dir, backup_dir) != dirpath:
#             # If not, create it in Backup
#             new_dir = dirpath.replace(source_dir, backup_dir)
#             os.makedirs(new_dir, exist_ok=True)
#             print(f'Created {new_dir}')
#
#         # Copy any new files in the current directory to Backup
#         for filename in filenames:
#             source_file = os.path.join(dirpath, filename)
#             backup_file = os.path.join(dirpath.replace(source_dir, backup_dir), filename)
#             if not os.path.exists(backup_file):
#                 shutil.copy2(source_file, backup_file)
#                 print(f'Copied {source_file} to {backup_file}')
#     time.sleep(30)
