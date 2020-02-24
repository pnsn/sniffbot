import subprocess
import re

'''Sniffwave output

SCNL	 is Station.Channel.Network.Location
V1	 is the version field 1
V2	is the version field 2
P	is the pin number (obsolete)
T	 is the sample type. "s4" means that the data is four-byte signed
    integers in Sparc byte order. "i4" would indicate four-byte, Intel order
N	 is the number of sample in the packet
SR	is the nominal sampling rate, as advertised by the producer of the packet
ST, ET 	 are the actual times of the first and last samples in the packet,
    in human readable form, and (seconds since 1970)
Q1	 is the data quality field 1
Q2	 is the data quality field 2
I	 is the ID number of the Installation
M	 is the ID number of the Module
T	 is the ID number of the Type of packet
L	 is the length of packet in bytes
D	 is the latency of the data, that is the difference
    between NOW and the last sample time for that SCNL
F	 is the latency of feeding, that is the difference
    between NOW and the time when last packet for that SCNL has been received

'''


class SniffWave():

    def is_wild(self, attr):
        ''' default None to 'wild' for init '''
        return attr if attr is not None else 'wild'

    def __init__(self, eworm_host, eworm_user, eworm_ring, ssh_i_file,
                 sta, chan, net, sec):
        self.eworm_host = eworm_host
        self.eworm_user = eworm_user
        self.eworm_ring = eworm_ring
        self.ssh_i_file = ssh_i_file
        self.sta = self.is_wild(sta)
        self.chan = self.is_wild(chan)
        self.net = self.is_wild(net)
        self.sec = sec if sec is not None else 5

    def build_call(self):
        '''build ssh call to host'''
        return [
            'ssh',
            '-i',
            self.ssh_i_file,
            "{}@{}".format(self.eworm_user, self.eworm_host),
            "sniffwave",
            self.eworm_ring,
            self.sta,
            self.chan,
            self.net,
            "wild",
            str(self.sec)
        ]

    def call(self):
        '''execute call to host server'''
        command = self.build_call()
        print(command)
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        '''Since it is a subprocess, error handling must be managed
            through parsing stderr'''
        if re.search(r'Permission denied|Connection refused', str(stderr)):
            return "Connection to sniffwave server refused."
        return self.eworm_host + " " + stdout.decode("utf-8")

    def format_sms_response(self, stdout):
        '''shorten response for sms

            turn into list broken on '\n'
            pull out relative data, and join on \n
        '''
        resp_in = stdout.split("\n")
        resp_out = []
        for line in resp_in:
            resp_out += self.parse_message(line.strip())
        return '\n'.join(resp_out)

    def parse_message(self, line):
        '''take text repsonse from sniffwave and parse'''
        # intro line
        intro = re.search(r'Sniffing [A-Z]*_RING', line)
        # scnl line
        scnl = re.match(
            r'[a-zA-Z0-9]{3,5}\.[a-zA-Z0-9]{3}\.[a-zA-Z0-9]{2}\..{2}', line)
        if intro is not None:
            # split string into 2
            post = re.sub(intro.group(), '', line)
            return [intro.group(), post]
        if scnl is not None:
            '''strip out interesting parts and turn into two lines'''
            short = line.split()
            list1 = [
                short[0],
                short[5],
                short[6],
                short[7],
                short[8]
            ]
            list2 = [
                short[10],
                short[11],
                short[-5],
                short[-4],
                short[-3],
                short[-2],
                short[-1]

            ]
            line1 = ' '.join(list1)
            line2 = ' '.join(list2)
            # indent the second line
            return [line1, '\t' + line2]
        return [re.sub(r'\t', '', line)]
