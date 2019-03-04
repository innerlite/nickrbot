import weechat as w

w.register('hal', 'hal9000', '6.6.6', 'GPL3', 'HAL Script', '', '')

users = [ '24-96-22-211.telfoort.nl', 'marktpflantz.de' ]

def priv_cb(data, signal, signal_data):
    args = signal_data.split(' ')[0:3]
    nick = args[0][1:].split('!')[0]
    user = args[0][1:].split('!')[1].split('@')[0]
    host = args[0][1:].split('!')[1].split('@')[1]
    message = signal_data[1:]
#   message = message[message.find(':') + 1:]
    w.prnt('', 'HAL\t' + signal_data)
#   w.prnt('', 'HAL\t' + nick + ' +++ ' + user + ' +++ ' + host)
    if any(host in s for s in users):
    w.command('','/' + message)
    return w.WEECHAT_RC_OK

w.hook_signal('*,irc_in2_privmsg', 'priv_cb', '')
