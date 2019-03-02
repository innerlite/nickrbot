SCRIPT_NAME    = "wBot"
SCRIPT_AUTHOR  = "innerlite"
SCRIPT_VERSION = "1.0"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "Weechat Bot Commands"

import weechat as w

def wtrigger(data, buffer, args):
    global kserver, kchannel, knick #, mode
    if options["enabled"] == "on":
        try:
            srvmsg = args.split(" PRIVMSG ", 1)
        except:
            return w.WEECHAT_RC_OK
        try:
            kchannel, query = srvmsg.split(" :{} ".format(options["hello_trigger"]), 1)
        except ValueError:
            return w.WEECHAT_RC_OK

        kserver = str(buffer.split(",", 1)[0])
        knick = w.info_get("irc_nick_from_host", args)
        query = query.replace(" ", "%20")

        w.hook_process('*', 30 * 1000, "wbuffer", "")

#        w.command("","/wait 1m /python unload %s" % SCRIPT_NAME) <-- test

    return w.WEECHAT_RC_OK

def wbuffer(reaction, data, command, out, er):
    rtnbuf = "{},{}".format(kserver, kchannel)
    buffer = w.info_get("irc_buffer", rtnbuf)
    botnick = w.info_get("irc_nick", kserver)
    if kchannel == botnick:
        #private
        command = "msg {} {}".format(knick, reaction)
    else:
        #channel
        command = "msg {} {}".format(kchannel, reaction) 
#        command = "msg {} hello".format(kchannel, reaction)

#    w.prnt("", command) <-- test

    cmdprefix = "/"
    w.command(buffer, cmdprefix + command)
    return w.WEECHAT_RC_OK
    
### begin weechat plugin configuration stuff ###
def config_cb(data, option, value):
    """callback when script option is changed."""
    opt = option.split(".")[-1]
    options[opt] = value
    return w.WEECHAT_RC_OK

def get_option(option):
    """returns value of w.option."""
    return w.config_string(w.config_get("{}.{}".format(plugin_config, option)))

default_options = {"enabled": "on",
                   "hello_trigger": "!hello"}

plugin_config = "plugins.var.python.{}".format(SCRIPT_NAME)

if __name__ == "__main__":
    if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
        for option, value in default_options.items():
            if not w.config_is_set_plugin(option):
                w.config_set_plugin(option, value)

        options = {"enabled": get_option("enabled"),
                   "hello_trigger": get_option("hello_trigger")
                  }  
### end weechat plugin configuration stuff ####

        # start
        w.hook_signal("*,irc_in_privmsg", "wtrigger", "data")
        w.hook_config("{}.*".format(plugin_config), "config_cb", "")