# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 10:14:15 2024

@author: nollr
"""

import re

def is_valid_code(code):
    """ Überprüfen, ob der Code dem Format 'HP:0000013' entspricht """
    return re.match(r"HP:\d{7}", code) is not None

def extract_info(document, code):
    pattern = fr"\[Begriff\]\nid: {code}\n(.*?)\n(?=\[Begriff\]|\Z)"
    match = re.search(pattern, document, re.DOTALL)
    if match:
        begriff_abschnitt = match.group(1)

        # Extrahieren des Namens
        name_match = re.search(r"name: ([^\n]+)\n", begriff_abschnitt)
        name = name_match.group(1) if name_match else None

        # Extrahieren und Formatieren der Synonyme
        synonyms = re.findall(r"synonym: \"([^\"]+)\"", begriff_abschnitt)
        formatted_info = set([name])  # Beginnen mit einem Set, das den Namen enthält

        for synonym in synonyms:
            synonym_formatted = synonym.replace(',', '')  # Entfernen von Kommas
            formatted_info.add(synonym_formatted)  # Hinzufügen zum Set, um Duplikate zu vermeiden

        # Entfernen von None und Zusammenfügen der Informationen
        if None in formatted_info:
            formatted_info.remove(None)
        combined_info = ', '.join(formatted_info)
        return combined_info
    return None

# Lesen des Textdokuments (ohne vollständigen Pfad)
document_path = "hp full de.txt"
with open(document_path, 'r', encoding='utf-8') as file:
    document = file.read()

# Eingabeaufforderung für den Nutzer
input_codes = input("Please enter the codes in the format 'HP:0000013' (separated by a comma): ")
codes_list = input_codes.split(',')

# Extrahieren der Informationen und Ausgabe in der Konsole
for code in codes_list:
    code = code.strip()  # Entfernen von Leerzeichen um den Code
    if not is_valid_code(code):
        print(f"Error: '{code}' is not a valid code. Correct format: 'HP:0000013'")
        continue
    combined_info = extract_info(document, code)
    if combined_info:
        print(f"Code: {code}, Name und Synonyms: {combined_info}")
    else:
        print(f"No information found for Code: {code}")

