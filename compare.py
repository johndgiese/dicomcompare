import sys
import csv
from collections import OrderedDict

import dicom

ignored_attributes = 'PixelData'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('USAGE: python compare.py OUT IN1 [IN2 ...]')
        sys.exit(1)

    all_keys = set()
    for fn in sys.argv[2:]:
        dataset = dicom.read_file(fn)
        all_keys.update(dataset.dir())

    sorted_keys = sorted(all_keys)

    attributes = OrderedDict((k, []) for k in sorted_keys)
    for fn in sys.argv[2:]:
        dataset = dicom.read_file(fn)
        for k in all_keys:
            if hasattr(dataset, k):
                attributes[k].append(str(getattr(dataset, k)))
            else:
                attributes[k].append('')

    headers = ['DICOM Attribute'] + sys.argv[2:]

    with open(sys.argv[1], 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for attribute_name, values in attributes.items():
            if not attribute_name in ignored_attributes:
                writer.writerow([attribute_name] + values)
