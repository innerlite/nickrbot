# -*- coding: utf-8 -*-

# Channel limiter for weechat
# This script will limit a channel to the 
# current number of users plus 5 once every min.

import weechat

weechat.register('rxtx', 'Channel limiter', '0.01', 'GPL3', 'Channel limiter', '', '')

def cl_timer_cb(data, remaining_calls):
    weechat.command('', 'cl_cmd_cb', '')
    return weechat.WEECHAT_RC_OK

weechat.hook_timer(60000, 0, 0, 'cl_timer_cb', '')

def cl_cmd_cb(data, signal, signal_data):
    server = signal.split(",")[0]
    msg = weechat.info_get_hashtable("irc_message_parse", {"message": signal_data})
    buffer = weechat.info_get("irc_buffer", "%s,%s" % (server, msg["channel"]))
    count = weechat.string_eval_expression("${buffer.nicklist_count}", {"buffer": buffer}, {}, {})
    
    weechat.prnt(buffer, 'total users: ' +  count)

    return weechat.WEECHAT_RC_OK
