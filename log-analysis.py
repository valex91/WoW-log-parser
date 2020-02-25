#!/usr/bin/python3
import argparse
import re

equipMap = dict()
guidMap = dict()

playerGUIDregex = re.compile(r'Player-(\d){4}-(\w){8}')
playerNameRegex = re.compile(r'Player-\d{4}-\w{8},"(\w*-\w*)"')
equipDataRegex = re.compile(r'(\(\d*,\d*,\((\d*,*){0,3}\),\(\d*\),\(\d*\)\))')


def mergeMaps(guidNameMap, equipMap):
    nameAndEquipMap = dict()

    for guid in list(guidNameMap):
        name = guidNameMap.get(guid, None)
        equip = equipMap.get(guid, None)

        nameAndEquipMap[name] = equip
    return nameAndEquipMap


def main(logPath):
    with open(logPath) as f:
        for line in f.readlines():
            guidAndNameMatch = playerNameRegex.search(line)
            if guidAndNameMatch:
                guid, name = guidAndNameMatch.group().split(',')
                if not(guid in guidMap):
                    guidMap[guid] = name

            if line.find('COMBATANT_INFO') > -1:
                playerGUID = playerGUIDregex.search(line).group()

                if playerGUID in equipMap:
                    continue
                equipMap[playerGUID] = equipDataRegex.findall(line)
        f.close()

    print(mergeMaps(guidMap, equipMap))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='extract player info from the log file')
    parser.add_argument('--src', dest='src',
                        help='the path to the log file from')
    args = parser.parse_args()

    main(args.src)
