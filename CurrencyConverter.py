# Currency Converter Project

import sys
import requests
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QLineEdit, QListWidget)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from datetime import datetime, date, time, timedelta
import random


class Currency_Converter(QWidget):
    def __init__(self):
        super().__init__()
        self.headline = QLabel("Currency Converter", self)
        self.ask_selection = QLabel("Please select the Currency", self)

        self.from_currency_dropdown = QComboBox(self)
        self.to_currency_dropdown = QComboBox(self)

        self.amount_input_box = QLineEdit(self)
        self.swap_button = QPushButton("\u21C4", self)
        self.exchnage_amount_box = QLineEdit(self)
        self.error_info = QLabel(self)

        self.canvas = FigureCanvasQTAgg(Figure())
        self.ax = self.canvas.figure.add_subplot(111)     

        self.history_label = QLabel("Conversion History", self)
        self.history_list = QListWidget(self)
        self.clear_history_button = QPushButton("Clear History", self)  

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Currency Converter App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.headline)
        vbox.addWidget(self.ask_selection)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.from_currency_dropdown)
        hbox1.addWidget(self.to_currency_dropdown)

        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.amount_input_box)
        hbox2.addWidget(self.swap_button)
        hbox2.addWidget(self.exchnage_amount_box)

        vbox.addLayout(hbox2)

        vbox.addWidget(self.error_info)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.history_label)
        self.history_list.setMaximumHeight(150)
        vbox.addWidget(self.history_list)
        vbox.addWidget(self.clear_history_button)

        self.setLayout(vbox)

        self.headline.setObjectName("headline")
        self.ask_selection.setObjectName("ask_selection")
        self.to_currency_dropdown.setObjectName("to_currency_dropdown")
        self.from_currency_dropdown.setObjectName("from_currency_dropdown")
        self.amount_input_box.setObjectName("amount_input_box")
        self.exchnage_amount_box.setObjectName("exchnage_amount_box")
        self.swap_button.setObjectName("swap_button")
        self.error_info.setObjectName("error_info")

        self.headline.setAlignment(Qt.AlignCenter)
        self.ask_selection.setAlignment(Qt.AlignCenter)
        self.amount_input_box.setAlignment(Qt.AlignCenter)
        self.exchnage_amount_box.setAlignment(Qt.AlignCenter)
        self.error_info.setAlignment(Qt.AlignCenter)

        self.amount_input_box.setFixedWidth(100)
        self.amount_input_box.setFixedHeight(40)

        self.swap_button.setFixedWidth(40)
        self.swap_button.setFixedHeight(40)

        self.exchnage_amount_box.setFixedWidth(100)
        self.exchnage_amount_box.setFixedHeight(40)

        self.loadStylecss()
        self.amount_input_box.textChanged.connect(self.get_exchnage_amount)
        self.from_currency_dropdown.currentTextChanged.connect(self.get_exchnage_amount)
        self.to_currency_dropdown.currentTextChanged.connect(self.get_exchnage_amount)
        self.swap_button.clicked.connect(self.swap_currencies)
        self.clear_history_button.clicked.connect(self.clear_history)
        self.load_dropdown_currencies()
        

    def loadStylecss(self):
        try:
            with open("CurrencyConverter.css", "r") as C:
                self.setStyleSheet(C.read())
        except FileNotFoundError:
            print("CurrencyConverter.css not found")

    def swap_currencies(self):
        from_amount = self.from_currency_dropdown.currentText()
        to_amount = self.to_currency_dropdown.currentText()

        self.from_currency_dropdown.currentTextChanged.disconnect(self.get_exchnage_amount)
        self.to_currency_dropdown.currentTextChanged.disconnect(self.get_exchnage_amount)
        
        self.from_currency_dropdown.setCurrentText(to_amount)
        self.to_currency_dropdown.setCurrentText(from_amount)

        self.from_currency_dropdown.currentTextChanged.connect(self.get_exchnage_amount)
        self.to_currency_dropdown.currentTextChanged.connect(self.get_exchnage_amount)

        self.get_exchnage_amount()


    def load_dropdown_currencies(self):
        api_key = "bca7637ed97e3c301a94d7aa"
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data["result"] == "success":
                codes = [code[0] for code in data["supported_codes"]]
                self.from_currency_dropdown.blockSignals(True)
                self.to_currency_dropdown.blockSignals(True)

                self.from_currency_dropdown.clear()
                self.to_currency_dropdown.clear()
                self.from_currency_dropdown.addItems(codes)
                self.to_currency_dropdown.addItems(codes)

                self.from_currency_dropdown.setCurrentText("USD")
                self.to_currency_dropdown.setCurrentText("PKR")

                self.from_currency_dropdown.blockSignals(False)
                self.to_currency_dropdown.blockSignals(False)

                self.error_info.clear()

        except Exception as e:
            if self.from_currency_dropdown.count() == 0:
                self.display_error("Check Internet Connection")

    def get_exchnage_amount(self):
        api_key = "bca7637ed97e3c301a94d7aa"
        from_currency = self.from_currency_dropdown.currentText()
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            self.diplay_exchnage_amount(data)
            self.update_chart(data)

        except requests.exceptions.HTTPError as HTTPerror:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from server")
                case _:
                    self.display_error(f"HTTP Error Occured:\n{HTTPerror}")
            
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nPlease check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nRequest took too long")
        except requests.exceptions.RequestException as req_excep:
            self.display_error(f"Request Error:\n{req_excep}")


    def display_error(self, message):
        self.error_info.setText(message)

    def diplay_exchnage_amount(self, data):
        if not self.amount_input_box.text():
            self.exchnage_amount_box.clear()
            self.error_info.clear()
            return

        try:
            amount = float(self.amount_input_box.text())
        except ValueError:
            self.display_error("Please enter a valid amount")
            return
        
        to_currency = self.to_currency_dropdown.currentText()
        from_currency = self.from_currency_dropdown.currentText()

        try:
            rate = data["conversion_rates"][to_currency]
        except KeyError:
            self.display_error(f"Currency {to_currency} not found")
            return

        result = amount * rate
        formatted_result = f"{result:.3f}"
        self.exchnage_amount_box.setText(formatted_result)

        self.error_info.clear()

        self.save_to_history(amount, from_currency, to_currency, result)


    def update_chart(self, data):
        from_c = self.from_currency_dropdown.currentText()    
        to_c = self.to_currency_dropdown.currentText()

#        api_key = "bca7637ed97e3c301a94d7aa"
#
#        dates = []
#        rates = []
#
#        for i in range(7):
#            date = datetime.now() - timedelta(days=i)
#            url = f"https://v6.exchangerate-api.com/v6/{api_key}/history/{from_c}/{date.year}/{date.month}/{date.day}"

#            try:
#                response = requests.get(url)
#                history_data = response.json()
#                if history_data.get("result") == "success":
#                    rate = data["conversion_rates"].get(to_c)
#                    if rate:
#                        dates.append(date.strftime("%b %d"))
#                        rates.append(rate)
#            except:
#                continue

#        if rates:
#            dates.reverse()
#            rates.reverse()
    

        try:
            current_rate = data["conversion_rates"][to_c]
        except KeyError:
            current_rate = 1.0

        dates = []
        for i in range(6, -1, -1):
            d = datetime.now() - timedelta(days=i)
            dates.append(d.strftime("%b %d"))

        rates = []
        last_rate = current_rate
        for i in range(7):
            variation = last_rate * random.uniform(-0.02, 0.02)
            last_rate = last_rate + variation
            rates.append(round(last_rate, 4))
        
        rates[-1] = current_rate

        self.ax.clear()
        
        chart_color = random.choice(['#588157', '#bc6c25', '#2d5a27', '#d4a373'])
        
        self.ax.plot(dates, rates, marker='o', linestyle='-', color=chart_color, linewidth=2)
        
        self.ax.set_title(f"{from_c} to {to_c} (7-Day Trend) (Mock Data)", color="#2d5a27", fontsize=10)
        self.ax.set_facecolor('#fefae0')
        
        self.canvas.figure.autofmt_xdate()
        self.canvas.figure.tight_layout()
        self.canvas.draw()


    def save_to_history(self, amount, from_currency, to_currency, result):
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")

        history_text = f"{amount:.2f} {from_currency} → {result:.2f} {to_currency} ({time_str})"

        self.history_list.insertItem(0, history_text)

        if self.history_list.count() > 20:
            self.history_list.takeItem(self.history_list.count() - 1)

    def clear_history(self):
        self.history_list.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    cc = Currency_Converter()
    cc.show()
    sys.exit(app.exec_())