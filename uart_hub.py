from migen import *
# from litex.soc.cores.spi_flash import SPIFlash
from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform

from litex.soc.integration.soc_core import SoCMini
from litex.soc.integration.builder import Builder
from litex.soc.cores.uart import UARTWishboneBridge
from litex.soc.cores.uart import UARTPHY, UART
from litex.soc.cores.spi import SPIMaster


_io = [
    ("clk100", 0, Pins("P126"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("P104"), IOStandard("LVCMOS33"), # GPIO-N21
                  Misc("SLEW=FAST")),
        Subsignal("rx", Pins("P101"), IOStandard("LVCMOS33"),  # GPIO-N20
                  Misc("SLEW=FAST"))),
    ("spiflash", 0,
        Subsignal("cs_n", Pins("P38"), IOStandard("LVCMOS33")), # SCS - IO_L65N_CSO_B_2
        Subsignal("clk",  Pins("P70"), IOStandard("LVCMOS33")), # SCK - IO_L1P_CCLK_2
        Subsignal("mosi", Pins("P64"), IOStandard("LVCMOS33")), # SDO - IO_L3N_MOSI_CSI_B_MISO0_2
        Subsignal("miso", Pins("P65"), IOStandard("LVCMOS33"))  # SDI - IO_L3P_D0_DIN_MISO_MISO1_2
    ),
    (("uart0", 0,
        Subsignal("tx", Pins("P100"), IOStandard("LVCMOS33")), # GPIO-P21
        Subsignal("rx", Pins("P102"), IOStandard("LVCMOS33"))  # GPIO-P20
    )),

    ("user_btn", 0, Pins("P124"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("user_btn", 1, Pins("P123"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("user_btn", 2, Pins("P121"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("user_btn", 3, Pins("P120"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("user_btn", 4, Pins("P73"), IOStandard("LVCMOS33"), Misc("PULLUP")),

    ("user_led", 0, Pins("P119"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 1, Pins("P118"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 2, Pins("P117"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 3, Pins("P116"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 4, Pins("P115"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 5, Pins("P114"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 6, Pins("P112"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 7, Pins("P111"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 8, Pins("P99"), IOStandard("LVCMOS33"), Drive(8)), # GPIO-N35
    #("user_led", 9, Pins("P100"), IOStandard("LVCMOS33"), Drive(8)),
    #("user_led", 10, Pins("P102"), IOStandard("LVCMOS33"), Drive(8)),

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

        self.submodules.crg = CRG(platform.request("clk100"), ~platform.request("user_btn", 0))

        self.submodules.serial_bridge = UARTWishboneBridge(platform.request("serial", 0), sys_clk_freq)
        self.add_wb_master(self.serial_bridge.wishbone)

        self.submodules.spiflash = SPIMaster(platform.request("spiflash"),
            data_width   = 32,
            sys_clk_freq = sys_clk_freq,
            spi_clk_freq = 1e6)
        self.add_csr("spiflash")

        self.add_uart("uart0")
        """uart0 = platform.request("uart0", 0)
        self.submodules.uart0_phy = UARTPHY(uart0, sys_clk_freq, baudrate=9600)
        self.submodules.uart0 = UART(
            phy=self.uart0_phy,
            tx_fifo_depth=16,
            rx_fifo_depth=16,
            phy_cd="sys")

        self.add_csr("uart0_phy")
        self.add_csr("uart0")"""

        btn1 = platform.request("user_btn", 1)
        led6 = platform.request("user_led", 6)
        led7 = platform.request("user_led", 7)
        led0 = platform.request("user_led", 0) 
        # led8 seems to be wrong?
        self.comb += [
            led0.eq(btn1)
        ]

soc = BaseSoC(platform)

builder = Builder(soc, output_dir="build", csr_csv="csr.csv")
builder.build(build_name="top")
# platform.build(module)
