from migen import *
from migen.genlib.fifo import SyncFIFO

class UARTModule(Module):
    def __init__(self, sys_clk_freq, baudrate, data_bits=8, stop_bits=1):
        # Module's interface
        self.tx_data = Signal(data_bits)
        self.tx_en = Signal()
        self.tx = Signal()
        self.submodules.tx_fifo = SyncFIFO(16, data_bits)

        # # #

        ce     = Signal()
        n = sys_clk_freq / baudrate
        tx_n = Signal(max=data_bits+stop_bits) # enough to count to 10
        counter_preload = int(n - 1)
        counter = Signal(max=int(n - 1))

        # Combinatorial assignements
        self.comb += ce.eq(counter == 0)

        # Synchronous assignments
        self.sync += [
            If(~self.tx_en,
                self.tx.eq(1)
            ).Else(
                If(ce,
                    If(tx_n == 0,
                        tx_n.eq(tx_n + 1),
                        self.tx.eq(0),
                    ).Elif(tx_n == (data_bits+stop_bits),
                        tx_n.eq(0),
                        self.tx.eq(1),
                        self.tx_en.eq(0)
                    ).Else(
                        self.tx.eq(self.tx_data[0]),
                        self.tx_data.eq(Cat(self.tx_data[1:], 0)),
                        tx_n.eq(tx_n + 1)
                    ),
                    counter.eq(counter_preload)
                ).Else(
                    counter.eq(counter - 1)
                )
            )
        ]

if __name__ == '__main__':
    dut = UARTModule(100e6, 115200)

    def dut_tb(dut):
        c = Signal(8)
        c = 0x11

        for i in range(1024):
            yield
        yield dut.tx_data.eq(c)
        yield dut.tx_en.eq(1)
        for i in range(4096*3):
            yield

    run_simulation(dut, dut_tb(dut), vcd_name="tick.vcd")
