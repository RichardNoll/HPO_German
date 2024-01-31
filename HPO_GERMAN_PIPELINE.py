# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 10:14:15 2024

@author: nollr
"""

import re

def is_valid_code(code):
    """ Überprüfen, ob der Code dem Format 'HP:0000013' entspricht """
    return re.match(r"HP:\d{7}", code) is not None

def extract_info(document, code, include_def):
    pattern = fr"\[Begriff\]\nid: {code}\n(.*?)\n(?=\[Begriff\]|\Z)"
    match = re.search(pattern, document, re.DOTALL)
    if match:
        begriff_abschnitt = match.group(1)

        # Extrahieren des Namens
        name_match = re.search(r"name: ([^\n]+)\n", begriff_abschnitt, re.IGNORECASE)
        name = name_match.group(1) if name_match else None

        # Extrahieren und Formatieren der Synonyme
        synonyms = re.findall(r"synonym: \"([^\"]+)\"", begriff_abschnitt)
        formatted_info = set([name])  # Beginnen mit einem Set, das den Namen enthält

        for synonym in synonyms:
            formatted_info.add(synonym)  # Hinzufügen zum Set, um Duplikate zu vermeiden

        # Entfernen von None und Zusammenfügen der Informationen
        if None in formatted_info:
            formatted_info.remove(None)
        combined_info = ', '.join(formatted_info)

        # Extrahieren der Definition, falls gewünscht
        if include_def:
            def_match = re.search(r"def: \"([^\"]+)\"", begriff_abschnitt)
            definition = def_match.group(1) if def_match else "No definition found"
            combined_info += f" - Definition: {definition}"

        return combined_info
    return None


    
def find_code_by_name_or_synonym(document, search_term):
    """ Findet den Code basierend auf einem gegebenen Namen oder Synonym. """
    pattern = fr"\[Begriff\]\nid: (HP:\d{{7}})\n(.*?)(?=\[Begriff\]|\Z)"
    for match in re.finditer(pattern, document, re.DOTALL | re.IGNORECASE):
        code, begriff_abschnitt = match.groups()
        name_match = re.search(r"name: ([^\n]+)\n", begriff_abschnitt, re.IGNORECASE)
        synonyms = re.findall(r"synonym: \"([^\"]+)\"", begriff_abschnitt, re.IGNORECASE)

        if name_match and search_term.lower() == name_match.group(1).lower():
            return code
        if any(synonym.lower() == search_term.lower() for synonym in synonyms):
            return code
    return None

# Lesen des Textdokuments (ohne vollständigen Pfad)
document_path = "hp full de.txt"
with open(document_path, 'r', encoding='utf-8') as file:
    document = file.read()

# Eingabeaufforderung für den Nutzer
search_type = input("Would you like to search for a code or  a name ? (code/name): ").lower()


if search_type == 'code':
    # Eingabeaufforderungen für den Nutzer
    input_codes = input("Please enter the codes in the format 'HP:0000013' (separated by commas): ")
    codes_list = input_codes.split(',')
    include_def_input = input("Do you want to include definitions? (yes/no): ")
    include_def = include_def_input.strip().lower() == 'yes'

    # Extrahieren der Informationen und Ausgabe in der Konsole
    for code in codes_list:
        code = code.strip()  # Entfernen von Leerzeichen um den Code
        if not is_valid_code(code):
            print(f"Error: '{code}' is not a valid code. Correct format: 'HP:0000013'")
            continue
        combined_info = extract_info(document, code, include_def)
        if combined_info:
            print(f"Code: {code}, Name and Synonyms: {combined_info}")
        else:
            print(f"No information found for Code: {code}")
# Hier den Code für die Code-Suche einfügen
elif search_type in ['name']:
    search_term = input("Please enter a German name or synonym: ")

    code = find_code_by_name_or_synonym(document, search_term)
    if code:
        print(f"Zu '{search_term}' found Code: {code}")
    else:
        print(f"'{search_term}' was not found.")
        
        