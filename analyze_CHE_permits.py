import os
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential

import pandas as pd

species_data_headings = ['Scientific Name', 'Common Name', 'Appendix', 'Source', 'Purpose', 'Description', 'Quantity', 'Country of Origin', 
                         'Origin Permit Number', 'Origin Date', 'Country of ReExport', 'ReExport Permit Number', 'ReExport Date']


temp_dict = {
    'Scientific Name-1': '',
    'Common Name-1': '',
    'Appendix-1': '',
    'Source-1': '',
    'Purpose-1': '',
    'Description-1': '',
    'Quantity-1': '',
    'Country of Origin-1': '',
    'Origin Permit Number-1': '',
    'Origin Date-1': '',
    'Country of ReExport-1': '',
    'ReExport Permit Number-1': '',
    'ReExport Date-1': '',
    'Scientific Name-2': '',
    'Common Name-2': '',
    'Appendix-2': '',
    'Source-2': '',
    'Purpose-2': '',
    'Description-2': '',
    'Quantity-2': '',
    'Country of Origin-2': '',
    'Origin Permit Number-2': '',
    'Origin Date-2': '',
    'Country of ReExport-2': '',
    'ReExport Permit Number-2': '',
    'ReExport Date-2': '',
    'Scientific Name-3': '',
    'Common Name-3': '',
    'Appendix-3': '',
    'Source-3': '',
    'Purpose-3': '',
    'Description-3': '',
    'Quantity-3': '',
    'Country of Origin-3': '',
    'Origin Permit Number-3': '',
    'Origin Date-3': '',
    'Country of ReExport-3': '',
    'ReExport Permit Number-3': '',
    'ReExport Date-3': ''
}


permit_data = {
    'Export Permit': '',
    'ReExport Permit': '',
    'Other': '',
    'Country of Import': '',
    'Country of Export or ReExport': '',
    'Name and Address of Importer': '',
    'Name and Address of Exporter': '',
    'Permit Number': '',
    'Permit Date of Issue': '',
    'Permit Expiry Date': ''
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
    appendix = [i for i, x in enumerate(species_list) if  "Appendix" in x]
    source = [i for i, x in enumerate(species_list) if  "Source" in x]
    purpose = [i for i, x in enumerate(species_list) if  "Purpose" in x]
    desc = [i for i, x in enumerate(species_list) if  "Description" in x]
    quantity = [i for i, x in enumerate(species_list) if  "Quantity" in x]
    countryOrigin = [i for i, x in enumerate(species_list) if  "Country of Origin" in x]
    originPermit = [i for i, x in enumerate(species_list) if  "Origin Permit Number" in x]
    originDate = [i for i, x in enumerate(species_list) if  "Origin Date" in x]
    countryReexport = [i for i, x in enumerate(species_list) if  "Country of ReExport" in x]
    reexportPermit = [i for i, x in enumerate(species_list) if  "ReExport Permit Number" in x]
    reexportDate = [i for i, x in enumerate(species_list) if  "ReExport Date" in x]

    for x in range(len(species_list)):
        species_list[x] = species_list[x].split('@')[1]
    

    for x in range(length):
        output_data.append([species_list[scienceName[x]], species_list[commonName[x]], species_list[appendix[x]], species_list[source[x]], species_list[purpose[x]], species_list[desc[x]],
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
                value = validate_data(field.value)

                if name in list(permit_data.keys()):
                    permit_data[name] = value
                else:
                    temp_dict[name] = value
                
            n = 13
            temp_list = [list(temp_dict.values())[i:i+n] for i in range(0, len(list(temp_dict.values())), n)]
            for l in temp_list:
                if (l[0]) is not None:
                    for x in range(len(species_data_headings)):
                        species_list.append(species_data_headings[x] + '@' + str(l[x]))
            organize_data()
            output_data.clear()
            species_list.clear()
    write_to_excel(output)
