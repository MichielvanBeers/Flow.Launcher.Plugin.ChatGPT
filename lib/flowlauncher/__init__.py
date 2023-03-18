# -*- coding: utf-8 -*-

from ._version import get_versions
from .FlowLauncher import FlowLauncher  # noqa
from .FlowLauncherAPI import FlowLauncherAPI  # noqa

__version__ = get_versions()["version"]
del get_versions

__license__ = 'MIT'
__short_description__ = 'Flow Launcher supports Python by JsonRPC.'
