import socket
import json
import os
import sys
import requests

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 65432
    print(HOST)
except socket.error as error:
    print("Lỗi khi tạo socket: " + error)
    sys.exit(1)

try:
    sock.bind((HOST, PORT))
    sock.listen(10)
except socket.gaierror as error:
    print("Address-related error connecting to server: ", error)
    sys.exit(1)
except socket.error as error:
    print("Lỗi kết nối: ", error)
    sys.exit(1)

print("Waiting for Client")
conn, addr = sock.accept()
try:
    print("Connected by ", addr)
    while True:
        MenuChoose = conn.recv(1024)
        ClientChoose = (int)(MenuChoose.decode("utf8"))

        # Sign in process
        if ClientChoose == 1:
            print("Client yêu cầu đăng nhập")

            print("Loading Database...")
            with open("user.json", "r") as fin:
                userdata = json.load(fin)
            print("Hoàn thành Load Database")
            c = 1
            UserName = conn.recv(1024)
            PassWord = conn.recv(1024)
            print("Thông tin đăng nhập của Client:")
            print("Username: " + UserName.decode("utf8"))
            print("Password: " + PassWord.decode("utf8"))
            for temp in userdata:
                if UserName.decode("utf8") == temp['username'] and PassWord.decode("utf8") == temp['password']:
                    c = 0   # Sign in information wrong
            if c == 0:
                msg = "Sign in successfully"
            else:
                msg = "Sign in failed"
            print(msg)
            conn.sendall(bytes(msg, "utf8"))

            print("Bắt đầu quá trình quy đổi tiền tệ")
            while True:
                print("Đang lấy dữ liệu từ tổ chức thứ ba...")
                response = requests.get(f'https://freecurrencyapi.net/api/v2/latest?apikey=4a29fab0-698e-11ec-bcc8-61c50220b664')
                data = response.json();
                currency_rate = data["data"]
                print("Lấy dữ liệu thành công")
                print("Bắt đầu nhận dữ liệu từ Client và phản hồi")
                CurrencyNeedConvert = conn.recv(1024)
                print("Client muốn quy đổi từ " + CurrencyNeedConvert.decode("utf8") + "sang VNĐ")
                if CurrencyNeedConvert.decode("utf8") == "USD":
                    print("Đã tìm thấy loại tiền tệ Client yêu cầu")
                    conn.sendall(bytes("1", "utf8"))
                    conn.sendall(bytes((str)(currency_rate["VND"]), "utf8"))
                elif CurrencyNeedConvert.decode("utf8") in currency_rate:
                    print("Đã tìm thấy loại tiền tệ Client yêu cầu")
                    conn.sendall(bytes((str)(currency_rate[CurrencyNeedConvert.decode("utf8")]),"utf8"))
                    conn.sendall(bytes((str)(currency_rate["VND"]),"utf8"))
                else:
                    msg = "Không tìm thấy đơn vị tiền tệ này!"
                    print("Loại tiền tệ này không tồn tại")
                    conn.sendall(bytes(msg, "utf8"))

        # Sign up process
        if ClientChoose == 2:
            print("Client yêu cầu Đăng ký Account mới")
            c = 1
            UserName = conn.recv(1024)
            PassWord = conn.recv(1024)
            print("Thông tin đăng ký của Client:")
            print("Username: " + UserName.decode("utf8"))
            print("Password: " + PassWord.decode("utf8"))

            print("Loading Database...")
            with open("user.json", "r") as fin:
                userdata = json.load(fin)
            print("Hoàn thành Load Database")

            for temp in userdata:
                if UserName.decode("utf8") == temp['username'] and PassWord.decode("utf8") == temp['password']:
                    c = 0   # User Existed
            if c == 0:
                print("Không thể đăng ký do tài khoản đã tồn tại")
                msg = "User Existed"
            else:
                print("Đăng ký thành công. Đang ghi dữ liệu vào Database...")
                userdata.append({'username' : UserName.decode("utf8"), 'password' : PassWord.decode("utf8")})
                with open("user.json", "w") as fout:
                    json.dump(userdata, fout)
                msg = "Sign up successfully"
                print("Hoàn thành ghi dữ liệu vào Database")
            conn.sendall(bytes(msg, "utf8"))

        # Exit Process
        if ClientChoose == 3:
            break

except KeyboardInterrupt:
    conn.close()
    # s.close()
finally:
    conn.close()
    # s.close()
