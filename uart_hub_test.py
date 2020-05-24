from litex import RemoteClient

wb = RemoteClient(debug=True)
wb.open()

class UART:
    def __init__(self, regs, name):
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
            


uart0 = UART(wb.regs, "uart0")
uart0.write(0x76)
uart0.read()

uart1 = UART(wb.regs, "uart1")
uart1.write(0x76)
uart1.read()

uart2 = UART(wb.regs, "uart2")
uart2.write(0x76)
uart2.read()

uart3 = UART(wb.regs, "uart3")
uart3.write(0x76)
uart3.read()

wb.close()
