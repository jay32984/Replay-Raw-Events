import logging, logging.handlers, socket, subprocess
from Tkinter import *

PORT = 514
PROT = socket.SOCK_STREAM

class simpleGUI:
    def __init__(self, master):
        self.master = master
        self.logger = logging.getLogger()
        self.num_of_times = 1
        self.logstosend = ""
        self.hostname = "localhost"
        self.messageframe = Frame(height=1, pady=5)
        self.messageframe.grid(row=6, column=0, columnspan=3, sticky=S+E+W)

        master.title("Replay Raw Logs")

        self.label = Label(master, text="File path here")
        self.label.grid(row=0, column=0, sticky=W)
        self.label2 = Label(master, text="Raw log to send")
        self.label3 = Label(master, text="Number of times to run")
        self.label4 = Label(master, text="Hostname or IP")
        self.label5 = Label(master, text="Port")

        self.filepath_entry = Entry(master, width=30)
        self.filepath_entry.grid(row=0, column=1, sticky=W)

        self.string_entry = Entry(master, width=30)
        self.label2.grid(row=1, column=0, sticky=W)
        self.string_entry.grid(row=1, column=1, sticky=W)

        self.numtimes_entry = Entry(master, width=10)
        self.label3.grid(row=2, column=0, sticky=W)
        self.numtimes_entry.grid(row=2, column=1, sticky=W)

        self.host_entry = Entry(master, width=20)
        self.label4.grid(row=3, column=0,sticky=W)
        self.host_entry.grid(row=3,column=1, sticky=W)

        self.port_entry = Entry(master, width=20)
        self.label5.grid(row=4, column=0, sticky=W)
        self.port_entry.grid(row=4, column=1, sticky=W)

        self.variable = StringVar(master)
        self.variable.set("TCP")
        self.ports_option = OptionMenu(master, self.variable, "TCP", "UDP")
        self.ports_option.grid(row=2, column=2, sticky=W)

        self.simple_button = Button(master, text="Connect", command=self.createLogger)
        self.simple_button.grid(row=3, column=2, sticky=W)

        self.close_button = Button(master, text="Send Logs", command=self.sendlogs)
        self.close_button.grid(row=4, column=2, sticky=W)

        self.scrollbar = Scrollbar(self.messageframe)
        #self.scrollbar.grid(sticky=E)
        self.status_message = Text(self.messageframe, height=1, width=30, yscrollcommand=self.scrollbar.set, relief=SUNKEN)

        #self.status_message.grid(row=4, column=1, columnspan=1, sticky=W+S+E+N)
        #self.scrollbar.grid(sticky=W + S, row=4, column=2)
        self.status_message.pack(side=LEFT, fill=BOTH, expand=1)
        self.scrollbar.pack(side=LEFT)
        self.scrollbar.config(command=self.status_message.yview)

    def gethostname(self):
        if self.host_entry.get() == '':
            self.hostname='localhost'
        else:
            self.hostname=self.host_entry.get()

    def getport(self):
        global PORT
        if self.port_entry.get() == '':
            PORT = 514
        else:
            try:
                PORT = int(self.port_entry.get())
            except:
                self.status_message.insert(1.0, "That's not a port... Defaulted to 514\n")
                PORT = 514

    def createLogger(self):
        if self.variable == "TCP":
            PROT = socket.SOCK_STREAM
        else:
            PROT = socket.SOCK_DGRAM
        # Set port here after adding it to GUI
        self.gethostname()
        self.getport()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        syslogHandler = logging.handlers.SysLogHandler(address=(self.hostname, PORT), socktype=PROT)
        self.logger.addHandler(syslogHandler)
        self.status_message.insert(1.0, "Socket bound successfully to "+self.hostname+"\n")
        #self.variable_msg.set(self.variable_msg.get()+"\n")
        #self.variable_msg.set(self.variable_msg.get()+"socket bound successfully")

    def sendlogs(self):
        # set num of times and logs to send variables
        if self.num_of_times!=1:
            self.num_of_times = int(self.numtimes_entry.get())
        self.logstosend = self.string_entry.get()
        # then run the following
        for i in range(self.num_of_times):
            self.logger.info(self.logstosend)
        x = self.filepath_entry.get()
        self.status_message.insert(1.0, "Following string sent: "+self.logstosend+"\n")
        try:
            filename = open(x, 'rb')
            self.status_message.insert(1.0, "Found a file... Reading")
            for line in filename:
                self.logger.info(line)
            filename.close()
            self.status_message.insert(1.0, "Closing file")
        #except subprocess.CalledProcessError as error1:
        except:
            self.status_message.insert(1.0, "File not found... Moving on.\n")
            #self.variable_msg.set(self.variable_msg.get()+"\n")
            #self.variable_msg.set(self.variable_msg.get()+"filename is blank")
            pass





root = Tk()
GUIthing = simpleGUI(root)
root.mainloop()
