# -*- coding: utf-8 -*-

import weechat as w

SCRIPT_NAME    = "PickNick"
SCRIPT_AUTHOR  = "innerlite"
SCRIPT_VERSION = "0.02a"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "PickNick, The short & effective nick regainer for 'headless' irc networks"

if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
              SCRIPT_DESC, '', ''):
    w.hook_signal("irc_server_connected", SCRIPT_NAME, "")
	
#zonder deze var werkt het script ook omdat de string in de conf leeg is, probleem is dat het op elke server/buffer de nick veranderd.
#test = w.config_string(w.config_get("irc.server_default.addresses"))

def timer_cb(server_name, signal):
    w.prnt('', '==>\t%s' % (server_name))
    il = w.infolist_get("irc_server", "", server_name)
    sbuffer = w.buffer_search("irc", server_name + "#")
    cur_nick = ''
    forced_nick = ''
    if w.infolist_next(il):
        cur_nick = w.infolist_string(il, 'nick')
        nicks = w.infolist_string(il, 'nicks')
        forced_nick = nicks.split(',')[0]
#        password = w.infolist_string(il, 'password')
    w.infolist_free(il)
    if (cur_nick != forced_nick):
        w.command(sbuffer, "/nick %s" % (forced_nick))
#        w.command(sbuffer, "/msg nickserv ghost %s %s" % (forced_nick, password))
#        w.command(sbuffer, "/msg nickserv identify %s" % (password))
    return w.WEECHAT_RC_OK

w.hook_timer(1000, 0, 0, 'timer_cb', '')
