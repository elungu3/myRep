import os
import shutil
from datetime import datetime
import time


def backup_generator():

    """
    This function is generating a backup directory called 'Replica' with exactly match from the source dir.
    There are no parameters, as the location of both dir (the source and replica) has to be given in the CLI.
    The function also generates a log file which contains all the operations done and the time of them.
    Synchronization interval should be given in terminal as an input (and) it is measured in minutes.
    All the operations done are also printed in terminal.
    """

    source_location = input("Enter the absolute path of the file to backup: ")
    backup_location = input("Enter the absolute path to the location where you want the backup: ")
    log_location = input("Enter the absolute path to where you want the log file: ")
    time_sync = int(input("Please specify the time (in minutes) you want to sync the file with the backup file: "))

    while True:
        source_b = os.listdir(source_location)
        l_backup = []
        l_source = []
        deleted_elem = []
        for k in source_b:
            l_source.append(k)
        if "Replica" in os.listdir(backup_location):
            backup_b = os.listdir(f"{backup_location}\Replica")
            for i in backup_b:
                l_backup.append(i)
            for each_file in backup_b:
                if str(each_file) not in l_source:
                    deleted_elem.append(each_file)
                    _ = str(backup_location + r'\Replica' + f"\{each_file}")
                    try:
                        os.remove(path=_)
                        print(f"{each_file} was deleted from the Replica directory "
                                f"because it was no longer in the Source directory")
                    except PermissionError or OSError:
                        shutil.rmtree(path=_)
                        print(f"{each_file} was deleted from the Replica directory "
                              f"because it was no longer in the Source directory")
        shutil.copytree(source_location, f"{backup_location}\Replica", dirs_exist_ok=True)
        for each_file in source_b:
            if each_file in l_backup:
                print(f"{each_file} is already in that directory and it's now updated")
            else:
                print(f"{each_file} was added in the backup directory")

        with open(f'{log_location}\log.txt', 'a') as f:
            f.write(f"The backup directory is at the location: {backup_location} @ " + str(datetime.now()) + "\n")
            for each_file in source_b:
                if each_file in l_backup:
                    f.write(f"{each_file} was updated in the backup directory \n")
                else:
                    f.write(f"{each_file} was added in the backup directory \n")
            for j in deleted_elem:
                f.write(f"Removing {j} from Replica as it was removed from Source directory \n")
            f.write("\n")
            time.sleep(time_sync*60)
