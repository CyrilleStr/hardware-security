import logging
import pyvisa
from pyvisa import constants

__author__ = "Marina Shchavleva"
__maintainer__ = "Marina Shchavleva"
__email__ = "shchamar@fit.cvut.cz"
__status__ = "garbage"

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_oscilloscopes():
    rm = pyvisa.ResourceManager()
    return rm.list_resources(query = '?*::INSTR')


class Oscilloscope:
    def __init__(self):
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources(query='USB?*::INSTR')
        
        self.resource =  None

        for instr in resources:
            print(f"Trying {instr}...")
            try:
                self.resource =  rm.open_resource(
                    instr, # oscilloscope_id used to be here
                    read_termination = '\n',
                    write_termination = '\n')
                break
            except:
                continue
                
        if self.resource is None:
            raise Exception("No instrument found.")


        self.resource.timeout = 20000
        if self.resource.timeout == None:
            logger.debug('timeout set to eternity')
        else:
            logger.debug('timeout set to %dms', self.resource.timeout)

        self.resource.query_delay = 0.1
        logger.debug('query_delay set to %fs', self.resource.query_delay)
        self.write('*CLS')
        print('connected to the oscilloscope with *IDN:',
            self.query('*IDN?'))

    def __del__(self):
        self.close()

    def close(self):
        logger.debug('closing oscilloscope connection...')
        self.resource.close()

    def write(self, *args):
        logger.debug('%s', ', '.join(map(str, args)))
        return self.resource.write(*args)

    def query(self, *args):
        logger.debug('%s...', ', '.join(map(str, args)))
        data = self.resource.query(*args)
        logger.debug('%s %s', args[0], data)
        return data

    def command_binary(self, query, data: bytes):
        logger.debug('%s, len: %d', query, len(data))
        return self.resource.write_binary_values(
                query,
                data,
                datatype='B')

    def query_binary(self, query):
        logger.debug('%s...', query)
        data = self.resource.query_binary_values(
                query,
                datatype='B',
                container = bytes)
        logger.debug('%s, len: %d', query, len(data))
        return data

    def query_check(self, command):
        print(command, self.resource.query(command+'?'))

    def print_error_queue(self):
        err = self.query(':SYST:ERR?')
        while err.split(',')[0] != '+0':
            print(err)
            err = self.query(':SYST:ERR?')

    def command_check(self, command, value):
        data = self.resource.write(command + ' ' + value)
        self.query_check(command)
        self.print_error_queue()
        return data

    def save_conf(self, filename):
        logger.debug('to filename %s', filename)
        data = self.query_binary(':SYSTem:SETup?')
        out_file = open(filename, 'wb')
        len_written = out_file.write(data)
        out_file.close()
        logger.debug('read %d, written %d', len(data), len_written)
        return len(data) - len_written

    def load_conf(self, filename):
        logger.debug('from filename %s', filename)
        in_file = open(filename, 'rb')
        data = in_file.read()
        len_written = self.command_binary(':SYSTem:SETup', data)
        in_file.close()
        logger.debug('read %d, written %d', len(data), len_written)
        return len(data) - len_written

    def setup_measurement(self):
        logger.debug('')
        self.command_check(":ACQuire:TYPE", "NORMal")
        self.command_check(":ACQuire:COUNt", "2")
        self.command_check(":TIMebase:MODE", "MAIN")
        self.command_check(":WAVeform:UNSigned", "1")
        self.command_check(":WAVeform:BYTeorder", "LSBFirst")
        self.command_check(":WAVeform:FORMat", "BYTE")
        self.command_check(":WAVeform:SOURce", "CHANnel1")
        self.command_check(":WAVeform:POINts:MODE", "RAW")
        self.command_check(":ACQuire:COMPlete", "100")
        self.command_check(":WAVeform:POINts", "300000")
