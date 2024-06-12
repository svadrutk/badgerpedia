import re

def extract_classes(text, departments_list):
    # Join departments list into a regex pattern
    departments_pattern = '|'.join(departments_list)

    # Build a pattern to find class names like MATH 320 or 340
    class_pattern = r'(?:\b(?:' + departments_pattern + r')\s+\d{3}[A-Z]?(?:/[A-Z&\s-]+)*|\d{3}[A-Z]?)'

    # Build a pattern to find groups of classes within parentheses
    pattern = r'\((?:' + class_pattern + r'(?:\s*,\s*' + class_pattern + r')*\s*(?:or\s+' + class_pattern + r'(?:\s*,\s*' + class_pattern + r')*)*)\)'

    matches = re.findall(pattern, text)

    extracted_classes = []
    last_department = None

    for match in matches:
        classes = re.findall(class_pattern, match)
        classes_with_departments = []

        for class_name in classes:
            if not re.match(r'\d{3}[A-Z]?', class_name):
                last_department = class_name.split()[0]
            else:
                class_name = last_department + ' ' + class_name

            classes_with_departments.append(class_name)

        extracted_classes.append(classes_with_departments)

    return extracted_classes

# Example usage:
departmentsList = [
    "ACCT I S", "ACT SCI", "AFROAMER", "AFRICAN", "A A E", "AGROECOL", "AGRONOMY", "A F AERO", "AMER IND", "ANATOMY",
    "ANAT&PHY", "ANESTHES", "AN SCI", "ANTHRO", "ABT", "ART", "ART ED", "ART HIST", "ASIAN AM", "ASIAN", "ASIALANG",
    "ASTRON", "ATM OCN", "BIOCHEM", "BSE", "BIOLOGY", "BIOCORE", "B M E", "BIOMDSCI", "BMOLCHEM", "B M I", "BOTANY",
    "CRB", "CBE", "CHEM", "CHICLA", "CIV ENGR", "CSCS", "CLASSICS", "CNP", "COM ARTS", "CS&D", "C&E SOC", "COMP BIO",
    "COMP LIT", "COMP SCI", "CNSR SCI", "COUN PSY", "CURRIC", "DY SCI", "DANCE", "DERM", "DS", "ECON", "ELPA", "ED POL",
    "ED PSYCH", "E C E", "EMER MED", "E M A", "E P", "E P D", "ESL", "ENGL", "ENTOM", "ENVIR ST", "FAM MED", "FISC",
    "FINANCE", "FOLKLORE", "FOOD SCI", "F&W ECOL", "FRENCH", "GEN&WS", "GEN BUS", "GENECSLR", "GENETICS", "GEOG",
    "G L E", "GEOSCI", "GERMAN", "GNS", "GREEK", "HEBR-BIB", "HEBR-MOD", "HISTORY", "HIST SCI", "HORT", "HDFS", "H ONCOL",
    "I SY E", "INFO SYS", "INTEGART", "ILS", "INTEGSCI", "INTER-AG", "INTEREGR", "INTER-LS", "INTER-HE", "STDYABRD",
    "INTL BUS", "INTL ST", "ITALIAN", "JEWISH", "JOURN", "KINES", "LAND ARC", "LACIS", "LATIN", "LAW", "LEGAL ST", "L I S",
    "LSC", "LINGUIS", "LITTRANS", "M H R", "MARKETNG", "M S & E", "MATH", "M E", "MD GENET", "M M & I", "MED PHYS",
    "MED SC-M", "MED SC-V", "MEDICINE", "MEDIEVAL", "MICROBIO", "M&ENVTOX", "MOL BIOL", "MUSIC", "MUS PERF", "NAV SCI",
    "NEURSURG", "NEUROL", "NEURODPT", "NTP", "N E", "NURSING", "NUTR SCI", "OBS&GYN", "OCC THER", "ONCOLOGY", "OTM",
    "OPHTHALM", "PATH-BIO", "PATH", "PEDIAT", "PHM SCI", "PHMCOL-M", "PHARMACY", "PHM PRAC", "PHILOS", "PHY THER",
    "PHY ASST", "PHYSICS", "PHYSIOL", "PL PATH", "PLANTSCI", "POLI SCI", "POP HLTH", "PORTUG", "PSYCHIAT", "PSYCH",
    "PUB AFFR", "PUBLHLTH", "RADIOL", "REAL EST", "RHAB MED", "RP & SE", "RELIG ST", "R M I", "SCAND ST", "STS", "SR MED",
    "SLAVIC", "SOC WORK", "SOC", "SOIL SCI", "SPANISH", "STAT", "SURGERY", "SURG SCI", "THEATRE", "URB R PL", "ZOOLOGY"
]

text1 = "E C E/COMP SCI 354 and (COMP SCI 367 or 400) or graduate/professional standing or declared in the Capstone Certificate in Computer Sciences for Professionals"
text2 = "(MATH 320 or 340) and (STAT 511, 541, POP HLTH/B M I 551, STAT 324, 371, or STAT/F&W ECOL/HORT 571)) or graduate/professional standing"
text3 = "(MATH/COMP SCI 240 or STAT/COMP SCI/MATH 475) and (COMP SCI 367 or 400), or graduate/professional standing, or declared in the Capstone Certificate in Computer Sciences for Professionals"

print(extract_classes(text1, departmentsList))
print(extract_classes(text2, departmentsList))
print(extract_classes(text3, departmentsList))
