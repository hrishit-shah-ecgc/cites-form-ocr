import os
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential
import time

import pandas as pd

species_data_headings = ['Scientific Name', 'Common Name', 'AppendixSource','Quantity', 'Description', 'OriginCountry', 
                         'OriginPermit', 'OriginDate', 'ReExportCountry', 'ReExportPermit', 'ReExportDate']


temp_dict = {
    'Scientific Name-1': '',
    'Common Name-1': '',
    'AppendixSource-1': '',
    'Description-1': '',
    'Quantity-1': '',
    'OriginCountry-1': '',
    'OriginPermit-1': '',
    'OriginDate-1': '',
    'ReExportCountry-1': '',
    'ReExportPermit-1': '',
    'ReExportDate-1': '',
    'Scientific Name-2': '',
    'Common Name-2': '',
    'AppendixSource-2': '',
    'Description-2': '',
    'Quantity-2': '',
    'OriginCountry-2': '',
    'OriginPermit-2': '',
    'OriginDate-2': '',
    'ReExportCountry-2': '',
    'ReExportPermit-2': '',
    'ReExportDate-2': '',
}


permit_data = {
    'Export Permit': '',
    'ReExport Permit': '',
    'Other': '',
    'Permittee': '',
    'Consingee': '',
    'Purpose': '',
    'Original Permit Number': '',
    'Original Valid Until': '',
    'Original Date Of Issue': ''
    
}

species_list = []
output_data = []
all_data = []

def validate_data(extracted_string):
    if extracted_string is not None and '*' in extracted_string:
        value = None
    else: 
        value = extracted_string
    return value

def analyze_with_model(file_path):
    endpoint = ""
    key = ""

    form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
    model_id = ""

    with open(file_path, "rb") as fd:
        form = fd.read()

    poller = form_recognizer_client.begin_recognize_custom_forms(model_id=model_id, form=form)
    result = poller.result()
    return result

def organize_data():
    length = len([i for i, x in enumerate(species_list) if  "Common Name" in x])

    scienceName = [i for i, x in enumerate(species_list) if  "Scientific Name" in x]
    commonName = [i for i, x in enumerate(species_list) if  "Common Name" in x]
    appendix = [i for i, x in enumerate(species_list) if  "AppendixSource" in x]
    desc = [i for i, x in enumerate(species_list) if  "Description" in x]
    quantity = [i for i, x in enumerate(species_list) if  "Quantity" in x]
    countryOrigin = [i for i, x in enumerate(species_list) if  "OriginCountry" in x]
    originPermit = [i for i, x in enumerate(species_list) if  "OriginPermit" in x]
    originDate = [i for i, x in enumerate(species_list) if  "OriginDate" in x]
    countryReexport = [i for i, x in enumerate(species_list) if  "ReExportCountry" in x]
    reexportPermit = [i for i, x in enumerate(species_list) if  "ReExportPermit" in x]
    reexportDate = [i for i, x in enumerate(species_list) if  "ReExportDate" in x]

    for x in range(len(species_list)):
        species_list[x] = species_list[x].split('@')[1]

    print(len(quantity), len(countryOrigin), len(originPermit), len(originDate), len(countryReexport), len(reexportPermit))
    

    for x in range(2):
        output_data.append([species_list[scienceName[x]], species_list[commonName[x]], species_list[appendix[x]], species_list[desc[x]],
        species_list[quantity[x]], species_list[countryOrigin[x]], species_list[originPermit[x]], species_list[originDate[x]], species_list[countryReexport[x]], species_list[reexportPermit[x]],
        species_list[reexportDate[x]]])
    
    for x in range(len(output_data)):
        output_data[x] = list(permit_data.values()) + output_data[x]
    all_data.extend(output_data)

def write_to_excel(name):
    print(all_data)
    df = pd.DataFrame(all_data, columns = list(permit_data.keys()) + species_data_headings) 
    df.to_csv(name, index=False)

def main(files, output):
    all_data.clear()
    for file in files:
        for recognized_form in analyze_with_model(file):
            for name, field in recognized_form.fields.items():

                if name in list(permit_data.keys()):
                    permit_data[name] = field.value
                else:
                    temp_dict[name] = field.value
                
            n = 11
            print(temp_dict)
            temp_list = [list(temp_dict.values())[i:i+n] for i in range(0, len(list(temp_dict.values())), n)]
            print(temp_list)
            for l in temp_list:
                print(len(l))
                print(len(species_data_headings))
                if (l[0]) is not None:
                    for x in range(len(species_data_headings)):
                        species_list.append(species_data_headings[x] + '@' + str(l[x]))
            print(species_list)
            organize_data()
            output_data.clear()
            species_list.clear()
    write_to_excel(output)


