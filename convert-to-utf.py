import os
import chardet 

def convert_file(filepath:str) -> str:
  outfile =os.path.splitext(filepath)[0] + "-utf8"+ os.path.splitext(filepath)[1]
  content = ""
  data=bytes()
  with open(file=filepath, mode="rb") as f:
      data = f.read()
  for encoding in ["utf-8", "utf-16", "GB2312", "GBK", "unicode", "GB18030", "Latin1"]:
      try:
          content = data.decode(encoding)
          break
      except:
          continue
  
  f = open(outfile, "w")
  f.write(content)
  f.close()
  if os.path.exists(outfile) and os.path.getsize(outfile) > 0:
    return True
  else:
    print('failed to convert or output utf format file')
    return False
  
filename = os.getenv('filename', '')
if len(filename)>0:
  convert_file(filename)