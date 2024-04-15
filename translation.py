# @name: translate.py
# @license: GNU Affero General Public License, Version 3 <https://www.gnu.org/licenses/agpl-3.0.en.html>
# @author: Alexandre Villares
# @purpose: Translate Markdown files
# @acknowledgements:
# Based on work by Simon Bowie <ad7588@coventry.ac.uk> 

from time import sleep
import json
from pathlib import Path
import urllib

import frontmatter  # pip install python-frontmatter

from libretranslatepy import LibreTranslateAPI

#url = 'https://translate.direitosdigitais.pt'
url = "https://libretranslate.eownerdead.dedyn.io"
lt = LibreTranslateAPI(url)
input_language = 'pt'
output_language = 'en'

input_directory = Path('/home/villares/GitHub/material-aulas/Processing-Python-py5/')
output_directory = Path('/home/villares/GitHub/python-visual-context/Processing-Python-py5/')
 
# iterate over files with .md suffix in the input directory
input_files = [fp.relative_to(input_directory) for fp in Path(input_directory).rglob("*.md")] 
print(input_files)
output_files = [fp.relative_to(output_directory) for fp in Path(output_directory).rglob("*.md")] 

to_do = set(input_files) - set(output_files)
for file_path in to_do:
    # read Markdown file
    text = frontmatter.load(input_directory / file_path)
    try:
        text.content = lt.translate(text, input_language, output_language)
    except urllib.error.HTTPError:
        print('skipping', file_path)
        continue

    # create output subdirectory if it doesn't exist
    write_directory = output_directory / file_path.parent
    print(output_directory / file_path, f'new folder: {not write_directory.exists()}')
    write_directory.mkdir(parents=True, exist_ok=True)
 
    # write new Markdown file
    with open(output_directory / file_path, 'w') as f:
        f.write(frontmatter.dumps(text))
