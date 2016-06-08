import os,sys,thread,socket
import url
import pickle
import hashlib
CLIENT_NUM = 50                 #max client can be connected
MAX_DATA_RECV = 4096            #message max size
redirectFile = open('redirectFile.pkl', 'rb')           #phishing words mapping file
forbiddenFile = open('forbiddenFile.pkl', 'rb')         #forbidden words mapping file
redirectDict = pickle.load(redirectFile)
forbiddenDict = pickle.load(forbiddenFile)
def ProxyClient(connectionSocket, addr):
    #message header parse to find the host and port
    request = connectionSocket.recv(MAX_DATA_RECV)
    head_line = request.split(r'\n')[0]
    url = head_line.split(' ')[1]
    print head_line
    print
    print "URL", url
    print   
    ########################
#     newMD5 = hashlib.md5()
#     newMD5.update(url)
#     cacheFilename = newMD5.hexdigest()+'.cached'
    #########################
    
    httpPos = url.find("://")
    if (httpPos == -1):
        t = url
    else:
        t = url[(httpPos+3):]
        
    portPos = t.find(":")
    
    webServerPos = t.find("/")
    if webServerPos == -1:
        webServerPos = len(t)
    
    webServer = ""
    port = -1
    if (portPos == -1 or webServerPos<portPos):
        port = 80
        webServer = t[:webServerPos]
    else:
        port = int(t[(portPos+1):][:webServerPos-portPos-1])
        webServer = t[:portPos]
    ###########################
#     notModified = False
#     dataToUpdate = ""
#     if os.path.exists(cacheFilename):
#         print 'Cache hit'
#         cacheFile = open(cacheFilename, 'rb')
#         cacheData = cacheFile.readlines()
#         for eLine in cacheData:
#             if "Date:" in eLine:
#                 try:
#                     modifiedRequest = head_line+'''\nHost: '''+webServer+'''\r\nIf-Modified-Since:'''+eLine.partition("Date:")[2]+'''\r\n\r\n'''
#                     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                     s.connect((webServer, port))
#                     s.send(modifiedRequest)
#                     while 1:
#                         data = s.recv(MAX_DATA_RECV)
#                     
#                         if len(data)>0:
#                                 ######lock here
#                             if "304 Not Modified" in data:
#                                 notModified = True
#                                 
#                                 break;
#                             else:
#                                 dataToUpdate = dataToUpdate+data
#                                 connectionSocket.send(data)
#                                 
#                         else:
#                             break
#                     s.close()
#                 except socket.error, (message):
#                     if s:
#                         s.close()
#                     print "Runtime Error:", message
#                     sys.exit(1) 
#                 break    
#         cacheFile.close()           
#         if notModified:
#             for eLine in cacheData:
#                 connectionSocket.send(eLine)
#         else:
#             cacheFile = open(cacheFilename, 'wb')
#             cacheFile.writelines(dataToUpdate)
#     else:
                       

    ###################################
    #matching the host to the phishing list and forbidden dictionary
    findFlag = False
    findFlag2 = False
    #matching to the phishing dictionary
    for redirectItem in redirectDict.keys():
        if redirectItem in webServer:   #got it!
            port = 80  #redirect to phishing port and host
            request = request.replace(webServer, redirectDict[redirectItem])
            webServer = redirectDict[redirectItem]
            findFlag = True
            break;
    print "Connect to:", webServer, port
    #matching to the forbidden dictionary
    if not findFlag:
        for forbiddenItem in forbiddenDict:
            if forbiddenItem in webServer:  #got it and sent 403 message to client
                connectionSocket.send('''HTTP/1.1 403 Forbidden\r\nContent-Type: text/html; charset=UTF-8\r\nDate: Wed, 08 Jan 2014 03:39:14 GMT\r\nServer: GFE/2.0\r\nAlternate-Protocol: 80:quic\r\n\r\n<html><head><title>Sorry...</title></head><body>you are forbidden by this request.</body></html>''')
                findFlag2 = True
                break;
    #Proxy Client
    if findFlag or (not findFlag and not findFlag2):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webServer, port))    #connect to the server
            s.send(request)
            while 1:    #receive message 
                data = s.recv(MAX_DATA_RECV)
                print type(data)
                if len(data)>0:
                    connectionSocket.send(data)
                else:
                    break
            s.close()
            connectionSocket.close()
        except socket.error, (message):
            if s:
                s.close()
            if connectionSocket:
                connectionSocket.close()
            print "Runtime Error:", message
            sys.exit(1)
def Server():
    port = int(raw_input("Enter port:"))  
    host = '127.0.0.1'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))    #bind the port to the socket
        s.listen(CLIENT_NUM)    #listen the "knocking"
    except socket.error, (message):
        if s:
            s.close()
        print "Socket create failed:", message
        sys.exit(1)
    
    while 1:    #listening...
        connectionSocket, addr = s.accept() #dispatch a thread to the connection
        print "s.accept()"
        thread.start_new_thread(ProxyClient, (connectionSocket, addr))
    s.close()
Server()

