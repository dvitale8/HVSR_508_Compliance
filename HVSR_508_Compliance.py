import os                   #imports OS module. OS module allows for file searching and editing.
import subprocess           #imports subprocess module. Subprocess module allows for external executables (like the Exiftool) to be run.


def find_GRILLA_output():
    loop = 1   
    # Makes sure a valid file path is entered.
    while loop == 1:
        file_directory = input("Where are the files you want to work with? Enter file directory: ")
        if os.path.exists(file_directory):
            print(f"The file path '{file_directory} exists. Navigating now.","\n")
            loop = 0
        else:
            print(f"The file path '{file_directory} does not exist. Please enter a valid file path.")

    for root,dirs,files in os.walk(file_directory):
    # need root to contain dirs that includes text string "GRILLA"
        if "GRILLA" in root:
            n =0
            while n < len(files)-1:
                if files[n].endswith('.txt'):
                    #print("present")
                    #print(files[n])
                    txt_present = 'Y'
                    n=n+len(files)
                else:
                    #print("not present")
                    txt_present = 'N'
                    n=n+1
            n=0
            while n < len(files)-1:
                if files[n].endswith('.bmp'):
                    bmp_present = 'Y'
                    #print(files[n])
                    n=n+len(files)
                else:
                    bmp_present = 'N'
                    n=n+1
            n=0
            while n < len(files)-1:
                if files[n].endswith('.jpg'):
                    jpg_present = 'Y'
                    #print(files[n])
                    n=n+len(files)
                else:
                    jpg_present = 'N'
                    n=n+1
            #add some type of counting element that runs through all files in list 

            if jpg_present=='N' and bmp_present =='Y' and txt_present =='Y':
                print(root)
                print("match")
                #need to convert root to file directory
                convert(root)
                print("Metadata edited")
            else:
                print(root)
                print("no match")

def convert(root): 
    bmp_to_jpg(root)
    Exif_Tool_overview(root)
    print()
            

def Exif_Tool_overview(root):
    #The Elif_Tool_overview function allow the user to choose the metadata modifications they want to perform
    # User can change the file name based on an associated txt document, add a metadata comment or both.
    change_name(root)
    exifTool = "/Users/dvitale/exiftool.exe"
    comment ='test'
    #add_comment_to_jpg(exifTool, root,comment)
    comment_choice(exifTool, root)
    # calls the change_name function and then the add_metadata function based on user input
    
        
def bmp_to_jpg(root):
    # converts .bmp files to .jpg
    from PIL import Image
    #imports PIL library
    input_directory = root
    output_directory = root

    file_list = os.listdir(input_directory)

    for file_name in file_list:
        if file_name.lower().endswith('.bmp'):
            input_file_path = os.path.join(input_directory, file_name)
            output_file_name = os.path.splitext(file_name)[0] + '.jpg'
            output_file_path = os.path.join(output_directory, output_file_name)
            #finds all bmp files and creates an output file path that uses the bmp name but chages the file type to jpg

            with Image.open(input_file_path) as img:
                img.save(output_file_path, 'JPEG')
            #convets .bmp to .jpg
    #print("conversion succesful", "\n")

def change_name(root):
    files = os.listdir(root)
    #print("\n", "List of files in the directory:","\n", files, "\n")
    #lists files in given file path
    txt_files = [file for file in files if file.endswith(".txt")]
    #extracts txt files from list
    #print("List of.txt files:","\n", txt_files,"\n")
    if txt_files:
        first_txt_file =txt_files[0]
        with open(os.path.join(root, first_txt_file), 'r') as txt_file:
                first_line = txt_file.readline().strip()
        first_line = first_line.replace('"','')
        first_line = first_line.replace(',','')
        first_line = first_line.replace('_','')
        first_line = first_line.replace(' ','_')
        #print("First line of the .txt file:","\n", first_line,"\n")
    # Pull first line of .txt and assign it to a variable
    jpg_files = [file for file in files if file.endswith(".jpg")]
    #print("List of .jpg files:","\n", jpg_files,"\n")
    # Takes all .jpg from  the file directory and adds them to a list.
    for jpg_file in jpg_files:
        base_name, extension = os.path.splitext(jpg_file)
        new_name = first_line + base_name + extension
        print(jpg_file, "renamed to", new_name, "\n")
        old_path = os.path.join(root, jpg_file)
        new_path = os.path.join(root, new_name)
    # Create new name field that combines first_Line of .txt and name of .jpg
        os.rename(old_path, new_path)
    #renames .jpg



def add_comment_to_jpg( exifTool, root, comment):
#uses Exiftool to add comment to metadata
    exifTool = "/Users/dvitale/exiftool.exe"
    command = [exifTool, "-comment="+comment, root]
    subprocess.run(command)

def comment_choice(exifTool, root):
    #print (os.listdir(root))
    for filename in os.listdir(root):
    # Allows user to pick comment from a list of preset comments or create their own.
    #iterates through all .jpg files in the previously definced file path.
        if filename.lower().endswith(".jpg"):
            preset_1 = "Plot of Horizontal to Vertical Spectral Ratio that plots frequency in Hertz on the x-axis and amplitude (a dimensionless value) on the y-axis.  The resonance frequency is indicated at the top of the plot."
            preset_2 = "Single component spectra plot frequency in Hertz are shown on the x axis and acceleration in mm/s per Hertz are plotted on the y-axis.   The north-south component is green; the east-west component is blue; and up-down (vertical) is pink."
            if 'HVSR' in filename:
                print(filename)
                file_path = os.path.join(root, filename)
                add_comment_to_jpg(exifTool,file_path, preset_1)
                print(f"comment added to {file_path}: {preset_1}")
                print()
            if 'PowSpecTot' in filename:
                print(filename)
                file_path = os.path.join(root, filename)
                add_comment_to_jpg(exifTool,file_path, preset_2)
                print(f"comment added to {file_path}: {preset_2}")
                print()
find_GRILLA_output()


# learn how to export code so others can use it
# Create visual workflow





