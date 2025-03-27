import os

temp = ".\Temp"
folder = ".\Plates"

if not os.path.exists(folder):
    os.makedirs(folder)

# Delete files smaller than 10 KB
def delete_small():
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:            
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)/1024
                if size < 10:
                    os.remove(file_path)
                    count += 1
        except Exception as e:
            print(f"Error deleting the file: {str(e)}")

    print(f"Deleted {count} files")

def get_int(name):
    return int(name.split(".")[0])

def get_last():
    last = 0
    files = sorted(os.listdir(folder), key=get_int)
    if files:
        file = files[-1]
        last = get_int(file)
    return last

sort_temp = sorted(os.listdir(temp), key=get_int) 
sort_folder = sorted(os.listdir(folder), key=get_int)
last = get_last()

def rename_temp_files():
    #variables 
    count = 0
    #Sort the files in the temp folder
    if os.path.exists(folder):
        for i, file in enumerate(sort_temp):
            num = get_int(file)
            if(i + 1 == num):
                continue
            else:
                file_path = os.path.join(temp, file)
                try:
                    if os.path.isfile(file_path):
                        new_file_path = os.path.join(temp, f"{i + 1}.jpg")
                        os.rename(file_path, new_file_path)
                        count += 1
                except Exception as e:
                    print(f"Error renaming the file: {str(e)}")
    print(f"Renamed {count} files in the temp folder")

def move_files():
    count = 0 
    for file in sort_temp:
        for i in range(1,len(sort_temp)+1):
            print(i)
            if file == f"{i}.jpg":
                file_path = os.path.join(temp, file)
                new_file_path = os.path.join(folder, f"{i + last}.jpg")
                os.rename(file_path, new_file_path)
                count += 1

    folder_name = folder.split(".\\")[1]
    print(f"Moved {count} files to the {folder_name} folder")

def main():
    rename_temp_files()
    move_files()

if __name__ == "__main__":
    main()