import pywinusb.hid as hid
from win32api import keybd_event

from PyQt5 import Qt, QtCore
qt_app = Qt.QApplication([])

hid_vendor_id =  0x0b57
hid_product_id = 0x1304
ptt_key = ptt_key=0x08

class App:
    sound_enabled = True

    def __init__(self):
        self.connected_devices = []
        self.hid_device_filter = hid.HidDeviceFilter(vendor_id=hid_vendor_id, product_id=hid_product_id)
        self.hid_device_list = None

    def start(self):
        global ptt_key
        ptt_key = hex(int(uidialog.leButtonCode.text(), 16))
        print ( "Looking for Device..." )

        self.hid_device_list = self.hid_device_filter.get_devices()
        if self.hid_device_list:
            for device in self.hid_device_list:
                self.connected_devices.append(device)
                device.open()
                device.set_raw_data_handler(self.raw_input_callback)
            uidialog.lStatus.setText(
                qt_app.translate("Dialog", "<font color=\"green\">connected</font>", None, -1))

        else:
            print ( "Oh No, no devices were found! \n" )

    def raw_input_callback(self, data):
        print(data)
        if data[2] == 1:
            keybd_event(self.ptt_key, 0, 0x0000, 0)
        elif data[2] == 0:
            keybd_event(self.ptt_key, 0, 0x0002, 0)


    def stopping_raw_callback(self):
        for dev in self.connected_devices:
            dev.close()
        uidialog.lStatus.setText(
            qt_app.translate("Dialog", "<font color=\"red\">disconnected</font>", None, -1))


# кнопочка по которой показывается виртуальныя клава для выбора кнопки
class MyButtonOpenKeySelector(Qt.QPushButton):
    def __init__(self, parent=None):
        Qt.QPushButton.__init__(self, parent)
        self.setFlat(True)
        self.setCheckable(True)
        self.pressed.connect(self.slot_checked)

    def slot_checked(self):
        if self.isChecked():
            my_virtual_keyboard_selector.hide()
            widget.resize(268, 60)
        else:
            my_virtual_keyboard_selector.show()
            widget.resize(500, 400)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        # Dialog.resize(268, 70)  заместо этого делаем:
        Dialog.setMinimumSize(268, 60)
        Dialog.setMaximumSize(500, 400)

        Dialog.grid = Qt.QGridLayout(Dialog)# создаём виртуальную "сетку"
        Dialog.grid.setSpacing(0)
        Dialog.grid.setContentsMargins(0,0,0,0)

        # кнопочка для показа клавиатуры
        self.label = MyButtonOpenKeySelector(Dialog) # невидимая кнопочка которая маскируется под лейбел
        Dialog.grid.addWidget(self.label, 0, 0, 1, 1)

        self.leButtonCode = Qt.QLineEdit(Dialog)
        self.leButtonCode.setReadOnly(True)
        Dialog.grid.addWidget(self.leButtonCode, 0, 1, 1, 1)
        self.leButtonCode.setText("0x08")

        self.pbStart = Qt.QPushButton(Dialog)
        Dialog.grid.addWidget(self.pbStart, 1, 0, 1, 1)

        self.pbStop = Qt.QPushButton(Dialog)
        Dialog.grid.addWidget(self.pbStop, 1, 1, 1, 1)

        # ещё одна новая кнопочка для отладки... можно удалить...
        self.pballdevices = Qt.QPushButton(Dialog)
        self.pballdevices.setMaximumWidth(10)
        self.pballdevices.pressed.connect(my_list_hids.obnivit)
        Dialog.grid.addWidget(self.pballdevices, 0, 2, 2, 1)

        self.lStatus = Qt.QLabel(Dialog)
        self.lStatus.setMaximumHeight(15)
        self.lStatus.setAlignment(Qt.Qt.AlignCenter)
        Dialog.grid.addWidget(self.lStatus, 2, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(qt_app.translate("Dialog", "Hot Key", None, -1))
        self.pbStart.setText(qt_app.translate("Dialog", "Start", None, -1))
        self.label.setText(qt_app.translate("Dialog", "Button code", None, -1))
        self.pbStop.setText(qt_app.translate("Dialog", "Stop", None, -1))
        self.lStatus.setText(qt_app.translate("Dialog", "<font color=\"red\">disconnected</font>", None, -1))


def hideEvent(event):
    trayIcon.show()
    widget.setVisible(False)
    Qt.QWidget.hideEvent(widget, event)

def restore_widget():
    widget.setVisible(True)
    Qt.QWidget.showNormal(widget)
    trayIcon.hide()

chislo_codes = {
    '0':0x30,
    '1':0x31,
    '2':0x32,
    '3':0x33,
    '4':0x34,
    '5':0x35,
    '6':0x36,
    '7':0x37,
    '8':0x38,
    '9':0x39,
    '+': 0xBB,
    '-': 0xBD,
    '\\': 0xDC,
    ',': 0xBC,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    ']': 0xDD,
    "'": 0xDE,
    '`': 0xC0
}
key_codes = {
    'a':0x41,
    'b':0x42,
    'c':0x43,
    'd':0x44,
    'e':0x45,
    'f':0x46,
    'g':0x47,
    'h':0x48,
    'i':0x49,
    'j':0x4A,
    'k':0x4B,
    'l':0x4C,
    'm':0x4D,
    'n':0x4E,
    'o':0x4F,
    'p':0x50,
    'q':0x51,
    'r':0x52,
    's':0x53,
    't':0x54,
    'u':0x55,
    'v':0x56,
    'w':0x57,
    'x':0x58,
    'y':0x59,
    'z':0x5A,
}
spec_codes = {
    'esc': 0x1B,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    'backspace':0x08,
    'tab':0x09,
    'enter': 0x0D,
    'spacebar': 0x20,
    'shift':0x10,
    'ctrl':0x11,
    'alt':0x12,
    'clear': 0x0C,
    'pause':0x13,
    'page_up':0x21,
    'page_down':0x22,
    'end':0x23,
    'home':0x24,
    'select':0x29,
    'print':0x2A,
    'execute':0x2B,
    'print_screen':0x2C,
    'ins':0x2D,
    'del':0x2E,
    'help':0x2F
}
other_codes = {
    'caps_lock': 0x14,
    'scroll_lock': 0x91,
    'left_shift':0xA0,
    'right_shift ':0xA1,
    'left_control':0xA2,
    'right_control':0xA3,
    'left_menu':0xA4,
    'right_menu':0xA5,
    'brwsr_back':0xA6,
    'brwsr_forward':0xA7,
    'brwsr_refresh':0xA8,
    'brwsr_stop':0xA9,
    'search':0xAA,
    'favorites':0xAB,
    'start_and_home':0xAC,
    'vol_mute':0xAD,
    'vol_Down':0xAE,
    'vol_up':0xAF,
    'next_track':0xB0,
    'previous_track':0xB1,
    'stop_media':0xB2,
    'play/pause':0xB3,
    'start_mail':0xB4,
    'select_media':0xB5,
    'start_app_1':0xB6,
    'start_app_2':0xB7,
    'attn_key':0xF6,
    'crsel_key':0xF7,
    'exsel_key':0xF8,
    'play_key':0xFA,
    'zoom_key':0xFB,
    'clear_key':0xFE
}

# сам виджет виртуальной клавы
class MyVirtualKeyboardSelector(Qt.QWidget):

    # прототип для всех кнопочек
    class MySelectButton(Qt.QPushButton):
        def __init__(self, name, code):
            Qt.QPushButton.__init__(self)
            self.setMinimumHeight(18)
            self.setMaximumHeight(100)
            self.name = name
            self.setText(name)
            self.code = hex(code)
            self.pressed.connect(self.najal)

        def najal(self):
            uidialog.leButtonCode.setText(str(self.code))

    def __init__(self):
        Qt.QWidget.__init__(self)
        self.hide()

        self.grid = Qt.QGridLayout(self)
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0,0,0,0)
        self.buttons = []

        self.widget_nabor1 = Qt.QGroupBox()
        self.widget_nabor1.setTitle("keys")
        self.widget_nabor1.grid = Qt.QGridLayout(self.widget_nabor1)
        self.widget_nabor1.grid.setSpacing(0)
        self.widget_nabor1.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.addWidget(self.widget_nabor1, 0, 0, 1, 1)

        x = 0
        for nabor in [chislo_codes, key_codes]:
            i = 0
            for vk, cod in nabor.items():
                new_buttn = self.MySelectButton(vk, cod)
                self.buttons.append(new_buttn)
                self.widget_nabor1.grid.addWidget(new_buttn, x, i, 1, 1)
                i = i + 1
                if i > 11:
                    x += 1
                    i = 0
            x += 1

        self.widget_nabor_Func = Qt.QGroupBox()
        self.widget_nabor_Func.setTitle("Func")
        self.widget_nabor_Func.grid = Qt.QGridLayout(self.widget_nabor_Func)
        self.widget_nabor_Func.grid.setSpacing(0)
        self.widget_nabor_Func.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.addWidget(self.widget_nabor_Func, 1, 0, 1, 2)

        # кнопочки можно добавлять так:
        i = 0
        x = 0
        for vk, cod in {
                'F1':0x70,
                'F2':0x71,
                'F3':0x72,
                'F4':0x73,
                'F5':0x74,
                'F6':0x75,
                'F7':0x76,
                'F8':0x77,
                'F9':0x78,
                'F10':0x79,
                'F11':0x7A,
                'F12':0x7B,
                'F13':0x7C,
                'F14':0x7D,
                'F15':0x7E,
                'F16':0x7F,
                'F17':0x80,
                'F18':0x81,
                'F19':0x82,
                'F20':0x83,
                'F21':0x84,
                'F22':0x85,
                'F23':0x86,
                'F24':0x87
        }.items():
            new_buttn = self.MySelectButton(vk, cod)
            self.buttons.append(new_buttn)
            self.widget_nabor_Func.grid.addWidget(new_buttn, i, x, 1, 1)
            x += 1
            if x > 11:
                x = 0
                i += 1

        self.widget_numpads = Qt.QGroupBox()
        self.widget_numpads.setTitle("NUM_PAD")
        self.widget_numpads.grid = Qt.QGridLayout(self.widget_numpads)
        self.widget_numpads.grid.setSpacing(0)
        self.widget_numpads.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.addWidget(self.widget_numpads, 0, 1, 1, 1)

        # или так
        self.widget_numpads.grid.addWidget(self.MySelectButton('lck', 0x90), 0, 0, 1, 1)
        self.widget_numpads.grid.addWidget(self.MySelectButton('/',   0x6F), 0, 1, 1, 1)
        self.widget_numpads.grid.addWidget(self.MySelectButton('*',   0x6A), 0, 2, 1, 1)
        self.widget_numpads.grid.addWidget(self.MySelectButton('-',   0x6D), 0, 3, 1, 1)

        self.widget_numpads.grid.addWidget(self.MySelectButton('7',   0x67), 1, 0, 1, 1)
        self.widget_numpads.grid.addWidget(self.MySelectButton('8',   0x68), 1, 1, 1, 1)
        self.widget_numpads.grid.addWidget(self.MySelectButton('9',   0x69), 1, 2, 1, 1)
        self.widget_numpads.grid.addWidget(self.MySelectButton('+',   0x6B), 1, 3, 2, 1)

        self.widget_numpads.grid.addWidget(self.MySelectButton('4',   0x64), 2, 0, 1, 1)
        self.widget_numpads.grid.addWidget(self.MySelectButton('5',   0x65), 2, 1, 1, 1)
        self.widget_numpads.grid.addWidget(self.MySelectButton('6',   0x66), 2, 2, 1, 1)

        self.widget_numpads.grid.addWidget(self.MySelectButton('1',   0x61), 3, 0, 1, 1)
        self.widget_numpads.grid.addWidget(self.MySelectButton('2',   0x62), 3, 1, 1, 1)
        self.widget_numpads.grid.addWidget(self.MySelectButton('3',   0x63), 3, 2, 1, 1)
        self.widget_numpads.grid.addWidget(self.MySelectButton('ent', 0x6E), 3, 3, 2, 1)

        self.widget_numpads.grid.addWidget(self.MySelectButton('0',   0x60), 4, 0, 1, 2)
        self.widget_numpads.grid.addWidget(self.MySelectButton('.',   0x6C), 4, 2, 1, 1)


        self.widget_nabor_other = Qt.QGroupBox()
        self.widget_nabor_other.setTitle("other")
        self.widget_nabor_other.grid = Qt.QGridLayout(self.widget_nabor_other)
        self.widget_nabor_other.grid.setSpacing(0)
        self.widget_nabor_other.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.addWidget(self.widget_nabor_other, 2, 0, 1, 2)

        # и даже так:
        i = 0
        for nabor in [spec_codes, other_codes]:
            for vk, cod in nabor.items():
                new_buttn = self.MySelectButton(vk, cod)
                self.buttons.append(new_buttn)
                self.widget_nabor_other.grid.addWidget(new_buttn, i//6, i%6, 1, 1)
                i += 1

my_virtual_keyboard_selector = MyVirtualKeyboardSelector()

class MyTable_all_hid(Qt.QListWidget):
    def __init__(self):
        Qt.QListWidget.__init__(self)
        self.setWindowFlags(Qt.Qt.Popup)
        self.setMinimumHeight(300)

    def obnivit(self):
        self.clear()
        hid_device_filter = hid.HidDeviceFilter()
        hid_device_list = hid_device_filter.get_devices()
        for i in hid_device_list:
            self.addItem(str(i))
        self.setGeometry(widget.geometry())
        self.show()

    def mousePressEvent(self, event):
        Qt.QListWidget.mousePressEvent(self, event)
        self.hide()


my_list_hids = MyTable_all_hid()

if __name__ == '__main__':
    app = App()

    widget = Qt.QWidget()
    uidialog = Ui_Dialog()
    uidialog.setupUi(widget)
    widget.grid.addWidget(my_virtual_keyboard_selector, 3, 0, 1, 2)

    uidialog.pbStart.clicked.connect(app.start)
    uidialog.pbStop.clicked.connect(app.stopping_raw_callback)

    trayIcon = Qt.QSystemTrayIcon(
        Qt.QIcon("myicon.png"), widget)

    widget.hideEvent = hideEvent
    trayIcon.activated.connect(restore_widget)
    widget.show()

    qt_app.exec() # Ой всё!
