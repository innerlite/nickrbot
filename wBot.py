SCRIPT_NAME    = "wBot"
SCRIPT_AUTHOR  = "innerlite"
SCRIPT_VERSION = "1.0"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "Weechat Bot Commands"

import weechat as w

def wtrigger(data, buffer, args):
    global kserver, kchannel, knick, mode, query
    if options["enabled"] == "on":
        try:
            null, srvmsg = args.split(" PRIVMSG ", 1)
        except:
            return w.WEECHAT_RC_OK

        try:
            kchannel, query = srvmsg.split(" :{} ".format(options["op_trigger"]), 1)
            mode = "op"
        except ValueError:
            try:
                kchannel, query = srvmsg.split(" :{} ".format(options["kick_trigger"]), 1)
                mode = "kick"
            except ValueError:
                try:
                    kchannel, query = srvmsg.split(" :{} ".format(options["ban_trigger"]), 1) 
                    mode = "ban"
                except ValueError:
                    try:
                        kchannel, query = srvmsg.split(" :{} ".format(options["voice_trigger"]), 1)
                        mode = "voice"
                    except ValueError:    

                        return w.WEECHAT_RC_OK

        kserver = str(buffer.split(",", 1)[0])
        knick = w.info_get("irc_nick_from_host", args)
#        query = query.replace(" ", "%20")
        query = query.replace(" ", "")
        auto_cmd = " ".format(query)

        w.hook_process(auto_cmd, 30 * 1000, "wbuffer", "")

    return w.WEECHAT_RC_OK

def wbuffer(reaction, data, command, out, er):
    rtnbuf = "{},{}".format(kserver, kchannel)
    buffer = w.info_get("irc_buffer", rtnbuf)
    botnick = w.info_get("irc_nick", kserver)
    if kchannel == botnick:

        #in private

#        command = "msg {} {}".format(knick, reaction) origineel
        if mode == 'op': command = "op {} {}".format(knick, query)
        if mode == 'kick': command = "kick {} {}".format(knick, query)
        if mode == 'ban': command = "kickban {} {}".format(knick, query)
        if mode == 'voice': command = "voice {} {}".format(knick, query)    

    else:

        #on channel

            if mode == 'op': command = "op {} {}".format(kchannel, query)
            if mode == 'kick': command = "kick {} {}".format(kchannel, query)
            if mode == 'ban': command = "kickban {} {}".format(kchannel, query)
            if mode == 'voice': command = "voice {} {}".format(kchannel, query)       

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


plugin_config = "plugins.var.python.{}".format(SCRIPT_NAME)
default_options = {"enabled": 'on',
                   "op_trigger": '!op',
                   'kick_trigger': '!kick',
                   "ban_trigger": '!ban',
                   "voice_trigger": '!voice'}


if __name__ == "__main__":
    if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
        for option, value in default_options.items():
            if not w.config_is_set_plugin(option):
                w.config_set_plugin(option, value)

        options = {"enabled": get_option("enabled"),
                   "op_trigger": get_option("op_trigger"),
                   "kick_trigger": get_option("kick_trigger"),
                   "ban_trigger": get_option("ban_trigger"),
                   "voice_trigger": get_option("voice_trigger")
                  }  
### end weechat plugin configuration stuff ####

# start
w.hook_signal("*,irc_in_privmsg", "wtrigger", "data")
w.hook_config("{}.*".format(plugin_config), "config_cb", "")
