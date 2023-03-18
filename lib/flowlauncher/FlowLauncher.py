# -*- coding: utf-8 -*-


import inspect
import sys
from json import loads, dumps


class FlowLauncher:
    """
    Flow.Launcher python plugin base
    """

    def __init__(self):

        # defalut jsonrpc
        self.rpc_request = {'method': 'query', 'parameters': ['']}
        self.debugMessage = ""
        
        if len(sys.argv) > 1:
            
            # Gets JSON-RPC from Flow Launcher process.
            self.rpc_request = loads(sys.argv[1])

        # proxy is not working now
        # self.proxy = self.rpc_request.get("proxy", {})

        request_method_name = self.rpc_request.get("method", "query")
        request_parameters = self.rpc_request.get("parameters", [])

        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        request_method = dict(methods)[request_method_name]
        results = request_method(*request_parameters)

        if request_method_name in ("query", "context_menu"):
            print(dumps({
                "result": results,
                "debugMessage": self.debugMessage
            }))

    def query(self, param: str = '') -> list:
        """
        sub class need to override this method
        """
        return []

    def context_menu(self, data) -> list:
        """
        optional context menu entries for a result
        """
        return []

    def debug(self, msg: str):
        """
        alert msg
        """
        self.debugMessage = msg
