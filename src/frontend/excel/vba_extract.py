import os
import shutil
from oletools.olevba3 import VBA_Parser

EXCEL_FILE_EXTENSIONS = ('xlsb', 'xls', 'xlsm', 'xla', 'xlt', 'xlam',)

def parse(workbook_path):
    vba_path = workbook_path + '.vba'
    vba_parser = VBA_Parser(workbook_path)
    vba_modules = vba_parser.extract_all_macros() if vba_parser.detect_vba_macros() else []

    for _, _, _, content in vba_modules:
        decoded_content = content
        lines = []
        if '\r\n' in decoded_content:
            lines = decoded_content.split('\r\n')
        else:
            lines = decoded_content.split('\n')
        if lines:
            name = lines[0].replace('Attribute VB_Name = ', '').strip('"')
            content = [line for line in lines[1:] if not (
                line.startswith('Attribute') and 'VB_' in line)]
            if content and content[-1] == '':
                content.pop(len(content)-1)
                lines_of_code = len(content)
                non_empty_lines_of_code = len([c for c in content if c])
                if non_empty_lines_of_code > 0:
                    if not os.path.exists(os.path.join(vba_path)):
                        os.makedirs(vba_path)
                    with open(os.path.join(vba_path, name + '.bas'), 'w') as f:
                        f.write('\n'.join(content))


if __name__ == '__main__':
    for root, dirs, files in os.walk('.'):
        for f in dirs:
            if f.endswith('.vba'):
                shutil.rmtree(os.path.join(root, f))

        for f in files:
            if f.endswith(EXCEL_FILE_EXTENSIONS):
                parse(os.path.join(root, f))