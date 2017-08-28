import csv

 
fieldnames = ['Column1', 'Column2', 'Column3', 'Column4']
rows = [{'Column1': '0', 'Column2': '1', 'Column3': '2', 'Column4': '3'},
{'Column1': '0', 'Column2': '1', 'Column3': '2', 'Column4': '3'},
{'Column1': '0', 'Column2': '1', 'Column3': '2', 'Column4': '3'},
{'Column1': '0', 'Column2': '1', 'Column3': '2', 'Column4': '3'},
{'Column1': '0', 'Column2': '1', 'Column3': '2', 'Column4': '3'}]
dict_writer = csv.DictWriter(file('your.csv', 'wb'), fieldnames=fieldnames)
dict_writer.writeheader() 
dict_writer.writerows(rows)