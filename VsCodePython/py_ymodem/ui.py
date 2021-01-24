#coding=utf-8
 
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter import messagebox
from ctypes import *
import serial.tools.list_ports
import threading
from ymodem import YMODEM
import os
from time import sleep
 
app = Tk()
comportbox = Combobox(app, width=7, height=10)
baudratebox = Combobox(app, width=8, height=10)
red_canvas = Canvas(app, width=50, height=50, bg="red")
green_canvas = Canvas(app, width=50, height=50, bg="green")
progress_bar = Canvas(app, width=350, height=26, bg="white")
fill_line = progress_bar.create_rectangle(2, 2, 0, 27, width=0, fill="green") 
ser = serial.Serial(bytesize=8, parity='N', stopbits=1, timeout=1, write_timeout=3)
linsten_lock = threading.Lock()
need_listen = 0
exit_listen = False
 
def upgrade_callback(total_packets, file_size, file_name):
    if len(progress_bar.gettags("text")) == 0:
        progress_bar.create_text(175, 15, text=file_name, tags="text")
    progress = total_packets*350/(file_size/1024)
    progress_bar.coords(fill_line, (0, 0, progress, 30))
 
def set_connect_logo(is_connected = True):
    if is_connected:
        red_canvas.place_forget()
        green_canvas.place(x=100, y=60)
        comportbox.configure(state='disabled')
        baudratebox.configure(state='disabled')
    else:
        green_canvas.place_forget()
        red_canvas.place(x=100, y=60)
        comportbox.configure(state='enabled')
        baudratebox.configure(state='enabled')
 
 
def listen_connect_thread():
    global ser
    global need_listen
    global exit_listen
    global linsten_lock
    while exit_listen == False:
        linsten_lock.acquire()
        if need_listen == 0:
            linsten_lock.release()
            sleep(1)
            continue
        else:
            com_number = comportbox.get()
            port_found = 0
            plist = list(serial.tools.list_ports.comports())
        
            if len(plist) <= 0:
                if ser.is_open == True:
                    ser.close()
                set_connect_logo(False)
            else:
                for item in plist:
                    if com_number == item[0]:
                        port_found = 1
                        break
                if port_found == 0:
                    if ser.is_open == True:
                        ser.close()
                    set_connect_logo(False)
                else:
                    if ser.is_open == False:
                        try:
                            ser.port = com_number
                            ser.open()
                            set_connect_logo(True)
                        except Exception as e:
                            print(e)
                            pass
            linsten_lock.release()
            sleep(0.3)
            continue
 
def connect():
    global need_listen
    global ser
    com_number = comportbox.get()
    
    port_found = 0
    plist = list(serial.tools.list_ports.comports())
    
    if ser.is_open == True:
        messagebox.showinfo(title="Error", message="Already connected！")
        return
 
    if len(plist) <= 0:
        messagebox.showinfo(title="Error", message="No available serial!")
        need_listen = 0
        set_connect_logo(False)
        return
    else:
        for item in plist:
            if com_number == item[0]:
                port_found = 1
                break
        if port_found == 0:
            need_listen = 0
            set_connect_logo(False)
            messagebox.showinfo(title="Error", message="Cannot find serial "+com_number)
            return
    try:
        ser.port = com_number
        ser.baudrate = 115200 #int(baud_rate)
        if ser.is_open == False:
            ser.open()
    except Exception as e:
        if ser.is_open == False:
            need_listen = 0
            set_connect_logo(False)
        messagebox.showinfo(title="Error", message=e)
        return
 
    set_connect_logo(True)
    need_listen = 1
    
    global listen_connect
    if listen_connect.is_alive() == False:
        listen_connect.start()
 
    
def disconnect():
    global ser
    global need_listen
    global linsten_lock
    linsten_lock.acquire()
    need_listen = 0
    linsten_lock.release()
    #sleep(0.1)
 
    if ser.is_open == False:
        messagebox.showinfo(title="Error", message="Serial not connected！")
    else:
        try:
            ser.close()
        except Exception as e:
            messagebox.showinfo(title="Error", message=e)
            return
    need_listen = 0
    set_connect_logo(False)
 
def cancel():
    global ymodem_sender
    if upgrade_button['state'] == 'disabled':
        ymodem_sender.abort()
 
def upgrade():
    global upgrade_button
    if ser.is_open == False:
        messagebox.showinfo(title="Error", message="Please connect the serial first！")
        upgrade_button.configure(state='active')
        return
    file_list = filedialog.askopenfilenames(filetypes=[("bin file", "*.bin"),("all","*.*")])
    if len(file_list) <= 0:
        upgrade_button.configure(state='active')
        return
    else:
        ret_val = prepare_upgrade()
    if ret_val < 0:
        upgrade_button.configure(state='active')
        return
    
    upgrade_button.configure(state='disabled')
    disconnect_button.configure(state='disabled')
    upgrade_thread = threading.Thread(target=do_upgrade, args=(file_list,))
    upgrade_thread.start()
 
def show_progress_bar(show=True):
    if show:
        progress_bar.place(x=10, y=150)
    else:
        progress_bar.place_forget()
        progress_bar.coords(fill_line, (0, 0, 0, 30))
        progress_bar.delete('text')
 
def serial_reconnect(baud_rate=115200, timeout=1):
    need_sleep = 1
    if  ser.baudrate == baud_rate:
        need_sleep = 0
    try:
        ser.timeout = timeout
        ser.baudrate = baud_rate
        ser.close()
        ser.open()
    except Exception as e:
        raise Exception("Reconnect Fail")
    if need_sleep:
        sleep(1)
    
def do_upgrade(file_list):
    global upgrade_button
    need_listen = 0 
    sleep(1)
    baud_rate = baudratebox.get()
    try:
        serial_reconnect()
    except Exception as e:
        print(e)
    ser.write("\r".encode("utf-8"))
    ch_str = "upgrade -t 0 " + str(int(baud_rate)) + "\r"
    ser.write(ch_str.encode("utf-8"))
    sleep(1)
 
    for file in file_list:
        file_size = os.path.getsize(file)
        if file_size > 2*1024*1024:
            continue
        try:
            serial_reconnect(baud_rate=int(baud_rate), timeout=5)
        except Exception as e:
            print(e)
        show_progress_bar(True)
        if len(progress_bar.gettags("text")) == 0:
            progress_bar.create_text(175, 15, text=os.path.basename(file), tags="text")
        ser.read_all()
        ser.write("\r".encode("utf-8"))
        ser.write("upgrade -u\r".encode("utf-8"))
        
        while True:
            ch_str = ser.read(4).decode("utf-8")
            if ch_str == "CCCC":
                break
        ymodem_send(file)
        while True:
            if ser.read(1).decode("utf-8") == 'I':
                if ser.read(1).decode("utf-8") == 'E':
                    if ser.read(1).decode("utf-8") == 'T':
                        ymodem_sender.log.info("Receive IET")
                        show_progress_bar(False)
                        sleep(1)
                        break
                    else:
                        continue
                else:
                    continue
    
    show_progress_bar(False)
    try:
        ser.write("\r".encode("utf-8"))
        ser.write("upgrade -t 0 115200\r".encode("utf-8"))
        sleep(1)
        serial_reconnect()
    except Exception as e:
        print(e)
    upgrade_button.configure(state='active')
    disconnect_button.configure(state='active')
    need_listen = 1
    
def ymodem_send(file):
    global ymodem_sender
    try:
        file_stream = open(file, 'rb')
    except IOError as e:
        raise Exception("Open file fail!")
    file_name = os.path.basename(file)
    file_size = os.path.getsize(file)
    
    rate = baudratebox.get()
    
    try:
        serial_reconnect(baud_rate = int(rate), timeout=5)
    except Exception as e:
        messagebox.showinfo(title="Error", message="Connection error！")
        return
 
    try:
        ymodem_sender.send(file_stream, file_name, file_size, callback=upgrade_callback)
    except Exception as e:
        file_stream.close()
        raise
    file_stream.close()
  
def prepare_upgrade():
    global ser
    ser.flushOutput()
    ser.flushInput()
    ser.write("\r".encode("utf-8"))
    ret_str = ser.read(1024).decode("utf-8")
    
    b_reset= False
    if ret_str.find("IET") == -1:
        try:
            serial_reconnect(baud_rate = 9600)
            b_reset = True
        except Exception as e:
            messagebox.showinfo(title="Error", message=e)
            return -1
    ser.read_all()
    ser.write("flash -u\r".encode("utf-8"))
    sleep(0.5)
    read_byte = ser.read_all()
    
    if len(read_byte) <= 3:
        b_reset = True
    else:
        ret_str = read_byte[0:min(20,len(read_byte))].decode("utf-8")
        if ret_str.find("IET") != -1:
            b_reset = True
        else:
            b_reset = False
    if b_reset:
        messagebox.showinfo(title="Tips", message="Please reset/reconnect board first, then press [OK]")
        sleep(0.5)
        serial_reconnect()
    return 0
    
def sender_getc(size):
    return ser.read(size) or None
 
def sender_putc(data):
    send_data_mutex.acquire()
    ser.write(data)
    send_data_mutex.release()
 
 
connect_button = Button(app, text="连接", width=8, height=1, command=connect)
disconnect_button = Button(app, text="断开", width=8, height=1, command=disconnect)
upgrade_button = Button(app, text="升级", width=8, height=1, command=upgrade)
cancel_button = Button(app, text="取消升级", width=8, height=1, command=cancel) 
listen_connect = threading.Thread(target=listen_connect_thread)
send_data_mutex = threading.Lock()
ymodem_sender = YMODEM(sender_getc, sender_putc)
 
 
 
def init_layout():
    app.title("Py Ymodem Upgrade Tool")
    app.iconbitmap("H:/python study/VsCodePython/py_ymodem/python.ico")
    app.geometry('400x200') 
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.resizable(width=False, height=False)
 
    Label(app, text="端口：", font=('Arial', 14)).place(x=10, y=10)
 
    comportbox["value"] = ("COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9","COM10")
    comportbox.current(2)
    comportbox.place(x=75, y=14)
    
    Label(app, text="波特率：", font=('Arial', 14)).place(x=200, y=10)
 
    baudratebox["value"] = ("9600","115200","230400","576000")
    baudratebox.current(1)
    baudratebox.place(x=285, y=14)
    
    connect_button.place(x=10,y=50)
    disconnect_button.place(x=10,y=100)
    cancel_button.place(x=285,y=50)
    upgrade_button.place(x=285,y=100)
    
    show_progress_bar(False)
    
    set_connect_logo(False)
 
def main():
    init_layout()
    mainloop()
 
def on_closing():
    exit_listen = True
    sleep(0.4)
    try:
        ser.close()
    except Exception as e:
        print(e)
        pass 
    app.destroy()
 
if __name__ == '__main__':
    main()