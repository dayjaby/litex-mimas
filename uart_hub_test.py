from litex import RemoteClient

wb = RemoteClient()
wb.open()

class UART:
    def __init__(self, regs, name="uart"):
        self._txfull = getattr(regs, name + "_txfull")
        self._rxempty = getattr(regs, name + "_rxempty")
        self._rxtx = getattr(regs, name + "_rxtx")

    def txfull(self):
        return bool(self._txfull.read())

    def rxempty(self):
        return bool(self._rxempty.read())

    def write(self, c):
        if self.txfull():
            raise Exception("UART tx full")

    def read(self):
        return self._rxtx.read()
            


uart = UART(wb.regs)
print(uart.txfull())
print(uart.rxempty())
for i in range(10):
    print(i)
    uart.write('a')
    print("TX:{}".format(wb.regs.uart_tx.read()))
    print("RX:{}".format(wb.regs.uart_rx.read()))
    if not uart.rxempty():
        print(uart.read())

wb.close()
