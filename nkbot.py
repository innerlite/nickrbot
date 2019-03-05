import weechat

weechat.register('hal', 'hal9000', '6.6.6', 'GPL3', 'HAL Script', '', '')

users = [ '*!*@62-193-124-217.dsl.fionz.nl', '*!*@draxlerzer.de' ]

def priv_cb(data, signal, signal_data):

    args = signal_data.split(' ')[0:3]
    nick = args[0][1:].split('!')[0]
    user = args[0][1:].split('!')[1].split('@')[0]
    host = args[0][1:].split('!')[1].split('@')[1]
    target = args[2]
    message = signal_data[1:]
    message = message[message.find(':') + 1:]

    # weechat.prnt('', 'HAL\t' + signal_data)
    # weechat.prnt('', 'HAL\t' + nick + ' +++ ' + user + ' +++ ' + host + ' +++ ' + target)

    if any(host in s for s in users):
        if message[0] == '/':
            weechat.command('', message)
        # weechat.prnt('', 'HAL\tMatch!')
        # weechat.prnt('', 'HAL\t' + message)
    # 
    return weechat.WEECHAT_RC_OK

weechat.hook_signal('*,irc_in2_privmsg', 'priv_cb', '')

