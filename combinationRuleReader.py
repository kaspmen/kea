import os
import yaml
import ast
from recipeLocalization import loadLocalization
from tester import convert_hexastring

### input localization language as needed
language = "Danish"

amase_localization_path = f"C:/Users/KM/Desktop/SGI/AMASE/Localization/{language}/Text"
localizationFile = os.path.join(amase_localization_path, "Strings_Materials.txt")

amase_base_path = "C:/Users/KM/Desktop/SGI/AMASE"
recipesLookup = os.path.join(amase_base_path, "recipesLookup.yaml")
baseMaterials = os.path.join(amase_base_path, "baseMaterials.yaml")

combinationRulesList = []
toolInteractionRulesList = []
seperationRulesList = []

materialDict = {}

# load a dict of baseMaterials.yaml
with open(baseMaterials) as materials:
    baseMaterialsData = yaml.load(materials, Loader=yaml.FullLoader)

    for key, value in baseMaterialsData.items():
        materialDict[int(key)] = value


with open(recipesLookup) as recipes:
    recipes = yaml.load(recipes, Loader=yaml.FullLoader)

    localizationData = loadLocalization(amase_localization_path, localizationFile)
    idMaterials = convert_hexastring(recipesLookup, baseMaterials, 'ruleSet', 'combinationRules')
 

    for rule in recipes['recipes']:

        localized_names = [localizationData.get(str(materialDict[mat]), str(mat)) for mat in idMaterials]
    
        combinationRuleObj = {
            'name': rule['name'],
            'localized_names' : localized_names,
        }
        combinationRulesList.append(combinationRuleObj)


if __name__ == "__main__":

    n = 0
    
    for rule in combinationRulesList:

        n += 1
        print(f"{n}{rule}\n")

