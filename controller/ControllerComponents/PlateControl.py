from PyQt6.QtWidgets import QWidget, QHeaderView, QTableWidgetItem, QMessageBox
from PyQt6 import uic

from model.Dish.Dish import Dish
from model.Dish.Dish_DAO import Dish_DAO

from datetime import datetime
from datetime import date
import pandas as PD
import sqlite3

File_Qt = "view/components/Dish.ui"


class PlateControl(QWidget):
    def __init__(self) -> None:
        super(PlateControl, self).__init__()
        uic.loadUi(File_Qt, self)

        self.Table.horizontalHeader().setStretchLastSection(True)
        self.Table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.LoadData()

        self.BtnAdd.clicked.connect(self.RegisterDish)
        self.BtnEdit.clicked.connect(self.EditDish)
        self.BtnDelete.clicked.connect(self.DeleteDish)
        self.GenerateExcel.clicked.connect(self.Excel)

        self.BtnGetData.clicked.connect(self.GetText)
        self.BtnClean.clicked.connect(self.ClearField)

    def LoadData(self):
        list = Dish_DAO.SelectAll()
        for x in list:
            self.AddTableWidget(x)

    def ClearField(self):
        self.InputName.clear()
        self.InputDescription.clear()

    def GetText(self):
        Line = self.Table.currentRow()

        if Line == -1:
            Alert = QMessageBox()
            Alert.setIcon(QMessageBox.Icon.Warning)
            Alert.setWindowTitle("Alerta")
            Alert.setText("SELECIONE UMA LINHA NA TABELA PARA PEGAR OS DADOS!!")
            Alert.setStandardButtons(QMessageBox.StandardButton.Ok)
            x = Alert.exec()
        else:
            self.InputName.setText(self.Table.item(Line, 1).text())
            self.InputDescription.setText(self.Table.item(Line, 2).text())

    def Excel(self):
        connect = sqlite3.connect("./database/Restaurant.db")
        W = PD.read_sql_query("SELECT * FROM Dish ORDER BY Status ASC;", connect)
        W.to_excel("./DocsExcel/Lista_Cadastrado.xls", sheet_name="Platos", index=False)

        Alert = QMessageBox()
        Alert.setIcon(QMessageBox.Icon.Information)
        Alert.setWindowTitle("Alerta")
        Alert.setText("PLANILHA CRIADA COM SUCESSO, ESTÁ NA PASTA 'DocsExcel' !!")
        Alert.setStandardButtons(QMessageBox.StandardButton.Ok)
        x = Alert.exec()

    def RegisterDish(self):
        Hour = datetime.now()

        Name = self.InputName.text()
        Description = self.InputDescription.text()
        Price = self.InputPrice.text()
        Status = self.InputStatus.currentText()
        Created_at = f"{date.today()}  {Hour.hour}:{Hour.minute}"

        if Name == "" or Description == "" or Price == "" or Status == "":
            Alert = QMessageBox()
            Alert.setIcon(QMessageBox.Icon.Warning)
            Alert.setWindowTitle("Alerta")
            Alert.setText("PREENCHA TODOS OS CAMPOS !!")
            Alert.setStandardButtons(QMessageBox.StandardButton.Ok)
            x = Alert.exec()
        else:
            New = Dish(-1, Name, Description, Price, Status, Created_at)
            Id = Dish_DAO.AddDAO(New)
            New.Id = Id
            self.AddTableWidget(New)

            Alert = QMessageBox()
            Alert.setIcon(QMessageBox.Icon.Information)
            Alert.setWindowTitle("Alerta")
            Alert.setText("CADASTRO REALIZADO COM SUCESSO!!")
            Alert.setStandardButtons(QMessageBox.StandardButton.Ok)
            x = Alert.exec()

            self.ClearField()

    def DeleteDish(self):
        Line = self.Table.currentRow()

        if Line == -1:
            Alert = QMessageBox()
            Alert.setIcon(QMessageBox.Icon.Warning)
            Alert.setWindowTitle("Alerta")
            Alert.setText("SELECIONE UMA LINHA NA TABELA!!")
            Alert.setStandardButtons(QMessageBox.StandardButton.Ok)
            x = Alert.exec()
        else:
            LineId = self.Table.item(Line, 0)
            Id = LineId.text()

            Alert = QMessageBox()
            Alert.setIcon(QMessageBox.Icon.Warning)
            Alert.setWindowTitle("Alerta")
            Alert.setText(
                f"TEM CERTEZA QUE QUER APAGAR ESSE PRATO DO CARDÁPIO? CUJO Id {Id}"
            )
            Alert.setStandardButtons(
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            x = Alert.exec()

            if x == 1024:
                Line = self.Table.currentRow()
                LineId = self.Table.item(Line, 0)
                Id = LineId.text()
                self.Table.removeRow(Line)
                Dish_DAO.DeleteDAO(int(Id))
            if x == 4194304:
                x = Alert.close()

    def EditDish(self):
        Hour = datetime.now()
        Line = self.Table.currentRow()

        if Line == -1:
            Alert = QMessageBox()
            Alert.setIcon(QMessageBox.Icon.Warning)
            Alert.setWindowTitle("Alerta")
            Alert.setText("SELECIONE UMA LINHA NA TABELA!!")
            Alert.setStandardButtons(QMessageBox.StandardButton.Ok)
            x = Alert.exec()
        else:
            Name = self.InputName.text()
            Description = self.InputDescription.text()
            Price = self.InputPrice.text()
            Status = self.InputStatus.currentText()
            Created_at = f"{date.today()}  {Hour.hour}:{Hour.minute}"

            if Name == "" or Description == "" or Price == "" or Status == "":
                Alert = QMessageBox()
                Alert.setIcon(QMessageBox.Icon.Warning)
                Alert.setWindowTitle("Alerta")
                Alert.setText("PREENCHA TODOS OS CAMPOS !!")
                Alert.setStandardButtons(QMessageBox.StandardButton.Ok)
                x = Alert.exec()
            else:
                LineId = self.Table.item(Line, 0)
                Id = LineId.text()
                Update = Dish(-1, Name, Description, Price, Status, Created_at)
                self.Edition(Update)
                Dish_DAO.EditDAO(Update, int(Id))

                Alert = QMessageBox()
                Alert.setIcon(QMessageBox.Icon.Information)
                Alert.setWindowTitle("Alerta")
                Alert.setText("DADOS ATUALIZADOS COM REALIZADO COM SUCESSO!!")
                Alert.setStandardButtons(QMessageBox.StandardButton.Ok)
                x = Alert.exec()

                self.ClearField()

    def Edition(self, w: Dish):
        Hour = datetime.now()

        Line = self.Table.currentRow()

        Name = self.InputName.text()
        Description = self.InputDescription.text()
        Price = self.InputPrice.text()
        Status = self.InputStatus.currentText()
        Created_at = f"{date.today()}  {Hour.hour}:{Hour.minute}"

        Name = QTableWidgetItem(w.Name)
        Description = QTableWidgetItem(w.Description)
        Price = QTableWidgetItem(f"R$ {w.Price}")
        Status = QTableWidgetItem(w.Status)
        Created_at = QTableWidgetItem(w.Created_at)

        self.Table.setItem(Line, 1, Name)
        self.Table.setItem(Line, 2, Description)
        self.Table.setItem(Line, 3, Price)
        self.Table.setItem(Line, 4, Status)
        self.Table.setItem(Line, 5, Created_at)

    def AddTableWidget(self, w: Dish):
        Line = self.Table.rowCount()
        self.Table.insertRow(Line)

        Id = QTableWidgetItem(str(w.Id))
        Name = QTableWidgetItem(w.Name)
        Description = QTableWidgetItem(w.Description)
        Price = QTableWidgetItem(f"R$ {w.Price}")
        Status = QTableWidgetItem(w.Status)
        Created_at = QTableWidgetItem(w.Created_at)

        self.Table.setItem(Line, 0, Id)
        self.Table.setItem(Line, 1, Name)
        self.Table.setItem(Line, 2, Description)
        self.Table.setItem(Line, 3, Price)
        self.Table.setItem(Line, 4, Status)
        self.Table.setItem(Line, 5, Created_at)
