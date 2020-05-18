from migen import *
from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform

_io = [
    ("clk100", 0, Pins("P126"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("P44"), IOStandard("LVCMOS33"),
                  Misc("SLEW=FAST")),
        Subsignal("rx", Pins("P43"), IOStandard("LVCMOS33"),
                  Misc("SLEW=FAST"))),

    # Despite being marked as "sw" these are actually buttons which need
    # debouncing.
    # sw1 (user_btn:0) through sw6 (user_btn:5)
    ("user_btn", 0, Pins("P124"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("user_btn", 1, Pins("P123"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("user_btn", 2, Pins("P121"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("user_btn", 3, Pins("P120"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    # Use SW6 as the reset button for now.
    ("user_btn", 4, Pins("P73"), IOStandard("LVCMOS33"), Misc("PULLUP")),

    # LEDs 1 through 8
    ("user_led", 0, Pins("P119"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 1, Pins("P118"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 2, Pins("P117"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 3, Pins("P116"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 4, Pins("P115"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 5, Pins("P114"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 6, Pins("P112"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 7, Pins("P111"), IOStandard("LVCMOS33"), Drive(8)),

]

_connectors = [
#    ("P6", "T3 R3 V5 U5 V4 T4 V7 U7"),
#    ("P7", "V11 U11 V13 U13 T10 R10 T11 R11"),
#    ("P8", "L16 L15 K16 K15 J18 J16 H18 H17")
]


class Platform(XilinxPlatform):
    name = "mimas"
    default_clk_name = "clk100"
    default_clk_period = 10

    # The MimasV2 has a XC6SLX9 which bitstream takes up ~2.6Mbit (1484472 bytes)
    # 0x80000 offset (4Mbit) gives plenty of space
    gateware_size = 0x80000

    # M25P16 - component U1
    # 16Mb - 75 MHz clock frequency
    # FIXME: Create a "spi flash module" object in the same way we have SDRAM
    # module objects.
    #	/*             name,  erase_cmd, chip_erase_cmd, device_id, pagesize, sectorsize, size_in_bytes */
    #	FLASH_ID("st m25p16",      0xd8,           0xc7, 0x00152020,   0x100,    0x10000,      0x200000),
    spiflash_model = "m25p16"
    spiflash_read_dummy_bits = 8
    spiflash_clock_div = 4
    spiflash_total_size = int((16/8)*1024*1024) # 16Mbit
    spiflash_page_size = 256
    spiflash_sector_size = 0x10000

    def __init__(self):
        XilinxPlatform.__init__(self, "xc6slx9-tqg144", _io, toolchain="ise")

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)

    def create_programmer(self):
        raise NotImplementedError

platform = Platform()
led = platform.request("user_led")
# Create our module (fpga description)
module = Module()

# Create a counter and blink a led
counter = Signal(26)
module.comb += led.eq(counter[25])
module.sync += counter.eq(counter + 1)

platform.build(module)
