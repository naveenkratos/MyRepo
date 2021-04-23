
from prettytable import PrettyTable

class TableCreator:

    def __init__(self,config,mongo):
        self.config = config
        self.mongo = mongo
        self.createTable()
        self.rowCount = 0

    def createTable(self):

        tabular_fields = ["S.NO","IP", "Country", "Owner","Detected urls","UnDetected urls","Detected Downloaded Samples","UnDetected Downloaded Samples"]
        self.tabular_table = PrettyTable()
        self.tabular_table.field_names = tabular_fields 

    def insertRow(self,rowData):
        self.rowCount += 1
        rowData.insert(0,str(self.rowCount))
        self.tabular_table.add_row(rowData)

    def getHtmlTableData(self):

        return self.tabular_table.get_html_string()

