#Only a stub, to see if the code runs. 

from Excelutilities.workbook_debugging.workbook_similarity_measures import similarity_values_only

book2 = r"C:\Users\ethan\OneDrive\Documents\workbook similarity test 2.xlsx"
book1 = r"C:\Users\ethan\OneDrive\Documents\test for similarity.xlsx"
val=similarity_values_only(book1=book1, sheet1="Sheet1", book2=book2, sheet2="Sheet2")
print(val)