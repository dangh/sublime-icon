import sublime
import os
import subprocess
import hashlib
import stat

APP_PATH = sublime.executable_path()[0:-28]
CACHE_PATH = os.path.join(sublime.cache_path(), "sublime-icon")
FILEICON_URL = (
    "https://raw.githubusercontent.com/mklement0/fileicon/master/bin/fileicon"
)


def log(*msg):
    print("[sublime-icon]", *msg)


def download(url, filepath):
    subprocess.call(
        ["curl", "--create-dirs", "--fail", "--location", "--output", filepath, url]
    )


def fileicon(argv):
    fileicon_path = os.path.join(CACHE_PATH, "fileicon")
    if not os.path.isfile(fileicon_path):
        download(FILEICON_URL, fileicon_path)
        os.chmod(fileicon_path, stat.S_IEXEC)
    try:
        subprocess.check_output([fileicon_path] + argv)
    except subprocess.CalledProcessError as e:
        log(e.output.decode().strip())
        raise e


def update_icon(settings=None):
    if not settings:
        settings = sublime.load_settings("sublime-icon.sublime-settings")

    icon_url = settings.get("icon_url")
    if not icon_url:
        log("reset icon")
        fileicon(["rm", APP_PATH])
        return

    if not os.path.isdir(CACHE_PATH):
        os.mkdir(CACHE_PATH)

    current_icon = None
    icon_path = os.path.join(
        CACHE_PATH, "icon_" + hashlib.md5(icon_url.encode()).hexdigest()
    )
    try:
        with open(os.path.join(CACHE_PATH, "icon_current"), "r") as f:
            current_icon = f.readline()
    except:
        pass

    if current_icon == icon_path:
        log("icon already set")
        return

    if not os.path.isfile(icon_path):
        log("download icon from", icon_url)
        download(icon_url, icon_path)

    log("set icon from", icon_url)
    fileicon(["set", APP_PATH, icon_path])

    with open(os.path.join(CACHE_PATH, "icon_current"), "w") as f:
        f.write(icon_path)


def plugin_loaded():
    settings = sublime.load_settings("sublime-icon.sublime-settings")

    settings.add_on_change("icon_url", update_icon)

    update_icon(settings)
