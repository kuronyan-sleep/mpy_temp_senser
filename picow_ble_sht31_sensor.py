import bluetooth
import struct
import time
import machine
import ubinascii
from ble_advertising import advertising_payload
from micropython import const
from machine import Pin, I2C

# STH31 I2Cアドレス
STH31_ADDR = 0x44  # STH31のI2Cアドレス（デフォルト）

# 温度センサのUUIDなどの設定
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_INDICATE_DONE = const(20)

_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_TEMP_CHAR = (
    bluetooth.UUID(0x2A6E),
    _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,
)
_ENV_SENSE_SERVICE = (
    _ENV_SENSE_UUID,
    (_TEMP_CHAR,),
)

class BLETemperature:
    def __init__(self, ble, name=""):
        # I2C設定
        self.i2c = I2C(0, scl=Pin(18), sda=Pin(19))
        # PicoWのI2Cピン（SCL:5, SDA:4）
        # WSP32のI2Cピン（SCL:18, SDA:19）
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_ENV_SENSE_SERVICE,))
        self._connections = set()
        if len(name) == 0:
            name = 'Pico %s' % ubinascii.hexlify(self._ble.config('mac')[1], ':').decode().upper()
        print('Sensor name %s' % name)
        self._payload = advertising_payload(
            name=name, services=[_ENV_SENSE_UUID]
        )
        self._advertise()

    def _irq(self, event, data):
        # 接続の管理
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # 再度広告を出して新しい接続を待つ
            self._advertise()
        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data

    def update_temperature(self, notify=False, indicate=False):
        # 温度の取得と送信
        temp_deg_c = self._get_temp()
        print("write temp %.2f degc" % temp_deg_c)
        self._ble.gatts_write(self._handle, struct.pack("<h", int(temp_deg_c * 100)))  # 温度値を格納
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    self._ble.gatts_notify(conn_handle, self._handle)
                if indicate:
                    self._ble.gatts_indicate(conn_handle, self._handle)

    def _advertise(self, interval_us=500000):
        # BLE広告を出す
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def _get_temp(self):
        # STH31センサから温度を取得
        # センサからデータを読み取る
        self.i2c.writeto(STH31_ADDR, b'\x24\x00')  # 一度温度測定を開始するコマンド
        time.sleep(0.5)  # 測定に時間がかかるため待機
        data = self.i2c.readfrom(STH31_ADDR, 6)  # 温度データは6バイト
        # 取得したデータを解析
        raw_temp = (data[0] << 8 | data[1]) & 0xFFFF
        temp_deg_c = -45 + (175 * raw_temp / 65535.0)  # STH31の補正式
        return temp_deg_c

def demo():
    ble = bluetooth.BLE()
    temp = BLETemperature(ble)
    counter = 0
#    led = Pin('LED', Pin.OUT)
    while True:
        if counter % 10 == 0:
            temp.update_temperature(notify=True, indicate=False)
#        led.toggle()
        time.sleep_ms(1000)
        counter += 1

if __name__ == "__main__":
    demo()
