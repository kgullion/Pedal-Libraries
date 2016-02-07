import xml.etree.ElementTree as ET
import csv


def main():
    with open('LBRBUILD') as csvfile:
        library = ET.parse('Library.lbr')
        for row in csv.reader(csvfile):
            name = row[0]
            parts = set(row[1:])
            packages = set()
            symbols = set()
            devices = set()
            for device in library.iter('deviceset'):
                if device.get('name') in parts:
                    devices.add(device)
                    symbols |= set(g.get('symbol') for g in device.iter('gate'))
                    packages |= set(d.get('package') for d in device.iter('device'))

            out = ET.parse('Template.lbr')

            root = out.getroot().iter('devicesets')
            for device in devices:
                root.append(device)

            lib = library.getroot().iter('package')
            root = out.getroot().iter('packages')
            for package in lib:
                if package.get('name') in symbols:
                    root.append(package)

            lib = library.getroot().iter('symbol')
            root = out.getroot().iter('symbols')
            for symbol in lib:
                if symbol.get('name') in symbols:
                    root.append(symbol)

            out.write(name + '.lbr')

if __name__ == "__main__":
    main()
