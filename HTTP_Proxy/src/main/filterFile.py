import pickle, os, cStringIO
redirectDict = {"baidu": "m.jb51.net",
         "4399": "www.pythonclub.org",
         "google": "blog.csdn.net",}
forbiddenDict = ["163", "126", "sogou", "qq"]
output = open('redirectFile.pkl', 'wb')
output2 = open('forbiddenFile.pkl', 'wb')
pickle.dump(redirectDict, output, -1)
pickle.dump(forbiddenDict, output2, -1)
output.close()
output2.close()
f = open('223.txt', 'rb')
fileBuffer = cStringIO.StringIO(f.read())
f.close()
print fileBuffer.seek(0, 0)
print len(fileBuffer.read())
fileBuffer.__sizeof__()
