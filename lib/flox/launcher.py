# -*- coding: utf-8 -*-
import json
import sys
from time import time

"""
Slightly modified wox.py credit: https://github.com/Wox-launcher/Wox
"""

class Launcher(object):
    """
    Launcher python plugin base
    """

    def __del__(self, debug=None):
        self.run(debug)

    def run(self, debug=None):
        if debug:
            self._debug = debug
        self.rpc_request = {'method': 'query', 'parameters': ['']}
        if len(sys.argv) > 1:
            self.rpc_request = json.loads(sys.argv[1])
        if 'settings' in self.rpc_request.keys():
            self._settings = self.rpc_request['settings']
            self.logger.debug('Loaded settings from RPC request')
        if not self._debug:
            self._debug = self.settings.get('debug', False)
        if self._debug:
            self.logger_level("debug")
        self.logger.debug(f'Request:\n{json.dumps(self.rpc_request, indent=4)}')
        self.logger.debug(f"Params: {self.rpc_request.get('parameters')}")
        # proxy is not working now
        # self.proxy = rpc_request.get("proxy",{})
        request_method_name = self.rpc_request.get("method")
        #transform query and context calls to internal flox methods
        if request_method_name == 'query' or request_method_name == 'context_menu':
            request_method_name = f"_{request_method_name}"

        request_parameters = self.rpc_request.get("parameters")

        request_method = getattr(self, request_method_name)
        try:
            results = request_method(*request_parameters) or self._results
        except Exception as e:
            self.logger.exception(e)
            results = self.exception(e) or self._results
        line_break = '#' * 10
        ms = int((time() - self._start) * 1000)
        self.logger.debug(f'{line_break} Total time: {ms}ms {line_break}')
        if request_method_name == "_query" or request_method_name == "_context_menu":
            results = {"result": results}
            if self._settings != self.rpc_request.get('Settings') and self._settings is not None:
                results['SettingsChange'] = self.settings

            print(json.dumps(results))

    def query(self,query):
        """
        sub class need to override this method
        """
        return []

    def context_menu(self, data):
        """
        optional context menu entries for a result
        """
        return []

    def exception(self, exception):
        """
        exception handler
        """
        return []

    def debug(self,msg):
        """
        alert msg
        """
        print("DEBUG:{}".format(msg))
        sys.exit()

    def change_query(self, query, requery=False):
        """
        change query
        """
        print(json.dumps({"method": f"{self.api}.ChangeQuery","parameters":[query,requery]}))

    def shell_run(self, cmd):
        """
        run shell commands
        """
        print(json.dumps({"method": f"{self.api}.ShellRun","parameters":[cmd]}))

    def close_app(self):
        """
        close launcher
        """
        print(json.dumps({"method": f"{self.api}.CloseApp","parameters":[]}))

    def hide_app(self):
        """
        hide launcher
        """
        print(json.dumps({"method": f"{self.api}.HideApp","parameters":[]}))

    def show_app(self):
        """
        show launcher
        """
        print(json.dumps({"method": f"{self.api}.ShowApp","parameters":[]}))

    def show_msg(self, title, sub_title, ico_path=""):
        """
        show messagebox
        """
        print(json.dumps({"method": f"{self.api}.ShowMsg","parameters":[title,sub_title,ico_path]}))

    def open_setting_dialog(self):
        """
        open setting dialog
        """
        self.logger.debug(json.dumps({"method": f"{self.api}.OpenSettingDialog","parameters":[]}))
        print(json.dumps({"method": f"{self.api}.OpenSettingDialog","parameters":[]}))

    def start_loadingbar(self):
        """
        start loading animation in wox
        """
        print(json.dumps({"method": f"{self.api}.StartLoadingBar","parameters":[]}))

    def stop_loadingbar(self):
        """
        stop loading animation in wox
        """
        print(json.dumps({"method": f"{self.api}.StopLoadingBar","parameters":[]}))

    def reload_plugins(self):
        """
        reload all launcher plugins
        """
        print(json.dumps({"method": f"{self.api}.ReloadPlugins","parameters":[]}))
