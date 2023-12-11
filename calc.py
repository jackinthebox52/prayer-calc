import requests
import math
import argparse

_supported_bones = {
    536: ['Dragon bones', 252],
    6812: ['Wyvern bones', 252],
    534: ['Babydragon bones', 105],
    3125: ['Jogre bones', 52.5],
    22780: ['Wyrm bones', 175],
    22783: ['Drake bones', 280],
    11943: ['Lava dragon bones', 297.5],
    6729: ['Dagannoth bones', 437.5],
    22786: ['Hydra bones', 385],
    4834: ['Ourg bones', 490],
    22124: ['Superior {dragon} bones', 525]
}


'''Takes in a string and returns the bone id if it is a supported bone, returns nil otherwise'''
def compareBones(name):
    for b_id, b_name in _supported_bones.items():
        b_name = b_name[0].lower().replace(' bones', '')
        if b_name in name.lower():
            return b_id
    return None # If no bone is found

'''Takes in level 1-99 and returns the experience required to reach that level.
    Formula taken from https://oldschool.runescape.wiki/w/Experience'''
def experienceTilLevel(level):
    total = 0
    for i in range(1, level):
        total += math.floor(i + 300 * pow(2, i / 7.0))
    return math.floor(total / 4)

'''Prints all supported bones.'''
def printBones():
    print('Supported bones: ', end='')
    for index, b_name in enumerate(_supported_bones.values()):
        print(b_name[0].lower().replace(' bones', ''), end='')
        if index < len(_supported_bones) - 1:   print(', ', end='')
        else:   print('.')
    return

'''Prints the help message'''
def printHelp():
    print('''
    Commands:
    -h : Displays this message
    -b : Displays supported bones
    [bone] [level] : Calculates the number of bones needed to reach the given level

    [bone] should not include the word 'bones' and is not case sensitive

    Example Usage: /bin/bash prayercalc dragon 99 
    ''')
    return


def parse_arguments():
    parser = argparse.ArgumentParser(description='Prayer Calculator')
    parser.add_argument('bone', type=str, help='The type of bone (e.g. dragon)')
    parser.add_argument('level', type=int, help='The target level (1-99)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    bone = args.bone.lower()
    level = args.level

    url = "https://prices.runescape.wiki/api/v1/osrs/latest"
    response = requests.get(url)
    data = response.json()['data']

    if bone == '-h':
        printHelp()
    elif bone == '-b':
        printBones()
    else:
        bone_id = compareBones(bone)
        if bone_id is None:
            print('Invalid bone type. Use -b to see supported bones:')
            printBones()
            print()
            print("[TIP]: use 'superior' for superior dragon bones")
            
        elif level < 1 or level > 99:
            print('Invalid level. Level must be between 1 and 99.')
        else:
            # Calculate the number of bones needed
            price = data[str(bone_id)]['high'] # Get the price of the bone
            xp_per = _supported_bones[bone_id][1]
            needed = math.ceil(experienceTilLevel(level) / xp_per)
            print(f'Number of {bone} bones needed to reach level {level}: {needed:,}')
            print(f'Cost: {(price*needed):,} gp at {price:,} gp per bone')

if __name__ == '__main__':
    parse_arguments()
    main()
