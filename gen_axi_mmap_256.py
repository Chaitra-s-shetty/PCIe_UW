import sys
from migen import *
from migen.fhdl import verilog
from litex.soc.interconnect import axi, stream
from litepcie.common import *
from litepcie.frontend.dma import descriptor_layout, LitePCIeDMAWriter, LitePCIeDMAReader
from litex.soc.interconnect.csr import *
from litepcie.tlp.depacketizer import LitePCIeTLPDepacketizer
from litepcie.tlp.packetizer import LitePCIeTLPPacketizer
from litepcie.core.crossbar import LitePCIeCrossbar
from litepcie.frontend.axi import LitePCIeAXISlave
from litepcie.core import LitePCIeEndpoint
from litepcie.core.msi import LitePCIeMSI
from test.common import seed_to_data
from test.model.host import *
from test.model.phy import PHY

def main():
    args=sys.argv[1:]
    if(len(args)==1):
        axi_data_width=int(args[0])
        # PHY -----------------------------------------------------------------------------
        phy = PHY(data_width=128, id=0, bar0_size=1*MB, debug=False)
        # Endpoint -------------------------------------------------------------------------
        endpoint = LitePCIeEndpoint(phy,
            address_width        = 32,
            max_pending_requests = 8
        )
        #module instance ----------------------------------------------------------------
        axi_mmap=LitePCIeAXISlave(endpoint, data_width=axi_data_width, id_width=4)
        module_name='axi_mmap_'+str(axi_data_width)
        ios=set()
        ios=set(axi_mmap.axi.aw.flatten())|set(axi_mmap.axi.ar.flatten())|set(axi_mmap.axi.r.flatten())|set(axi_mmap.axi.w.flatten())|set(axi_mmap.axi.b.flatten())|set(axi_mmap.dma_rd.port.sink.flatten())|set(axi_mmap.dma_wr.port.source.flatten())
        #ios.add(axi_mmap.dma_rd)
        print("generate axi port with axi data width=",args[0])
        verilog.convert(axi_mmap,ios,name=module_name).write(module_name+'.v')
        print("Finished generating ", module_name,".v")
        
if __name__ == "__main__":
    main()
