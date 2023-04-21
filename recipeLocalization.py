import os


def loadLocalization(file_path, file_name):
    localization_dict = {}

    localization_file = os.path.join(file_path, file_name)

    with open(localization_file, 'r', encoding='utf-8') as lf: 

        for line in lf:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            if ':' not in line:
                # error if a line does not have exactly one colon
                raise ValueError(f"Invalid line in {localization_file}: {line}")
            key, value = line.split(':', 1)
            localization_dict[key.strip()] = value.strip()

    return localization_dict

