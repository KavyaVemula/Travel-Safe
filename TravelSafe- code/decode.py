from qrtools import QR
myCode = QR(filename=u"C:\\Users\\kavyareddy\\Downloads\\drivert.png")
if myCode.decode():
  print myCode.data
  print myCode.data_type
  print myCode.data_to_string()
  
