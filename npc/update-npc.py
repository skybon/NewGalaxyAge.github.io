#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Импорты
import json

## Хелперы
def writeln(file, string):
    file.write(string)
    file.write('\n')

def writelntab(file, string, tabcount):
    file.write(tabcount * '\t')
    file.write(string)
    file.write('\n')

## Инициализация
propertiesList = {
    "point": {
        "weight":   "0b10000",
        "icon":     "/point.png",
        "text":     "Поинты!"
    },
    "neut": {
        "weight":   "0b01000",
        "icon":     "/neut.png",
        "text":     "Нейтрят!"
    },
    "jam": {
        "weight":   "0b00100",
        "icon":     "/jam.png",
        "text":     "Джамят!"
    },
    "dps": {
        "weight":   "0b00010",
        "icon":     "/dps.png",
        "text":     "ДПСят!"
    },
    "web": {
        "weight":   "0b00001",
        "icon":     "/web.png",
        "text":     "Сеткуют!"
    }
}

typeList = {
    "frigate": "Фригаты"
}

lasttype = ''

class Ship:
    def __init__(self, shipname, shiptype, shipweight, properties):
        self.name = shipname
        self.type = shiptype
        self.weight = shipweight
        self.properties = properties
    def __repr__(self):
        return repr((self.name, self.type, self.weight, self.properties))

ships = []

## Погнали!
JSON = json.load(open('data.json'))

for i, val in enumerate(JSON):
    weight = 0
    for v in val['properties']:
        weight += int(propertiesList[v]['weight'], 2)
    ships.append(Ship(val['name'], val['type'], weight, val['properties']))

ships.sort(key=lambda ship: ship.weight, reverse=True)

with open('index.rst', 'w') as f:
    writeln(f, "Описание NPC")
    writeln(f, 12 * '=') # FIXME magic number

for val in ships:
    with open('index.rst', 'a') as f:
        if lasttype != val.type:
            writeln(f, typeList[val.type])
            signcount = len(typeList[val.type]) / 2 # FIXME WTF вообще с Python, почему len() от русской строки удваивается?
            writeln(f, signcount * '-')
            writeln(f, '.. glossary::')
            lasttype = val.type

        writeln(f, '')
        writelntab(f, val.name, 1)

        for v in val.properties:
            writelntab(f, '.. image:: ' + propertiesList[v]['icon'], 2)
            writelntab(f, propertiesList[v]['text'], 2)