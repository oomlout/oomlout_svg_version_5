import glob
import os
import shutil

def main(**kwargs):
    #get a list of directories in things folder
    things_dir = "parts"
    things_list = glob.glob(things_dir + "/*/")
    for thing in things_list:
        #get just the top directory name
        thing = thing.replace(things_dir, "")
        directory_oomp_base = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
        
        thing_sanitized = thing.replace("\\", "/")
        #remove trailing slash if there
        if thing_sanitized[-1] == "/":
            thing_sanitized = thing_sanitized[:-1]
        thing_sanitized = thing_sanitized.replace("/", "")
        thing_sanitized = thing_sanitized.replace("oobb_", "")

        directory_oomp_thing = f"{directory_oomp_base}/oobb_part_{thing_sanitized}"
        directory_thing = f"{things_dir}{thing}"
        directory_oomp_thing_working_yaml = f"{directory_oomp_thing}/working.yaml"
        if os.path.exists(directory_oomp_thing_working_yaml):
            print(f"copy {directory_oomp_thing_working_yaml} to {directory_thing}")
            shutil.copy(directory_oomp_thing_working_yaml, directory_thing)
            pass
        pass





if __name__ == "__main__":
    kwargs = {}
    main(**kwargs)