import os
import yaml
import ast
from recipeLocalization import loadLocalization
from converter import conv_hex_to_dec


# input localization language as needed
language = "Danish"

amase_localization_path = f"C:/Users/Pedersen/OneDrive/Skrivebord/SGI/amase-recipes/amase-recipes/Localization/{language}/Text"
localizationFileMaterials = os.path.join(amase_localization_path, "Strings_Materials.txt")
localizationFileTools = os.path.join(amase_localization_path, "Strings_Tools.txt")

amase_base_path = "C:/Users/Pedersen/OneDrive/Skrivebord/SGI/amase-recipes/amase-recipes"
recipesLookup = os.path.join(amase_base_path, "recipesLookup.yaml")
baseMaterials = os.path.join(amase_base_path, "baseMaterials.yaml")
interactionTools = os.path.join(amase_base_path, "interactionTools.yaml")

combinationRulesList = []
toolInteractionRulesList = []
seperationRulesList = []

materialDict = {}
toolDict = {}

# load a dict of baseMaterials.yaml
with open(baseMaterials) as materials:
    baseMaterialsData = yaml.load(materials, Loader=yaml.FullLoader)

    for key, value in baseMaterialsData.items():
        materialDict[int(key)] = value


# load a dict of interactionTools.yaml
with open(interactionTools) as tools:
    interactionToolsData = yaml.load(tools, Loader=yaml.FullLoader)

    for key, value in interactionToolsData.items():
        toolDict[int(key)] = value


with open(recipesLookup) as recipes:
    recipes = yaml.load(recipes, Loader=yaml.FullLoader)

    localizationData = loadLocalization(amase_localization_path, localizationFileMaterials)
    localizationToolData = loadLocalization(amase_localization_path, localizationFileTools)

 
    with open("output.txt", "w") as outfile:
        for recipe in recipes['recipes']:

            recipeResult = recipe['name']
            allowedMaterials = recipe['allowedMaterials']

            # slice the allowedMaterials into 2 character chunks so they can be translated to their corresponding strings in baseMaterials.yaml
            allowedMaterials_chunks = str([allowedMaterials[i:i+8][:2] for i in range(0, len(allowedMaterials), 8)])

            # convert hexadecimal to decimal so the id of the material can be used
            idMaterials = [int(hex_num, 16) for hex_num in ast.literal_eval(allowedMaterials_chunks)]

            # get the localized names for the recipes and the recipe components
            localized_material = [localizationData.get(str(materialDict[mat]), str(mat)) for mat in idMaterials]

            localized_recipe_result = localizationData.get(recipeResult)

            recipeObj = {
                'key': recipeResult,
                'localized_key' : localized_recipe_result,
                'materialId': [{mat: materialDict[mat]} for mat in idMaterials],
                'localized_material_Id': localized_material,
                'combinationRules': [],
                'toolInteractionRules' : [],
                'seperationRules' : []
            }



            ### Combintaion Rules ####
            for rule in recipe['ruleSet']['combinationRules']:

                combinationRule = rule['name']
                sourceMaterials = rule['sourceMaterials']
                resultingMaterials = rule['resultingMaterials']


                conv_resultingMaterials = conv_hex_to_dec(resultingMaterials)
                localized_resultingMaterials = [localizationData.get(str(materialDict[mat]), str(mat)) for mat in conv_resultingMaterials]

                conv_sourceMaterials = conv_hex_to_dec(sourceMaterials)
                localized_ingredients = [localizationData.get(str(materialDict[mat]), str(mat)) for mat in conv_sourceMaterials]

                
                combinationRuleObj = {
                    'key': combinationRule,
                    'localized_key' : localized_resultingMaterials,
                    'localized_combination_materials' : localized_ingredients
                }
                recipeObj['combinationRules'].append(combinationRuleObj)
            

            ### Tool Interaction Rules ###
            for rule in recipe['ruleSet']['toolInteractionRules']:

                toolInteractionRule = rule['name']
                toolSourceMaterials = rule['sourceMaterials']
                toolResultingMaterials = rule['resultingMaterials']
                toolType = rule['toolType']

                localizedTool = interactionToolsData.get(toolType)

                conv_toolResultingMaterials = conv_hex_to_dec(toolResultingMaterials)
                localized_toolResultingMaterials = [localizationData.get(str(materialDict[mat]), str(mat)) for mat in conv_toolResultingMaterials]

                conv_toolSourceMaterials = conv_hex_to_dec(toolSourceMaterials)
                localized_toolIngredients = [localizationData.get(str(materialDict[mat]), str(mat)) for mat in conv_toolSourceMaterials]


                toolInteractionRuleObj = {
                    'key': toolInteractionRule,
                    'localized_key' : localized_toolResultingMaterials,
                    'sourceMaterials': localized_toolIngredients,
                    'toolType': toolType,
                    'localizedTool' : localizedTool,
                    'conditional' : rule['conditional'],
                    'conditionalvalue' : rule['conditionalValue']
                }
                recipeObj['toolInteractionRules'].append(toolInteractionRuleObj)


            ### Seperation Interaction Rules ###
            for rule in recipe['ruleSet']['seperationRules']:

                seperationRule = rule['name']
                seperationToolType = rule['toolType']
                seperationSourceMaterials = rule['sourceMaterials']
                seperationResultingMaterials = rule['resultingMaterials']
                toolType = rule['toolType']

                localizedTool = interactionToolsData.get(toolType)                

                conv_seperationResultingMaterials = conv_hex_to_dec(seperationResultingMaterials)
                localized_seperationResultingMaterials = [localizationData.get(str(materialDict[mat]), str(mat)) for mat in conv_seperationResultingMaterials]

                conv_seperationSourceMaterials = conv_hex_to_dec(seperationSourceMaterials)
                localized_seperationIngredients = [localizationData.get(str(materialDict[mat]), str(mat)) for mat in conv_seperationSourceMaterials]

                seperationRuleObj = {
                    'key': seperationRule,
                    'localized_key': localized_seperationResultingMaterials,
                    'toolType': seperationToolType,
                    'localizedTool':localizedTool,
                    'sourceMaterials': localized_seperationIngredients,
                }
                recipeObj['seperationRules'].append(seperationRuleObj)



            print(f"{recipeObj}\n")
            outfile.write(f"\n{recipeObj}\n")
            outfile.close
