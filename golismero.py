#!/usr/bin/env python
# -*- coding: utf-8 -*-


__license__="""
GoLismero 2.0 - The web knife.

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

__all__ = ["launcher", "show_banner"]


#----------------------------------------------------------------------
# Metadata

__author__ = "Daniel Garcia Garcia a.k.a cr0hn (@ggdaniel) - cr0hn<@>cr0hn.com"
__copyright__ = "Copyright 2011-2013 - GoLismero Project"
__credits__ = ["Daniel Garcia Garcia a.k.a cr0hn (@ggdaniel)", "Mario Vilas (@Mario_Vilas)"]
__maintainer__ = "cr0hn"
__email__ = "golismero.project<@>gmail.com"
__version__ = "2.0.0a1"


#----------------------------------------------------------------------
# Show program banner
def show_banner():
    print
    print "|--------------------------------------------------|"
    print "| GoLismero - The Web Knife                        |"
    print "| Contact: golismero.project<@>gmail.com           |"
    print "|                                                  |"
    print "| Daniel Garcia a.k.a cr0hn (@ggdaniel)            |"
    print "| Mario Vilas (@mario_vilas)                       |"
    print "|--------------------------------------------------|"
    print


#----------------------------------------------------------------------
# Python version check.
# We must do it now before trying to import any more modules.
#
# Note: this is mostly because of argparse, if you install it
#       separately you can try removing this check and seeing
#       what happens (we haven't tested it!).

import sys
from sys import version_info, exit
if __name__ == "__main__":
    if version_info < (2, 7) or version_info >= (3, 0):
        show_banner()
        print "[!] You must use Python version 2.7"
        exit(1)


#----------------------------------------------------------------------
# Fix the module load path when running as a portable script and during installation.

import os
from os import path
try:
    _FIXED_PATH_
except NameError:
    here = path.split(path.abspath(__file__))[0]
    if not here:  # if it fails use cwd instead
        here = path.abspath(os.getcwd())
    thirdparty_libs = path.join(here, "thirdparty_libs")
    if path.exists(thirdparty_libs):
        has_here = here in sys.path
        has_thirdparty_libs = thirdparty_libs in sys.path
        if not (has_here and has_thirdparty_libs):
            if has_here:
                sys.path.remove(here)
            if has_thirdparty_libs:
                sys.path.remove(thirdparty_libs)
            if __name__ == "__main__":
                # As a portable script: use our versions always
                sys.path.insert(0, thirdparty_libs)
                sys.path.insert(0, here)
            else:
                # When installing: prefer system version to ours
                sys.path.insert(0, here)
                sys.path.append(thirdparty_libs)
    _FIXED_PATH_ = True


#----------------------------------------------------------------------
# Imported modules

import argparse
import datetime
import textwrap

from ConfigParser import RawConfigParser
from os import getenv, getpid


#----------------------------------------------------------------------
# GoLismero modules

from golismero.api.config import Config
from golismero.common import OrchestratorConfig, AuditConfig, \
                             get_default_config_file, get_profile, \
                             get_available_profiles
from golismero.main import launcher
from golismero.main.orchestrator import Orchestrator
from golismero.managers.pluginmanager import PluginManager
from golismero.managers.processmanager import PluginContext


#----------------------------------------------------------------------
# Custom argparse actions

# --enable-plugin
class EnablePluginAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        assert self.dest == "enabled_plugins"
        values = values.strip()
        if values.lower() == "all":
            namespace.enabled_plugins  = ["all"]
            namespace.disabled_plugins = []
        else:
            enabled_plugins = getattr(namespace, "enabled_plugins", [])
            if "all" not in enabled_plugins:
                enabled_plugins.append(values)
            disabled_plugins = getattr(namespace, "disabled_plugins", [])
            if values in disabled_plugins:
                disabled_plugins.remove(values)

# --disable-plugin
class DisablePluginAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        assert self.dest == "disabled_plugins"
        values = values.strip()
        if values.lower() == "all":
            namespace.enabled_plugins  = []
            namespace.disabled_plugins = ["all"]
        else:
            disabled_plugins = getattr(namespace, "disabled_plugins", [])
            if "all" not in disabled_plugins:
                disabled_plugins.append(values)
            enabled_plugins = getattr(namespace, "enabled_plugins", [])
            if values in enabled_plugins:
                enabled_plugins.remove(values)

# --no-output
class ResetListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, [])

# --cookie-file
class ReadValueFromFileAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            with open(values, "rU") as f:
                data = f.read()
        except IOError, e:
            parser.error("Can't read file %r. Error: %s" % (values, e.message))
        setattr(namespace, self.dest, data)

#----------------------------------------------------------------------
# Command line parser using argparse

def cmdline_parser():
    parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
    parser.add_argument("targets", metavar="TARGET", nargs="*", help="one or more target web sites")

    gr_main = parser.add_argument_group("main options")
    gr_main.add_argument("--config", metavar="FILE", help="global configuration file", default=get_default_config_file())
    gr_main.add_argument("--profile", metavar="NAME", help="profile to use")
    gr_main.add_argument("--profile-list", action="store_true", help="list available profiles and quit")
    gr_main.add_argument("--ui-mode", metavar="MODE", help="UI mode")
    gr_main.add_argument("-v", "--verbose", action="count", help="increase output verbosity")
    gr_main.add_argument("-q", "--quiet", action="store_const", dest="verbose", const=0, help="suppress text output")
    gr_main.add_argument("--color", action="store_true", dest="colorize", help="use colors in console output")
    gr_main.add_argument("--no-color", action="store_false", dest="colorize", help="suppress colors in console output")
##    gr_main.add_argument("--forward-io", metavar="ADDRESS:PORT", help="forward all input and output to the given TCP address and port")

    gr_audit = parser.add_argument_group("audit options")
    gr_audit.add_argument("--audit-name", metavar="NAME", help="customize the audit name")
    gr_audit.add_argument("--audit-db", metavar="DATABASE", dest="audit_db", help="specify a database connection string")

    gr_report = parser.add_argument_group("report options")
    gr_report.add_argument("-o", "--output", dest="reports", metavar="FILENAME", action="append", help="write the results of the audit to this file [default: stdout]")
    gr_report.add_argument("-no", "--no-output", dest="reports", action=ResetListAction, help="do not output the results")
    gr_report.add_argument("--only-vulns", action="store_true", dest="only_vulns", help="display only vulnerable resources")

    gr_net = parser.add_argument_group("network options")
    gr_net.add_argument("--max-connections", help="maximum number of concurrent connections per host")
    gr_net.add_argument("--allow-subdomains", action="store_true", dest="include_subdomains", help="include subdomains in the target scope")
    gr_net.add_argument("--forbid-subdomains", action="store_false", dest="include_subdomains", help="do not include subdomains in the target scope")
    gr_net.add_argument("--subdomain-regex", metavar="REGEX", help="filter subdomains using a regular expression")
    gr_net.add_argument("-r", "--depth", type=int, help="maximum spidering depth")
    gr_net.add_argument("-l", "--max-links", type=int, help="maximum number of links to analyze (0 => infinite)")
    gr_net.add_argument("-f","--follow-redirects", action="store_true", dest="follow_redirects", help="follow redirects")
    gr_net.add_argument("-nf","--no-follow-redirects", action="store_false", dest="follow_redirects", help="do not follow redirects")
    gr_net.add_argument("-ff","--follow-first", action="store_true", dest="follow_first_redirect", help="always follow a redirection on the target URL itself")
    gr_net.add_argument("-nff","--no-follow-first", action="store_false", dest="follow_first_redirect", help="don't treat a redirection on a target URL as a special case")
    gr_net.add_argument("-pu","--proxy-user", metavar="USER", help="HTTP proxy username")
    gr_net.add_argument("-pp","--proxy-pass", metavar="PASS", help="HTTP proxy password")
    gr_net.add_argument("-pa","--proxy-addr", metavar="ADDRESS:PORT", help="HTTP proxy address in format: address:port")
    gr_net.add_argument("--cookie", metavar="COOKIE", help="set cookie for requests")
    gr_net.add_argument("--cookie-file", metavar="FILE", action=ReadValueFromFileAction, dest="cookie", help="load a cookie from file")
    gr_net.add_argument("--persistent-cache", action="store_true", dest="use_cache_db", help="use a persistent network cache [default in distributed modes]")
    gr_net.add_argument("--volatile-cache", action="store_false", dest="use_cache_db", help="use a volatile network cache [default in standalone mode]")

    gr_plugins = parser.add_argument_group("plugin options")
    gr_plugins.add_argument("-P", "--enable-plugin", metavar="NAME", action=EnablePluginAction, dest="enabled_plugins", help="customize which plugins to load")
    gr_plugins.add_argument("-NP", "--disable-plugin", metavar="NAME", action=DisablePluginAction, dest="disabled_plugins", help="customize which plugins not to load")
    gr_plugins.add_argument("--max-process", metavar="N", type=int, help="maximum number of plugins to run concurrently")
    gr_plugins.add_argument("--plugins-folder", metavar="PATH", help="customize the location of the plugins" )
    gr_plugins.add_argument("--plugin-list", action="store_true", help="list available plugins and quit")
    gr_plugins.add_argument("--plugin-info", metavar="NAME", dest="plugin_name", help="show plugin info and quit")

    return parser


#----------------------------------------------------------------------
# Start of program

def main():

    # Show the program banner.
    show_banner()

    # Get the command line parser.
    parser = cmdline_parser()

    # Parse the command line options.
    try:
        args = sys.argv[1:]
        envcfg = getenv("GOLISMERO_SETTINGS")
        if envcfg:
            args = parser.convert_arg_line_to_args(envcfg) + args
        P = parser.parse_args(args)

        # Load the Orchestrator options.
        cmdParams = OrchestratorConfig()
        if P.profile:
            cmdParams.profile = P.profile
        else:
            cmdParams.profile = None
        if P.config:
            cmdParams.config_file = path.abspath(P.config)
            if not path.isfile(cmdParams.config_file):
                raise ValueError("File not found: %r" % cmdParams.config_file)
            cmdParams.from_config_file(cmdParams.config_file)
        else:
            cmdParams.config_file = None
        if cmdParams.profile:
            cmdParams.profile_file = get_profile(cmdParams.profile)
            cmdParams.from_config_file(cmdParams.profile_file)
        else:
            cmdParams.profile_file = None
        cmdParams.from_object(P)

        # Load the target audit options.
        # TODO: this should be done by the UI plugin somehow.
        auditParams = AuditConfig()
        auditParams.from_object(P)

    # Show exceptions as command line parsing errors.
    except Exception, e:
        ##raise    # XXX DEBUG
        parser.error(str(e))

    # Get the plugins folder from the parameters.
    # If no plugins folder is given, use the default.
    # TODO: allow more than one plugin location!
    plugins_folder = cmdParams.plugins_folder
    if not plugins_folder:
        plugins_folder = path.abspath(__file__)
        plugins_folder = path.dirname(plugins_folder)
        plugins_folder = path.join(plugins_folder, "plugins")
        if not path.isdir(plugins_folder):
            from golismero import common
            plugins_folder = path.abspath(common.__file__)
            plugins_folder = path.dirname(plugins_folder)
            plugins_folder = path.join(plugins_folder, "plugins")
            if not path.isdir(plugins_folder):
                parser.error("Default plugins folder not found, aborting!")
        cmdParams.plugins_folder = plugins_folder


    #------------------------------------------------------------
    # List plugins and quit.

    if P.plugin_list:

        # Load the plugins list
        try:
            manager = PluginManager()
            manager.find_plugins(plugins_folder)
        except Exception, e:
            print "[!] Error loading plugins list: %s" % e.message
            exit(1)

        # Show the list of plugins.
        print "-------------"
        print " Plugin list"
        print "-------------"

        # UI plugins...
        ui_plugins = manager.get_plugins("ui")
        if ui_plugins:
            print
            print "-= UI plugins =-"
            for name in sorted(ui_plugins.keys()):
                info = ui_plugins[name]
                print "+ %s: %s" % (name[3:], info.description)

        # Report plugins...
        report_plugins = manager.get_plugins("report")
        if ui_plugins:
            print
            print "-= Report plugins =-"
            for name in sorted(report_plugins.keys()):
                info = report_plugins[name]
                print "+ %s: %s" % (name[7:], info.description)

        # Testing plugins...
        testing_plugins = manager.get_plugins("testing")
        if testing_plugins:
            print
            print "-= Testing plugins =-"
            names = sorted(testing_plugins.keys())
            names = [x[8:] for x in names]
            stages = [ (v,k) for (k,v) in manager.STAGES.iteritems() ]
            stages.sort()
            for _, stage in stages:
                s = stage + "/"
                p = len(s)
                slice = [x[p:] for x in names if x.startswith(s)]
                if slice:
                    print
                    print "%s stage:" % stage.title()
                    for name in slice:
                        info = testing_plugins["testing/%s/%s" % (stage, name)]
                        print "+ %s: %s" % (name, info.description)

        if os.sep != "\\":
            print
        exit(0)


    #------------------------------------------------------------
    # Display plugin info and quit.

    if P.plugin_name:

        # Load the plugins list.
        try:
            manager = PluginManager()
            manager.find_plugins(plugins_folder)
        except Exception, e:
            print "[!] Error loading plugins list: %s" % e.message
            exit(1)

        # Show the plugin information.
        try:
            try:
                m_plugin_info = manager.get_plugin_by_name(P.plugin_name)
            except KeyError:
                try:
                    m_found = manager.search_plugins_by_name(P.plugin_name)
                    if len(m_found) > 1:
                        print "[!] Error: which plugin did you mean?"
                        for plugin_name in m_found.iterkeys():
                            print "\t%s" % plugin_name
                        exit(1)
                    m_plugin_info = m_found.pop(m_found.keys()[0])
                except Exception:
                    raise KeyError(P.plugin_name)
            Config._context = PluginContext( orchestrator_pid = getpid(),
                                                  plugin_info = m_plugin_info,
                                                    msg_queue = None )
            m_plugin_obj = manager.load_plugin_by_name(m_plugin_info.plugin_name)
            message = m_plugin_obj.display_help()
            message = textwrap.dedent(message)
            print "Information for plugin: %s" % m_plugin_info.display_name
            print "----------------------"
            print "Location: %s" % m_plugin_info.descriptor_file
            print "Source code: %s" % m_plugin_info.plugin_module
            if m_plugin_info.plugin_class:
                print "Class name: %s" % m_plugin_info.plugin_class
            if m_plugin_info.description != m_plugin_info.display_name:
                print
                print m_plugin_info.description
            if message.strip().lower() != m_plugin_info.description.strip().lower():
                print
                print message
        except KeyError:
            print "[!] Plugin name not found"
            exit(1)
        except ValueError:
            print "[!] Plugin name not found"
            exit(1)
        except Exception, e:
            print "[!] Error recovering plugin info: %s" % e.message
            exit(1)
        exit(0)


    #------------------------------------------------------------
    # List profiles and quit.
    if P.profile_list:
        profiles = sorted(get_available_profiles())
        if not profiles:
            print "No available profiles!"
        else:
            print "-------------------"
            print " Available profiles"
            print "-------------------"
            print
            for name in profiles:
                try:
                    p = RawConfigParser()
                    p.read(get_profile(name))
                    desc = p.get("DEFAULT", "description")
                except Exception:
                    desc = None
                if desc:
                    print "%s: %s" % (name, desc)
                else:
                    print name
        if os.sep != "\\":
            print
        exit(0)


    #------------------------------------------------------------
    # Check if all options are correct.

    try:
        cmdParams.check_params()
        auditParams.check_params()
    except Exception, e:
        parser.error(e.message)


    #------------------------------------------------------------
    # Launch GoLismero.


    # Background job mode disabled for now, until we
    # find a way to make screen.py work without hacks.
    launcher.run(cmdParams, auditParams)
    exit(0)




    # (horrible spaghetti code follows)

    # Background process. Forward all I/O through a TCP/IP socket.
    if P.forward_io:
        import socket
        try:
            host, port = P.forward_io.split(":")
            host, port = host.strip(), port.strip()
            try:
                port = int(port)
            except Exception:
                port = socket.getservbyname(port)
            assert 0 < port < 65535
            socket.gethostbyname(host)
        except Exception:
            print "[!] Error: invalid address: %s" % P.forward_io
            exit(1)
        s = socket.socket()
        try:
            s.connect((host, port))
            fd = s.makefile("r+", 0)
            try:
                stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr
                try:
                    sys.stdin, sys.stdout, sys.stderr = fd, fd, fd
                    try:
                        launcher.run(cmdParams, auditParams)
                    except Exception:
                        import traceback
                        traceback.print_exc()
                        raise
                finally:
                    sys.stdin, sys.stdout, sys.stderr = stdin, stdout, stderr
            finally:
                fd.close()
        finally:
            try:
                try:
                    s.shutdown(2)
                finally:
                    s.close()
            except Exception:
                pass

    # Foreground process. Receive all forwarded I/O from the background process.
    else:
        import subprocess, socket, select, colorizer
        if P.colorize:
            colorizer.init()
        s = socket.socket()
        try:
            s.bind(("127.0.0.1",0))
            s.listen(1)
            port = s.getsockname()[1]
            executable = sys.executable
            if executable.lower().endswith("python.exe"):
                executable = executable[:-10] + "pythonw.exe"
            with open(os.devnull, "r+") as null_fd:
                process = subprocess.Popen(
                    [executable] + sys.argv + ["--forward-io", "127.0.0.1:%d" % port],
                    stdin = null_fd, stdout = null_fd, stderr = null_fd)
                try:
                    try:
                        a = s.accept()[0]
                        try:
                            while True:
                                try:
                                    r, w, e = select.select([a],[],[a])
                                except KeyboardInterrupt:
                                    if os.sep == "\\":
                                        import ctypes
                                        ctypes.windll.kernel32.GenerateConsoleCtrlEvent(0, process.pid) # CTRL_C_EVENT
                                    else:
                                        import signal
                                        process.send_signal(signal.SIGINT)
                                if e:
                                    print "[!] Socket error!"
                                    sys.stdout.flush()
                                    raise Exception("Socket error")
                                if r:
                                    d = a.recv(65335)
                                    if not d: break
                                    sys.stdout.write(d)
                                    sys.stdout.flush()
                                if w:
                                    a.sendall(sys.stdin.read(65335))
                        finally:
                            try:
                                a.shutdown(2)
                            finally:
                                a.close()
                    except Exception:
                        process.terminate()
                        raise
                finally:
                    process.wait()
        finally:
            s.close()


#------------------------------------------------------------
if __name__ == '__main__':
    main()
