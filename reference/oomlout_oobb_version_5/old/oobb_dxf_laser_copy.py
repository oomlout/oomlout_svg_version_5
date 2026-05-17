import oomB

def dxf_copy_to_laser():
    directory_base = fr"parts"
    directory_laser= fr'C:\GH\oomlout_oobb_version_4\useful_files\oobb_laser'
    oomB.file_copy_search(directory_base,"laser-flat.dxf",output_dir=directory_laser)

def folders_to_folder_dxf():
    input_dir = fr'C:\GH\oomlout_oobb_version_4\things'
    output_dir = fr'C:\GH\oomlout_oobb_version_4\useful_files\oobb_laser'
    filename = "laser_flat.dxf"
    copy_and_rename_file(input_dir, output_dir, filename)
    copy_dir = fr"C:\DB\Dropbox\LALA-Laser Files\oobb_files"
    oomB.file_copy_filter(input_dir=output_dir, output_dir=copy_dir, filter_str="")

def folders_to_folder_stl():
    input_dir = fr'C:\GH\oomlout_oobb_version_4\things'
    output_dir = fr'C:\GH\oomlout_oobb_version_4\useful_files\oobb_3dpr'
    filename = "3dpr.stl"
    copy_and_rename_file(input_dir, output_dir, filename)
    
def folders_to_folder_svg():
    input_dir = fr'C:\GH\oomlout_oobb_version_4\things'
    output_dir = fr'C:\GH\oomlout_oobb_version_4\useful_files\oobb_svg'
    filename = "laser-flat.svg"
    copy_and_rename_file(input_dir, output_dir, filename)

def folders_to_folder_png():
    input_dir = fr'C:\GH\oomlout_oobb_version_4\things'
    output_dir = fr'C:\GH\oomlout_oobb_version_4\useful_files\oobb_png'
    filename = "3dpr.png"
    copy_and_rename_file(input_dir, output_dir, filename)



import os
import shutil
def copy_and_rename_file(input_dir, output_dir, filename):
    for folder_name in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder_name)
        if os.path.isdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                output_file_name = folder_name + os.path.splitext(filename)[1]
                output_file_path = os.path.join(output_dir, output_file_name)
                #check for directory if not there make it
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                try:    
                    shutil.copy(file_path, output_file_path)
                except:
                    print("Error copying file: " + file_path)

def folders_to_folder_all():
    folders_to_folder_dxf()
    folders_to_folder_stl()
    folders_to_folder_svg()    
    folders_to_folder_png()

if __name__ == "__main__":
    #dxf_copy_to_laser()
    folders_to_folder_all()

