import os

def checkAndCreateFolder(source):

    # Check whether the specified path exists or not
    isExist = os.path.exists(source)

    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(source)
        print(f"The {source} directory is created!")
