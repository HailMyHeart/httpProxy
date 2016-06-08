import pickle, os
redirectDict = {"hit": "www.baidu.com",
         "4399": "www.zhihu.com",
         "google": "www.baidu.com",}
forbiddenDict = ["163", "126", "sogou", "qq"]
output = open('redirectFile.pkl', 'wb')
output2 = open('forbiddenFile.pkl', 'wb')
# Pickle the list using the highest protocol available.
pickle.dump(redirectDict, output, -1)
pickle.dump(forbiddenDict, output2, -1)
output.close()
output2.close()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print BASE_DIR, os.path.join(BASE_DIR,'templates')