import os
from fnmatch import fnmatch
from shutil import copyfile


# senate_dir = os.path.join(os.environ["HOME"], "Desktop", "congress-master", "data", "115", "bills", "s")
# house_dir = os.path.join(os.environ["HOME"], "Desktop", "congress-master", "data", "115", "bills", "s")

# senate_files = []

# pattern = "data.json"
# dirs = next(os.walk(senate_dir))[1]
# for d in dirs:
#   data_file = os.path.join(senate_dir, d, pattern)
#   senate_files.append()
#   # for name in files:
#   #   if fnmatch(name, pattern):
#   #     print(os.path.join(path, name))

def getDataFiles(chamber, session, target_folder_name):
  directory = os.path.join(os.environ["HOME"], "Desktop", "congress-master", "data", f"{session}", "bills", f"{chamber}")
  pattern = "data.json"
  child_dirs = next(os.walk(directory))[1]
  filenames = []
  for d in child_dirs:
    try:
      data_file = os.path.join(directory, d, pattern)
      print(f"Copying file {d}_{pattern}")
      copyfile(data_file, f"./{target_folder_name}/{d}_{pattern}")
    except:
      print(f'{d} has no {pattern} file.. skipping {d}')

  return filenames
  
getDataFiles('s', 113, '113_data')
getDataFiles('hr', 113, '113_data')