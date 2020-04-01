
class LocalCommand:

    def __init__(self, command):
        self.command = command.decode()


class Command:

    def __init__(self, device, command):

        self.device = device
        self.command = command.split(',')
    
    def getCommand(self):
        return self.command[0]
    
    def getDeviceCommand(self):
        if len(self.command) == 1:
            return self.command[0].encode()
        else:
            return self.command[0].encode() + b' ' + ' '.join(self.command[1:]).encode()
        
    def __str__(self):
        return 'Command for %s -> %s' % (self.device, self.command)



