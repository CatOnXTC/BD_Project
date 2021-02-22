from faker import Faker
import xlwt 
from sqlalchemy import create_engine
import sqlite3
import pathlib
import sys

path = pathlib.Path(__file__).parent.absolute()
fake = Faker('pl_PL')
workbook = xlwt.Workbook()  
sheet = workbook.add_sheet("Random_Data") 

def generateFakeData(n):
    sheet.write(0, 0, 'FIRST_NAME') 
    sheet.write(0, 1, 'LAST_NAME') 
    sheet.write(0, 2, 'PESEL') 

    Faker.seed(0)
    for i in range(n):
        sheet.write(i+1,0,fake.first_name_nonbinary())
        sheet.write(i+1,1,fake.last_name_nonbinary())
        sheet.write(i+1,2,fake.pesel())
    workbook.save(str(path)+"\\users.xls")
  
if __name__ == "__main__":
    if (len(sys.argv) > 1):
        generateFakeData(int(sys.argv[1])) 
    else:
        generateFakeData(20)