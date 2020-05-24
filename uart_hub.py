from migen import *
from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform

from litex.soc.integration.soc_core import SoCMini
from litex.soc.integration.builder import Builder
from litex.soc.cores.uart import UARTWishboneBridge
from litex.soc.cores.uart import UARTPHY, UART

_io = [
    ("clk100", 0, Pins("P126"), IOStandard("LVCMOS33")),

    # for WishboneUARTBridge
    ("serial", 0,
        Subsignal("tx", Pins("P104"), IOStandard("LVCMOS33"), # GPIO-N21
                  Misc("SLEW=FAST")),
        Subsignal("rx", Pins("P101"), IOStandard("LVCMOS33"),  # GPIO-N20
                  Misc("SLEW=FAST"))),
    ("uart0", 0,
        Subsignal("tx", Pins("P100"), IOStandard("LVCMOS33"), # GPIO-P21
                  Misc("SLEW=FAST")),
        Subsignal("rx", Pins("P102"), IOStandard("LVCMOS33"),  # GPIO-P20
                  Misc("SLEW=FAST"))),
]

class Platform(XilinxPlatform):
    name = "mimas"
    default_clk_name = "clk100"
    default_clk_period = 10

    def __init__(self):
        XilinxPlatform.__init__(self, "xc6slx9-tqg144", _io, toolchain="ise")

platform = Platform()

class BaseSoC(SoCMini):
    def __init__(self, platform, **kwargs):
        sys_clk_freq = int(100e6)
        SoCMini.__init__(self, platform, sys_clk_freq, csr_data_width=32,
            ident="My first LiteX System On Chip", ident_version=True)

        serial = platform.request("serial", 0)
        self.submodules.serial_bridge = UARTWishboneBridge(serial, sys_clk_freq)
        self.add_wb_master(self.serial_bridge.wishbone)

        self.submodules.uart0 = ResetInserter()(UART(
            phy=UARTPHY(platform.request("uart0", 0), sys_clk_freq, baudrate=9600),
            tx_fifo_depth=16,
            rx_fifo_depth=16,
            phy_cd="sys"))
        self.add_constant("UART_POLLING")

        self.add_csr("uart0")

soc = BaseSoC(platform)

builder = Builder(soc, output_dir="build", csr_csv="csr.csv")
builder.build(build_name="top")
