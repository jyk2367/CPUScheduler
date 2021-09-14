from tkinter import *
from tkinter import filedialog, ttk
from tkinter.simpledialog import *
import os


class Process:
    def __init__(self, line):
        self.processID = int(line[1])
        self.arriveTime = int(line[2])
        self.burstTime = int(line[3])

    def __str__(self):
        return "ProcessID : {}, ArriveTime : {}, BurstTime : {}".format(self.processID, self.arriveTime, self.burstTime)


class ReadyQueueElement:
    def __init__(self, processID, arriveTime, burstTime, waitingTime, remainTime):
        self.processID = processID
        self.arriveTime = arriveTime
        self.burstTime = burstTime
        self.waitingTime = waitingTime
        self.remainTime = remainTime

    def __str__(self):
        return "ProcessID : {},arriveTime : {} ,burstTime : {}, waitingTime : {},remainTime : {}".format(self.processID, self.arriveTime, self.burstTime, self.waitingTime, self.remainTime)


class Result:
    def __init__(self, processID, arriveTime, startP, burstTime, waitingTime, remainTime):
        self.processID = processID
        self.arriveTime = arriveTime
        self.startP = startP
        self.burstTime = burstTime
        self.waitingTime = waitingTime
        self.remainTime = remainTime

        self.turnaroundTime = waitingTime+burstTime
        self.responseTime = startP-arriveTime

    def __str__(self):
        return "ProcessID : {},arriveTime : {} ,startP : {}, BurstTime : {}, waitingTime : {}, turnaroundTime : {}, responseTime : {}, remainTime : {}".format(
            self.processID, self.arriveTime, self.startP, self.burstTime, self.waitingTime, self.turnaroundTime, self.responseTime, self.remainTime)


class SJF_Algorithm:
    def __init__(self):
        self.currentProcess = 0  # 현재 프로세스
        self.cpuTime = 0  # 현재 프로세스가 동작하는 시점부터 시간
        self.cpuDown = 0  # 현재 프로세스의 끝시간
        self.runTime = 0  # 프로세서 동작 시간

    def copyP(self, rq):

        newP = ReadyQueueElement(
            rq.processID, rq.arriveTime, rq.burstTime, rq.waitingTime, rq.remainTime)
        return newP

    def PtSJF(self, list_P):
        # 프로세스 arriveTime 순으로 정렬
        list_P = sorted(list_P, key=lambda Process: Process.arriveTime)
        List_E=[]
        resultList = list()
        readyQueue = list()

        while True:
            while len(list_P) != 0:
                if self.runTime == list_P[0].arriveTime:
                    readyQueue.append(ReadyQueueElement(
                        list_P[0].processID, list_P[0].arriveTime, list_P[0].burstTime, 0, list_P[0].burstTime))
                    if self.currentProcess != 0:
                        readyQueue = sorted(
                            readyQueue, key=lambda ReadyQueueElement: ReadyQueueElement.burstTime)
                        if runningProcess.remainTime > readyQueue[0].burstTime and self.cpuTime != self.cpuDown:
                            List_E.append(self.runTime)
                            readyQueue.append(runningProcess)
                            self.currentProcess = 0
                    del list_P[0]
                else:
                    break

            if self.currentProcess == 0:
                if(len(readyQueue) != 0):
                    rq = readyQueue[0]
                    runningProcess = self.copyP(rq)
                    resultList.append(
                        Result(rq.processID, rq.arriveTime, self.runTime, rq.burstTime, rq.waitingTime, rq.remainTime))
                    self.cpuDown = rq.burstTime
                    self.cpuTime = rq.burstTime-rq.remainTime
                    self.currentProcess = rq.processID
                    del readyQueue[0]
            else:
                if self.cpuTime == self.cpuDown:
                    List_E.append(self.runTime)
                    runningProcess.remainTime = 0
                    self.currentProcess = 0
                    if len(readyQueue) > 0:
                        readyQueue = sorted(
                            readyQueue, key=lambda ReadyQueueElement: ReadyQueueElement.burstTime)
                    continue

            for rq in readyQueue:
                rq.waitingTime += 1
            self.runTime += 1
            self.cpuTime += 1
            if self.currentProcess != 0:
                if(runningProcess.remainTime > 0):
                    runningProcess.remainTime -= 1
            if not (len(list_P) != 0 or len(readyQueue) != 0 or self.currentProcess != 0):
                break

        return self.runTime-1,List_E,resultList

    def NonPtSJF(self, list_P):
        # 프로세스 arriveTime 순으로 정렬
        list_P = sorted(list_P, key=lambda Process: Process.arriveTime)
        List_E=[]
        resultList = list()
        readyQueue = list()
        while True:
            while len(list_P) != 0:
                # 프로세스 readyqueue에 넣는 시점이 왔을 경우
                if self.runTime == list_P[0].arriveTime:
                    readyQueue.append(ReadyQueueElement(
                        list_P[0].processID, list_P[0].arriveTime, list_P[0].burstTime, 0, list_P[0].burstTime))
                    del list_P[0]
                else:
                    break

            # 현재 프로세스가 없다면
            if self.currentProcess == 0:
                # 프로세스 실행
                if(len(readyQueue) != 0):
                    rq = readyQueue[0]
                    resultList.append(
                        Result(rq.processID, rq.arriveTime, self.runTime, rq.burstTime, rq.waitingTime, rq.remainTime))
                    self.cpuDown = rq.burstTime
                    self.cpuTime = 0
                    self.currentProcess = rq.processID
                    del readyQueue[0]
            else:
                # 프로세스 burst time 다 됐으면
                if self.cpuTime == self.cpuDown:
                    List_E.append(self.runTime)
                    self.currentProcess = 0
                    if len(readyQueue) > 0:
                        readyQueue = sorted(
                            readyQueue, key=lambda ReadyQueueElement: ReadyQueueElement.burstTime)
                    continue

            for rq in readyQueue:
                rq.waitingTime += 1

            self.runTime += 1
            self.cpuTime += 1
            if not (len(list_P) != 0 or len(readyQueue) != 0 or self.currentProcess != 0):
                break
        return self.runTime-1, List_E,resultList


def ganttChart(list_result,Pnum,RUNTIME,List_E):
    window = Tk()
    window.title("%s" % (os.path.basename(FILEPATH)))
    
    #간트 차트 가로 길이 설정용
    WIDTH=1200
    RST=WIDTH*0.9
    REND=WIDTH*0.27
    window.geometry("{}x900+500+300".format(int(WIDTH)))
    
    window.wm_attributes("-topmost", 1)

    myCanvas = Canvas(window, bg="white", width=WIDTH, height=300)

    myCanvas.create_rectangle(
        WIDTH-RST, 100, WIDTH-REND, 200, fill="white", outline="black")

    waiting_dup = dict()
    turnaround_dup = dict()
    waitingTime=0
    turnaroundTime=0
    executionTime=0
    for r in list_result:
        print(r)
        if r.processID not in waiting_dup.keys():
            executionTime += r.burstTime
            waiting_dup[r.processID] = 0
            turnaround_dup[r.processID] = 0

    for r in list_result:
        if r.processID in waiting_dup.keys():
            if waiting_dup[r.processID] < r.waitingTime:
                waiting_dup[r.processID] = r.waitingTime
            if turnaround_dup[r.processID]< r.turnaroundTime:
                turnaround_dup[r.processID] = r.turnaroundTime

    for i in waiting_dup.values():
        waitingTime += int(i)
    for i in turnaround_dup.values():
        turnaroundTime += int(i)
    AWT = float(waitingTime)/len(waiting_dup)
    TAT=float(turnaroundTime)/len(turnaround_dup)

    myCanvas.create_text(
        WIDTH-REND+150, 110, text="total execution time = %d" % executionTime, fill="black")
    myCanvas.create_text(
        WIDTH-REND+150, 130, text="Average Waiting time = %.2f" % AWT, fill="black")
    myCanvas.create_text(
        WIDTH-REND+150, 150, text="Average TurnAround time = %.2f" %TAT, fill="black")
    myCanvas.create_text(
        WIDTH-REND+150, 170, text="CPU utilization Ratio = %.2f%%" %((float(executionTime)/RUNTIME)*100), fill="black")
    myCanvas.create_text(
        WIDTH-REND+150, 190, text="throughput = %.2f" %(float(Pnum)/RUNTIME), fill="black")


        

    myCanvas.create_text(WIDTH-RST, 220, text="0", fill="black", font=("times", 10))
    myCanvas.create_text(WIDTH-REND, 220, text=RUNTIME,fill="black", font=("times", 10))

    et = ((WIDTH-REND)-(WIDTH-RST))/RUNTIME
    for i in range(len(list_result)):
        
        dx =WIDTH-RST+et*list_result[i].startP
        dx_=WIDTH-RST+et*List_E[i]
        myCanvas.create_line(dx, 200, dx, 100, fill="black", width=3)
        myCanvas.create_line(dx_, 200, dx_, 100, fill="black", width=3)
        myCanvas.create_text(dx, 220, text=str(list_result[i].startP),
                             fill="black", font=("times", 10))
        myCanvas.create_text(dx, 240, text="P" +
                             str(list_result[i].processID), fill="black", font=("times", 10))
        myCanvas.create_text(dx_, 220, text=str(List_E[i]),
                             fill="black", font=("times", 10))
        myCanvas.create_text(dx, 240, text="P" +
                             str(list_result[i].processID), fill="black", font=("times", 10))


    myCanvas.grid(row=0, column=0)


    treeview1 = ttk.Treeview(window, columns=["one", "two", "three", "four", "five"], displaycolumns=[
                             "one", "two", "three", "four", "five"])
    treeview1.column("#0", width=80, anchor="center")
    treeview1.heading("#0", text="ProcessID", anchor="center")

    treeview1.column("#1", width=120, anchor="center")
    treeview1.heading("one", text="시작시간(startP)", anchor="center")

    treeview1.column("#2", width=130, anchor="center")
    treeview1.heading("two", text="실행시간(turnaroundT)", anchor="center")

    treeview1.column("#3", width=120, anchor="center")
    treeview1.heading("three", text="burstTime", anchor="center")

    treeview1.column("#4", width=120, anchor="center")
    treeview1.heading("four", text="응답시간(responseT)", anchor="center")

    treeview1.column("#5", width=120, anchor="center")
    treeview1.heading("five", text="waitingTime", anchor="center")
    i = 0
    for r in list_result:
        treeview1.insert('', 'end', text=r.processID, values=[
                         r.startP, r.turnaroundTime, r.burstTime, r.responseTime, r.waitingTime], iid=str(i)+"번")
        i += 1

    treeview1.grid(row=1, column=0)

    treeview2 = ttk.Treeview(window, columns=["one", "two", "three", "four", "five"], displaycolumns=[
                             "one", "two", "three", "four", "five"])
    treeview2.column("#0", width=80, anchor="center")
    treeview2.heading("#0", text="ProcessID", anchor="center")

    treeview2.column("#1", width=120, anchor="center")
    treeview2.heading("one", text="시작시간(startP)", anchor="center")

    treeview2.column("#2", width=130, anchor="center")
    treeview2.heading("two", text="실행시간(turnaroundT)", anchor="center")

    treeview2.column("#3", width=120, anchor="center")
    treeview2.heading("three", text="burstTime", anchor="center")

    treeview2.column("#4", width=120, anchor="center")
    treeview2.heading("four", text="응답시간(responseT)", anchor="center")

    treeview2.column("#5", width=120, anchor="center")
    treeview2.heading("five", text="waitingTime", anchor="center")

    dict_dup = dict()
    for r in list_result:
        if r.processID in dict_dup.keys():
            dict_dup[r.processID][1] = r.turnaroundTime
            dict_dup[r.processID][4] = r.waitingTime
        else:
            dict_dup[r.processID] = [r.startP, r.turnaroundTime,
                                     r.burstTime, r.responseTime, r.waitingTime]
    i = 0
    dict_dup = sorted(dict_dup.items(), key=lambda x: x[0])
    for d in dict_dup:
        treeview2.insert('', 'end', text=d[0], values=d[1], iid=str(i)+"번")
        i += 1

    treeview2.grid(row=2, column=0)

    window.mainloop()


while(True):
    list_P = list()
    Pnum=0
    root = Tk()
    root.withdraw()

    FILEPATH = filedialog.askopenfilename()
    try:
        with open(FILEPATH, "r") as f:
            root.destroy()
            while True:
                line = f.readline()
                if line == "":
                    break
                line = list(map(str, line.split()))
                list_P.append(Process(line))
                Pnum+=1
        f.close()
    except FileNotFoundError:
        print('파일이 없습니다.')
        break

    SJF = SJF_Algorithm()
    Menu = Tk()
    Menu.withdraw()
    MENU = askinteger("Menu","1.Preemptive   2.NonPreemptive",minvalue=1,maxvalue=2)
    Menu.destroy()
    # Menu 1 : Preemptive SJF Scheduling
    if MENU == 1:
        RUNTIME,List_E,list_result = SJF.PtSJF(list_P)
        ganttChart(list_result,Pnum, RUNTIME, List_E)

    # Menu 2 : Non-Preemptive SJF Scheduling
    elif MENU == 2:
        RUNTIME,List_E,list_result = SJF.NonPtSJF(list_P)
        ganttChart(list_result,Pnum, RUNTIME, List_E)
    else:
        break
