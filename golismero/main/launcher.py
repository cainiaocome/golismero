#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GoLismero launcher.
"""

__license__ = """
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

Golismero project site: https://github.com/cr0hn/golismero/
Golismero project mail: golismero.project<@>gmail.com

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

__all__ = ["run"]

from .console import Console
from .orchestrator import Orchestrator
from ..api.net.web_utils import detect_auth_method, check_auth
from ..common import OrchestratorConfig, AuditConfig, get_default_config_file

import datetime
import traceback


#----------------------------------------------------------------------
def run(options, *audits):
    """
    Runs GoLismero in the current process.

    Optionally starts the requested audits. Pass each audit configuration
    object as a positional argument.

    Returns when (if) GoLismero finishes executing.

    :param options: Orchestrator settings.
    :type options: OrchestratorConfig

    :param audits: Audit settings.
    :type audits: AuditConfig

    :returns: Exit code.
    :rtype: int

    :raises TypeError: Invalid configuration objects.
    """

    # Validate and sanitize the arguments.
    options, audits = _sanitize_config(options, audits)

    # Set the console verbosity level.
    Console.level = options.verbose

    # Launch GoLismero.
    try:

        # Show the start message.
        Console.display("GoLismero started at %s" % datetime.datetime.now())

        # Detect auth in proxy, if specified.
        for auditParams in audits:
            if auditParams.proxy_addr:
                if auditParams.proxy_user:
                    if not check_auth(auditParams.proxy_addr, auditParams.proxy_user, auditParams.proxy_pass):
                        Console.display_error("[!] Authentication failed for proxy: '%s'." % auditParams.proxy_addr)
                        return 1
                else:
                    auth, _ = detect_auth_method(auditParams.proxy_addr)
                    if auth:
                        Console.display_error("[!] Authentication required for proxy: '%s'. Use '--proxy-user' and '--proxy-pass' to set the username and password." % auditParams.proxy_addr)
                        return 1

        # Run the Orchestrator.
        with Orchestrator(options) as orchestrator:
            orchestrator.run(*audits)

    # On error, show a fatal error message.
    except Exception, e:
        Console.display_error("[!] Fatal error: %s\n%s" % (str(e), traceback.format_exc()))
        return 1

    # Show the exit message.
    except KeyboardInterrupt:
        Console.display("GoLismero cancelled by the user at %s" % datetime.datetime.now())
        return 1
    except SystemExit, e:
        Console.display("GoLismero stopped at %s" % datetime.datetime.now())
        return e.code
    Console.display("GoLismero finished at %s" % datetime.datetime.now())
    return 0


#----------------------------------------------------------------------
def _sanitize_config(options, audits):
    """
    Validate and sanitize the arguments to the launcher.

    :param options: Orchestrator settings.
    :type options: OrchestratorConfig

    :param audits: Audit settings.
    :type audits: AuditConfig

    :returns: Sanitized options.
    :rtype: tuple(OrchestratorConfig, tuple(AuditConfig...))

    :raise TypeError: Bad argument types.
    """

    # Process the Orchestrator config.
    if options is None:
        options = OrchestratorConfig()
    elif not isinstance(options, OrchestratorConfig):
        raise TypeError("Expected OrchestratorConfig, got %s instead" % type(options))
    if not hasattr(options, "profile"):
        options.profile = None
        options.profile_file = None
    if not hasattr(options, "config_file"):
        options.config_file = get_default_config_file()
    if not hasattr(options, "plugin_load_overrides"):
        options.plugin_load_overrides = []
    options.check_params()

    # Process the Audit config.
    sane_audits = []
    for params in audits:
        if params is None:
            params = AuditConfig()
        elif not isinstance(params, AuditConfig):
            raise TypeError("Expected AuditConfig, got %s instead" % type(params))
        if not hasattr(params, "profile"):
            params.profile = options.profile
            params.profile_file = options.profile_file
        if not hasattr(params, "config_file"):
            params.config_file = options.config_file
        if not hasattr(params, "plugin_load_overrides"):
            params.plugin_load_overrides = options.plugin_load_overrides
        if not hasattr(params, "targets") or not params.targets:
            if not hasattr(options, "targets"):
                raise ValueError("No targets selected!")
            params.targets = list(options.targets)
        params.check_params()
        sane_audits.append(params)

    # Return the sanitized options.
    return options, tuple(sane_audits)
