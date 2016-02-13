#!/usr/bin/env python
import xml.etree.ElementTree as ET
import csv


def main():
    print("building", end="")
    with open('LBRBUILD') as csvfile:
        library = ET.parse('Library.lbr')
        for row in csv.reader(csvfile):
            print(".", end=""),
            name = row[0]
            parts = set(s.strip() for s in row[1:])
            packages = set()
            symbols = set()
            devices = set()
            for device in library.iter('deviceset'):
                if device.get('name').strip() in parts:
                    devices.add(device)
                    symbols |= set(g.get('symbol') for g in device.iter('gate'))
                    packages |= set(d.get('package') for d in device.iter('device'))

            out = ET.parse('Template.lbr')
            
            root = next(out.getroot().iter('devicesets'))
            for device in devices:
                root.append(device)
            
            out.write(name + '.lbr')
            
            lib = library.getroot().iter('package')
            root = next(out.getroot().iter('packages'))
            for package in lib:
                if package.get('name') in packages:
                    root.append(package)
            
            out.write(name + '.lbr')
            
            lib = library.getroot().iter('symbol')
            root = next(out.getroot().iter('symbols'))
            for symbol in lib:
                if symbol.get('name') in symbols:
                    root.append(symbol)

            out.write(name + '.lbr')
    print()

if __name__ == "__main__":
    main()
