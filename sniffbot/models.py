import os
import csv
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

    LOG_PATH = os.getenv("SNIFF_LOG_PATH")

    def is_wild(self, attr):
        '''default None to 'wild' '''
        return attr if attr is not None else 'wild'

    def __init__(self, sta):
        self.sta = self.is_wild(sta)

    def parse_log(self):
        ''' Log lines of form:

        ['RCM.HHN.UW.-- 2020/02/05 07:18:00.30 752 [D: 1.2s F: 1.8s]']
        '''
        response = ''
        full_path = os.path.join(os.path.dirname(__file__),
                                 self.LOG_PATH)
        with open(full_path) as csvfile:
            sniffwave = csv.reader(csvfile)
            # find all unique channels and keep the latest one
            unique_chan = {}
            # filter station name out
            regex = r'' + re.escape(self.sta) + \
                    r'\.[a-zA-Z0-9]{3}\.[a-zA-Z0-9]{2}\..{2}'
            for line in sniffwave:
                try:
                    m = re.match(regex, line[0])
                    chan = m.group()
                    if m:
                        unique_chan[chan] = line[0]
                except IndexError:
                    pass
                '''overwrite each value assumes write in cron order'''
                # unique_chan[sniff] = sniff

            for chan in unique_chan.values():
                response += "".join(chan) + "\n"
            return response
