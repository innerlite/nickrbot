# -*- coding: utf-8 -*-
# innerlite Amsterdam 2019, poort587@gmail.com
# Picknick is an oldschool nick regainer, it will check every 2 minutes
# to take back the configurated nickname 
# in your weechat settings for networks without NickServ.

import weechat as w

w.register('picknick', 'innerlite', '1.0b', 'GPL3', 'Simplest nick regainer for networks without NickServ', '', '')

cnetwork = 'ircnet,# ' #replace only the name ircnet with your own added network name.

def ccheck(server_name, data):
    ci = w.infolist_get('irc_server', '', server_name)
    pbuffer = w.info_get('irc_buffer', cnetwork)
    cnick = ''
    cfnick = ''
    if w.infolist_next(ci):
        cnick = w.infolist_string(ci, 'nick')
        cnicks = w.infolist_string(ci, 'nicks')
        cfnick = cnicks.split(',')[0]
    w.infolist_free(ci)
    if (cnick != cfnick):
        w.command(pbuffer, '/nick %s' % (cfnick))
    return w.WEECHAT_RC_OK

w.hook_timer(120000, 0, 0, 'ccheck', '') #change the timer interval here in milliseconds (120000 = 2min. = default).
