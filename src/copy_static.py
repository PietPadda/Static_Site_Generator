import os  # for file operations
import shutil  # for file utilities


# recursive function
# removes all content from public dir
# copies all content from static dir & subdir) to public dir
# log path of each file to debug
def copy_static(source="static", destination="public"):
    # clean "public" folder
    if os.path.exists(destination):  # if the path exists
        shutil.rmtree(destination)  # remove it and content
    os.mkdir(destination)  # create folder
    print(f"Debug: {destination} folder created")
    static_items = os.listdir(source)  # list of file paths

    # loop each file AND subfolder in "static"
    for item in static_items:
        source_path = os.path.join(source, item)  # static item path
        destination_path = os.path.join(destination, item)  # public item path
        # if a folder (not a file)
        if os.path.isdir(source_path):
            print(f"Debug: {destination_path} is a folder, recurse")
            os.mkdir(destination_path)  # create subfolder in public
            copy_static(source_path, destination_path)  # recurse folder UNTIL we reach files
        # otherwise it's a file
        else:
            print(f"Debug: {destination_path} is a file, copy it")
            shutil.copy(source_path, destination_path)  # copy file to path
