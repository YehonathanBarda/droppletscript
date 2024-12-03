import os
from dropplet_functions import *

"""
@authors: Lyrie Edler and Yehonathan Barda

This script calculates the contact angle of all the images in the working folder and stores the results in a log file.
The working folder is defined by the WORKING_FOLDER variable and the accepted image formats are defined by the ACCEPTED_IMAGE_FORMATS variable.
The results are stored in the LOG_FILE file.

"""

# Define the working folder and the accepted image formats
WORKING_FOLDER = '.'
ACCEPTED_IMAGE_FORMATS = ['jpeg', 'jpg']

# Create a log file to store the results
LOG_FILE = os.path.join(WORKING_FOLDER,'results.log')

# Open the log file in write mode
log_file = open(LOG_FILE, 'w')
Found_Image = False # Flag to check if any images were found

for file_name in os.listdir(WORKING_FOLDER):
    if file_name.split('.')[-1] in ACCEPTED_IMAGE_FORMATS:
        Found_Image = True
        contact_angle = calculate_contact_angle(os.path.join(WORKING_FOLDER,file_name))
        log_file.write(f"File: {file_name}, Contact Angle: {contact_angle} degrees\n")
        print('\n')

if not Found_Image:
    log_file.write("No images found in the working folder\n")
    print("No images found in the working folder")
else:
    print("Results stored in the {} file".format(LOG_FILE))

# Close the log file
log_file.close()