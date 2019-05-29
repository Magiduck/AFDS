#!"C:\Users\tijsv\Google Drive\Minor\Project\AFDS\venv\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'buildozer==0.40.dev0','console_scripts','buildozer-remote'
__requires__ = 'buildozer==0.40.dev0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('buildozer==0.40.dev0', 'console_scripts', 'buildozer-remote')()
    )
