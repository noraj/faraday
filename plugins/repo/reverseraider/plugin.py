#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Faraday Penetration Test IDE
Copyright (C) 2013  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

'''

from __future__ import with_statement
from plugins import core
import re
import os
import sys


current_path = os.path.abspath(os.getcwd())

__author__ = "Francisco Amato"
__copyright__ = "Copyright (c) 2013, Infobyte LLC"
__credits__ = ["Francisco Amato"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Francisco Amato"
__email__ = "famato@infobytesec.com"
__status__ = "Development"


class ReverseraiderParser(object):
    """
    The objective of this class is to parse an xml file generated by the reverseraider tool.

    @param reverseraider_filepath A proper simple report generated by reverseraider
    """

    def __init__(self, output):

        lists = output.split("\r\n")
        self.items = []

        if re.search("ReverseRaider domain scanner|Error opening", output) is not None:
            return

        for line in lists:
            if line <> "":
                print "(%s)" % line
                info = line.split("\t")
                if info.__len__() > 0:
                    item = {'host': info[0], 'ip': info[1]}
                    print "host = %s, ip = %s" % (info[0], info[1])
                    self.items.append(item)


class ReverseraiderPlugin(core.PluginBase):
    """
    Example plugin to parse reverseraider output.
    """

    def __init__(self):
        core.PluginBase.__init__(self)
        self.id = "Reverseraider"
        self.name = "Reverseraider XML Output Plugin"
        self.plugin_version = "0.0.1"
        self.version = "0.7.6"
        self.options = None
        self._current_output = None
        self._current_path = None
        self._command_regex = re.compile(
            r'^(sudo \.\/reverseraider|\.\/reverseraider).*?')
        self._completition = {
            "": "reverseraider -d domain | -r range [options]",
            "-r": "range of ipv4 or ipv6 addresses, for reverse scanning",
            "-d": "domain, for wordlist scanning (example google.com)",
            "-w": "wordlist file (see wordlists directory...)",
            "-t": "requests timeout in seconds",
            "-P": "enable numeric permutation on wordlist (default off)",
            "-D": "nameserver to use (default: resolv.conf)",
            "-T": "use TCP queries instead of UDP queries",
            "-R": "don't set the recursion bit on queries",
        }

        global current_path

    def canParseCommandString(self, current_input):
        if self._command_regex.match(current_input.strip()):
            return True
        else:
            return False

    def parseOutputString(self, output, debug=False):
        """
        This method will discard the output the shell sends, it will read it from
        the xml where it expects it to be present.

        NOTE: if 'debug' is true then it is being run from a test case and the
        output being sent is valid.
        """

        if debug:
            parser = ReverseraiderParser(output)
        else:

            parser = ReverseraiderParser(output)

            for item in parser.items:
                h_id = self.createAndAddHost(item['ip'])
                i_id = self.createAndAddInterface(
                    h_id, item['ip'], ipv4_address=item['ip'])

        del parser

    def processCommandString(self, username, current_path, command_string):
        """
        """
        return None


def createPlugin():
    return ReverseraiderPlugin()

if __name__ == '__main__':
    parser = ReverseraiderParser(sys.argv[1])
    for item in parser.items:
        if item.status == 'up':
            print item
