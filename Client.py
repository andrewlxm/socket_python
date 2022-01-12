import os
import socket
import os
import sys

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as error:
    print("Lỗi tạo Socket: ", error)
    sys.exit(1)

host = input("Nhập địa chỉ IP: ")
port = input("Nhập số port của Server (65432): ")

try:
    server_Adrress = (host, int(port))
    client.connect(server_Adrress)
except socket.gaierror as error:
    print("Address-related error connecting to server: ", error)
    sys.exit(1)
except socket.error as error:
    print("Error: ", error)
    sys.exit(1)

try:
    while True:
        os.system('CLS')
        print("MENU")
        print("1. Đăng Nhập")
        print("2. Đăng Ký")
        print("3. Thoát")
        choose = input("Lựa chọn của bạn: ")
        client.sendall(bytes(choose,"utf8"))

        if choose == '1':
            UserName = input("Username: ")
            PassWord = input("Password: ")
            client.sendall(bytes(UserName, "utf8"))
            client.sendall(bytes(PassWord, "utf8"))
            data = client.recv(1024)
            print(data.decode("utf8"))
            if data.decode("utf8") == "Sign in successfully":
                while True:
                    Currency = input("Bạn muốn đổi từ đơn vị tiền tệ nào sang VND? ")
                    client.sendall(bytes(Currency, "utf8"))
                    data_recv = client.recv(1024)
                    if data_recv.decode("utf8") == "NO":
                        print("Không tìm thấy loại tiền tệ")
                    else:
                        CurrencyNeedConvert_recv = data_recv
                        VND_recv = client.recv(1024)
                        MoneyInCurrency = float(CurrencyNeedConvert_recv.decode("utf8"))
                        VND = float(VND_recv.decode("utf8"))
                        FromVNDToCurrency = VND/MoneyInCurrency
                        print("1" + Currency + " = " + str(FromVNDToCurrency) + "VND.")
                        Money = input("Bạn muốn đổi bao nhiêu tiền từ " + Currency + " sang VND? ")
                        MoneyInVND = int(Money) * FromVNDToCurrency
                        print(Money + Currency + " = " + str(MoneyInVND) + "VND.")
                    Continue = "-1"
                    while Continue != "1" or Continue != "0":
                        Continue = input("Bạn muốn tiếp tục không? 1: CÓ/ 0: KHÔNG ")
                        if Continue == "0" or Continue == "1":
                            break
                    if Continue == "0":
                        break
        if choose == '2':
            UserName = input("Username: ")
            PassWord = input("Password: ")
            client.sendall(bytes(UserName, "utf8"))
            client.sendall(bytes(PassWord, "utf8"))
            data = client.recv(1024)
            print(data.decode("utf8"))
        if choose == '3':
            break;
except KeyboardInterrupt:
    client.close()
finally:
    client.close()

