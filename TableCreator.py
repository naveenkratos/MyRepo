
from prettytable import PrettyTable

class TableCreator:

    def __init__(self,config,mongo):
        self.config = config
        self.mongo = mongo
        self.createTable()

    def createTable(self):

        tabular_fields = ["IP", "Country", "Owner","Detected urls","UnDetected urls","Detected Downloaded Samples","UnDetected Downloaded Samples"]
        self.tabular_table = PrettyTable()
        self.tabular_table.field_names = tabular_fields 

    def insertRow(self,rowData):

        self.tabular_table.add_row(rowData)

    def getHtmlTableData(self):

        return self.tabular_table.get_html_string()

