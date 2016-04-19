import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import numpy as np

class allCpuStats:
    def __init__(self, filenames):
        self.filenames = filenames
        self.cpustats = []
        self.parse()

    def parse(self):
        for filename in self.filenames:
            cstat = cpuStat(filename)
            #cstat.parse()
            self.cpustats.append(cstat)

    @staticmethod
    def draw(cpu_stat, myplt):
        timeArray = []
        for i in range(0, len(cpu_stat.user)):
            timeArray.append(i * 2)
            cpu_stat.sys[i] += cpu_stat.user[i]
            cpu_stat.wait[i] += cpu_stat.sys[i]

        myplt.xlabel("Time",fontsize=13)
        myplt.ylabel("CPU Usage",fontsize=13)
        myplt.ylim(0, 100)
        myplt.xlim(0, timeArray[-1])
        # plt.plot(timeArray, self.used, 'b*')
        #myplt.plot(timeArray, cpu_stat.user, "r", color="blue", label="user")
        red_patch = mpatches.Patch(color="red", label="sys")

        myplt.fill_between(timeArray, 0, cpu_stat.wait, facecolor="yellow")
        myplt.fill_between(timeArray, 0, cpu_stat.sys, facecolor="red")
        myplt.fill_between(timeArray, 0, cpu_stat.user)
        plt.axvline(timeArray[200],hold=None,label='1',color='blue',linestyle='solid')
        plt.axvline(timeArray[400],hold=None,label=None,color='purple',linestyle='solid')
        plt.axvline(timeArray[600],hold=None,label=None,color='purple',linestyle='solid')
        plt.annotate('Stage0', xy = (50, 100), xytext = (100, 90))
        plt.annotate('Stage1', xy = (50,100), xytext = (500, 90))
        plt.annotate('Stage2', xy = (50, 100), xytext = (800, 90))

        #myplt.grid(True)
        myplt.legend(loc="best",shadow=False,prop={'size':8})
        p_user = mpatches.Rectangle((0, 0), 1, 1, fc="b")
        p_sys = mpatches.Rectangle((0, 0), 1, 1, fc="r")
        p_wait = mpatches.Rectangle((0, 0), 1, 1, fc="y")
        myplt.legend([p_user, p_sys, p_wait], ["USER", "SYS", "WAIT"],loc="best",shadow=False,prop={'size':9})

        #myplt.show()

    def draw_all(self):
        for i in range(0, len(self.cpustats)):
            ax = plt.subplot(3, len(self.cpustats)/3, i)
            plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1,top=0.95,wspace=0.3,hspace=0.2)
            plt.sca(ax)
            self.draw(self.cpustats[i], plt)

        #plt.show()

    def draw_avg(self):
        user_avg = self.cpustats[0].user
        sys_avg = self.cpustats[0].sys
        wait_avg = self.cpustats[0].wait
        for i in range(1, len(self.cpustats)):
            user_avg = [x + y for (x, y) in zip(user_avg, self.cpustats[i].user)]
            sys_avg = [x + y for (x, y) in zip(sys_avg, self.cpustats[i].sys)]
            wait_avg = [x + y for (x, y) in zip(wait_avg, self.cpustats[i].wait)]
            #print user_avg

        #print user_avg

        user_avg = [user_avg[i] / len(self.cpustats) for i in range(0, len(user_avg))]
        sys_avg = [sys_avg[i] / len(self.cpustats) for i in range(0, len(sys_avg))]
        wait_avg = [wait_avg[i] / len(self.cpustats) for i in range(0, len(wait_avg))]

        #print user_avg

        stat_avg = cpuStat(None, user_avg, sys_avg, wait_avg)
        self.draw(stat_avg, plt)
        plt.show()

class cpuStat:
    def __init__(self, filename, user=None, sys=None, wait=None):
        self.filename = filename
        if user is None and sys is None and wait is None:
            self.user = []
            self.sys = []
            self.wait = []
        else:
            self.user = user
            self.sys = sys
            self.wait = wait

        if filename is not None:
            self.parse()

    def parse(self):
        f = open(self.filename, "r")
        test_line = f.readline()
        lines = test_line.split()
        if lines[0] != "procs":
            print "Error cpu stat file"
            exit(1)

        f.seek(0)
        for line in f:
            stats = line.split()
            if len(stats) == 17 and stats[0] != "r":
                self.user.append(int(stats[12]))
                self.sys.append(int(stats[13]))

                self.wait.append(int(stats[15]))








