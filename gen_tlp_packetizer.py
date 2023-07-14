import sys
from migen import *
from migen.fhdl import verilog
from litepcie.common import *
from litepcie.core.common import *
from litex.gen.genlib.misc import chooser
from litepcie.tlp.common import *
from litepcie.tlp.packetizer import LitePCIeTLPPacketizer

def main():
    args=sys.argv[1:]
    if(len(args)==1):
        #axi_data_width=int(args[0])
       packetizer=LitePCIeTLPPacketizer(data_width=64, endianness="little", address_width=32)
       module_name = 'packetizer_1'

       ios=set()
       ios=set(packetizer.req_sink.flatten())|set(packetizer.cmp_sink.flatten())|set(packetizer.source.flatten())
       print("generate axi port with axi data width=", args[0])
       verilog.convert(packetizer, ios, name=module_name).write(module_name + '.v')
       print("Finished generating ", module_name, ".v")

if __name__ == "__main__":
    main()
