import os                   #imports OS module. OS module allows for file searching and editing.
import subprocess           #imports subprocess module. Subprocess module allows for external executables (like the Exiftool) to be run.
import shutil               #imports shutil module. Shutil module offers a number of high-level file operations like copying and removing fils.


def find_GRILLA_output():
    loop = 1   
    while loop == 1: #Makes sure a valid file path is entered.
        file_directory = input("Where are the files you want to work with? Enter file directory: ") #Asks user to enter directory
        if os.path.exists(file_directory): #Checks to see if user input file directory exists
            print()
            print(f"The file path '{file_directory} exists. Navigating now.","\n")
            loop = 0 #breaks loop if user entered a valid file directory
        else: #Loop continues if  user did not enter a valid file directory until a valid file directory is entered
            print(f"The file path '{file_directory} does not exist. Please enter a valid file path.")

    for root, dirs, files in os.walk(file_directory):
        if "GRILLA" in root:# need root to contain dirs that includes text string "GRILLA"
            n =0
            while n < len(files)-1: #Checks to see if there is a .txt file in the above root
                if files[n].endswith('.txt'):
                    txt_present = 'Y' #defines variable to indicate .txt file is present
                    n=n+len(files) #stops looking for .txt files
                else:
                    txt_present = 'N'#defines variable to indicate .txt file is not present
                    n=n+1 #adds one to the loop count and keeps looking for .txt file
            n=0
            while n < len(files)-1: #Checks to see if there is a .bmp file in the above root
                if files[n].endswith('.bmp'):
                    bmp_present = 'Y'#defines variable to indicate .bmp file is present
                    n=n+len(files) #stops looking for .bmp files
                else:
                    bmp_present = 'N'#defines variable to indicate .bmp file is not present
                    n=n+1 #adds one to the loop count and keeps looking for .bmp file
            n=0
            while n < len(files)-1: #Looks through all files in input directory for files ending with jpg
                if files[n].endswith('.jpg'): #If jpg file is found:
                    jpg_present = 'Y'   # variable is changed to Y
                    n=n+len(files) #stops looking
                else:
                    jpg_present = 'N' # If the first file is not a jpg, the code looks through all other files 'N' is assigned to variable if no jpgs are present
                    n=n+1 

            if jpg_present=='N' and bmp_present =='Y' and txt_present =='Y': #checks to see if file contains the necessary file types to run the 508 compliance code
                print("Checking the following folder for necessary files:")
                print(root) #prints file path
                print("Necessary files found") #prints to inform user there was a match
                convert(root) #if there is a match, the convert function is ran
                print("Metadata edited") #prints to inform metadata was edited
                print("____________________________________________________________________________________________________________________")
            else: #occurs if file does not contain the necessary file types to run the 508 compliance code
                print("Checking the following folder for necessary files:")
                print(root) #prints root
                print("Necessary files not found") #informs user that the file did not match desired input

def convert(root): #takes root from "find_GRILLA_output()", locates bmps, converts them to jpgs, and adds metadata comment
    bmp_to_jpg(root) # calls bmp_to_jpg() function which takes root from "find_GRILLA_output", locates bmps, converts them to jpgs
    Exif_Tool_overview(root) # calls Exif_Tooloverview() function whichtakes jpgs from "bmp_to_jpgs()", renames them using .txt file, and adds metadata comment
    print() #breaks up output text
            

def Exif_Tool_overview(root): #Uses Exiftool to add metadata comment
    first_txt_file = change_name(root) # calls change_name() function which locates the txt file in GRILLA output and assigns the first line of text to a variable.
    exifTool = "/Users/dvitale/exiftool.exe" # IMPORTANT - assigns users ExifTool file path to a variable so other functions can utilize
                                             # The above line must be changed to the location where the user saved the ExifTool
    comment_choice(exifTool, root, first_txt_file) #calls comment_choice() function which adds predefined comments to jpgs

    
        
def bmp_to_jpg(root): # converts .bmp files to .jpg
    from PIL import Image # type: ignore #imports PIL library
    input_directory = root #converted jpg will be saved in the same location as the original bmp. 
    output_directory = root

    file_list = os.listdir(input_directory) #creates list of files in input directory

    for file_name in file_list: #looks through list of files in the input directory
        if file_name.lower().endswith('.bmp'): #looks for bmp files
            input_file_path = os.path.join(input_directory, file_name) #creates file path to bmp image by joining the input directory and file name
            output_file_name = os.path.splitext(file_name)[0] + '.jpg' # takes bmp file and changes the named file type to jpg
            output_file_path = os.path.join(output_directory, output_file_name) #creates file path to jpg image by joining the output directory and file name

            with Image.open(input_file_path) as img:
                img.save(output_file_path, 'JPEG') # converts .bmp to .jpg

def change_name(root):
    files = os.listdir(root) #lists files in given file path
    txt_files = [file for file in files if file.endswith(".txt")] #extracts txt files from list
    if txt_files:
        first_txt_file =txt_files[0] # selects first text file in the list of text files.
        print('\n',"Text file used for name change and metadata addition:")
        print(first_txt_file, '\n') # prints name of first txt file
        with open(os.path.join(root, first_txt_file), 'r') as txt_file:
                first_line = txt_file.readline().strip() # assigns first line of text to a variable
        first_line = first_line.replace('"','')    # Cleans up first line of text
        first_line = first_line.replace(',','')    # Cleans up first line of text
        first_line = first_line.replace('_','')    # Cleans up first line of text
        first_line = first_line.replace(' ','_')   # Cleans up first line of text
    jpg_files = [file for file in files if file.endswith(".jpg")] # Takes all .jpg from  the file directory and adds them to a list.
    for jpg_file in jpg_files:
        base_name, extension = os.path.splitext(jpg_file) #extracts jpg file extension
        new_name = first_line + base_name + extension # joins original name, first line of txt file, and file extension
        print(jpg_file, "renamed to", new_name) #informs user of new file name
        old_path = os.path.join(root, jpg_file) # assigns original file path to variable
        new_path = os.path.join(root, new_name) # assigns new file path to variable
        os.rename(old_path, new_path) # renames file using os package
    return(first_txt_file) #returns first txt file so that it can be used later in the metadata comment choice



def add_comment_to_jpg( exifTool, root, comment): #uses Exiftool to add comment to metadata
    command = [exifTool, "-comment="+comment, root] #creates command that utilizes Exiftool to add a comment to a file
    subprocess.run(command) #runs command

def comment_choice(exifTool, root, first_txt_file): # utilizes add_comment_to_jpg() function, predefined comments, and lines of the .txt file to add metadata comment
    #print(root) #TEMPORARY
    #print("598792348493")
    for filename in os.listdir(root):
        if filename.lower().endswith(".jpg"): #for all jpgs in file
            preset_1 = "Plot of Horizontal to Vertical Spectral Ratio that plots frequency in Hertz on the x-axis and amplitude (a dimensionless value) on the y-axis.  The resonance frequency is indicated at the top of the plot."
            preset_2 = "Single component spectra plot frequency in Hertz are shown on the x axis and acceleration in mm/s per Hertz are plotted on the y-axis.   The north-south component is green; the east-west component is blue; and up-down (vertical) is pink."
            if 'HVSR' in filename: # adds specific pre-defined comment if "HVSR" is in the file name
                #print(filename)
                file_path = os.path.join(root, filename) #assigns file path to variable
                txt_file = os.path.join(root, first_txt_file) # assigns file path to first text file

                with open(txt_file, 'r') as file: #opens text file
                    lines = file.readlines() #reads lines in text file
                    if len(lines)>=13: 
                        line_13 = lines[12] # assigns 13th line to a variable if the txt has 13 lines or greater
                        #print(line_13) # prints 13th line of text
                preset_1 = preset_1 + line_13 # adds preset comment and 13th line of txt for a more meaningful comment.
                print()
                add_comment_to_jpg(exifTool,file_path, preset_1) # adds comment to jpg
                print(f"comment added to {file_path}: {preset_1}") #prints comment and file path to inform user which comment was added to which file
                print() #prints line for spacing in output
            if 'PowSpecTot' in filename: # adds specific pre-defined comment if "PowSpecTot" is in the file nam
                #print(filename)
                file_path = os.path.join(root, filename)
                add_comment_to_jpg(exifTool,file_path, preset_2) # adds comment to jpg
                print(f"comment added to {file_path}: {preset_2}") #prints comment and file path to inform user which comment was added to which file
                print()
    hold(root) #calls hold() function which creates a folder that unnessecary files are moved to

def hold(root): #defines function which creates a folder that unnessecary files are moved to
    folder_name = 'Hold' #defines name of new folder
    folder_path = os.path.join(root,folder_name) #defines path to the new folder
    if not os.path.exists(folder_path): #checks to make sure hold file does not already exist (this check is not case sensitive)
        os.makedirs(folder_path) #if "hold" folder does not exist, "hold" folder is created
        print("Hold folder created. Moving the following files to the hold folder:")
    else:
        print("Hold Folder already exists") #informs the user that "hold" folder already exists and code carries on

    for filename in os.listdir(root): #create a list of all files in the current root
        if filename.lower().endswith(".bmp"): #finds all bmp files
            print(filename)
            file_path2 = os.path.join(root, filename) #creates full file path to each bmp file
            shutil.move(file_path2, folder_path) #moves bmp to "hold" folder
            
        if filename.lower().endswith(".jpg_original"): #finds all .jpg_original files
            print(filename)
            file_path3 = os.path.join(root, filename) #creates full file path to each jpg_original file
            shutil.move(file_path3, folder_path) #moves bmp to "hold" folder

find_GRILLA_output()



