#!/usr/bin/env python

# A thin wrapper over the thin wrapper that is ufw
# Usage:
#   import easyufw as ufw
#   ufw.disable()        # disable firewall
#   ufw.enable()         # enable firewall
#   ufw.allow()          # default allow -- allow all
#   ufw.allow(22)        # allow port 22, any protocol
#   ufw.allow(22,'tcp')  # allow port 22, tcp protocol
#   ufw.allow('22/tcp')  # allow port 22, tcp protocol
#   ufw.allow(53,'udp')  # allow port 53, udp protocol
#   ufw.allow(53,'udp')  # allow port 53, udp protocol
#   ufw.deny()           # default deny -- deny all
#   ufw.deny(22,'tcp')   # deny port 22, tcp protocol
#   ufw.delete(22)       # delete rules referencing port 22
#   ufw.reset()          # restore defaults
#   ufw.status()         # return status string (default verbose=True)
#   ufw.run("allow 22") # directly run command as if from command line

import ufw.frontend
import ufw.common
import gettext

progName = ufw.common.programName
gettext.install(progName)#, unicode=True) # for i18n; fixes '_' not defined
ui = ufw.frontend.UFWFrontend(False) # no dryrun -- do it live
backend = ui.backend
parse_command = ufw.frontend.parse_command

def _parse(actionstr):
    # parse commands like "allow 22", "reset", "default allow"
    argv = [progName]
    argv.extend(actionstr.split(' ')) # generate bogus argv to parse
    pr = parse_command(argv)
    return pr

def run(actionstr, force=False):
    # run command with an explicit force argument
    pr = _parse(actionstr)
    rule = pr.data.get('rule','') # commands like reset don't have a rule
    iptype = pr.data.get('iptype','')
    return ui.do_action(pr.action,rule,iptype,force)

def reset(force=True):
    run('reset',force=force)

def enable():
    ui.set_enabled(True)

def disable():
    ui.set_enabled(False)

def allow(port=None, protocol=None):
    # port int; protocol str ['tcp','udp']
    pp = None
    if port is not None:
        pp = "" # port and protocol string
        pp += str(port)
        
        if protocol is not None:
            pp += '/' + protocol

    _allow(pp)

def _allow(pp=None):
    # pp = port and protocol string ['22','22/tcp','53/udp']
    # port without protocol includes all protocols
    if pp is None:
        run('default allow')
    else:
        run('allow ' + pp)

def deny(port=None, protocol=None):
    # port int; protocol str ['tcp','udp']
    pp = None
    if port is not None:
        pp = "" # port and protocol string
        pp += str(port)

        if protocol is not None:
            pp += '/' + protocol

    _deny(pp)

def _deny(pp=None):
    # pp = port and protocol string
    if pp is None:
        run('default deny')
    else:
        run('deny ' + pp)

def delete(port):
    # delete all rules by destination port
    while _delete(port): pass # while ports deleted re-enumerate and continue

def _delete(port):
    for i,rule in enumerate(backend.get_rules()):
        rule_port = None
        try:
            rule_port = int(rule.dport)
        except:
            pass
        if port == rule_port:
            run("delete " + str(i+1), force=True)
            return True # delete one rule; enumeration changes after delete
    return False

def status(verbose=True):
    cmd = 'status'
    if verbose:
        cmd += ' verbose'
    return run(cmd)
