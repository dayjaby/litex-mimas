from migen import *
from migen.genlib.fifo import SyncFIFO

from litex.soc.cores.uart import UARTPHY, UART, UARTPads

class UARTModule(Module):
    def __init__(self, sys_clk_freq, baudrate):

        self.submodules.uart0_phy = UARTPHY(UARTPads(), sys_clk_freq, baudrate=baudrate)
        self.submodules.uart0 = UART(
            phy=self.uart0_phy,
            tx_fifo_depth=16,
            rx_fifo_depth=16,
            phy_cd="sys")


if __name__ == '__main__':
    dut = UARTModule(100e6, 115200)

    def dut_tb(dut):
        yield from dut.uart0._rxtx.write(0x01)
        yield from [None] * 4096

    run_simulation(dut, dut_tb(dut), vcd_name="uart.vcd")
