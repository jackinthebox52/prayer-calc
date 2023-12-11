import requests
import math

_supported_bones = {
    536: 'Dragon bones',
    6812: 'Wyvern bones',
    534: 'Babydragon bones',
    3125: 'Jorgre bones',
    22780: 'Wyrm bones',
    22783: 'Drake bones',
    11943: 'Lava dragon bones',
    6729: 'Dagannoth bones',
    22786: 'Hydra bones',
    4834: 'Ourg bones',
    22124: 'Superior dragon bones'
}


'''Takes in a string and returns the bone id if it is a supported bone, returns nil otherwise'''
def compareBones(name):
    for b_id, b_name in _supported_bones.items():
        b_name = b_name.lower().replace(' bones', '')
        if b_name in name.lower():
            return b_id
    return nil # If no bone is found

def experienceTillLevel(level):
    total = 0
    for i in range(1, level):
        total += math.floor(i + 300 * pow(2, i / 7.0))
    return math.floor(total / 4)


def main():
    url = "https://prices.runescape.wiki/api/v1/osrs/latest"
    response = requests.get(url)
    data = response.json()['data']
    for item in data:
        if int(item) in _supported_bones.keys():
            print(item)
    return

def printBones():
    print('Supported bones: ', end='')
    for index, b_name in enumerate(_supported_bones.values()):
        print(b_name.lower().replace(' bones', ''), end='')
        if index < len(_supported_bones) - 1:   print(', ', end='')
        else:   print('.')
    return


if __name__ == '__main__':
    printBones()