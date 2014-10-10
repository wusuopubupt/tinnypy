"""
@author : wdxbupt2009@gmail.com
@desc   : import data from excel to mysql db
@date   : 2014-10-10

"""

import xlrd
import MySQLdb

def import_data_from_excel():
    # Open the workbook and define the worksheet
    book = xlrd.open_workbook("cities.xls")
    sheet = book.sheet_by_name("Sheet1") 
    
    db = MySQLdb.connect (host="localhost", user = "user", passwd = "xxx", db = "cities")
    cursor = db.cursor()
    query = """INSERT INTO cities(xy, dock_xy) VALUES ('%s,%s', '%s, %s')"""
    
    # Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
    for r in range(1, sheet.nrows):
          #city_name      = sheet.cell(r,).value
          city_x = sheet.cell(r,1).value
          city_y = sheet.cell(r,2).value
          dock_x = sheet.cell(r,3).value
          dock_y = sheet.cell(r,3).value
    
          values = (city_x, city_y, dock_x, dock_y)
          cursor.execute(query, values)
    
    cursor.close()
    # Commit the transaction
    db.commit()
    db.close()
    
    print("Done...")

def main():
    import_data_from_excel()

if __name__ == "__main__":
    main()
