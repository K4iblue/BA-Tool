# easyufw

## setup

[easyufw][] is that wrapper that
allows [ufw][] to be called as a simple api.

You can pull easyufw from GitLab like this:
```
git clone https://gitlab.com/dhj/easyufw.git
```

You also need ufw and you need to run easyufw
with root privileges because ufw requires it:
```
sudo pip install ufw
sudo python
```

## try it
Once you're all set up you can type
these commands into a python terminal to get a feel for how
easy it is.

#### WARNING: the interface is live -- there is no dry run. Commands you run will modify firewall settings on the machine.  Be careful.

```
import easyufw.easyufw as ufw

print ufw.status()
ufw.enable() # enable the firewall
ufw.deny('22/tcp') # disable ssh -- could disable active sessions!
ufw.allow('22/tcp') # enable ssh -- '22' alone or as int includes tcp and udp
ufw.delete(22) # delete all rules for port 22 -- int required
ufw.disable() # this will leave your firewall disabled! (default in ubuntu, but IMO, not recommended)
```

Look ma, no hands.

easyufw sets up the ufw front end interface
and parser to funnel commands to the ufw
backend. You can use `ufw.run('cmd')`,
e.g. `ufw.run('allow 22/tcp')`,
to run any command as if it was from the
command line.

easyufw also handles
internationalization initialization
(yes that's real) so you don't
get a `global name '_' is not defined`
error.

## Potential Improvements

Python packaging so you could `pip install easyufw` would be nice.

There is no dryrun capability in the
easyufw api, but it is an option in ufw.

[easyufw]:https://gitlab.com/dhj/easyufw
[ufw]:https://wiki.ubuntu.com/UncomplicatedFirewall
