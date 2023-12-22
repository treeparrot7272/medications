#!/usr/bin/env python3

import pyperclip
from dealing_with_frequencies import cleaner_function
import pprint

# Read text from clipboard
text_body = pyperclip.paste()


def create_medication_list(med_dict):
    active_message = "Medications:\n"
    prn_message = "PRN Medications:\n"

    for medications in med_dict.keys():
        if med_dict[medications]['regular']:
            for different_doses in range(0, len(med_dict[medications]['regular'])):
                active_message += str(medications).title() + " " + str(med_dict[medications]['regular'][different_doses]) + " " + str(med_dict[medications]['regular_freq'][different_doses]) + "\n"
        if med_dict[medications]['prn']:
            for different_doses in range(0, len(med_dict[medications]['prn'])):
                prn_message += str(medications).title() + " " + str(med_dict[medications]['prn'][different_doses]) + " " + str(med_dict[medications]['prn_freq'][different_doses]) + "\n"
        
        final_message = active_message + "\n\n" + prn_message
    return final_message


# Split the text body into two sections
sections = text_body.split('\n\n')  # assuming there's an empty line between the two sections
med_names = [name.replace('PRN','').strip() for name in sections[0].split('\n') if name.strip()]
med_with_doses = [dose.strip() for dose in sections[1].split('\n') if dose.strip()]
med_with_frequencies = [freq.strip() for freq in sections[2].split('\n') if freq.strip()]
med_dict = {}

for med in med_with_doses:
    # Check if the medication ends with 'PRN'
    is_prn = med.endswith('PRN')

        # Remove 'PRN' from the medication string if present
    if is_prn:
        med = med.replace('PRN', '').strip()


    # Extract name and dose
    parts = med.split()
    name = ' '.join(parts[:-2])  # Everything except the last two words (dose and unit)
    dose = ' '.join(parts[-2:]).replace('unit(s)', 'U').replace('microgram(s)', 'mcg')  # Last two words (dose and unit)

    # Initialize dictionary structure for new medications
    if name not in med_dict:
        med_dict[name] = {"regular": [], "prn": [], "regular_freq": [], "prn_freq": []}
    # Add dose to the appropriate list
    if is_prn:
        #if dose not in med_dict[name]["prn"]:
            med_dict[name]["prn"].append(dose)
    else:
        #if dose not in med_dict[name]["regular"]:
            med_dict[name]["regular"].append(dose)


med_dict = cleaner_function(med_dict, med_with_frequencies)


final_dict = {name: med_dict[name] for name in med_names if name in med_dict}

pprint.pprint(final_dict)
#print(create_medication_list(final_dict))
pyperclip.copy(create_medication_list(final_dict))



