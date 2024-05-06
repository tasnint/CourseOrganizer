# course-organizer
The Course Organizer

This Python script is designed to automate the process of organizing course-related files by copying files from a specified source directory (Downloads) to dynamically created directories based on course codes. The program interacts with the user to get a course code, creates a course-specific folder on the user's desktop, and then schedules tasks to regularly check for and copy files containing the course code in their names from the Downloads folder to a date-stamped subdirectory within the course-specific folder. This setup helps in managing course materials by segregating them into clearly organized folders.

How to Run the Program Requirements Python: 
The script requires Python 3 to run.
You can download and install it from python.org. 
schedule Library: 
This Python script uses the schedule library for scheduling tasks. You need to install this library using pip. 
Setup Install Python: 
Download and install Python 3 from the official Python website. Ensure Python and pip are correctly installed by running python3 --version and pip3 --version in your terminal. 
Install Dependencies: 
Open your terminal and install the required schedule library using pip: 
pip3 install schedule 
Prepare the Script Download the Script: Clone the repository or download the script file to your local machine. 
If the repository is on GitHub, you can clone it with:
git clone https://github.com/tasnint/course-organizer.git 
Navigate to the directory containing the script: 
cd path/to/your/script 
Run the Script: Execute the script using Python 3. From the directory where your script is located, run: 
python3 your_script_name.py 
Follow the on-screen prompts to enter the course code for which you want to organize files.
Usage Notes User Interaction: 
The script will prompt you to enter a course code. After entering a valid code, the script starts monitoring the specified Downloads directory and copies files containing the course code into a date-stamped directory within the course-specific folder on your desktop. Automation: The script will continue to run and monitor the directory until you manually stop it with Ctrl + C or close the terminal. Stopping the Script Terminate the Script: You can stop the script by pressing Ctrl + C in the terminal where the script is running. Additional Information Configuring Paths: You might need to adjust the paths specified in the script (source_dir and destination_dir) based on your operating system and file system structure, the code provided is comptabile with a Linux CLI. Scheduling: The script is set to check for new files every minute. You can adjust this frequency by modifying the schedule function call within the script.
