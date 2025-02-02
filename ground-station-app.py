import sys
import json
import random
import folium
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QUrl
from hyi_controller import HYIPacket

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atmaca Rocket Team - Ground Station Data Visualization Tool")
        self.setGeometry(400, 200, 1090, 650)
        self.setWindowIcon(QIcon("resources/icon.ico"))

        self.status_bar = self.statusBar()

        self.hyi_io_status = False
        self.test_mode_status = False
        self.data_list = []

        try:
            with open("config.json", "r") as file:
                self.config_json = json.loads(file.read())
        except FileNotFoundError:
            with open("config.json", "w") as file:
                file.write('{\n\t"theme": "White" \n}')
            with open("config.json", "r") as file:
                self.config_json = json.loads(file.read())
        finally:
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
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.port_selection_widget = QWidget(self.central_widget)
        self.layout.addWidget(self.port_selection_widget)
        
        main_layout = QVBoxLayout(self.port_selection_widget)
        self.port_selection_widget.setLayout(main_layout)

        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("resources/logo.png"))
        main_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        form_layout = QFormLayout()
    
        self.combo_box_ports = QComboBox()
        form_layout.addRow("Port:", self.combo_box_ports)
        self.refresh_port()

        self.combo_box_baud_rate1 = QComboBox()
        baud_rates = ["9600", "19200", "38400", "57600", "115200"]
        self.combo_box_baud_rate1.addItems(baud_rates)
        self.combo_box_baud_rate1.setCurrentIndex(4)
        form_layout.addRow("Baund", self.combo_box_baud_rate1)

        main_layout.addLayout(form_layout)

        self.button_select_ports = QPushButton("Connect")
        self.button_select_ports.clicked.connect(self.on_select_ports_clicked)
        self.button_select_ports.setShortcut("Return")
        main_layout.addWidget(self.button_select_ports)

        self.button_refresh_port = QPushButton("Refresh")
        self.button_refresh_port.clicked.connect(self.refresh_port)
        self.button_refresh_port.setShortcut("Ctrl+R")
        main_layout.addWidget(self.button_refresh_port)

        main_layout.addSpacing(20)

        self.button_test_mode = QPushButton("Test Mode")
        self.button_test_mode.clicked.connect(self.start_test_mode)
        self.button_test_mode.setShortcut("Ctrl+Shift+T")
        main_layout.addWidget(self.button_test_mode)

    def create_main_screen(self):
        self.tab_widget = QTabWidget(self.central_widget)
        self.layout.addWidget(self.tab_widget)

        self.create_intro_tab()  
        self.create_data_tab()
        self.create_map_tab()
        self.create_serial_port_tab()
        self.create_hyi_tab()

        self.create_settings_tab()
        with open("config.json", "r") as file:
            self.config_json = json.loads(file.read())

            if self.config_json["theme"] == "White":
                self.theme_changer.setCurrentIndex(1)
            elif self.config_json["theme"] == "Dark":
                self.theme_changer.setCurrentIndex(0)

    def create_intro_tab(self):
        self.tab_intro = QWidget()
        layout = QVBoxLayout(self.tab_intro)

        # Logo ve pencere adı
        logo_label = QLabel(self.tab_intro)
        logo_label.setPixmap(QPixmap("resources/logo.png"))  
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        
        title_label = QLabel(self.windowTitle(), self.tab_intro)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        self.tab_widget.addTab(self.tab_intro, "Entry")


    def create_data_tab(self):
        tab_veriler1 = QWidget()
        self.tab_widget.addTab(tab_veriler1, "Datas")

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

        self.label_altitude1 = QLabel("Altitude:", tab_veriler1)
        self.line_edit_altitude1 = QLineEdit(tab_veriler1)
        self.line_edit_altitude1.setReadOnly(True)
        form_layout1.addRow(self.label_altitude1, self.line_edit_altitude1)

        self.label_pressure1 = QLabel("Pressure:", tab_veriler1)
        self.line_edit_pressure1 = QLineEdit(tab_veriler1)
        self.line_edit_pressure1.setReadOnly(True)
        form_layout1.addRow(self.label_pressure1, self.line_edit_pressure1)

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

        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl("file:///map.html"))
        layout.addWidget(self.webview)

        self.tab_widget.addTab(self.tab_map, "Map")

    def create_serial_port_tab(self):
        tab_serial_port = QWidget()
        layout = QVBoxLayout(tab_serial_port)

        self.text_edit_raw_data1 = QTextEdit(tab_serial_port)
        self.text_edit_raw_data1.setReadOnly(True)
        layout.addWidget(self.text_edit_raw_data1)

        self.tab_widget.addTab(tab_serial_port, "Serial Port")

    def create_hyi_tab(self):
        tab_hyi = QWidget()
        main_layout_hyi = QVBoxLayout(tab_hyi)
        form_layout_hyi = QFormLayout(tab_hyi)
        button_layout_hyi = QVBoxLayout(tab_hyi)

        # COM port seçici
        self.hyi_port = QComboBox(tab_hyi)
        for port in QSerialPortInfo.availablePorts():
            if self.combo_box_ports.currentText() == port.portName():
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

        form_layout_hyi.addRow(QLabel("<hr>"))

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
        self.hyi_start_button = QPushButton("Start Data Transfer", tab_hyi)
        self.hyi_stop_button = QPushButton("Stop Data Transfer", tab_hyi)
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
        current_port_label = QLabel(f"{self.serial_port.portName() if hasattr(self, 'serial_port') else 'COM port bağlı değil'}", tab_settings)
        form_layout_settings.addRow("Port:", current_port_label)

        current_baund_label = QLabel(f"{self.serial_port.baudRate() if hasattr(self, 'serial_port') else 'COM port bağlı değil'}", tab_settings)
        form_layout_settings.addRow("Baund:", current_baund_label)

        # Bağlantıyı kesme butonu
        disconnect_button = QPushButton("Disconnect Serial Port", tab_settings)
        disconnect_button.clicked.connect(self.disconnect_port)
        form_layout_settings.addRow(disconnect_button)      
        
        form_layout_settings.addRow(QLabel("<hr>"))

        save_data_button = QPushButton("Save Received Data", tab_settings)
        save_data_button.clicked.connect(self.save_data)
        form_layout_settings.addRow(save_data_button)

        self.save_data_status_label = QLabel("Last Saved Data:", tab_settings)
        form_layout_settings.addRow(self.save_data_status_label)

        form_layout_settings.addRow(QLabel("<hr>"))

        self.theme_changer = QComboBox(tab_settings)
        self.theme_changer.addItems(["Dark", "White"])
        self.theme_changer.currentIndexChanged.connect(self.change_theme)
        form_layout_settings.addRow("Theme:", self.theme_changer)

        layout.addLayout(form_layout_settings)

        self.tab_widget.addTab(tab_settings, "Settings")

    def refresh_port(self):
        self.combo_box_ports.clear()
        self.serial_ports = QSerialPortInfo.availablePorts()
        for port in self.serial_ports:
            self.combo_box_ports.addItem(port.portName())

    def disconnect_port(self):
        if self.test_mode_status:
            self.status_bar.showMessage(f"Ground Station: Test mode disconnected.")
            self.test_timer.stop()
            self.tab_widget.clear()
            self.init_port_selection_screen()
        else:
            self.status_bar.showMessage(f"Ground Station: Serial port {self.serial_port.portName()} disconnected.")
            self.serial_port.close()
            self.tab_widget.clear()
            self.init_port_selection_screen()

    def on_select_ports_clicked(self):
        port1 = self.combo_box_ports.currentText()
        baud_rate1 = int(self.combo_box_baud_rate1.currentText())
        self.serial_port = QSerialPort()
        self.serial_port.setBaudRate(baud_rate1)
        self.serial_port.setPortName(port1)

        if self.serial_port.open(QIODevice.ReadOnly):
            self.status_bar.showMessage(f"Ground Station: Serial port {port1} opened.")
            self.serial_port.readyRead.connect(self.read_data)
            self.port_selection_widget.setVisible(False)
            self.create_main_screen()
        else:
            self.status_bar.showMessage(f"Ground Station: Failed to open serial port {port1}.")

    def read_data(self):
        try:
            while self.serial_port.canReadLine():
                data = self.serial_port.readLine().data().decode('ascii').strip()
                self.text_edit_raw_data1.append(data)
                
                json_data = json.loads(data)
                
                self.update_fields(json_data)

                timestamp = datetime.datetime.now()
                json_data['timestamp'] = str(timestamp)  
                self.data_list.append(json_data)  

                if self.hyi_io_status:
                    packet = self.hyi.create_packet(team_id=int(self.hyi_team_id.text()), altitude=float(self.line_edit_altitude1.text()), rocket_latitude=float(self.line_edit_latitude1.text()), rocket_longitude=float(self.line_edit_longitude1.text()))
                    self.hyi.write_serial_port(packet)
                    self.packet_hyi_label.setText(self.hyi.return_packet(packet))
                    self.packet_checksum_label.setText(str(self.hyi.checksum))
                    self.packet_counter_label.setText(str(self.hyi.counter))
        except UnicodeDecodeError:
            pass
        except json.JSONDecodeError as e:
            # self.status_bar.showMessage(f"JSON çözümleme hatası: {e}")
            pass
        except ValueError:
            self.status_bar.showMessage("Enter the Client ID value.")
            self.stop_hyi()
        except Exception as e:
            self.status_bar.showMessage(f"Data reading error: {e}")

    def update_fields(self, data):
        try:
            self.line_edit_name1.setText(str(data.get("name", "")))
            self.line_edit_package_number1.setText(str(data.get("packageNumber", "")))
            self.line_edit_latitude1.setText(str(data.get("latitude", "")))
            self.line_edit_longitude1.setText(str(data.get("longitude", "")))
            self.line_edit_speed1.setText(str(data.get("speed", "")))
            self.line_edit_pressure1.setText(str(data.get("pressure", "")))
            self.line_edit_altitude1.setText(str(data.get("altitude", "")))
            self.line_edit_pitch1.setText(str(data.get("pitch", "")))
            self.line_edit_roll1.setText(str(data.get("roll", "")))
            self.line_edit_yaw1.setText(str(data.get("yaw", "")))
            self.line_edit_status1.setText(str(data.get("status", "")))
            
            js_code = f"updateMarker({data.get("latitude", "")}, {data.get("longitude", "")});"
            self.webview.page().runJavaScript(js_code)
        except Exception as e:
            self.status_bar.showMessage(f"Data update error: {e}")

    def start_test_mode(self):
        self.test_mode_status = True
        self.status_bar.showMessage(f"The application is running in test mode.")
        self.port_selection_widget.setVisible(False)
        self.create_main_screen()
        self.test_timer = QTimer(self)
        self.test_timer.timeout.connect(self.generate_test_data)
        self.test_timer.start(1000)  

    def generate_test_data(self):
        test_data = {
            "name": "Rocket",
            "package_number": random.randint(1, 1000),
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180),
            "speed": random.uniform(0, 500),
            "pressure": random.uniform(900, 1100),
            "altitude": random.uniform(0, 10000),
            "pitch": random.uniform(-180, 180),
            "roll": random.uniform(-180, 180),
            "yaw": random.uniform(-180, 180),
            "status": 1
        }

        self.update_fields(test_data)

    def start_hyi(self):
        try:
            self.hyi_io_status = True
            self.hyi = HYIPacket(port=self.hyi_port.currentText(), baudrate=self.hyi_baud_rate.currentText())
            self.hyi.connect()
            self.hyi_port.setEnabled(False)
            self.hyi_baud_rate.setEnabled(False)
            self.hyi_team_id.setEnabled(False)
            self.hyi_start_button.setEnabled(False)
            self.hyi_stop_button.setEnabled(True)
            self.status_bar.showMessage(f"HYİ: Serial port {self.hyi_port.currentText()} opened.")
        except Exception as e:
            self.hyi_io_status = False
            self.status_bar.showMessage(f"Connection error to HYİ: {e}")
            self.hyi_start_button.setEnabled(True)

    def stop_hyi(self):
        try:
            self.hyi.disconnect()
            self.hyi_io_status = False
            self.hyi_start_button.setEnabled(True)
            self.hyi_port.setEnabled(True)
            self.hyi_baud_rate.setEnabled(True)
            self.hyi_team_id.setEnabled(True)
            self.hyi_stop_button.setEnabled(False)
            self.status_bar.showMessage(f"HYI: {self.hyi_port.currentText()} connection was disconnected.")
        except:
            self.hyi_io_status = True
            self.status_bar.showMessage(f"HYI: {self.hyi_port.currentText()} connection was not disconnected.")

    def save_data(self):
        # Kullanıcıya dosya kaydetme yerini sor
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Received Data", "", "JSON Files (*.json);;All Files (*)", options=options)

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.data_list, file, indent=4, ensure_ascii=False)
                self.status_bar.showMessage(f"The data was saved to file {file_path}.")
                self.save_data_status_label.setText(f"Last Saved Data: {file_path} - {str(datetime.datetime.now())[:-7]}")
            except Exception as e:
                self.status_bar.showMessage(f"Data saving error: {e}")

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
