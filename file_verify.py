import os
import fnmatch

def file_in_directory():
    location=(r"/data/PROJECTS/NAPT_Project/rawdata/inventory/")
    for file in os.listdir(location):
        if fnmatch.fnmatch(file, '*AlarmQuery*'):
            file_name="huawei"
        if fnmatch.fnmatch(file, '*ciena_alarms*'):
            file_name="ciena"
    # print(file_name)

    return file_name

def get_file_names_and_remove():
    location="/data/PROJECTS/NAPT_Project/rawdata/inventory/"
    full_list = os.listdir(location)
    str_list=['Query', 'ciena_alarms']
    final_list = [nm for ps in str_list for nm in full_list if ps in nm]
    for file_name in final_list:
        # print(file_name)
        os.remove(location+file_name)

def main():
    file_in_directory()
    get_file_names_and_remove()
   
if __name__ == "__main__":
    main()
