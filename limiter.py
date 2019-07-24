import weechat 

weechat.register('nickback', 'innerlite', '0.02',
           'GPL3', 'Get your nick back!', "", "")

def get_notify_list():
    infolist = weechat.infolist_get('irc_notify', "", "")
    if not infolist:
        return
    common.clear()
    while weechat.infolist_next(infolist):
        nick = weechat.infolist_string(infolist, 'nick')
#        server = weechat.infolist_string(infolist, 'server_name')
    weechat.infolist_next(infolist)
    weechat.infolist_free(infolist)

def notify_quit_cb(data, signal, signal_data):
    server, nick = signal_data.split(",")
    buf = weechat.info_get("irc_buffer", server + ",," + nick)
    if buf is None:
        return weechat.WEECHAT_RC_OK
    weechat.command(buf, '/wait 3 /nick ' + nick)
    weechat.command(buf, '/wait 4 /notify del ' + nick)
    return weechat.WEECHAT_RC_OK

def notify_cmd_cb(*args, **kwargs):
    get_notify_list()
    return weechat.WEECHAT_RC_OK

weechat.hook_signal('irc_notify_quit', 'notify_quit_cb', '')
weechat.hook_command_run('/notify add ', 'notify_cmd_cb', '')
weechat.hook_command_run('/notify del ', 'notify_cmd_cb', '')
get_notify_list()
