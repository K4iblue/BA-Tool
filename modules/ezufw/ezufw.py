"""
### ufw default policies
# sudo ufw default deny incoming
# sudo ufw default allow outgoing

# sudo ufw allow ssh
# sudo ufw allow http
# sudo ufw allow https
# sudo ufw allow ssl

# sudo ufw allow from 10.0.0.1

## deny all ssh, but allow from ip
# sudo ufw allow from 10.0.0.1 to any port 22
# sudo ufw allow from <ip> to any port 80

## deny
# ufw status numbered
# sudo ufw delete [:rule-number]

# sudo ufw deny icmp
# sudo ufw deny from <ip>
"""
import gettext
import re
from typing import List, Any

from ufw.backend_iptables import UFWBackendIptables
from ufw.common import programName
from ufw.frontend import UFWFrontend, parse_command

gettext.install(programName)

"""Splitter for commands. Includes more than 1 space."""
SPLITTER = re.compile(r'\s+')

"""Ports splitter. Default is ','"""
PORT_SPLITTER = re.compile(r',')

"""IPv4 regex"""

IPV4_REGEX = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

EMPTY = ""

# noinspection SpellCheckingInspection
_configure_ufw = {
    'dryrun': False,
    'rootdir': None,
    'datadir': None
}


# noinspection SpellCheckingInspection
def configure(dryrun, rootdir=None, datadir=None):
    _configure_ufw['dryrun'] = dryrun
    _configure_ufw['rootdir'] = rootdir
    _configure_ufw['datadir'] = datadir


def rules() -> List:
    """
    :return: list of stored rules from UFW.
    """
    return UFWBackendIptables(**_configure_ufw).get_rules()


def enable() -> None:
    """
    Enable the UFW.
    """
    UFWFrontend(**_configure_ufw).set_enabled(True)


def disable() -> None:
    """
    Disable the UFW.
    """
    UFWFrontend(**_configure_ufw).set_enabled(False)


def _command(*cmd: Any) -> Any:
    """
    Inner method to build command using UFW command parser.

    :param cmd: arguments for command.
    :return: string, parsed command.
    """
    command = [programName]
    for c in map(str, cmd):
        command.extend(SPLITTER.split(c))
    return parse_command(command)


def execute(*cmd, force: bool = False) -> str:
    """
    Execute provided command with UFW.

    :param cmd: arguments for command.
    :param force: True if force, otherwise False. False by default.
    """
    ufw_cmd = _command(*cmd)
    rule = ufw_cmd.data.get('rule', EMPTY)
    ip_type = ufw_cmd.data.get('iptype', EMPTY)
    return UFWFrontend(**_configure_ufw).do_action(ufw_cmd.action, rule, ip_type, force)


def reset(default_policies: bool = True, force: bool = True) -> None:
    """
    Reset UFW configuration.
    Default policies includes:
    * default deny incoming,
    * default allow outgoing.

    :param default_policies: default True. Default policies will be applied.
    :param force: True if force, otherwise False. True by default.
    """
    execute('reset', force=force)
    if default_policies:
        execute("default", "deny", "incoming", force=force)
        execute("default", "allow", "outgoing", force=force)


def delete_by_port(*ports: Any) -> List:
    """
    Remove the rules connected with specified port. Counter keep numbering for the rule.
    When the rule is removed from ufw other rules are lifted and rules' indexes are changed.

    :return: list of removed rules.
    """
    removed_rules = []
    selected_ports = [max(0, int(port)) for port in ports]

    counter = 1
    for rule in rules():
        rule_port = -1 if rule.dport is None else int(rule.dport)
        if rule_port in selected_ports:
            removed_rules.append(rule)
            execute("delete", counter, force=True)
        else:
            counter += 1
    return removed_rules


def delete_by_ip(*ip_address: Any) -> List:
    """
    Remove the rules connected to specific ip_address.
    """
    removed_rules = []
    counter = 1
    for rule in rules():
        if rule.src in ip_address:
            removed_rules.append(rule)
            execute("delete", counter, force=True)
        else:
            counter += 1

    return removed_rules


def denyA(port_and_protocol: str = None) -> str:
    cmd = ('default', 'deny') if port_and_protocol is None else ("deny", port_and_protocol)
    return execute(*cmd)


def deny(port: int = None, protocol: int = None) -> str:
    values = []
    if port is not None:
        values.append(port)
        if protocol is not None:
            values.append("/")
            values.append(protocol)
    return denyA(None if not values else "".join(map(str, values)))


def deny_from(ip_address: str, *ports: Any) -> None:
    if ports:
        for port in ports:
            execute("deny", "from", ip_address, "to", "any", "port", port)
    else:
        execute("deny", "from", ip_address)


def allow_from(ip_address: str, *ports: Any) -> None:
    if ports:
        for port in ports:
            execute("allow", "from", ip_address, "to", "any", "port", port)
    else:
        execute("allow", "from", ip_address)


def insert(ip_address: str, index: int = 1, comment: str = "") -> str:
    """
    UFW (iptables) rules are applied in order of insertion. When the rule is matched other rules are skipped.
    In case when given IP should be banned, the rule must be on top.
    """
    cmd = ["insert", index, "deny", "from", ip_address]
    if comment:
        cmd.extend(["comment", comment])
    return execute(*cmd)


def status(verbose: bool = True) -> str:
    cmd = ("status", "verbose") if verbose else ("status",)
    return execute(*cmd)
