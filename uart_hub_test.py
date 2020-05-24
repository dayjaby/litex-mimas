from litex import RemoteClient

wb = RemoteClient(debug=True)
wb.open()

class UART:
    def __init__(self, regs, name="uart0"):
        self._txfull = getattr(regs, name + "_txfull")
        self._rxempty = getattr(regs, name + "_rxempty")
        self._rxtx = getattr(regs, name + "_rxtx")

    def txfull(self):
        return bool(self._txfull.read())

    def rxempty(self):
        return bool(self._rxempty.read())

    def write(self, c):
        self._rxtx.write(c)

    def read(self):
        return self._rxtx.read()
            


uart = UART(wb.regs)
print("TX Full: {}".format(uart.txfull()))
print("RX Empty: {}".format(uart.rxempty()))
for i in range(10):
    #if not uart.txfull():
    uart.write(0x76)
    #if not uart.rxempty():
    #    print(uart.read())

wb.close()
