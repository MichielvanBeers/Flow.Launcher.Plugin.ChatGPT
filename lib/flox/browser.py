import logging
from subprocess import Popen, PIPE, CREATE_NO_WINDOW
import webbrowser
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER as HKCU, HKEY_LOCAL_MACHINE as HKLM

log = logging.getLogger(__name__)

DEFAULT_BROWSER_KEYWORD = "*"
MICROSOFT_EDGE = 'msedge'
CHROME = 'chrome'
FIREFOX = 'firefox'
NEW_WINDOW_ARG = "--new-window"


CHROME_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
FIREFOX_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe"
MSEDGE_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe"
DEFAULT_BROWSER_PATH = r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice"

DEFAULT_BROWSERS = {
    CHROME: CHROME_PATH,
    FIREFOX: FIREFOX_PATH,
    MICROSOFT_EDGE: MSEDGE_PATH,
    DEFAULT_BROWSER_KEYWORD: DEFAULT_BROWSER_PATH
}

def get_reg(path, base_path=HKLM, name=""):
    try:
        with OpenKey(base_path, path) as key:
            return QueryValueEx(key, name)[0]
    except FileNotFoundError:
        log.exception(f'Can\'t find browser "{path}"')

class Browser(object):

    def __init__(self, settings):
        self.Name = None
        self.Path = None
        self.PrivateArg = None
        self.EnablePrivate = False
        self.OpenInTab = True
        self.Editable = False
        self.CustomBrowserIndex = settings.get('CustomBrowserIndex', 0)
        self.CustomBrowserList = settings.get('CustomBrowserList', [])
        try:
            self.current_browser = self.CustomBrowserList[self.CustomBrowserIndex]
        except IndexError:
            self.current_browser = {}
        for item in self.current_browser:
            setattr(self, item, self.current_browser[item])

    def open(self, url):
        try:
            cmd = [self.get_exe(), url]
            if self.current_browser.get('EnablePrivate', False):
                cmd.append(self.current_browser['PrivateArg'])
            if not self.OpenInTab:
                cmd.append(NEW_WINDOW_ARG)
            log.debug(f'Opening {url} with {cmd}')
            Popen(cmd, creationflags=CREATE_NO_WINDOW)
        # All else fails, open in default browser and log error
        except Exception as e:
            log.exception(f'Can\'t open {url} with {self.Name}')
            webbrowser.open(url)

    def get_exe(self):
        key = self.Path or DEFAULT_BROWSER_KEYWORD
        if key == DEFAULT_BROWSER_KEYWORD:
            browser = get_reg(DEFAULT_BROWSER_PATH, HKCU, 'Progid')
            key = browser.split('-')[0].replace('url', '').replace('HTML', '').lower()
        if key in DEFAULT_BROWSERS:
            _path = DEFAULT_BROWSERS.get(key)
            return get_reg(_path)
        else:
            return key