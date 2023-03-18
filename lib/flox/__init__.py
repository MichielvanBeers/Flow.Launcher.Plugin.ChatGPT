import sys
import traceback
import os
import json
import time
import webbrowser
import urllib.parse
from datetime import date
import logging
import logging.handlers
from pathlib import Path
from typing import Union
from functools import wraps, cached_property
from tempfile import gettempdir

from .launcher import Launcher
from .browser import Browser
from .settings import Settings

PLUGIN_MANIFEST = 'plugin.json'
FLOW_LAUNCHER_DIR_NAME = "FlowLauncher"
SCOOP_FLOW_LAUNCHER_DIR_NAME = "flow-launcher"
WOX_DIR_NAME = "Wox"
FLOW_API = 'Flow.Launcher'
WOX_API = 'Wox'
APP_DIR = None
USER_DIR = None
LOCALAPPDATA = Path(os.getenv('LOCALAPPDATA'))
APPDATA = Path(os.getenv('APPDATA'))
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CURRENT_WORKING_DIR = Path().cwd()
LAUNCHER_NOT_FOUND_MSG = f"Unable to locate Launcher directory\nCurrent working directory: {CURRENT_WORKING_DIR}"


launcher_dir = None
path = CURRENT_WORKING_DIR
if SCOOP_FLOW_LAUNCHER_DIR_NAME.lower() in str(path).lower():
    launcher_name = SCOOP_FLOW_LAUNCHER_DIR_NAME
    API = FLOW_API
elif FLOW_LAUNCHER_DIR_NAME.lower() in str(path).lower():
    launcher_name = FLOW_LAUNCHER_DIR_NAME
    API = FLOW_API
elif WOX_DIR_NAME.lower() in str(path).lower():
    launcher_name = WOX_DIR_NAME
    API = WOX_API
else:
    raise FileNotFoundError(LAUNCHER_NOT_FOUND_MSG)

while True:
    if len(path.parts) == 1:
        raise FileNotFoundError(LAUNCHER_NOT_FOUND_MSG)
    if path.joinpath('Settings').exists():
        USER_DIR = path
        if USER_DIR.name == 'UserData':
            APP_DIR = USER_DIR.parent
        elif str(CURRENT_WORKING_DIR).startswith(str(APPDATA)):
            APP_DIR = LOCALAPPDATA.joinpath(launcher_name)
        else:
            raise FileNotFoundError(LAUNCHER_NOT_FOUND_MSG)
        break

    path = path.parent

APP_ICONS = APP_DIR.joinpath("Images")
ICON_APP = APP_DIR.joinpath('app.png')
ICON_APP_ERROR = APP_DIR.joinpath(APP_ICONS, 'app_error.png')
ICON_BROWSER = APP_DIR.joinpath(APP_ICONS, 'browser.png')
ICON_CALCULATOR = APP_DIR.joinpath(APP_ICONS, 'calculator.png')
ICON_CANCEL = APP_DIR.joinpath(APP_ICONS, 'cancel.png')
ICON_CLOSE = APP_DIR.joinpath(APP_ICONS, 'close.png')
ICON_CMD = APP_DIR.joinpath(APP_ICONS, 'cmd.png')
ICON_COLOR = APP_DIR.joinpath('color.png')
ICON_CONTROL_PANEL = APP_DIR.joinpath('ControlPanel.png')
ICON_COPY = APP_DIR.joinpath('copy.png')
ICON_DELETE_FILE_FOLDER = APP_DIR.joinpath('deletefilefolder.png')
ICON_DISABLE = APP_DIR.joinpath('disable.png')
ICON_DOWN = APP_DIR.joinpath('down.png')
ICON_EXE = APP_DIR.joinpath('exe.png')
ICON_FILE = APP_DIR.joinpath('file.png')
ICON_FIND = APP_DIR.joinpath('find.png')
ICON_FOLDER = APP_DIR.joinpath('folder.png')
ICON_HISTORY = APP_DIR.joinpath('history.png')
ICON_IMAGE = APP_DIR.joinpath('image.png')
ICON_LOCK = APP_DIR.joinpath('lock.png')
ICON_LOGOFF = APP_DIR.joinpath('logoff.png')
ICON_OK = APP_DIR.joinpath('ok.png')
ICON_OPEN = APP_DIR.joinpath('open.png')
ICON_PICTURES = APP_DIR.joinpath('pictures.png')
ICON_PLUGIN = APP_DIR.joinpath('plugin.png')
ICON_PROGRAM = APP_DIR.joinpath('program.png')
ICON_RECYCLEBIN = APP_DIR.joinpath('recyclebin.png')
ICON_RESTART = APP_DIR.joinpath('restart.png')
ICON_SEARCH = APP_DIR.joinpath('search.png')
ICON_SETTINGS = APP_DIR.joinpath('settings.png')
ICON_SHELL = APP_DIR.joinpath('shell.png')
ICON_SHUTDOWN = APP_DIR.joinpath('shutdown.png')
ICON_SLEEP = APP_DIR.joinpath('sleep.png')
ICON_UP = APP_DIR.joinpath('up.png')
ICON_UPDATE = APP_DIR.joinpath('update.png')
ICON_URL = APP_DIR.joinpath('url.png')
ICON_USER = APP_DIR.joinpath('user.png')
ICON_WARNING = APP_DIR.joinpath('warning.png')
ICON_WEB_SEARCH = APP_DIR.joinpath('web_search.png')
ICON_WORK = APP_DIR.joinpath('work.png')


class Flox(Launcher):

    def __init_subclass__(cls, api=API, app_dir=APP_DIR, user_dir=USER_DIR):
        cls._debug = False
        cls.appdir = APP_DIR
        cls.user_dir = USER_DIR
        cls.api = api
        cls._start = time.time()
        cls._results = []
        cls._settings = None
        cls.font_family = '/Resources/#Segoe Fluent Icons'
        cls.issue_item_title = 'Report Issue'
        cls.issue_item_subtitle = 'Report this issue to the developer'

    @cached_property
    def browser(self):
        return Browser(self.app_settings)

    def exception(self, exception):
        self.exception_item(exception)
        self.issue_item(exception)

    def _query(self, query):
        self.args = query.lower()

        self.query(query)

    def _context_menu(self, data):
        self.context_menu(data)

    def exception_item(self, exception):
        self.add_item(
            title=exception.__class__.__name__,
            subtitle=str(exception),
            icon=ICON_APP_ERROR,
            method=self.change_query,
            dont_hide=True
        )

    def issue_item(self, e):
        trace = ''.join(traceback.format_exception(type(e), value=e, tb=e.__traceback__)).replace('\n', '%0A')
        self.add_item(
            title=self.issue_item_title,
            subtitle=self.issue_item_subtitle,
            icon=ICON_BROWSER,
            method=self.create_github_issue,
            parameters=[e.__class__.__name__, trace],
        )

    def create_github_issue(self, title, trace, log=None):
        url = self.manifest['Website']
        if 'github' in url.lower():
            issue_body = f"Please+type+any+relevant+information+here%0A%0A%0A%0A%0A%0A%3Cdetails open%3E%3Csummary%3ETrace+Log%3C%2Fsummary%3E%0A%3Cp%3E%0A%0A%60%60%60%0A{trace}%0A%60%60%60%0A%3C%2Fp%3E%0A%3C%2Fdetails%3E"
            url = f"{url}/issues/new?title={title}&body={issue_body}"
        webbrowser.open(url)

    def add_item(self, title:str, subtitle:str='', icon:str=None, method:Union[str, callable]=None, parameters:list=None, context:list=None, glyph:str=None, score:int=0, **kwargs):
        icon = icon or self.icon
        if not Path(icon).is_absolute():
            icon = Path(self.plugindir, icon)
        item = {
            "Title": str(title),
            "SubTitle": str(subtitle),
            "IcoPath": str(icon),
            "ContextData": context,
            "Score": score,
            "JsonRPCAction": {}
        }
        auto_complete_text = kwargs.pop("auto_complete_text", None)

        item["AutoCompleteText"] = auto_complete_text or f'{self.user_keyword} {title}'.replace('* ', '')
        if method:
            item['JsonRPCAction']['method'] = getattr(method, "__name__", method)
            item['JsonRPCAction']['parameters'] = parameters or []
            item['JsonRPCAction']['dontHideAfterAction'] = kwargs.pop("dont_hide", False)
        if glyph:
            item['Glyph'] = {}
            item['Glyph']['Glyph'] = glyph
            font_family =  kwargs.pop("font_family", self.font_family)
            if font_family.startswith("#"):
                font_family = str(Path(self.plugindir).joinpath(font_family))
            item['Glyph']['FontFamily'] = font_family
        for kw in kwargs:
            item[kw] = kwargs[kw]
        self._results.append(item)
        return self._results[-1]

    @cached_property
    def plugindir(self):
        potential_paths = [
            os.path.abspath(os.getcwd()),
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        ]

        for path in potential_paths:

            while True:
                if os.path.exists(os.path.join(path, PLUGIN_MANIFEST)):
                    return path
                elif os.path.ismount(path):
                    return os.getcwd()

                path = os.path.dirname(path)

    @cached_property
    def manifest(self):
        with open(os.path.join(self.plugindir, PLUGIN_MANIFEST), 'r') as f:
            return json.load(f)

    @cached_property
    def id(self):
        return self.manifest['ID']

    @cached_property
    def icon(self):
        return self.manifest['IcoPath']

    @cached_property
    def action_keyword(self):
        return self.manifest['ActionKeyword']

    @cached_property
    def version(self):
        return self.manifest['Version']

    @cached_property
    def appdata(self):
        # Userdata should be up two directories from plugin root
        return os.path.dirname(os.path.dirname(self.plugindir))

    @property
    def app_settings(self):
        with open(os.path.join(self.appdata, 'Settings', 'Settings.json'), 'r') as f:
            return json.load(f)

    @property
    def query_search_precision(self):
        return self.app_settings['QuerySearchPrecision']

    @cached_property
    def user_keywords(self):
        return self.app_settings['PluginSettings']['Plugins'].get(self.id, {}).get('UserKeywords', [self.action_keyword])

    @cached_property
    def user_keyword(self):
        return self.user_keywords[0]

    @cached_property
    def appicon(self, icon):
        return os.path.join(self.appdir, 'images', icon + '.png')

    @property
    def applog(self):
        today = date.today().strftime('%Y-%m-%d')
        file = f"{today}.txt"
        return os.path.join(self.appdata, 'Logs', self.appversion, file)

    
    @cached_property
    def appversion(self):
        return os.path.basename(self.appdir).replace('app-', '')

    @cached_property
    def logfile(self):
        file = "plugin.log"
        return os.path.join(self.plugindir, file)

    @cached_property
    def logger(self):
        logger = logging.getLogger('')
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s (%(filename)s): %(message)s',
            datefmt='%H:%M:%S')
        logfile = logging.handlers.RotatingFileHandler(
                self.logfile,
                maxBytes=1024 * 2024,
                backupCount=1)
        logfile.setFormatter(formatter)
        logger.addHandler(logfile)
        logger.setLevel(logging.WARNING)
        return logger

    def logger_level(self, level):
        if level == "info":
            self.logger.setLevel(logging.INFO)
        elif level == "debug":
            self.logger.setLevel(logging.DEBUG)
        elif level == "warning":
            self.logger.setLevel(logging.WARNING)
        elif level == "error":
            self.logger.setLevel(logging.ERROR)
        elif level == "critical":
            self.logger.setLevel(logging.CRITICAL)

    @cached_property
    def api(self):
        launcher = os.path.basename(os.path.dirname(self.appdir))
        if launcher == 'FlowLauncher':
            return FLOW_API
        else:
            return WOX_API

    @cached_property
    def name(self):
        return self.manifest['Name']

    @cached_property
    def author(self):
        return self.manifest['Author']

    @cached_property
    def settings_path(self):
        dirname = self.name
        setting_file = "Settings.json"
        return os.path.join(self.appdata, 'Settings', 'Plugins', dirname, setting_file)

    @cached_property
    def settings(self):
        if not os.path.exists(os.path.dirname(self.settings_path)):
            os.mkdir(os.path.dirname(self.settings_path))
        return Settings(self.settings_path)

    def browser_open(self, url):
        self.browser.open(url)

    @cached_property
    def python_dir(self):
        return self.app_settings["PluginSettings"]["PythonDirectory"]

    def log(self):
        return self.logger