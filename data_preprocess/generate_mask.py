#!/usr/bin/env python

'''
Generate Column and Table masks from Marmot Data
'''

import xml.etree.ElementTree as ET
import os
import click
import numpy as np
from PIL import Image


def sameTable(ymin_1, ymin_2, ymax_1, ymax_2):
    '''Check if columns belong to same table or not'''
    min_diff = abs(ymin_1 - ymin_2)
    max_diff = abs(ymax_1 - ymax_2)

    if min_diff <= 5 and max_diff <= 5:
        return True
    elif min_diff <= 4 and max_diff <= 7:
        return True
    elif min_diff <= 7 and max_diff <= 4:
        return True

    return False


def generate_masks(xml_file, table_mask_file, column_mask_file):
    # Parse xml file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find('size')

    # Parse dimensions
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    # Create grayscale image array
    col_mask = np.zeros((height, width), dtype=np.int32)
    table_mask = np.zeros((height, width), dtype=np.int32)

    got_first_column = False
    i = 0
    table_xmin, table_xmax = 10000, 0
    table_ymin, table_ymax = 10000, 0

    for column in root.findall('object'):
        bndbox = column.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        col_mask[ymin:ymax, xmin:xmax] = 255

        if got_first_column:
            if not sameTable(prev_ymin, ymin, prev_ymax, ymax):
                i += 1
                got_first_column = False
                table_mask[table_ymin:table_ymax, table_xmin:table_xmax] = 255

                table_xmin = 10000
                table_xmax = 0

                table_ymin = 10000
                table_ymax = 0

        if not got_first_column:
            got_first_column = True
            first_xmin = xmin

        prev_ymin = ymin
        prev_ymax = ymax

        table_xmin = min(xmin, table_xmin)
        table_xmax = max(xmax, table_xmax)

        table_ymin = min(ymin, table_ymin)
        table_ymax = max(ymax, table_ymax)

    table_mask[table_ymin:table_ymax, table_xmin:table_xmax] = 255

    im = Image.fromarray(col_mask.astype(np.uint8), 'L')
    im.save(column_mask_file)

    im = Image.fromarray(table_mask.astype(np.uint8), 'L')
    im.save(table_mask_file)


@click.command()
@click.argument('source_dir', type=click.Path())
@click.argument('dest_dir', default='.')
@click.option('--quiet', '-q', is_flag=True,
              help='do not perform dataset consistency check')
def main(source_dir, dest_dir, quiet):
    '''Generate Table and Column masks from Marmot Dataset.

    Command line arguments:\n
    \b
    source_dir -- path to marmot dataset directory with *.bmp and *.xml files,
                  e.g. ./Marmot_data
    dest_dir   -- top output directory for saving generated files. Default is
                  current directory. Two subdirectories will be created under
                  dest_dir separately for column and table mask files:
                    * dest_dir/column_mask
                    * dest_dir/table_mask

    Additionally check dataset for consistency:
    every *.xml is expected to have a corresponding *.bmp file.
    '''

    assert os.path.isdir(source_dir), \
      f"Source directory not found: {source_dir}"

    final_col_directory = os.path.join(dest_dir, 'column_mask')
    final_table_directory = os.path.join(dest_dir, 'table_mask')

    os.makedirs(final_col_directory, exist_ok=True)
    os.makedirs(final_table_directory, exist_ok=True)

    for fname in os.listdir(source_dir):
        fname = os.fsdecode(fname)
        if fname.endswith('.xml'):
            basename = fname[:-4]
            outfile = basename + '.jpeg'

            if not quiet:
                check_file_pairs(source_dir, basename)

            xmlfile = os.path.join(source_dir, fname)
            table_mask_file = os.path.join(final_table_directory, outfile)
            column_mask_file = os.path.join(final_col_directory, outfile)

            generate_masks(xmlfile, table_mask_file, column_mask_file)


def check_file_pairs(dname, basename) -> bool:
    '''In Marmot dataset, each .bmp file has a corresponding .xml file.
    Check if this is the case for given file <basename>.

    Return
    ------
    True if both <basename>.bmp and <basename>.xml exist
    False otherwise

    >>> check_file_pairs('./dataset/Marmot_data', '10.1.1.8.2121_4')
    >>> True
    '''
    labels = {True: 'Found', False: 'Missing'}
    bmp_file = os.path.join(dname, basename + '.bmp')
    xml_file = os.path.join(dname, basename + '.xml')
    bmp_ok = os.path.isfile(bmp_file)
    xml_ok = os.path.isfile(xml_file)
    ok = bmp_ok and xml_ok
    if not ok:
        msg = 'File pair is incomplete:\n{}\t{}\n{}\t{}\n'.format(
               labels[bmp_ok], bmp_file, labels[xml_ok], xml_file)
        print(msg)
    return ok


if __name__ == "__main__":
    exit(main())
