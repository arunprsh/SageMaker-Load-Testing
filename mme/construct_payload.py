headers = 'id,text,filename__v,format__v,size__v,charsize,pages__v'

id_ = '31011'
text = """Investigational Product Accountability Log


"""
filename__v = 'foo.docx'
format__v = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
size__v = '16290'
charsize = '768'
pages__v = '1'

row = ','.join([id_, repr(text), filename__v, format__v, size__v, charsize, pages__v])
PAYLOAD = headers + '\n' + row