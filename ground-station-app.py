import sys
import json
import random
import folium
import configparser
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QCheckBox, QLabel, QPushButton, QComboBox, QLineEdit, QTabWidget, QFormLayout, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from hyi_controller import HYIPacket

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atmaca Roket Takımı - Yer İstasyonu Veri Görüntüleme Aracı")
        self.setFixedSize(900, 550)
        self.setWindowIcon(QIcon("resources/icon.ico"))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.hyi_io_status = False

        self.layout = QVBoxLayout(self.central_widget)

        with open("config.json", "r") as file:
            self.config_json = json.loads(file.read())

            if self.config_json["theme"] == "White":
                with open("styles/style-white.qss", "r", encoding="utf-8") as style_file:
                    style_sheet = style_file.read()
                    self.setStyleSheet(style_sheet)
            elif self.config_json["theme"] == "Dark":
                with open("styles/style-dark.qss", "r", encoding="utf-8") as style_file:
                    style_sheet = style_file.read()
                    self.setStyleSheet(style_sheet)

        self.init_port_selection_screen()

    def init_port_selection_screen(self):
        self.port_selection_widget = QWidget(self.central_widget)
        self.layout.addWidget(self.port_selection_widget)
        
        main_layout = QVBoxLayout(self.port_selection_widget)
        self.port_selection_widget.setLayout(main_layout)

        logo_label = QLabel(self.port_selection_widget)
        logo_label.setPixmap(QPixmap("resources/logo.png"))  # Logonuzun yolunu buraya ekleyin
        main_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        form_layout = QFormLayout(self.port_selection_widget)
    
        self.combo_box_ports1 = QComboBox(self.port_selection_widget)
        form_layout.addRow("Port:", self.combo_box_ports1)

        self.combo_box_baud_rate1 = QComboBox(self.port_selection_widget)
        baud_rates = ["9600", "19200", "38400", "57600", "115200"]
        self.combo_box_baud_rate1.addItems(baud_rates)
        form_layout.addRow("Baund", self.combo_box_baud_rate1)

        main_layout.addLayout(form_layout)

        self.button_select_ports = QPushButton("Bağlan", self.port_selection_widget)
        self.button_select_ports.clicked.connect(self.on_select_ports_clicked)
        main_layout.addWidget(self.button_select_ports)

        self.button_test_mode = QPushButton("Test Modu", self.port_selection_widget)
        self.button_test_mode.clicked.connect(self.start_test_mode)
        main_layout.addWidget(self.button_test_mode)

        self.serial_ports = QSerialPortInfo.availablePorts()
        for port in self.serial_ports:
            self.combo_box_ports1.addItem(port.portName())

    def create_main_screen(self):
        self.tab_widget = QTabWidget(self.central_widget)
        self.layout.addWidget(self.tab_widget)

        self.create_intro_tab()  # Giriş sekmesi ekleniyor
        self.create_data_tab()
        self.create_map_tab()
        self.create_serial_port_tab()
        self.create_hyi_tab()
        self.create_settings_tab()

    def create_intro_tab(self):
        self.tab_intro = QWidget()
        layout = QVBoxLayout(self.tab_intro)

        # Logo ve pencere adı
        logo_label = QLabel(self.tab_intro)
        logo_label.setPixmap(QPixmap("resources/logo.png"))  # Logonuzun yolunu buraya ekleyin
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        
        title_label = QLabel(self.windowTitle(), self.tab_intro)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        self.tab_widget.addTab(self.tab_intro, "Giriş")


    def create_data_tab(self):
        tab_veriler1 = QWidget()
        self.tab_widget.addTab(tab_veriler1, "Veriler")

        form_layout1 = QFormLayout(tab_veriler1)

        self.label_name1 = QLabel("Name:", tab_veriler1)
        self.line_edit_name1 = QLineEdit(tab_veriler1)
        self.line_edit_name1.setReadOnly(True)
        form_layout1.addRow(self.label_name1, self.line_edit_name1)

        self.label_package_number1 = QLabel("Package Number:", tab_veriler1)
        self.line_edit_package_number1 = QLineEdit(tab_veriler1)
        self.line_edit_package_number1.setReadOnly(True)
        form_layout1.addRow(self.label_package_number1, self.line_edit_package_number1)

        self.label_latitude1 = QLabel("Latitude:", tab_veriler1)
        self.line_edit_latitude1 = QLineEdit(tab_veriler1)
        self.line_edit_latitude1.setReadOnly(True)
        form_layout1.addRow(self.label_latitude1, self.line_edit_latitude1)

        self.label_longitude1 = QLabel("Longitude:", tab_veriler1)
        self.line_edit_longitude1 = QLineEdit(tab_veriler1)
        self.line_edit_longitude1.setReadOnly(True)
        form_layout1.addRow(self.label_longitude1, self.line_edit_longitude1)

        self.label_speed1 = QLabel("Speed:", tab_veriler1)
        self.line_edit_speed1 = QLineEdit(tab_veriler1)
        self.line_edit_speed1.setReadOnly(True)
        form_layout1.addRow(self.label_speed1, self.line_edit_speed1)

        self.label_pressure1 = QLabel("Pressure:", tab_veriler1)
        self.line_edit_pressure1 = QLineEdit(tab_veriler1)
        self.line_edit_pressure1.setReadOnly(True)
        form_layout1.addRow(self.label_pressure1, self.line_edit_pressure1)

        self.label_altitude1 = QLabel("Altitude:", tab_veriler1)
        self.line_edit_altitude1 = QLineEdit(tab_veriler1)
        self.line_edit_altitude1.setReadOnly(True)
        form_layout1.addRow(self.label_altitude1, self.line_edit_altitude1)

        self.label_pitch1 = QLabel("Pitch:", tab_veriler1)
        self.line_edit_pitch1 = QLineEdit(tab_veriler1)
        self.line_edit_pitch1.setReadOnly(True)
        form_layout1.addRow(self.label_pitch1, self.line_edit_pitch1)

        self.label_roll1 = QLabel("Roll:", tab_veriler1)
        self.line_edit_roll1 = QLineEdit(tab_veriler1)
        self.line_edit_roll1.setReadOnly(True)
        form_layout1.addRow(self.label_roll1, self.line_edit_roll1)

        self.label_yaw1 = QLabel("Yaw:", tab_veriler1)
        self.line_edit_yaw1 = QLineEdit(tab_veriler1)
        self.line_edit_yaw1.setReadOnly(True)
        form_layout1.addRow(self.label_yaw1, self.line_edit_yaw1)

        self.label_status1 = QLabel("Status:", tab_veriler1)
        self.line_edit_status1 = QLineEdit(tab_veriler1)
        self.line_edit_status1.setReadOnly(True)
        form_layout1.addRow(self.label_status1, self.line_edit_status1)

    def create_map_tab(self):
        self.tab_map = QWidget()
        layout = QVBoxLayout(self.tab_map)

        # Generate Folium Map
        self.m = folium.Map(location=[0, 0], zoom_start=12)
        self.marker1 = folium.Marker([0, 0], popup='Roket', icon=folium.Icon(color='red')).add_to(self.m)

        self.map_path = "map.html"
        self.m.save(self.map_path)

        # Embed Folium Map using QWebEngineView
        self.webview = QWebEngineView()
        self.webview.setHtml(open(self.map_path, "r").read())
        layout.addWidget(self.webview)

        self.map_updater_selector = QCheckBox("Haritayı Otomatik Güncelle")
        self.map_updater_selector.setChecked(True)
        layout.addWidget(self.map_updater_selector)

        self.tab_widget.addTab(self.tab_map, "Harita")

    def create_serial_port_tab(self):
        tab_serial_port = QWidget()
        layout = QVBoxLayout(tab_serial_port)

        self.text_edit_raw_data1 = QTextEdit(tab_serial_port)
        self.text_edit_raw_data1.setReadOnly(True)
        layout.addWidget(self.text_edit_raw_data1)

        self.tab_widget.addTab(tab_serial_port, "Seri Port")

    def create_hyi_tab(self):
        tab_hyi = QWidget()
        main_layout_hyi = QVBoxLayout(tab_hyi)
        form_layout_hyi = QFormLayout(tab_hyi)
        button_layout_hyi = QVBoxLayout(tab_hyi)

        # COM port seçici
        self.hyi_port = QComboBox(tab_hyi)
        for port in QSerialPortInfo.availablePorts():
            if self.combo_box_ports1.currentText() == port.portName():
                pass
            else:
                self.hyi_port.addItem(port.portName())
        form_layout_hyi.addRow("COM Port:", self.hyi_port)

        # Baud rate seçici
        self.hyi_baud_rate = QComboBox(tab_hyi)
        baud_rates = ["9600", "19200", "38400", "57600", "115200"]
        self.hyi_baud_rate.addItems(baud_rates)
        self.hyi_baud_rate.setCurrentIndex(1)
        form_layout_hyi.addRow("Baud Rate:", self.hyi_baud_rate)

        # Team ID girişi
        self.hyi_team_id = QLineEdit(tab_hyi)
        form_layout_hyi.addRow("Team ID:", self.hyi_team_id)

        form_layout_hyi.addRow("", QLabel())

        self.packet_counter_label = QLabel(tab_hyi)
        form_layout_hyi.addRow("Counter:", self.packet_counter_label)

        self.packet_hyi_label = QLabel(tab_hyi)
        self.packet_hyi_label.setWordWrap(True)
        self.packet_hyi_label.setStyleSheet("font-size: 14px;")
        form_layout_hyi.addRow("Packet:", self.packet_hyi_label)

        self.packet_checksum_label = QLabel(tab_hyi)
        form_layout_hyi.addRow("Checksum:", self.packet_checksum_label)

        main_layout_hyi.addLayout(form_layout_hyi)

        # Başlat ve Durdur butonları
        self.hyi_start_button = QPushButton("Başlat", tab_hyi)
        self.hyi_stop_button = QPushButton("Durdur", tab_hyi)
        self.hyi_stop_button.setEnabled(False)

        main_layout_hyi.addLayout(button_layout_hyi)
        button_layout_hyi.addWidget(self.hyi_start_button)
        button_layout_hyi.addWidget(self.hyi_stop_button)

        # Bağlantıları yap
        self.hyi_start_button.clicked.connect(self.start_hyi)
        self.hyi_stop_button.clicked.connect(self.stop_hyi)

        self.tab_widget.addTab(tab_hyi, "HYI")

    def create_settings_tab(self):
            tab_settings = QWidget()
            layout = QVBoxLayout(tab_settings)

            form_layout_settings = QFormLayout(tab_settings)
            
            # Bağlı olan COM port bilgisi
            current_port_label = QLabel(f"Bağlı Port: {self.serial_port1.portName() if hasattr(self, 'serial_port1') else 'COM port bağlı değil'}", tab_settings)
            form_layout_settings.addRow("", current_port_label)

            # Bağlantıyı kesme butonu
            disconnect_button = QPushButton("Bağlantıyı Kes", tab_settings)
            disconnect_button.clicked.connect(self.disconnect_port)
            form_layout_settings.addRow(disconnect_button)

            form_layout_settings.addRow("", QLabel())

            theme_changer = QComboBox(tab_settings)
            theme_changer.addItems(["Dark", "White"])
            theme_changer.currentIndexChanged.connect(self.change_theme)
            form_layout_settings.addRow("Theme:", theme_changer)

            layout.addLayout(form_layout_settings)

            self.tab_widget.addTab(tab_settings, "Ayarlar")

    def disconnect_port(self):
        if hasattr(self, 'serial_port1'):
            self.serial_port1.close()
            self.tab_widget.clear()
            self.init_port_selection_screen()

    def on_select_ports_clicked(self):
        port1 = self.combo_box_ports1.currentText()
        baud_rate1 = int(self.combo_box_baud_rate1.currentText())
        self.serial_port1 = QSerialPort()
        self.serial_port1.setBaudRate(baud_rate1)
        self.serial_port1.setPortName(port1)

        if self.serial_port1.open(QIODevice.ReadOnly):
            print(f"1. Yer İstasyonu için seri port {port1} açıldı.")
            self.serial_port1.readyRead.connect(self.read_data1)
            self.port_selection_widget.setVisible(False)
            self.create_main_screen()
        else:
            print(f"1. Yer İstasyonu için seri port {port1} açılamadı.")

    def read_data1(self):
        try:
            while self.serial_port1.canReadLine():
                data = self.serial_port1.readLine().data().decode('ascii').strip()
                self.text_edit_raw_data1.append(data)
                self.update_fields1(data)

                if self.hyi_io_status:
                    packet = self.hyi.create_packet(team_id=int(self.hyi_team_id.text()), altitude=float(self.line_edit_altitude1.text()), rocket_latitude=float(self.line_edit_latitude1.text()), rocket_longitude=float(self.line_edit_longitude1.text()))
                    self.hyi.write_serial_port(packet)
                    self.packet_hyi_label.setText(self.hyi.return_packet(packet))
                    self.packet_checksum_label.setText(str(self.hyi.checksum))
                    self.packet_counter_label.setText(str(self.hyi.counter))
        except UnicodeDecodeError:
            pass
        # except Exception as e:
        #     print(f"Veri okuma hatası: {e}")

    def update_fields1(self, data):
        try:
            json_data = json.loads(data)
            self.line_edit_name1.setText(str(json_data.get("name", "")))
            self.line_edit_package_number1.setText(str(json_data.get("packageNumber", "")))
            self.line_edit_latitude1.setText(str(json_data.get("latitude", "")))
            self.line_edit_longitude1.setText(str(json_data.get("longitude", "")))
            self.line_edit_speed1.setText(str(json_data.get("speed", "")))
            self.line_edit_pressure1.setText(str(json_data.get("pressure", "")))
            self.line_edit_altitude1.setText(str(json_data.get("altitude", "")))
            self.line_edit_pitch1.setText(str(json_data.get("pitch", "")))
            self.line_edit_roll1.setText(str(json_data.get("roll", "")))
            self.line_edit_yaw1.setText(str(json_data.get("yaw", "")))
            self.line_edit_status1.setText(str(json_data.get("status", "")))
            
            if self.map_updater_selector.isChecked():
                latitude = json_data.get("latitude", 0.0)
                longitude = json_data.get("longitude", 0.0)
                self.marker1.location = [latitude, longitude]
                self.m.location = [latitude, longitude]
                self.m.save(self.map_path)
                self.webview.setHtml(open(self.map_path, "r").read())
        except json.JSONDecodeError as e:
            print(f"JSON çözümleme hatası: {e}")
        except Exception as e:
            print(f"Güncelleme hatası: {e}")

    def start_test_mode(self):
        self.port_selection_widget.setVisible(False)
        self.create_main_screen()
        self.test_timer = QTimer(self)
        self.test_timer.timeout.connect(self.generate_test_data)
        self.test_timer.start(1000)  # Every 1 second

    def generate_test_data(self):
        test_data = {
            "name": "TestRoket",
            "package_number": random.randint(1, 1000),
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180),
            "speed": random.uniform(0, 500),
            "pressure": random.uniform(900, 1100),
            "altitude": random.uniform(0, 10000),
            "pitch": random.uniform(-180, 180),
            "roll": random.uniform(-180, 180),
            "yaw": random.uniform(-180, 180),
            "status": "Testing"
        }
        self.update_fields1(json.dumps(test_data))

    def start_hyi(self):
        print("HYI başlatıldı.")
        try:
            self.hyi_io_status = True
            self.hyi = HYIPacket(port=self.hyi_port.currentText(), baudrate=self.hyi_baud_rate.currentText())
            self.hyi.connect()
            self.hyi_start_button.setEnabled(False)
            self.hyi_stop_button.setEnabled(True)
        except Exception as e:
            self.hyi_io_status = False
            print("HYİ'ye bağlanılamadı!")
            self.hyi_start_button.setEnabled(True)

    def stop_hyi(self):
        print("HYI durduruldu.")
        self.hyi.disconnect()
        self.hyi_io_status = False
        self.hyi_start_button.setEnabled(True)
        self.hyi_stop_button.setEnabled(False)

    def change_theme(self, state):
        if state == 0:
            with open("styles/style-dark.qss", "r", encoding="utf-8") as style_file:
                style_sheet = style_file.read()
                self.setStyleSheet(style_sheet)
            self.config_json["theme"] = "Dark"
            with open("config.json", "w", encoding="utf-8") as file:
                json.dump(self.config_json, file, indent=4, ensure_ascii=False)
        elif state == 1:
            with open("styles/style-white.qss", "r", encoding="utf-8") as style_file:
                style_sheet = style_file.read()
                self.setStyleSheet(style_sheet)
            self.config_json["theme"] = "White"
            with open("config.json", "w", encoding="utf-8") as file:
                json.dump(self.config_json, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
