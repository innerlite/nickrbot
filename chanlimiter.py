# -*- coding: utf-8 -*-
# Channel limiter for weechat
# This script will limit a channel to the 
# current number of users plus 5 once every min.

import weechat

count = 0 
new_count = 0 
server_chan = 'ircnet.#cyberworld'

def cl_cmd_cb(data, signal_data):
    global count
    global new_count
    buffer = weechat.buffer_search("irc", server_chan)
    new_count = weechat.string_eval_expression("${buffer.nicklist_count}", {"buffer": buffer}, {}, {})
    target = weechat.buffer_get_string(buffer, "name").split('.')[1]
    
    if count != new_count:
        weechat.command(buffer, '/mode ' + target + ' +l ' + new_count)
        count = new_count
    return weechat.WEECHAT_RC_OK

weechat.register('rxtx', 'Channel limiter', '0.01', 'GPL3', 'Channel limiter', '', '')
weechat.hook_timer(60000, 0, 0, 'cl_cmd_cb', '')

# count > total users in nicklist +3 (weechat got 3 extra 'users/groups' more in the nicklist then visible)
# todo: must work on all specified channels
