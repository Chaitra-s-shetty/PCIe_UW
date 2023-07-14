import sys
from migen import *
from migen.fhdl import verilog

from litepcie.tlp.common import *
from litepcie.tlp.depacketizer import LitePCIeTLPDepacketizer

def main():
    args = sys.argv[1:]
    if len(args) == 1:
        # input_data_width = int(args[0])

        # Module instance ----------------------------------------------------------------
        depacketizer = LitePCIeTLPDepacketizer(data_width=64, endianness="little", address_mask=0)
        module_name = "tlp_depacketizer_" 
        ios = set()
        ios = set(depacketizer.sink.flatten()) | set(depacketizer.req_source.flatten()) | set(depacketizer.cmp_source.flatten())
        verilog.convert(depacketizer, ios, name=module_name).write(module_name+'.v')
        print("Finished generating Verilog files.")


if __name__ == "__main__":
    main()

