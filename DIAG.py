import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import socket
import time
import struct
import os


form_class = uic.loadUiType("./ui/Client.ui")[0]

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
global Did1
global Did2
global Did3
global Did4

FIRST_PACKET =  bytearray(
    [0xcc, 0x33, 0x80, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x07, 0xdf, 0x02, 0x10, 0x03, 0x55, 0x55, 0x55, 0x55, 0x55]
    )
#cc 33 80 01 00 00 00 0a 07 df 03 28 03 01 55 55 55 55
SECOND_PACKET = bytearray(
    [0xcc, 0x33, 0x80, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x07, 0xdf, 0x03, 0x28, 0x03, 0x01, 0x55, 0x55, 0x55, 0x55]
    )

FINAL_MSG= bytearray(
    [0xcc, 0x33, 0x80, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x07, 0xdf, 0x05, 0x2e, 0xf1, 0x8A, 0x32, 0x11, 0x55, 0x55]
    )

SW_VERSION =  bytearray(
    [0xcc, 0x33, 0x80, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x07, 0xdf, 0x03, 0x22, 0xf1, 0x95, 0x55, 0x55, 0x55, 0x55]
    )

INT_VERSION =  bytearray(
    [0xcc, 0x33, 0x80, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x07, 0xdf, 0x03, 0x22, 0xf1, 0x96, 0x55, 0x55, 0x55, 0x55]
    )

SW1_WRITE =  bytearray(
    [0xcc, 0x33, 0x80, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x07, 0xdf, 0x04, 0x2e, 0xf1, 0xb1, 0x03, 0x55, 0x55, 0x55]
    )

SW2_WRITE =  bytearray(
    [0xcc, 0x33, 0x80, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x07, 0xdf, 0x04, 0x2e, 0xf1, 0xb1, 0x04, 0x55, 0x55, 0x55]
    )

SW1_VER_READ =  bytearray(
    [0xcc, 0x33, 0x80, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x07, 0xdf, 0x03, 0x22, 0xff, 0x01, 0x55, 0x55, 0x55, 0x55]
    )

SW2_VER_READ =  bytearray(
    [0xcc, 0x33, 0x80, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x07, 0xdf, 0x03, 0x22, 0xff, 0x02, 0x55, 0x55, 0x55, 0x55]
    )

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        QMainWindow.__init__(self) #QT_Designer Class name
        self.setupUi(self)
        self.pushButton.clicked.connect(self.VersionRead_click)
        self.pushButton_2.clicked.connect(self.InterRead_click)
        self.pushButton_3.clicked.connect(self.Closebtn_click)
        self.pushButton_4.clicked.connect(self.Sw1Read_click)
        self.pushButton_5.clicked.connect(self.Sw2Read_click)
        self.pushButton_6.clicked.connect(self.Sw1Write_click)
        self.pushButton_7.clicked.connect(self.Sw2Write_click)

        self.pushButton_8.clicked.connect(self.RegRead_click)
        self.comboBox.addItems(['','sw1_reg8','sw1_reg16','sw1_reg32','sw2_reg8','sw2_reg16','sw2_reg32'])
        self.comboBox.currentIndexChanged.connect(self.SwitchReg_sel)

    def VersionRead_click(self):
        data = ComControlService(SW_VERSION)

        text = "MCU_Version : "
        list =  text + chr(data[15])+ "." + chr(data[16]) + chr(data[17])
        self.textEdit.setText(list)
        self.textEdit_2.setText("MCUversion")

    def InterRead_click(self):
        data = ComControlService(INT_VERSION)

        text = "INT_Version : "
        list =  text + chr(data[15])+ "   #" + str(data[16])
        self.textEdit.setText(list)
        self.textEdit_2.setText("MCUversion")

    def Sw1Write_click(self):
        data = ComControlService(SW1_WRITE)
        self.textEdit_2.setText("Switch1 Flash")

    def Sw2Write_click(self):
        data = ComControlService(SW2_WRITE)
        self.textEdit_2.setText("Switch2 Flash")

    def Sw1Read_click(self):
        data = ComControlService(SW1_VER_READ)

        text = "SW1_Version : "
        list =  text + str(data[15])+ str(data[16])
        self.textEdit.setText(list)
        self.textEdit_2.setText("Switch1_version for MCU, not official version")

    def Sw2Read_click(self):
        data = ComControlService(SW2_VER_READ)

        text = "SW2_Version : "
        list =  text + str(data[15])+ str(data[16])
        self.textEdit.setText(list)
        self.textEdit_2.setText("Switch2_version for MCU, not official version")

    def RegRead_click(self):
        global Did1
        global Did2
        global Did3
        global Did4

        testval = int(self.textEdit_3.toPlainText(),16)
        testval_hex = hex(testval)
        print("testval", testval, "hexval", testval_hex)

        reg1 = (testval & 0xff000000) >>24
        reg2 = (testval & 0xff0000) >> 16
        reg3 = (testval & 0xff00) >> 8
        reg4 = (testval & 0xff)

        print("reg1:", hex(reg1),"reg2:", hex(reg2),"reg3:", hex(reg3), "reg4:", hex(reg4))

        SW_REG_WRITE = bytearray(
            [0xcc, 0x33, 0x80, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x07, 0xdf, 0x07, 0x2e, Did1, Did2, reg1, reg2, reg3, reg4]
        )
        print(SW_REG_WRITE)

        data = ComControlService(SW_REG_WRITE)
  
        time.sleep(1)

        SW_REG_READ = bytearray(
            [0xcc, 0x33, 0x80, 0x01, 0x00, 0x00, 0x00, 0x0a, 0x07, 0xdf, 0x03, 0x22, Did3, Did4, 0x55, 0x55, 0x55, 0x55]
        )

        print("Did4", Did4, type(Did4))


        if Did4 == 0x8:
            value = ComControlService(SW_REG_READ)
            value4 = hex(value[15])
            self.textEdit.setText("8bit_reg =" + value4)
        elif Did4 == 0x16:
            value = ComControlService(SW_REG_READ)
            value4 = hex(((value[15]) << 8) + value[16])
            self.textEdit.setText("16bit_reg =" + value4)
        elif Did4 == 0x32:
            value = ComControlService(SW_REG_READ)
            value4 = hex(((value[15]) << 32) + (value[16]<<16) + (value[17]<<8) + value[18] )
            self.textEdit.setText("32bit_reg =" + value4)
        else:
            self.textEdit.setText("Read Fail")

        list = testval_hex + "_register_Read finish"
        self.textEdit_2.setText(list)

    def Closebtn_click(self):
        # QMessageBox.about(self, "message", "clicked")
        #clientsocket.close()
        self.textEdit_2.setText("Close")
        myWindow.close()

    #def addComboBoxItem(self):


    def SwitchReg_sel(self):
        global Did1
        global Did2
        global Did3
        global Did4

        Index = self.comboBox.currentIndex()
        Text = self.comboBox.currentText()
        #print("IndexValue: %d", Index)

        if Index ==1:
            self.textEdit_2.setText(Text + "__select")
            Did1 = 0xf3
            Did2 = 0x08
            Did3 = 0xff
            Did4 = 0x08
        elif Index ==2:
            self.textEdit_2.setText(Text + "__select")
            Did1 = 0xf3
            Did2 = 0x16
            Did3 = 0xff
            Did4 = 0x16
        elif Index ==3:
            self.textEdit_2.setText(Text + "__select")
            Did1 = 0xf3
            Did2 = 0x32
            Did3 = 0xff
            Did4 = 0x32
        elif Index ==4:
            self.textEdit_2.setText(Text + "__select")
            Did1 = 0xf5
            Did2 = 0x08
            Did3 = 0xfe
            Did4 = 0x08
        elif Index ==5:
            self.textEdit_2.setText(Text + "__select")
            Did1 = 0xf5
            Did2 = 0x16
            Did3 = 0xfe
            Did4 = 0x16
        elif Index ==6:
            self.textEdit_2.setText(Text + "__select")
            Did1 = 0xf5
            Did2 = 0x32
            Did3 = 0xfe
            Did4 = 0x32
        else:
            self.textEdit_2.setText("Please register Type Select")


        #self.textEdit_2.setText("Index")





def ComControlService(a) -> None:
    server_info = ("10.0.4.0", 13404)
    client_info = ('10.0.128.0', 53126)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Binding")
        s.bind(client_info)
        print("Done Binding")
        s.setblocking(True)
        l_onoff = 1
        l_linger = 0
        s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                     struct.pack('ii', l_onoff, l_linger))
        print("Connecting to Server")

        s.connect(server_info)
        print("Done Connecting to Server")
        s.sendall(a)
        received = s.recv(1024)

        #s.sendall(SW_VERSION)

        #print(recievd)
        time.sleep(1)

        #s.sendall(SECOND_PACKET)
        #s.recv(1024)
        #time.sleep(5)

        # s.sendall(FINAL_MSG)
        # s.recv(1024)
        # time.sleep(5)

        #print("Done writing the MCU part number")

        s.close()

        return received
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def Client():
    clientsocket.connect((HOST, PORT))
    #msg = "hello"
    msg = 0x12
    #clientsocket.send(msg.encode())
    clientsocket.send(bytes(msg))
    print(msg)
    data = clientsocket.recv(2048)
    #print(data.decode())
    print(data)

if __name__ == "__main__":
    print(resource_path('client.ui'))
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    #Client()