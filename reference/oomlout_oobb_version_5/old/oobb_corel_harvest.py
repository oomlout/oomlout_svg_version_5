import oobb

import os
import shutil

def main():
    folder_things = "parts"

    filter =""
    overwrite = False

    make_svgs()

    #go through each folder in things   
    for folder in os.listdir(folder_things):
        if filter in folder:
            #if there's a file called laser.cdr
            if os.path.isfile(os.path.join(folder_things, folder, "outline.cdr")):
                #check if all expected svg files outline_neg outline_pos and indent are there
                file_check_arra
                y = ["outline_neg.svg", "outline_pos.svg", "indent.svg"]
                for file_check in file_check_array:
                    if not os.path.isfile(os.path.join(folder_things, folder, file_check)):
                        print(f"    missing {file_check}")
                        #exit()
                        
                

                #copy scad/decoration.scad to folder and rename to 3dpr.scad USING SHUTIL
                
                filename_scad = os.path.join(folder_things, folder, "3dpr.scad")
                #decide the file if indent_pos.svg
                shutil.copyfile("scad/decoration.scad", filename_scad)
                
                #test to see if filename with an stl ending exists 
                filename_stl = os.path.join(folder_things, folder, "3dpr.stl")
                if not os.path.isfile(filename_stl) or overwrite:
                    oobb.saveToAll(filename_scad)
                    pass
                else:
                    print(f"    skipping {filename_stl}")   

    
def make_svgs():
    #go through all folders in things
    folder_things = "parts"
    for folder in os.listdir(folder_things):
        files = ["outline_neg","outline_pos","indent",]
        for file in files:
            formats  =["svg"]
            for format in formats:
                #if the file .cdr exists
                if os.path.isfile(os.path.join(folder_things, folder, file + ".cdr")):
                    pass
                    #check if the format of that file exists if not create it by calling make_corel with the file and the format
                    if not os.path.isfile(os.path.join(folder_things, folder, file + "." + format)):
                        make_corel(file, format, folder)
            
import time

import subprocess

def make_corel(file, format, folder):
    #open file and export as format
    folder_things = "parts"
    print(f"    making {folder}/{file}.{format}")
    corel_app = r'CorelDRW.exe'
    #open file with corel draw 
    
    file_open = os.path.join(folder_things, folder, file + '.cdr')
    #add th working folder line to file_open
    file_open = os.path.join(os.getcwd(), file_open)
    system_call_line = rf'{corel_app} "{file_open}"'
    #os.system(system_call_line)
    #subprocess.Popen([corel_app, file_open])
    os.startfile(file_open)
    #wait 5 seconds until file is open
    time.sleep(15)
    #export file as format
    #mouse click at 150, 150 using pyautogui
    import pyautogui
    pyautogui.moveTo(150, 150)
    pyautogui.click()
    #maximize window on windows 10
        

    
    #sleep 5 seconds
    time.sleep(5)
    #send keyboard ctrl e then wait 5 seconds using pyautogui
    pyautogui.hotkey('ctrl', 'e')
    
    time.sleep(5)
    #send directory then press enter using pyauto gui
    pyautogui.typewrite(os.path.join(os.getcwd(), folder_things, folder, file + "." + format))
    #sleep 1
    time.sleep(1)
    #press enter
    pyautogui.press('enter')
    #sleep 10
    time.sleep(10)
    #press enter again
    pyautogui.press('enter')
    #wait 3 seconds
    time.sleep(3)
    #press y to overwrite   
    pyautogui.press('y')
    #wait 10 seconds
    time.sleep(10)
    #clsoe current file
    #send alt f
    pyautogui.hotkey('alt', 'f')
    #send c
    pyautogui.press('c')
    time.sleep(10)
    




    

if __name__ == "__main__":
    main()