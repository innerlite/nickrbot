# -*- coding: utf-8 -*-

import weechat as w

SCRIPT_NAME    = "NickrBot"
SCRIPT_AUTHOR  = "innerlite"
SCRIPT_VERSION = "0.01"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "NickrBot, The short & effective Nick(regain) Grabber for headless irc networks"

if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
              SCRIPT_DESC, '', ''):
    w.hook_signal("irc_server_connected", SCRIPT_NAME, "")

def timer_cb(data, signal, server_name):
    il = w.infolist_get("irc_server", "", server_name)
    sbuffer = w.buffer_search("irc", server_name + "#")
    if w.infolist_next(il):
        cur_nick = w.infolist_string(il, 'nick')
        nicks = w.infolist_string(il, 'nicks')
        forced_nick = nicks.split(',')[0]
#        password = w.infolist_string(il, 'password')
    w.infolist_free(il)
    if (cur_nick != forced_nick):
#        w.command(sbuffer, "/msg nickserv ghost %s %s" % (forced_nick, password))
        w.command(sbuffer, "/nick %s" % (forced_nick))
#        w.command(sbuffer, "/msg nickserv identify %s" % (password))
    return w.WEECHAT_RC_OK
	
w.hook_timer(3*100000, 0, 0, 'timer_cb', '')
