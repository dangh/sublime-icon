import subprocess
import os


def plugin_loaded():
    fileicon = os.path.abspath(__file__ + '/../bin/fileicon')
    app_path = '/Applications/Sublime Text.app'
    icon_path = os.path.abspath(__file__ + '/../sublime-icon.icns')
    no_icon = subprocess.call(['/usr/bin/env', 'bash', fileicon, 'test', app_path])
    if no_icon:
        subprocess.call(['/usr/bin/env', 'bash', fileicon, 'set', app_path, icon_path])
