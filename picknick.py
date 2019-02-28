# -*- coding: utf-8 -*-
# innerlite Amsterdam 2019, poort587@gmail.com
# Picknick is an oldschool nick regainer, it will check every 3 minutes
# to get the taken nick back on the setted network without NickServ.

import weechat as w

cname    = "picknick"
cauthor  = "innerlite"
cversion = "1.0b"
clicense = "GPL3"
cdesc    = "picknick, The short & effective nick regainer"

if w.register(cname, cauthor, cversion, clicense,
              cdesc, '', ''):
    w.hook_signal("irc_server_connected", cname, "")

def ccheck(server_name, signal):
    ci = w.infolist_get("irc_server", "", server_name)
    pbuffer = w.info_get("irc_buffer", "ircnet,# ")
    cnick = ''
    cfnick = ''
    if w.infolist_next(ci):
        cnick = w.infolist_string(ci, 'nick')
        nicks = w.infolist_string(ci, 'nicks')
        cfnick = nicks.split(',')[0]
    w.infolist_free(ci)
    if (cnick != cfnick):
        w.command(pbuffer, "/nick %s" % (cfnick))
    return w.WEECHAT_RC_OK

w.hook_timer(180000, 0, 0, 'ccheck', '')
