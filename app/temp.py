from app import db
import xlrd
from datetime import date
from app.models.info import Cource, Part_Course


book = xlrd.open_workbook('temp.xls')
sh = book.sheet_by_index(0)
i = 1
nows = date.today()
while sh.cell_value(rowx=i+1, colx=0) != 'end':

    ids = int(sh.cell_value(rowx=i, colx=0))
    keys = db.session.query(Cource).filter(Cource.to_student == int(sh.cell_value(rowx=i, colx=1))).first().id
    for j in range(80):
        if sh.cell_value(rowx=i, colx=j+2) == "done":
            print(ids, keys, " ", j)
    i += 1
