import pypyodbc

connection = pypyodbc.connect('Driver={SQL Server};'
                              'Server=;'
                              'Database=КомпьютерныйКлуб;')
cursor = connection.cursor()
