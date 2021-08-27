# CITES OCR

This project is a website which takes in input pdfs and runs them through an Azure form recognizer model. It will then take the results and output it in a .CSV file with each line representing a species in a permit

It has: 

 - Ability to select a folder for the input files
 - Ability to select a folder and name for the output .csv
 - Select country of permit 
 - Have it so the program can run indefinitely with intervals of repeat
 - Store the already analyzed files

# Basic Instructions 

 1. The webapp initially on the main screen where the user has to select the country and input/output locations
 2. The user can then select if they want to run the OCR once or multiple times. 
	 3. If it is run multiple times then the program will look at already existing files


# Installation

This program uses **Python and Flask** as the backend with **jinja2 templates** containing HTML and CSS in the frontend. There are various dependencies that need to be installed in order to use this program. They are listed in the **requirements.txt** file

## Running Locally
This program can be run locally using the command: `python app.py`
This will open a localhost:5000 in the browser window

# Azure
This program relies on the Microsoft Azure form recognizer service to be able to perform OCR and extract key value pairs. With each country's permit there needs to be an (endpoint and key) to access Azure Cognitive Services as well as, a model ID which represents the model of the specific country's permits.

Further documentation can be found: https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/
Visual Labelling: https://fott-preview.azurewebsites.net/
