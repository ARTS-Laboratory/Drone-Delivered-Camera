import board
import digitalio
import unireedsolomon as rs

from circuitpython_nrf24l01.rf24 import RF24

class NRF_communicate:
    
    #the initilization must include either signs or manifest
    def __init__(self, ce, csn, tx_pipe, rx_pipe, spi = board.SPI(), 
                 channel = 76, pa_level = -12, signs = None, manifest = None, encode = True):
        self.encode = encode
        if(encode):
            self.coder = rs.RSCoder(13,7)
        self.channel = 76
        self.nrf = RF24(spi, csn, ce)
        self.nrf.pa_level = pa_level # set power level (in decibels)
        self.nrf.open_tx_pipe(tx_pipe)
        self.nrf.open_rx_pipe(1, rx_pipe) # right now we only use pipe 1.
        self.nrf.dynamic_payloads = False
        self.nrf.allow_ask_no_ack = False
        self.nrf.payload_length = 16
        if(signs != None):
            self.manifest = Manifest(signs)
        elif(manifest != None):
            self.manifest = manifest
        else:
            raise Exception("Must include either signs or manifest in NRF_communicate initialization.")
    
    def is_sign(self, sig):
        if(sig == None):
            return False, ""
        if(self.encode):
            decoded = self.coder.decode_fast(sig.decode())[0]
        else:
            decoded = sig.decode()[:7]
        is_sig = self.manifest.contains_sign(decoded)
        print(decoded)
        return is_sig, decoded
    
    def block_until_sign(self):
        self.nrf.listen = True
        keep_looping = True
        sign = ""
        while(keep_looping):
            if self.nrf.available():
                # grab information about the received payload
                # payload_size, pipe_number = (self.nrf.any(), self.nrf.pipe)
                # fetch 1 payload from RX FIFO
                payload = self.nrf.read()  # also clears nrf.irq_dr status flag
                is_sig, sign = self.is_sign(payload)
                if(is_sig):
                    keep_looping = False
        self.manifest.on_sign(sign)
        return sign
    
    def add_sign(self, sign):
        self.manifest.add_sign(sign)
    
    # NOT WRITTEN
    def tx():
        pass
    # NOT WRITTEN
    def rx():
        pass
    
class Sign:
    
    def __init__(self, name, act_on_sign=False, funct=None, args = [], is_semi = False):
        self.act_on_sign = act_on_sign
        self.funct = funct
        self.args = args # add protection for length 1 tuple
        self.is_semi = is_semi
        if(is_semi):
            self.name = name
        elif(name[4:] == '---'):
            self.is_semi = True
            self.name = name[:4]
        else:
            self.name = name
            
    def on_sign(self, semisig = '---'):
        if(self.act_on_sign):
            if(self.is_semi):
                self.funct(*self.arg, semisig = semisig)
            else:
                self.funct(*self.args)
class Manifest:
    
    def __init__(self, signs):
        self.sign_dict = {}
        for sign in signs:
            self.sign_dict[sign.name] = sign
    
    def contains_sign(self, name):
        return (name[:4] in self.sign_dict.keys()) or (name in self.sign_dict.keys())
    
    def on_sign(self, name):
        if(name[:4] in self.sign_dict.keys()):
            self.sign_dict[name[:4]].on_sign(semisig = name[4:])
        else:
            self.sign_dict[name].on_sign()
    
    def add_sign(self, sign):
        self.sign_dict[sign.name] = sign
    
    # NOT WRITTEN
    def get_sign_names():
        pass