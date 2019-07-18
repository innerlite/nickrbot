# -*- coding: utf-8 -*-
# Channel limiter for weechat
# This script will limit a channel to the 
# current number of users plus 5 once every min.

import weechat

server_chans = 'ircnet.#cyberworld'

def cl_cmd_cb(data, signal_data):

    buffer = weechat.buffer_search("irc", server_chans)
    count = weechat.string_eval_expression("${buffer.nicklist_count}", {"buffer": buffer}, {}, {})
    target = weechat.buffer_get_string(buffer, "name").split('.')[1]
    
    weechat.command(buffer, '/mode ' + target + ' +l ' + count)
    return weechat.WEECHAT_RC_OK

weechat.register('rxtx', 'Channel limiter', '0.01', 'GPL3', 'Channel limiter', '', '')
weechat.hook_timer(60000, 0, 0, 'cl_cmd_cb', '')

# count > total users in nicklist +3 (weechat got 3 extra 'users/groups' more in the nicklist then visible)
# todo: must work on all specified channels in var server_chans 
#  '' : script may not change a limit when its the same after last change.
