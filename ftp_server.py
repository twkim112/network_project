import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# 디렉토리 생성
ftp_directory = "C:/ftp"
if not os.path.exists(ftp_directory):
    os.makedirs(ftp_directory)

# 사용자 설정
authorizer = DummyAuthorizer()
authorizer.add_user("user", "12345", ftp_directory, perm="elradfmw")
authorizer.add_anonymous(ftp_directory, perm="elradfmw")

# 핸들러 설정
handler = FTPHandler
handler.authorizer = authorizer

# FTP 서버 시작
server = FTPServer(("127.0.0.1", 21), handler)
server.serve_forever()
