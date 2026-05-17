import pyautogui
import clipboard
import random
import time
import os
import sys
import io
import jinja2
import pickle
import copy

# Import platform-specific key detection modules
if sys.platform == "win32":
    import msvcrt
else:
    # For Linux/Mac, we'll use a simpler approach
    import select
    import tty
    import termios


def robo_chatgpt_prompt_type(**kwargs):
    position = kwargs.get('position', [0, 0])
    robo_mouse_click(position=position)

    prompt = kwargs.get('prompt', '')
    print(f"Typing the prompt:")
    pyautogui.typewrite(prompt, interval=0.025)
    time.sleep(1)
    #press enter to send the prompt
    print("Pressing enter...")
    pyautogui.press('enter')
    robo_delay(delay=40)

def robo_chrome_close_tab(**kwargs):
    delay = kwargs.get('delay', 1)
    #close the tab
    print("closing tab")
    pyautogui.hotkey('ctrl', 'w')
    robo_delay(delay=delay)

def robo_chrome_open_url(**kwargs):
    url = kwargs.get('url', '')
    delay = kwargs.get('delay', 10)
    message = kwargs.get('message', f"Opening the url: {url}...")
    #open the url in chrome
    print(message)
    os.system(f"start chrome {url}")
    robo_delay(delay=delay)

def robo_chrome_save_url(**kwargs):
    url = kwargs.get('url', '')
    url_directory = kwargs.get('url_directory', '')
    directory = kwargs.get('directory', "")
    save_modes = kwargs.get('save_modes', ["txt","singlefile", "save_dialog", "raw"])
    
    
    file_name_singlefile = "singlefile.mhtml"
    file_name_save_dialog = "save_dialog.html"
    file_name_raw = "raw.html"
    file_name_txt = "page.txt"
    
    url_path = os.path.join(directory, url_directory)
    if not os.path.exists(url_path):
        os.makedirs(url_path)
    delay = kwargs.get('delay', 5)
    
    #open url
    robo_chrome_open_url(url=url, delay=15)
    
    message = kwargs.get('message', f"Saving the url: {url} to file: {url_path}...")
    print(message)
    if "raw" in save_modes:
    
        file_path = os.path.join(url_path, file_name_raw)
        #press ctrl u wait ctrl a, ctrl c, save clipboard to file
        robo_keyboard_press_ctrl_generic(string='u', delay=5)
        robo_delay(delay=5)
        robo_keyboard_select_all(delay=2)
        robo_keyboard_press_ctrl_generic(string='c', delay=2)
        content = clipboard.paste()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        #close tab
        robo_chrome_close_tab(delay=2)
    if "singlefile" in save_modes:
        coordinate_single_file = [1608, 76]
        file_path = os.path.join(url_path, file_name_singlefile)
        
        # Get the downloads directory
        import shutil
        downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        
        # Get initial list of files in downloads directory
        initial_files = set(os.listdir(downloads_dir))
        print(f"Initial files in downloads: {len(initial_files)}")
        
        # Click the SingleFile button
        print(f"Clicking SingleFile button at {coordinate_single_file}")
        robo_mouse_click(position=coordinate_single_file, delay=2)
        
        # Wait 15 seconds for download to start
        print("Waiting 15 seconds for download...")
        robo_delay(delay=15)
        
        # Check for new files
        current_files = set(os.listdir(downloads_dir))
        new_files = current_files - initial_files
        
        if not new_files:
            print("No new file found after 15 seconds, waiting another 30 seconds...")
            robo_delay(delay=30)
            current_files = set(os.listdir(downloads_dir))
            new_files = current_files - initial_files
        
        if not new_files:
            print("ERROR: No new file appeared in downloads directory after 45 seconds")
        else:
            # Get the newest file (in case multiple files appeared)
            new_file_name = max(new_files, key=lambda f: os.path.getctime(os.path.join(downloads_dir, f)))
            source_file = os.path.join(downloads_dir, new_file_name)
            
            print(f"Found new file: {new_file_name}")
            print(f"Moving from {source_file} to {file_path}")
            
            # Move the file to destination
            shutil.move(source_file, file_path)
            print(f"Successfully moved file to {file_path}")
    if "save_dialog" in save_modes:
        #press ctrl s wait type absolute path, press enter
        file_path = os.path.join(url_path, file_name_save_dialog)
        file_path_absolute = os.path.abspath(file_path)
        robo_keyboard_press_ctrl_generic(string='s', delay=5)
        robo_delay(delay=10)
        robo_keyboard_send(string=file_path_absolute, delay=2)
        robo_keyboard_press_enter(delay=20)
    if "txt" in save_modes:
        #mouse click 300,300
        robo_mouse_click(position=[300, 300], delay=2)
        #ctrl a ctrl c then save to text file
        file_path = os.path.join(url_path, file_name_txt)
        robo_keyboard_select_all(delay=2)
        robo_keyboard_press_ctrl_generic(string='c', delay=2)
        content = clipboard.paste()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    #close tab
    robo_chrome_close_tab(delay=2)
        
                                  
    #save the url to a text file
    
    
    robo_delay(delay=delay)

#corel things

def robo_corel_add_text(**kwargs):
    text = kwargs.get('text', 'Sample Text')
    font = kwargs.get('font', '')
    font_size = kwargs.get('font_size', '24')
    font_alignment = kwargs.get('font_alignment', 'center') # left, center, right
    x = kwargs.get('x', 100)
    y = kwargs.get('y', 100)
    delay = kwargs.get('delay', 5)
    message = kwargs.get('message', f"Adding text: {text} at position {x}, {y} with font {font} and size {font_size}...")
    #add text to corel
    print(message)
    #type text
    if True:
        #press f8 to select the text tool
        robo_keyboard_press_generic(string='f8', delay=2)
        #click at position x, y
        robo_mouse_click(position=[300, 300], delay=2)
        #type the text
        pyautogui.typewrite(str(text), interval=0.25)
        time.sleep(1)
        #press alt f
        #click pointer 16,145
        robo_mouse_click(position=[16, 145], delay=2)
        
    #set font
    if True:
        
        #press ctrl enter
        robo_keyboard_press_ctrl_enter(delay=2)
        #press tab 9 times
        robo_keyboard_press_tab(delay=0.5, repeat=9)
        if font != "":
            print(f"Setting font... {font}")
            #mouse click 510 110
            robo_mouse_click(position=[510, 105], delay=1)
            #type the font
            robo_delay(delay=1)
            if font != "":
                pyautogui.typewrite(font, interval=0.1)
            robo_delay(delay=2)         
            
        #press tab once
        robo_keyboard_press_tab(delay=0.5)
        if font_size != "":
            #type the font size
            pyautogui.typewrite(str(font_size), interval=0.025)
            time.sleep(5)
            #press enter
            robo_keyboard_press_enter(delay=2)
            #press down
            robo_keyboard_press_down(delay=1)
            #press up
            robo_keyboard_press_up(delay=1)
        if font_alignment != "":
            pass
    #set position
    if True:
        robo_corel_set_position(x=x, y=y, delay=2)
        
    robo_delay(delay=delay)

def robo_corel_add_text_box(**kwargs):
    text = kwargs.get('text', 'Sample Text')
    font = kwargs.get('font', '')
    font_size = kwargs.get('font_size', '24')
    font_alignment = kwargs.get('font_alignment', 'center') # left, center, right
    x = kwargs.get('x', 100)
    y = kwargs.get('y', 100)
    width = kwargs.get('width', 200)
    height = kwargs.get('height', 100)
    delay = kwargs.get('delay', 5)
    message = kwargs.get('message', f"Adding text: {text} at position {x}, {y} with font {font} and size {font_size}...")
    #add text to corel
    print(message)
    #type text
    if True:        
        #press f8 to select the text tool
        robo_keyboard_press_generic(string='f8', delay=2)
        #click at position x, y
        robo_mouse_drag(position=[300, 300], move=[200, 200], delay=2)
        #type the tex
        #remove double new lines
        text = text.replace("\\n\\n", "\\n")
        #split for \n
        text_lines = text.split("\\n")
        count = 0
        for text in text_lines:            
            if "<b>" in text:
                text_blocks = text.split("<b>")
                for i in text_blocks:
                    pyautogui.typewrite(i, interval=0.05)
                    robo_delay(delay=0.5)
                    #send ctrl b
                    robo_keyboard_press_ctrl_generic(string='b', delay=0.5)
            else:
                pyautogui.typewrite(text, interval=0.05)
                time.sleep(0.5)
            if len(text_lines) > 1 and count < len(text_lines) - 1:
                robo_keyboard_press_enter(delay=0.25)
            count += 1
        #press alt f
        #click pointer 16,145
        robo_mouse_click(position=[20, 145], delay=2)
        #set position
    #set font
    if True:
        #press ctrl enter
        robo_keyboard_press_ctrl_enter(delay=2)
        #press tab 9 times
        robo_keyboard_press_tab(delay=0.5, repeat=9)
        if font != "":
            print(f"Setting font... {font}")
            #mouse click 510 110
            robo_mouse_click(position=[510, 105], delay=1)
            #type the font
            robo_delay(delay=1)
            if font != "":
                pyautogui.typewrite(font, interval=0.1)
            robo_delay(delay=2)  
        #press tab once
        robo_keyboard_press_tab(delay=0.5)
        if font_size != "":
            #type the font size
            pyautogui.typewrite(str(font_size), interval=0.025)
            time.sleep(5)
            #press enter
            robo_keyboard_press_enter(delay=2)
        if font_alignment != "":
            pass
    #set size
    if True:
        robo_corel_set_size(width=width, height=height, delay=2)
        #press enter
        robo_keyboard_press_enter(delay=2)
    #set position    
    if True:
        robo_corel_set_position(x=x, y=y, delay=2)
    
    robo_delay(delay=delay)

def robo_corel_copy(**kwargs):
    delay = kwargs.get('delay', 1)
    copy_mode = kwargs.get('copy_mode', 'all')
    select_all = kwargs.get('select_all', False)
    if copy_mode == 'all':
        select_all = True
    message = kwargs.get('message', f"Copying the selected items in Corel...")
    #copy the selected items in corel
    print(message)
    #press ctrl a
    if select_all:        
        robo_corel_select_all(delay=2)
    #press ctrl c
    robo_keyboard_press_ctrl_generic(string='c', delay=delay)
    robo_delay(delay=delay)

def robo_corel_close_file(**kwargs):
    delay = kwargs.get('delay', 5)
    save_style = kwargs.get('save_style', "y")
    message = kwargs.get('message', f"Closing Corel...")
    #close corel
    print(message)
    #press alt_f
    robo_keyboard_press_alt_f(delay=5)
    #press c
    robo_keyboard_press_generic(string='c', delay=5)
    #if save_style is y then save the file    
    robo_keyboard_send(string=save_style, delay=2)
    #wait for the delay
    robo_delay(delay=delay)

def robo_corel_convert_to_curves(**kwargs):
    delay = kwargs.get('delay', 5)
    delay_keypress = kwargs.get('delay_keypress', 0.5)
    group = kwargs.get('group', True)
    ungroup = kwargs.get('ungroup', False)
    repeats = kwargs.get('repeats', 50)
    message = kwargs.get('message', f"Converting selected items to curves in Corel...")
    #convert selected items to curves in corel
    print(message)
    if ungroup:
        robo_corel_ungroup(select_all = True, delay=2)
    #press ctrl q
    for _ in range(repeats):
        robo_keyboard_press_ctrl_generic(string='q', delay=delay_keypress)
        #press tab
        robo_keyboard_press_tab(delay=delay_keypress)
    #mouse click 300,300
    if True:
        robo_mouse_click(position=[300, 300], delay=2)
    

    if group:
        robo_corel_group(select_all = True, delay=2)
    robo_delay(delay=delay)
    

def robo_corel_export_file(**kwargs):
    file_name = kwargs.get('file_name', '')
    file_type = kwargs.get('file_type', 'pdf')
    directory = kwargs.get('directory', '')
    if directory != '':
        file_name = os.path.join(directory, file_name)
    file_name_absolute = os.path.abspath(file_name)
    delay = kwargs.get('delay', 10)
    message = kwargs.get('message', f"Exporting the file: {file_name} as {file_type}...")
    print(message)
    #export the file in corel    
    if False:
        robo_keyboard_press_alt_f(delay=1)
        #send h twice
        robo_keyboard_press_generic(string='h', repeat=2, delay=1)
        #send enter
        robo_keyboard_press_enter(delay=1)
        #send filename absolute
        robo_keyboard_send(string=file_name_absolute, delay=2)
        #press enter to confirm
        robo_keyboard_press_enter(delay=2)
        #send y to overwrite
        robo_keyboard_send(string='y', delay=2)
        robo_delay(delay=delay)
    else:
        #select all
        robo_keyboard_select_all(delay=2)
        #send alt f
        robo_keyboard_press_alt_f(delay=3)
        #send e 
        robo_keyboard_press_generic(string='e', delay=20)
        # #send right
        # robo_keyboard_press_right(delay=2)
        # #send left
        # robo_keyboard_press_left(delay=2)
        #send tab
        #robo_keyboard_press_tab(delay=5, repeat=1)
        #mouse click because tab doesn't always work
        robo_mouse_click(position=[200, 429], delay=3)
        robo_mouse_click(position=[200, 429], delay=3)
        #send file type
        robo_keyboard_send(string=file_type, delay=5)
        #send enter
        robo_keyboard_press_enter(delay=5)      
        
        #sent shift tab once
        robo_keyboard_press_tab_shift(delay=5, repeat=1)
        #send file name absolute
        #send filename absolute
        robo_keyboard_send(string=file_name_absolute, delay=5)
        

        #press enter to confirm
        robo_keyboard_press_enter(delay=2)
        #send y to overwrite
        robo_keyboard_send(string='y', delay=20)
        #press enter to confirm
        robo_keyboard_press_enter(delay=20)
        
        robo_delay(delay=10)

def robo_corel_object_order(**kwargs):
    order = kwargs.get('order', 'to_front')    
    message = kwargs.get('message', f"Changing object order to: {order}")
    delay = kwargs.get('delay', 2)
    print(message)
    # Send the appropriate keyboard shortcuts to change the object order
    if order == 'to_front' or order == 'front':
        #press shift down
        pyautogui.keyDown('ctrl')
        time.sleep(0.1)
        pyautogui.hotkey('home')
        time.sleep(0.1)
        pyautogui.keyUp('ctrl')
    elif order == 'to_back' or order == 'back':
        pyautogui.keyDown('ctrl')
        time.sleep(0.1)
        pyautogui.hotkey('end')
        time.sleep(0.1)
        pyautogui.keyUp('ctrl')
    robo_delay(delay=delay)

def robo_corel_open(**kwargs):
    file_name = kwargs.get('file_name', '')
    #if file_name = try file_source
    if file_name == '':

        file_name = kwargs.get('file_source', '')
    directory = kwargs.get('directory', '')
    if directory != '':
        file_name = os.path.join(directory, file_name)
    delay = kwargs.get('delay', 45)
    message = kwargs.get('message', f"Opening the file: {file_name}...")
    #open the file in corel
    print(message)
    #os.system(f"start CorelDRW {file_name}")
    #os.system(f'start {file_name}')
    os.system(f'start "" "{file_name}"')
    robo_delay(delay=delay)

def robo_corel_group(**kwargs):
    delay = kwargs.get('delay', 2)
    select_all = kwargs.get('select_all', True)
    message = kwargs.get('message', f"Grouping the selected items in Corel...")
    #group the selected items in corel
    if select_all:
        robo_corel_select_all(delay=2)
    print(message)
    #press ctrl g
    robo_keyboard_press_ctrl_generic(string='g', delay=delay)
    robo_delay(delay=delay)

def robo_corel_import_file(**kwargs):
    file_name = kwargs.get('file_name', '')
    directory = kwargs.get('directory', '')
    x = kwargs.get('x', "")
    y = kwargs.get('y', "")
    angle = kwargs.get('angle', "")
    width = kwargs.get('width', "")
    height = kwargs.get('height', "")
    max_dimension = kwargs.get('max_dimension', "")
    special = kwargs.get('special', "")
    if directory != '':
        file_name = os.path.join(directory, file_name)
    file_name_absolute = os.path.abspath(file_name)
    #check if file exists
    if not os.path.exists(file_name_absolute):
        print(f"    Error: file {file_name_absolute} does not exist")
        robo_delay(delay=2)
        return
    delay = kwargs.get('delay', 10)
    message = kwargs.get('message', f"Importing the file: {file_name} at position {x}, {y} with size {width}x{height} and max dimension {max_dimension}...")
    print(message)
    #import the file in corel
    #press ctrl i
    robo_keyboard_press_ctrl_i(delay=10)
    if True:
        #send file name absolute
        robo_keyboard_send(string=file_name_absolute, delay=2)
        #press enter to confirm
        robo_keyboard_press_enter(delay=5)
    #click in window
    robo_mouse_click(position=[300, 300], delay=5)
    if special == "":
        
        robo_mouse_click(position=[300, 300], delay=5)
    #if x, y, width, height are all skipped then just return
    if angle != "":
        robo_corel_set_rotation(**kwargs)
    if x == "" and y == "" and width == "" and height == "" and max_dimension == "":

        return
    else:
        if x != "" or y != "":
            robo_corel_set_position(**kwargs)
        if width != "" or height != "" or max_dimension != "":
            robo_corel_set_size(**kwargs)
    

def robo_corel_paste(**kwargs):
    delay = kwargs.get('delay', 1)
    message = kwargs.get('message', f"Pasting the copied items in Corel...")
    x = kwargs.get('x', "")
    y = kwargs.get('y', "")
    width = kwargs.get('width', "")
    height = kwargs.get('height', "")
    max_dimension = kwargs.get('max_dimension', "")
    #paste the copied items in corel
    print(message)
    #press ctrl v
    robo_keyboard_press_ctrl_generic(string='v', delay=2)
    #if x, y, width, height are all skipped then just return
    if x != "" or y != "":
        robo_corel_set_position(x=x, y=y)
    if width != "" or height != "" or max_dimension != "":
        robo_corel_set_size(width=width, height=height, max_dimension=max_dimension, delay=2)
    robo_delay(delay=delay)

def robo_corel_save(**kwargs):
    message = kwargs.get('message', f"Saving the file")
    #save the file in corel
    print(message)
    #press ctrl s
    robo_keyboard_press_ctrl_generic(string='s', delay=10)


def robo_corel_save_as(**kwargs):
    
    filename = kwargs.get('file_name', '')
    directory = kwargs.get('directory', '')

    if directory != '':
        filename = os.path.join(directory, filename)
    filename_absolute = os.path.abspath(filename)
    message = kwargs.get('message', f"Saving the file {filename_absolute}")
    #save the file in corel
    print(message)
    #move back and forth to enable the save so it's always six
    #select all
    if True:
        robo_keyboard_select_all(delay=1)
        #send left
        robo_keyboard_press_left(delay=1)
        #send right
        robo_keyboard_press_right(delay=1)

    #press alt f
    robo_keyboard_press_alt_f(delay=1)
    #press down 6 times
    robo_keyboard_press_down(delay=0.5, repeat=6)
    #press enter
    robo_keyboard_press_enter(delay=5)
    #send the file name
    robo_keyboard_send(string=filename_absolute, delay=5)
    #press enter to confirm
    robo_keyboard_press_enter(delay=5)
    #y to overwrite
    robo_keyboard_send(string='y', delay=5)
    #wait 20 seconds
    robo_delay(delay=20)

def robo_corel_select_all(**kwargs):
    delay = kwargs.get('delay', 1)
    message = kwargs.get('message', f"Selecting all items in Corel...")
    #select all items in corel
    print(message)
    #click on pointer first
    robo_mouse_click(position=[24, 147], delay=1)
    #click 200,200
    robo_mouse_click(position=[200, 200], delay=1)
    #press ctrl a
    robo_keyboard_select_all(delay=delay)
    robo_delay(delay=delay)

def robo_corel_trace(**kwargs):
    return robo_corel_trace_clipart(**kwargs)
    #return robo_corel_trace_lineart(**kwargs)

def robo_corel_trace_clipart(**kwargs):
    message = kwargs.get('message', f"tracing lineart")
    number_of_colors = kwargs.get('number_of_colors', None)
    remove_background_color_from_entire_image = kwargs.get('remove_background_color_from_entire_image', False)
    
    delay_trace = kwargs.get('delay_trace', 30)
    detail_minus = kwargs.get('detail_minus', 5)
    smoothing = kwargs.get('smoothing', 25)
    corner_smoothness = kwargs.get('corner_smoothness', 0)
    #trace the clipart in corel
    print(message)
    #open trace menu
    if True:
        #press alt b
        robo_keyboard_press_alt_generic(string='b', delay=1)
        #trace    
        #press o
        robo_keyboard_send(string='o', delay=1)        
        #press right
        robo_keyboard_press_right(delay=1)
        #press down 0 times
        robo_keyboard_press_down(delay=0.5, repeat=3)
        #press enter
        robo_keyboard_press_enter(delay=10)
        #909,568
        #click to reduce bitmap
        if True:
            robo_keyboard_press_enter(delay=delay_trace)
            #robo_mouse_click(position=[909, 568], delay=30)
            #robo_mouse_click(position=[1030, 1950], delay=30)
            #all settings inherited    
    if remove_background_color_from_entire_image:
        #press tab 10 times
        robo_keyboard_press_tab(delay=0.5, repeat=10)
        #press space
        robo_keyboard_press_space(delay=1)
        #shift tab 6
        robo_keyboard_press_tab_shift(delay=0.5, repeat=10)
    #select max detail
    if True:
        #press tab 3 times
        robo_keyboard_press_tab(delay=0.5, repeat=3)
        #smoothing
        if smoothing != 25:
            #press tab once
            robo_keyboard_press_tab(delay=0.5)
            #press delete 3 times
            robo_keyboard_press_delete(delay=0.5, repeat=3)
            #delay 2
            robo_delay(delay=2)
            #send smoothing
            smoothing_str = str(smoothing)
            robo_keyboard_send(string=smoothing_str, delay=5)
            #delay delay
            robo_delay(delay=delay_trace)            
            #send shift tab once
            robo_keyboard_press_tab_shift(delay=0.5, repeat=1)
        #corner smoothness
        if corner_smoothness != 0:
            #press tab twice
            robo_keyboard_press_tab(delay=0.5, repeat=2)
            #press delete 3 times
            robo_keyboard_press_delete(delay=0.5, repeat=3)
            #send corner_smoothness
            robo_keyboard_send(string=str(corner_smoothness), delay=1)
            #delay delay
            robo_delay(delay=delay_trace)
            #send shift tab twice
            robo_keyboard_press_tab_shift(delay=0.5, repeat=2)
            
        #detail
        if True:
            #press up 20 times

            robo_keyboard_press_up(delay=0.15, repeat=20)
            #robo_mouse_click(position=[1359, 383], delay=30)        
            if detail_minus > 0:
                robo_delay(delay=delay_trace)
                #press down detail_minus times
                robo_keyboard_press_down(delay=0.15, repeat=detail_minus)
        #press shift tab 3 times
        robo_keyboard_press_tab_shift(delay=2, repeat=3)
        #wait 30 seconds
        robo_delay(delay=delay_trace)
    #set colors

    if number_of_colors is not None:
        #shift tab 11
        robo_keyboard_press_tab_shift(delay=0.5, repeat=11)
        #press right
        robo_keyboard_press_right(delay=0.5, repeat=1)
        #shift tab 9 times
        robo_keyboard_press_tab_shift(delay=0.25, repeat=9)
        #press number_of_colors
        robo_keyboard_send(string=str(number_of_colors), delay=1)
        robo_keyboard_press_tab(delay=0.25, repeat=1)
        #test to see if too few
        if True:
            #copy
            print("Testing to see if number of colors is too few...")
            test = robo_keyboard_copy(delay=2)
            if "value must be" in test.lower():
                print(f"   Number of colors {number_of_colors} is too few, increasing to 256")
                #send enter
                robo_keyboard_press_enter(delay=2)                
        robo_delay(delay=delay_trace)
        #tab 10 times
        robo_keyboard_press_tab(delay=0.25, repeat=9)
        #delay 5 seconds
        robo_delay(delay=delay_trace)
    robo_keyboard_press_enter(delay=5)
    robo_keyboard_press_enter(delay=delay_trace)

def robo_corel_trace_lineart(**kwargs):
    message = kwargs.get('message', f"tracing lineart")
    #trace the clipart in corel
    print(message)
    #press alt b
    robo_keyboard_press_alt_generic(string='b', delay=1)
    #press o
    robo_keyboard_send(string='o', delay=1)
    #press right
    robo_keyboard_press_right(delay=1)
    #press down 0 times
    #robo_keyboard_press_down(delay=0.5, repeat=3)
    #press enter
    robo_keyboard_press_enter(delay=30)
    #909,568
    #click to reduce bitmap
    robo_mouse_click(position=[909, 568], delay=30)
    #all settings inherited    
    if False:
        #press tab 10 times
        robo_keyboard_press_tab(delay=0.5, repeat=10)
        #press space
        robo_keyboard_press_space(delay=1)
        #shift tab 6
        robo_keyboard_press_tab_shift(delay=0.5, repeat=6)
        #send ctrl select all
        robo_keyboard_press_ctrl_generic(string='a', delay=1)
        #send 10
        robo_keyboard_send(string='0', delay=20)
        #press shift tab 4 times
        robo_keyboard_press_tab_shift(delay=0.5, repeat=4)
        #press enter
    #click to set detail all but one 1337,366
    robo_mouse_click(position=[1337, 366], delay=10)
    robo_keyboard_press_enter(delay=30)

def robo_corel_ungroup(**kwargs):
    delay = kwargs.get('delay', 2)
    repeats = kwargs.get('repeats', 50)
    message = kwargs.get('message', f"Ungrouping the selected items in Corel...")
    
    #press ctrl u
    for _ in range(repeats):        
        robo_keyboard_press_ctrl_generic(string='u', delay=1)
        #press tab
        robo_keyboard_press_tab(delay=0.25)
        print(".", end='', flush=True)
    print("")
    robo_delay(delay=delay)

def robo_corel_page_goto(**kwargs):
    page_number = kwargs.get('page_number', 1)
    delay = kwargs.get('delay', 5)
    message = kwargs.get('message', f"Going to page number: {page_number} in Corel...")
    print(message)
    #mouse click at 132 965
    robo_mouse_click(position=[132, 965], delay=2)
    #send page number
    robo_keyboard_send(string=str(page_number), delay=2)
    #press enter
    robo_keyboard_press_enter(delay=2)
    robo_delay(delay=delay)

def robo_corel_set_position(**kwargs):
    x = kwargs.get('x', "")
    y = kwargs.get('y', "")
    
    if x != "" and y != "":
        print(f"Setting the position to {x}, {y}")
        #send ctrl {enter}
        robo_keyboard_press_ctrl_enter(delay=1)
        #send tab
        robo_keyboard_press_tab(delay=0.5)
        robo_keyboard_send(string=str(x))
        robo_keyboard_press_tab(delay=0.5)
        robo_keyboard_send(string=str(y))
        #press enter
        robo_keyboard_press_enter(delay=0.5)

#set angle
def robo_corel_set_rotation(**kwargs):
    angle = kwargs.get('angle', "")
    if angle != "":
        print(f"Setting the rotation to {angle} degrees")
        #send ctrl {enter}
        robo_keyboard_press_ctrl_enter(delay=1)
        #send tab 5 times
        robo_keyboard_press_tab(delay=0.5, repeat=8)
        #send angle
        robo_keyboard_send(string=str(angle), delay=1)
        #press enter
        robo_keyboard_press_enter(delay=0.5)

def robo_corel_set_size(**kwargs):
    width = kwargs.get('width', "")
    height = kwargs.get('height', "")
    max_dimension = kwargs.get('max_dimension', "")
    delay = kwargs.get('delay', 2)
    select_all = kwargs.get('select_all', False)

    if select_all:
        robo_corel_select_all(delay=2)
    if width != "" and height != "":
        #set the size of the object        
        print(f"Setting the size to {width}x{height}")
        
        robo_keyboard_press_ctrl_enter(delay=1)
        #send tab 3 times
        robo_keyboard_press_tab(delay=0.5, repeat=3)
        #send width
        pyautogui.typewrite(f"{width}", interval=0.025)
        robo_keyboard_press_tab(delay=0.5)
        #send height
        pyautogui.typewrite(f"{height}", interval=0.025)
        robo_keyboard_press_enter(delay=0.5)
    elif width != "" or height != "":        
        #turn on the lock aspect ratio
        if True:            
            robo_keyboard_press_ctrl_enter(delay=1)
            #send tab 7 times
            robo_keyboard_press_tab(delay=0.5, repeat=7)
            # send space
            robo_keyboard_press_space(delay=0.5)
        robo_keyboard_press_ctrl_enter(delay=1)
        num_tabs = 3
        dimen = width
        if height != "":
            num_tabs = 4
            dimen = height
        robo_keyboard_press_tab(delay=0.5, repeat=num_tabs)
        #send dimension
        pyautogui.typewrite(f"{dimen}", interval=0.025)
        robo_keyboard_press_enter(delay=0.5)
        #turn off the lock aspect ratio
        if True:            
            robo_keyboard_press_ctrl_enter(delay=1)
            #send tab 7 times
            robo_keyboard_press_tab(delay=0.5, repeat=7)
            # send space
            robo_keyboard_press_space(delay=0.5)
    elif max_dimension != "":   
        #turn on the lock aspect ratio
        if True:            
            robo_keyboard_press_ctrl_enter(delay=1)
            #send tab 7 times
            robo_keyboard_press_tab(delay=0.5, repeat=7)
            # send space
            robo_keyboard_press_space(delay=0.5)     
        width_current = 0
        robo_keyboard_press_ctrl_enter(delay=1)
        #send tab 3 times
        robo_keyboard_press_tab(delay=0.5, repeat=3)
        try:
            width_current = float(robo_keyboard_copy(**kwargs).replace(" mm", ""))
        except Exception as e:
            print(f"Error reading width: {e}")
            width_current = 0
        #send tab 1 times
        robo_keyboard_press_tab(delay=0.5, repeat=1)
        try:
            height_current = float(robo_keyboard_copy(**kwargs).replace(" mm", ""))
        except Exception as e:
            print(f"Error reading height: {e}")
            height_current = 0

        if height_current > width_current:        
            #send max dimension
            robo_keyboard_send(string=str(max_dimension), delay=1)
        else:
            #send shift tab once
            robo_keyboard_press_tab_shift(delay=0.5, repeat=1)
            #send max dimension
            robo_keyboard_send(string=str(max_dimension), delay=1)
        #press enter
        robo_keyboard_press_enter(delay=0.5)
        #turn off the lock aspect ratio
        if True:            
            robo_keyboard_press_ctrl_enter(delay=1)
            #send tab 7 times
            robo_keyboard_press_tab(delay=0.5, repeat=7)
            # send space
            robo_keyboard_press_space(delay=0.5)

    robo_delay(delay=delay)
        

    

def robo_file_copy(**kwargs):

    method = kwargs.get('method', 'shutil')


    file_source = kwargs.get('file_source', '')
    file_destination = kwargs.get('file_destination', '')
    if file_source != "" and file_destination != "":
        if method == 'xcopy':
            #check if the file exists
            if os.path.isfile(file_source):        
                print(f"copying {file_source} to {file_destination}")
                #use xcopy with overwrite and no prompt
                os.system(f"xcopy {file_source} {file_destination} /Y /N /I")
            else:
                print(f"file {file_source} does not exist")
        elif method == 'shutil':
            #check if the file exists
            if os.path.isfile(file_source):
                print(f"copying {file_source} to {file_destination}")
                #use shutil to copy the file
                import shutil
                shutil.copy(file_source, file_destination)
            else:
                print(f"file {file_source} does not exist")

## google_doc stuf
#add text to google doc
def robo_google_doc_add_text(**kwargs):
    url = kwargs.get('url', '')
    text = kwargs.get('text', '')
    position = kwargs.get('position', 'end') # start, end
    delay = kwargs.get('delay', 5)
    format = kwargs.get('format', True) # bold, italic, underline
    down_times = kwargs.get('down_times', 20)
    method = kwargs.get('method', 'type') # keyboard, api

    if format:
        #remove double and triple new lines
        text = text.replace("\\n\\n", "\\n").replace("\\n\\n", "\\n")
        while "\n\n" in text:
            text = text.replace("\n\n", "\n")
        #/n/r with just /n
        text = text.replace("\\n\\r", "\\n").replace("\\r\\n", "\\n")
        #replace \t with {tab}
        text = text.replace("\\t", "{tab}")
        


    message = kwargs.get('message', f"Adding text to Google Doc at {url}...")
    #add text to google doc
    print(message)
    #open google doc
    os.system(f"start {url}")    
    robo_delay(delay=10)
    #move to position
    if position == 'start':
        robo_keyboard_press_ctrl_generic(string='home', delay=2)
    elif position == 'end':
        #press down 100 times to go to end
        robo_keyboard_press_down(delay=0.1, repeat=down_times)
        #add new line
        robo_keyboard_press_enter(delay=2)        
    #type text
    if method == 'type':
        robo_keyboard_send(string=text, delay=2)
        robo_delay(delay=delay)
    elif method == 'paste':
        #copy text to clipboard
        clipboard.copy(text)
        #paste
        robo_keyboard_press_ctrl_generic(string='v', delay=2)
        robo_delay(delay=delay)


def robo_google_doc_new(**kwargs):
    delay = kwargs.get('delay', 5)
    message = kwargs.get('message', f"Creating a new Google Doc...")
    template = kwargs.get('template', '')
    title = kwargs.get('title', '')
    folder = kwargs.get('folder', '')
    if template == '':
        template = 'https://docs.google.com/document/u/0/create'
        #create a new google doc
    print(message)
    #open new google doc
    os.system(f"start {template}")    
    robo_delay(delay=10)
    #use key strokes to create a copy alt_f, down three times enter, wait, send title, tab 5, enter, wait 10 send title
    if True:
        #press alt f
        robo_keyboard_press_alt_f(delay=2)
        #press down three times
        robo_keyboard_press_down(delay=0.5, repeat=3)
        #press enter
        robo_keyboard_press_enter(delay=5)
        if title != "":
            #send title
            robo_keyboard_send(string=title, delay=2)
        #press tab 5 times
        robo_keyboard_press_tab(delay=0.5, repeat=5)
        #press enter
        robo_keyboard_press_enter(delay=10)
    if title != "":
        #send title
        robo_keyboard_send(string=title, delay=2)
    if folder != "": #down four times then send folder name
        #press tab 4 times
        robo_keyboard_press_down(delay=0.5, repeat=4)
        #send folder name
        robo_keyboard_send(string=folder, delay=2)
    #use keyboard to get url to clipboard and return it ctrtl l to focus ctrl a ctrl c
    robo_keyboard_press_ctrl_generic(string='l', delay=2)
    robo_keyboard_press_ctrl_generic(string='a', delay=2)
    robo_keyboard_press_ctrl_generic(string='c', delay=2)
    #load from clipboard
    url = clipboard.paste()
    print(f"New Google Doc URL: {url}")
    robo_delay(delay=delay)
    return_value = {"url_google_doc": url}
    return return_value


def robo_git_clone_repo(**kwargs):
    repo = kwargs.get('repo', '')
    folder = kwargs.get('folder', 'c:\\gh')
    folder_repo = os.path.join(folder, repo)
    update = kwargs.get('update', False)

    folder_utility = f"c:\\gh\\{repo}"
        #if folder doesn't exist theb clone it
    if not os.path.exists(folder_utility):
        print(f"Cloning {repo} to {folder_utility}")
        # Clone the repository if folder doesn't exist
        clone_command = f"git clone https://github.com/oomlout/{repo}.git {folder_repo}"
        os.system(clone_command) 
    else:
        print(f"Folder {folder_utility} already exists")

    if update:
        os_directory_current = os.getcwd()
        print(f"Updating {repo} in {folder_utility}")
        # Change to the repository directory
        os.chdir(folder_utility)
        # Pull the latest changes
        os.system("git pull")
        #reset os directory
        os.chdir(os_directory_current)

#image
def robo_image_upscale(**kwargs):
    action = kwargs.get("action", {})
    if action == {}:
        action = copy.deepcopy(kwargs)
    directory = kwargs.get("directory", "")
    file_input = action.get("file_input", "")
    file_input = os.path.join(directory, file_input)
    file_input_full = os.path.abspath(file_input)
    #png or jpeg or jpg
    file_output_default = file_input.replace(".png", "_upscaled.png").replace(".jpg", "_upscaled.jpg").replace(".jpeg", "_upscaled.jpeg")
    file_output = action.get("file_output", file_output_default)
    if directory not in file_output:
        file_output = os.path.join(directory, file_output)
    upscale_factor = action.get("upscale_factor", 2)
    
    print(f"Upscaling image function file: {file_input_full} to {file_output} by a factor of {upscale_factor}")
    #robo_delay(delay=300)
    
    
    #if file_input is a file
    if os.path.isfile(file_input):
        #use pil; LANCZOS to upscale the image
        from PIL import Image
        try:
            #if outpurt file exists, delete
            if os.path.exists(file_output):
                os.remove(file_output)
                print(f"Removed existing output file {file_output}")
            with Image.open(file_input_full) as img:
                # Calculate new size
                new_size = (int(img.width * upscale_factor), int(img.height * upscale_factor))
                # Resize the image
                #img = img.resize(new_size, Image.LANCZOS)
                #use nearest
                img = img.resize(new_size, Image.NEAREST)
                # Save the upscaled image
                img.save(file_output)
                print(f"Image upscaled and saved to {file_output}")
                
                
        except Exception as e:
            print(f"Error upscaling image {file_input_full}: {e}")
            return
    else:
        print(f"file_input {file_input} does not exist, skipping image upscale")
        return
    #robo_delay(delay=20)

def robo_keyboard_close_tab(**kwargs):
    robo_chrome_close_tab(**kwargs)

def robo_keyboard_copy(**kwargs):
    delay = kwargs.get('delay', 1)
    position = kwargs.get('position', [0, 0])
    #click positionem of 
    if position != [0, 0]:
        pos = position
        pyautogui.click(pos[0], pos[1])
    #copy the text from the clipboard
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    #get the text from the clipboard
    clip = clipboard.paste()
    robo_delay(delay=delay)
    return clip

def robo_keyboard_paste(**kwargs):
    delay = kwargs.get('delay', 1)
    position = kwargs.get('position', [0, 0])
    text = kwargs.get('text', '')
    #click positionem of 
    if position != [0, 0]:
        pos = position
        pyautogui.click(pos[0], pos[1])
    #set the clipboard to the text
    clipboard.copy(text)
    #paste the text from the clipboard
    pyautogui.hotkey('ctrl', 'v')
    


def robo_keyboard_press_alt_f(**kwargs):
    kwargs["string"] = "f"
    robo_keyboard_press_alt_generic(**kwargs)

def robo_keyboard_press_alt_generic(**kwargs):
    string = kwargs.get('string', '')
    delay = kwargs.get('delay', 1)
    delay_keypress = kwargs.get('delay_keypress', 0.025)
    repeat = kwargs.get('repeat', 1)
    #press ctrl + string
    if repeat > 1:
        print(f"pressing alt + {string} {repeat} times")
        for i in range(repeat):
            pyautogui.hotkey('alt', string)
            time.sleep(delay_keypress)
        robo_delay(delay=delay)
    else:
        print(f"pressing alt + {string} once")
        pyautogui.hotkey('alt', string)
        robo_delay(delay=delay)

def robo_keyboard_press_ctrl_generic(**kwargs):
    string = kwargs.get('string', '')
    delay = kwargs.get('delay', 1)
    delay_keypress = kwargs.get('delay_keypress', 0.025)
    repeat = kwargs.get('repeat', 1)
    #press ctrl + string
    if repeat > 1:
        print(f"pressing ctrl + {string} {repeat} times")
        for i in range(repeat):
            pyautogui.hotkey('ctrl', string)
            time.sleep(delay_keypress)
        robo_delay(delay=delay)
    else:
        print(f"pressing ctrl + {string} once")
        pyautogui.hotkey('ctrl', string)
        robo_delay(delay=delay)

def robo_keyboard_press_ctrl_enter(**kwargs):
    kwargs["string"] = "enter"
    robo_keyboard_press_ctrl_generic(**kwargs)

def robo_keyboard_press_shift_enter(**kwargs):
    kwargs["string"] = "enter"
    robo_keyboard_press_shift_generic(**kwargs)

def robo_keyboard_press_ctrl_i(**kwargs):
    kwargs["string"] = "i"
    robo_keyboard_press_ctrl_generic(**kwargs)

#press esc
def robo_keyboard_press_escape(**kwargs):
    kwargs["string"] = "esc"
    robo_keyboard_press_generic(**kwargs)

#press down
def robo_keyboard_press_down(**kwargs):
    kwargs["string"] = "down"
    robo_keyboard_press_generic(**kwargs)

#press up
def robo_keyboard_press_up(**kwargs):
    kwargs["string"] = "up"
    robo_keyboard_press_generic(**kwargs)

#press left
def robo_keyboard_press_left(**kwargs):
    kwargs["string"] = "left"
    robo_keyboard_press_generic(**kwargs)

#press right
def robo_keyboard_press_right(**kwargs):
    kwargs["string"] = "right"
    robo_keyboard_press_generic(**kwargs)

#delete
def robo_keyboard_press_delete(**kwargs):
    kwargs["string"] = "delete"
    robo_keyboard_press_generic(**kwargs)

#press back space
def robo_keyboard_press_backspace(**kwargs):
    kwargs["string"] = "backspace"
    robo_keyboard_press_generic(**kwargs)

#press enter
def robo_keyboard_press_enter(**kwargs):
    kwargs["string"] = "enter"
    robo_keyboard_press_generic(**kwargs)

#press space
def robo_keyboard_press_space(**kwargs):
    kwargs["string"] = "space"
    robo_keyboard_press_generic(**kwargs)

#press tab
def robo_keyboard_press_tab(**kwargs):
    kwargs["string"] = "tab"
    robo_keyboard_press_generic(**kwargs)

#press tab
def robo_keyboard_press_tab_shift(**kwargs):
    kwargs["string"] = "tab"
    robo_keyboard_press_shift_generic(**kwargs)



#press string
def robo_keyboard_send(**kwargs):
    robo_keyboard_press_string(**kwargs)
        
def robo_keyboard_press_string(**kwargs):
    string = kwargs.get('string', '')
    delay = kwargs.get('delay', 1)
    delay_keypress = kwargs.get('delay_keypress', 0.025)    
    print(f"pressing {string} once")
    pyautogui.typewrite(string, interval=delay_keypress)
    robo_delay(delay=delay)

def robo_keyboard_press_generic(**kwargs):
    string = kwargs.get('string', '')
    delay = kwargs.get('delay', 1)
    delay_keypress = kwargs.get('delay_keypress', 0.258)
    repeat = kwargs.get('repeat', 1)
    #press escape to close the menu
    if repeat > 1:
        print(f"pressing {string} {repeat} times")
        for i in range(repeat):
            pyautogui.press(string)
            time.sleep(delay_keypress)
        robo_delay(delay=delay)
    else:
        print(f"pressing {string} once")
        pyautogui.press(string)
        robo_delay(delay=delay)

def robo_keyboard_press_shift_generic(**kwargs):
    string = kwargs.get('string', '')
    delay = kwargs.get('delay', 1)
    delay_keypress = kwargs.get('delay_keypress', 0.258)
    repeat = kwargs.get('repeat', 1)
    #press escape to close the menu
    if repeat > 1:
        print(f"pressing shift {string} {repeat} times")
        for i in range(repeat):
            pyautogui.keyDown('shift')
            pyautogui.press(string)
            pyautogui.keyUp('shift')
            time.sleep(delay_keypress)
        robo_delay(delay=delay)
    else:
        print(f"pressing shift {string} once")
        pyautogui.keyDown('shift')
        pyautogui.press(string)
        pyautogui.keyUp('shift')
        robo_delay(delay=delay)


def robo_keyboard_select_all(**kwargs):
    delay = kwargs.get('delay', 1)
    #select all
    print("selecting all")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    robo_delay(delay=delay)

def check_key_pressed():
    """Check if any key is pressed and return it, or None if no key is pressed"""
    try:
        if sys.platform == "win32":
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                return key
        else:
            # For Linux/Mac - simplified approach
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                key = sys.stdin.read(1).lower()
                return key
    except Exception as e:
        # If key detection fails, just continue without it
        pass
    return None

def robo_delay(**kwargs):
    delay = kwargs.get('delay', 1)
    rand = kwargs.get('rand', 0)
    message = kwargs.get('message', f"")
    if message != "":
        print(f"message")
    if rand > 0:
        rand_amount = random.randint(0, rand)
        delay = delay + rand_amount
    if delay <= 1:
        time.sleep(delay)
    elif delay > 5:
        print(f"<<<<<>>>>> waiting for {delay} seconds (press 's' to skip) or turn scroll lock off")
    
        splits = 10
        for i in range(splits):
            #print the progress bar
            print(".", end='', flush=True)
            for i in range(int(delay/splits)):
                # Check if 's' key is pressed
                key = check_key_pressed()
                if key == 's':
                    print("\nDelay skipped by pressing 's' key")
                    time.sleep(1)
                    return
                #check scroll lock state
                import ctypes

                if ctypes.windll.user32.GetKeyState(0x91) & 1 == 1:
                    print("Scroll Lock is OFF, skipping delay")
                    time.sleep(2)
                    pyautogui.press('scrolllock')
                    return
                time.sleep(1)
        print("")
    else:
        print(f"waiting for {delay} seconds (press 's' to skip)", end='', flush=True)
        for i in range(delay):
            #print the progress bar
            print(".", end='', flush=True)
            # Check if 's' key is pressed
            key = check_key_pressed()
            if key == 's':
                print("\nDelay skipped by pressing 's' key")
                time.sleep(5)
                return
            time.sleep(1)
        print("")

def robo_mouse_click(**kwargs):
    position = kwargs.get('position', [0, 0])
    delay = kwargs.get('delay', 1)
    button = kwargs.get('button', 'left')
    #click the mouse at the position
    print(f"Clicking at {position}...")
    pos = position
    pyautogui.click(pos[0], pos[1], button=button)
    robo_delay(delay=delay)

def robo_mouse_drag(**kwargs):
    position = kwargs.get('position', [0, 0])
    move = kwargs.get('move', [100, 100])
    position_start = kwargs.get('position_start', [])
    position_end = kwargs.get('position_end', [])
    delay = kwargs.get('delay', 1)
    duration = kwargs.get('duration', 0.5)
    button = kwargs.get('button', 'left')
    #drag the mouse from position_start to position_end
    print(f"Dragging from {position_start} to {position_end}...")
    pos_start = position
    pos_end = [position[0] + move[0], position[1] + move[1]]
    if position_start != [] and position_end != []:
        pos_start = position_start        
        pos_end = position_end
    pyautogui.moveTo(pos_start[0], pos_start[1])
    pyautogui.dragTo(pos_end[0], pos_end[1], duration=duration, button=button)
    robo_delay(delay=delay)

def robo_text_jinja_template(**kwargs):
    # import cProfile
    # profiler = cProfile.Profile()
    # profiler.enable()
    
    file_template = kwargs.get("file_template","")
    file_output = kwargs.get("file_output","")
    file_source = kwargs.get("file_source","")
    
    search_and_replace = kwargs.get("search_and_replace",[])

    dict_data = kwargs.get("dict_data",{})

    if dict_data == {} and file_source != "":
        #load yaml file
        import yaml
        old = False

        if old:
            with open(file_source, "r") as infile:
                dict_data = yaml.safe_load(infile)
        else:
            dict_data = load_yaml_unicode_test(file_source) 

    markdown_string = ""
    #if running in windows
    if os.name == "nt":
        file_template = file_template.replace("/", "\\")
    else:
        file_template = file_template.replace("\\", "/")
    with open(file_template, "r") as infile:
        markdown_string = infile.read()
    #data2 = copy.deepcopy(dict_data)
    #use pickle to deep copy the dictionary
    data2 = pickle.loads(pickle.dumps(dict_data, -1))

    pass

    #def fix search and replace for special characters
    data2 = fix_search_replace_special_characters(data2)

    #do search and replace
    if search_and_replace != []:
        for item in search_and_replace:
            search = item[0]
            replace = item[1]
            if search != "":
                for key in data2:
                    if isinstance(data2[key], str):
                        data2[key] = data2[key].replace(search, replace)

    try:
        markdown_string = jinja2.Template(markdown_string).render(p=data2)
    except Exception as e:
        print(f"error in jinja2 template: {file_template}")
        print(e)
        markdown_string = f"markdown_string_error\n{e}"
    #make directory if it doesn't exist
    directory = os.path.dirname(file_output)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    #mode = "open"
    mode = "buffer"
    
    if mode == "open":
        with open(file_output, "w", encoding="utf-8") as outfile:
            outfile.write(markdown_string)
            
    elif mode == "buffer":
        #write to a buffer then save for speen
        with io.StringIO() as outfile:
            outfile.write(markdown_string)
            with open(file_output, "w", encoding="utf-8") as outfile2:
                outfile2.write(outfile.getvalue())

def fix_search_replace_special_characters(data):
    """
    Recursively process a dictionary/list and replace special Unicode characters
    with their XML/SVG entity equivalents (&#xHHHH; format)
    """
    def fix_corrupted_utf8(text):
        """Fix common UTF-8 corruption patterns for various languages"""
        if not isinstance(text, str):
            return text
        
        # Map of corrupted character sequences to their correct Unicode code points
        # Process uppercase versions first to avoid case conflicts
        corrections = {
            # Romanian characters - UPPERCASE FIRST
            'A\xc8\u2122-': 'AȘ-',  # Special case for CARAȘ-SEVERIN pattern
            'E\xc8\u2122': 'EȘ',    # For MUREȘ, etc.
            'O\xc8\u2122': 'OȘ',    # For BOTOȘANI pattern  
            'A\xc8\u2122I': 'AȘI',  # For IAȘI pattern
            'A\xc8\u2122O': 'AȘO',  # For BRAȘOV pattern
            '\xc8\u2122I': 'ȘI',    # For CĂLĂRAȘI pattern
            '\xc8\u2122A': 'ȘA',    # For various patterns
            
            # Regular Romanian characters
            '\xc8\u203a': '\u021b',  # ț - Latin small letter t with comma below
            '\xc8\u203A': '\u021A',  # Ț - Latin capital letter T with comma below
            '\xc8\u0161': '\u0219',  # ș - Latin small letter s with comma below
            '\xc8\u0160': '\u0218',  # Ș - Latin capital letter S with comma below
            '\xc8\u2122': '\u0219',  # ș - Latin small letter s with comma below (lowercase variant)
            '\xc8\u2021': '\u0218',  # Ș - Latin capital letter S with comma below (uppercase variant)
            '\xc4\u0192': '\u0103',  # ă - Latin small letter a with breve
            '\xc4\u0191': '\u0102',  # Ă - Latin capital letter A with breve
            '\xc3\xa2': '\u00e2',    # â - Latin small letter a with circumflex
            '\xc3\xA2': '\u00e2',    # â - variant
            'È\u203a': '\u021b',     # Alternative: ț
            'È\u203A': '\u021A',     # Alternative: Ț
            'È\u0161': '\u0219',     # Alternative: ș
            'È\u0160': '\u0218',     # Alternative: Ș
            'È\u2122': '\u0219',     # Alternative: ș (lowercase, common in Romanian regions)
            'È\u2021': '\u0218',     # Alternative: Ș (uppercase variant)
            'Ä\u0192': '\u0103',     # Alternative: ă
            'Ä\u0191': '\u0102',     # Alternative: Ă
            'Ã\xa2': '\u00e2',       # Alternative: â
            'Ã\xA2': '\u00e2',       # Alternative: â
            
            # French characters
            '\xc3\xa9': '\u00e9',    # é - Latin small letter e with acute
            '\xc3\xa8': '\u00e8',    # è - Latin small letter e with grave
            '\xc3\xaa': '\u00ea',    # ê - Latin small letter e with circumflex
            '\xc3\xab': '\u00eb',    # ë - Latin small letter e with diaeresis
            '\xc3\xa0': '\u00e0',    # à - Latin small letter a with grave
            '\xc3\xa2': '\u00e2',    # â - Latin small letter a with circumflex
            '\xc3\xa7': '\u00e7',    # ç - Latin small letter c with cedilla
            '\xc3\xb9': '\u00f9',    # ù - Latin small letter u with grave
            '\xc3\xbb': '\u00fb',    # û - Latin small letter u with circumflex
            '\xc3\xbc': '\u00fc',    # ü - Latin small letter u with diaeresis
            '\xc3\xae': '\u00ee',    # î - Latin small letter i with circumflex
            '\xc3\xaf': '\u00ef',    # ï - Latin small letter i with diaeresis
            '\xc5\u201c': '\u0153',  # œ - Latin small ligature oe
            'Ã\xa9': '\u00e9',       # Alternative: é
            'Ã\xa8': '\u00e8',       # Alternative: è
            'Ã\xa7': '\u00e7',       # Alternative: ç
            
            # German characters
            '\xc3\xa4': '\u00e4',    # ä - Latin small letter a with diaeresis
            '\xc3\xb6': '\u00f6',    # ö - Latin small letter o with diaeresis
            '\xc3\x9f': '\u00df',    # ß - Latin small letter sharp s
            '\xc3\x84': '\u00c4',    # Ä - Latin capital letter A with diaeresis
            '\xc3\x96': '\u00d6',    # Ö - Latin capital letter O with diaeresis
            '\xc3\x9c': '\u00dc',    # Ü - Latin capital letter U with diaeresis
            'Ã\xa4': '\u00e4',       # Alternative: ä
            'Ã\xb6': '\u00f6',       # Alternative: ö
            'Ã\x9f': '\u00df',       # Alternative: ß
            
            # Spanish characters
            '\xc3\xb1': '\u00f1',    # ñ - Latin small letter n with tilde
            '\xc3\x91': '\u00d1',    # Ñ - Latin capital letter N with tilde
            '\xc3\xad': '\u00ed',    # í - Latin small letter i with acute
            '\xc3\xb3': '\u00f3',    # ó - Latin small letter o with acute
            '\xc3\xba': '\u00fa',    # ú - Latin small letter u with acute
            '\xc2\xa1': '\u00a1',    # ¡ - Inverted exclamation mark
            '\xc2\xbf': '\u00bf',    # ¿ - Inverted question mark
            'Ã\xb1': '\u00f1',       # Alternative: ñ
            'Ã\xad': '\u00ed',       # Alternative: í
            'Ã\xb3': '\u00f3',       # Alternative: ó
            
            # Portuguese characters
            '\xc3\xa3': '\u00e3',    # ã - Latin small letter a with tilde
            '\xc3\xb5': '\u00f5',    # õ - Latin small letter o with tilde
            'Ã\xa3': '\u00e3',       # Alternative: ã
            'Ã\xb5': '\u00f5',       # Alternative: õ
            
            # Polish characters
            '\xc5\u0201': '\u0105',  # ą - Latin small letter a with ogonek
            '\xc4\u2021': '\u0107',  # ć - Latin small letter c with acute
            '\xc4\u2122': '\u0119',  # ę - Latin small letter e with ogonek
            '\xc5\u201a': '\u0142',  # ł - Latin small letter l with stroke
            '\xc5\u201e': '\u0144',  # ń - Latin small letter n with acute
            '\xc3\xb3': '\u00f3',    # ó - Latin small letter o with acute (shared with Spanish)
            '\xc5\u0161': '\u015b',  # ś - Latin small letter s with acute
            '\xc5\xba': '\u017a',    # ź - Latin small letter z with acute
            '\xc5\xbc': '\u017c',    # ż - Latin small letter z with dot above
            
            # Czech characters
            '\xc4\u008d': '\u010d',  # č - Latin small letter c with caron
            '\xc4\u017e': '\u010f',  # ď - Latin small letter d with caron
            '\xc4\u203a': '\u011b',  # ě - Latin small letter e with caron
            '\xc5\u2122': '\u0148',  # ň - Latin small letter n with caron
            '\xc5\u2122': '\u0159',  # ř - Latin small letter r with caron
            '\xc5\u0161': '\u0161',  # š - Latin small letter s with caron
            '\xc5\u2022': '\u0165',  # ť - Latin small letter t with caron
            '\xc5\u00af': '\u016f',  # ů - Latin small letter u with ring above
            '\xc5\xbe': '\u017e',    # ž - Latin small letter z with caron
            
            # Greek characters (common ones)
            '\xce\xb1': '\u03b1',    # α - Greek small letter alpha
            '\xce\xb2': '\u03b2',    # β - Greek small letter beta
            '\xce\xb3': '\u03b3',    # γ - Greek small letter gamma
            '\xce\xb4': '\u03b4',    # δ - Greek small letter delta
            '\xce\xb5': '\u03b5',    # ε - Greek small letter epsilon
            
            # Currency and common symbols
            '\xc2\xa3': '\u00a3',    # £ - Pound sign
            '\xc2\xa5': '\u00a5',    # ¥ - Yen sign
            '\xe2\u201a\xac': '\u20ac',  # € - Euro sign
            '\xc2\xa9': '\u00a9',    # © - Copyright sign
            '\xc2\xae': '\u00ae',    # ® - Registered sign
            '\xe2\u201e\xa2': '\u2122',  # ™ - Trademark sign
            '\xc2\xb0': '\u00b0',    # ° - Degree sign
            '\xc2\xb1': '\u00b1',    # ± - Plus-minus sign
            '\xc3\u2014': '\u00d7',  # × - Multiplication sign
            '\xc3\xb7': '\u00f7',    # ÷ - Division sign
            
            # Quotation marks and dashes
            '\xe2\u20ac\u0153': '\u2018',  # ' - Left single quotation mark
            '\xe2\u20ac': '\u2019',    # ' - Right single quotation mark
            '\xe2\u20ac\u0153': '\u201c',  # " - Left double quotation mark
            '\xe2\u20ac': '\u201d',    # " - Right double quotation mark
            '\xe2\u20ac\u201c': '\u2013',  # – - En dash
            '\xe2\u20ac\u201d': '\u2014',  # — - Em dash
            '\xc2\xab': '\u00ab',    # « - Left-pointing double angle quotation mark
            '\xc2\xbb': '\u00bb',    # » - Right-pointing double angle quotation mark
        }
        
        result = text
        for corrupted, correct in corrections.items():
            result = result.replace(corrupted, correct)
        
        return result
    
    def unicode_to_svg_entity(text):
        """Convert a string with Unicode characters to SVG-safe entities"""
        if not isinstance(text, str):
            return text
        
        # First fix any corrupted UTF-8
        text = fix_corrupted_utf8(text)
        
        result = []
        for char in text:
            code_point = ord(char)
            # Only escape non-ASCII characters (code point > 127)
            # Keep regular ASCII characters as-is
            if code_point > 127:
                # Convert to XML/SVG entity format: &#xHEX;
                result.append(f'&#x{code_point:04X};')
            else:
                result.append(char)
        
        return ''.join(result)
    
    def process_value(obj):
        """Recursively process dictionary/list/string values"""
        if isinstance(obj, dict):
            return {k: process_value(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [process_value(item) for item in obj]
        elif isinstance(obj, str):
            return unicode_to_svg_entity(obj)
        else:
            return obj
    
    return process_value(data)

def load_yaml_unicode_test(file_path):
    import yaml

    # Load YAML - it should already be UTF-8 encoded correctly
    # Don't apply any transformations that might corrupt the characters
    with open(file_path, 'r', encoding='utf-8') as infile:
        data = yaml.safe_load(infile)
    
    return data

def robo_screenshot(**kwargs):
    position = kwargs.get('position', [0, 0])
    #if position is only two values add size to it
    if len(position) == 2:
        size = kwargs.get('size', [1920, 1080])
        position = [position[0], position[1], position[0] + size[0], position[1] + size[1]]
    delay = kwargs.get('delay', 1)
    folder = kwargs.get('folder', '')
    file_name = kwargs.get('file_name', 'screenshot.png')
    #take a screenshot
    print(f"Taking a screenshot at {position}...")
    pos = position
    screenshot = pyautogui.screenshot(region=(pos[0], pos[1], pos[2]-pos[0], pos[3]-pos[1]))
    #save the screenshot
    if folder != "":
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_name = f"{folder}\\{file_name}"
        print(f"Saving the screenshot to {file_name}...")
        screenshot.save(file_name)
    robo_delay(delay=delay)
    
def robo_convert_svg_to_pdf(**kwargs):
    robo_pdf_from_svg(**kwargs)


def robo_convert_svg_to_png(**kwargs):
    robo_png_from_svg(**kwargs)

def robo_pdf_from_svg(**kwargs):
    file_input = kwargs.get('file_input', '')
    file_output = kwargs.get('file_output', '')
    if file_output == '':
        file_output = file_input.replace('.svg', '.pdf')
    #convert using call to inkscape command line
    print(f"Converting {file_input} to {file_output}...")
    os.system(f"inkscape {file_input} --export-filename={file_output}")

def robo_convert_svg_to_png(**kwargs):
    robo_png_from_svg(**kwargs)

def robo_png_from_svg(**kwargs):
    file_input = kwargs.get('file_input', '')
    file_output = kwargs.get('file_output', '')
    if file_output == '':
        file_output = file_input.replace('.svg', '.png')
    #convert using call to inkscape command line
    print(f"Converting {file_input} to {file_output}...")
    os.system(f"inkscape {file_input} --export-filename={file_output}")

def robo_pdf_merge(**kwargs):
    import PyPDF2
    folder = kwargs.get('folder', '')
    fil = kwargs.get('files', '')
    filters = kwargs.get('filters', ['.pdf'])
    file_output = kwargs.get('file_output', 'merged.pdf')
    #if filter is a string make it an array
    if isinstance(filters, str):
        filter = [filter]
    if fil == '':
        fil = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                #only include if all filters are in file
                file_full = os.path.join(root, file)
                if all(f in file_full for f in filters):
                    fil.append(file_full)

    
    
    #merge the pdf files
    print(f"Merging {len(fil)} pdf files into {file_output}...")
    merger = PyPDF2.PdfMerger()
    for pdf in fil:
        print(f"  adding {pdf}")
        merger.append(pdf)
    merger.write(file_output)
    merger.close()
