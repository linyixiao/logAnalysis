import matplotlib.pyplot as plt

class allJvmStats:
    def __init__(self, filenames):
        self.filenames = filenames
        self.jstats = []
        #self.gstats = []
        self.parse()

    def parse(self):
        for filename in self.filenames:
            jstat = jvmStat(filename)
            #cstat.parse()
            self.jstats.append(jstat)
            #gstat = gcStat(filename)
            #self.gstats.append(filename)

    @staticmethod
    def draw(jvm_stat, myplt):
        timeArray = []
        maxMem = 0.0

        for i in range(0, len(jvm_stat.ec)):
            timeArray.append(i * 2)
            if jvm_stat.ec[i] > maxMem:
                maxMem = jvm_stat.ec[i]
            if jvm_stat.oc[i] > maxMem:
                maxMem = jvm_stat.oc[i]

        print maxMem

        myplt.xlabel("Time")
        myplt.ylabel("Memory Size (MB)")
        myplt.ylim(0, maxMem + 2000)
        myplt.xlim(0, timeArray[-1])
        # plt.plot(timeArray, self.used, 'b*')
        myplt.plot(timeArray, jvm_stat.ec, "r", color="blue", label="ec", linewidth=1.5)
        myplt.plot(timeArray, jvm_stat.eu, "r", color="red", label="eu", linewidth=1.5)
        myplt.plot(timeArray, jvm_stat.oc, "r", color="c", label="oc", linewidth=1.5)
        myplt.plot(timeArray, jvm_stat.ou, "r", color="g", label="ou", linewidth=1.5)
        #myplt.plot(timeArray, self.pc, "r", color="green", label="pc")
        #myplt.plot(timeArray, self.pu, "r", color="black", label="pu")
        myplt.legend(loc="best",shadow=False,prop={'size':9})
        #myplt.legend()
        #myplt.show()


    def draw_first(self):
        self.draw(self.jstats[0], plt)
        plt.show()

    def draw_all(self):
        for i in range(0, len(self.jstats)):
            ax = plt.subplot(3, len(self.jstats)/3, i)
            plt.subplots_adjust(left=0.08, right=0.95, bottom=0.1,top=0.95,wspace=0.4,hspace=0.2)
            plt.sca(ax)
            self.draw(self.jstats[i], plt)

        plt.show()

    def draw_avg(self):
        ec_avg = self.jstats[0].ec
        eu_avg = self.jstats[0].eu
        oc_avg = self.jstats[0].oc
        ou_avg = self.jstats[0].ou
        pc_avg = self.jstats[0].pc
        pu_avg = self.jstats[0].pu

        for i in range(1, len(self.jstats)):
            ec_avg = [x + y for (x, y) in zip(ec_avg, self.jstats[i].ec)]
            eu_avg = [x + y for (x, y) in zip(eu_avg, self.jstats[i].eu)]
            oc_avg = [x + y for (x, y) in zip(oc_avg, self.jstats[i].oc)]
            ou_avg = [x + y for (x, y) in zip(ou_avg, self.jstats[i].ou)]
            pc_avg = [x + y for (x, y) in zip(pc_avg, self.jstats[i].pc)]
            pu_avg = [x + y for (x, y) in zip(pu_avg, self.jstats[i].pu)]

        ec_avg = [ec_avg[i] / len(self.jstats) for i in range(0, len(ec_avg))]
        eu_avg = [eu_avg[i] / len(self.jstats) for i in range(0, len(eu_avg))]
        oc_avg = [oc_avg[i] / len(self.jstats) for i in range(0, len(oc_avg))]
        ou_avg = [ou_avg[i] / len(self.jstats) for i in range(0, len(ou_avg))]
        pc_avg = [pc_avg[i] / len(self.jstats) for i in range(0, len(pc_avg))]
        pu_avg = [pu_avg[i] / len(self.jstats) for i in range(0, len(pu_avg))]

        jstat_avg = jvmStat(None, ec_avg, eu_avg, oc_avg, ou_avg, pc_avg, pu_avg)

        self.draw(jstat_avg, plt)

        plt.show()

    def draw_gc(self):
        gc_stats = []
        for filename in self.filenames:
            gc_stat = gcStat(filename)
            #cstat.parse()
            gc_stats.append(gc_stat)

        ygc_avg = gc_stats[0].ygct
        gct_avg = gc_stats[0].gct

        for i in range(1, len(gc_stats)):
            ygc_avg = [x + y for (x, y) in zip(ygc_avg, gc_stats[i].ygct)]
            gct_avg = [x + y for (x, y) in zip(gct_avg, gc_stats[i].gct)]

        ygc_avg = [ygc_avg[i] / len(gc_stats) for i in range(0, len(ygc_avg))]
        gct_avg = [gct_avg[i] / len(gc_stats) for i in range(0, len(gct_avg))]

        #ygc_avg = [ygc_avg[i] - ygc_avg[i - 1] for i in range(1, len(ygc_avg))]
        #gct_avg = [gct_avg[i] - gct_avg[i - 1] for i in range(1, len(gct_avg))]

        #print ygc_avg

        timeArray = []
        for i in range(0, len(ygc_avg)):
            timeArray.append(i * 2)

        plt.xlabel("Time")
        plt.ylabel("GC Time")
        plt.ylim(0, 10)
        plt.xlim(0, timeArray[-1])

        plt.plot(timeArray, ygc_avg, "r", color="blue", label="young gc", linewidth=1.0)
        plt.plot(timeArray, gct_avg, "r", color="red", label="total gc", linewidth=1.0)

        plt.legend(loc='best',prop={'size':9})

        plt.show()



class gcStat:
    def __init__(self, filename):
        self.ygct = []
        self.fgct = []
        self.gct = []
        self.ygc = []
        self.fgc = []
        self.filename = filename
        self.parse()

    def parse(self):
        f = open(self.filename, "r")
        test_line = f.readline()
        lines = test_line.split()
        if len(lines) != 15:
            print "Error jvm stat file"
            exit(1)

        f.seek(1)
        for line in f:
            stats = line.split()
            if len(stats) == 15 and stats[0] != "S0C":
                self.ygct.append(float(stats[11]))
                self.fgct.append(float(stats[13]))
                self.gct.append(float(stats[14]))
                self.ygc.append(int(stats[10]))
                self.fgc.append(int(stats[12]))

class jvmStat:
    def __init__(self, filename, ec=None, eu=None, oc=None, ou=None, pc=None, pu=None):
        self.filename = filename
        if ec is None and eu is None and oc is None and ou is None and pc is None and pu is None:
            self.ec = []
            self.eu = []
            self.oc = []
            self.ou = []
            self.pc = []
            self.pu = []
        else:
            self.ec = ec
            self.eu = eu
            self.oc = oc
            self.ou = ou
            self.pc = pc
            self.pu = pu

        if filename is not None:
            self.parse()

    def parse(self):
        f = open(self.filename, "r")
        test_line = f.readline()
        lines = test_line.split()
        if len(lines) != 15:
            print "Error jvm stat file"
            exit(1)

        f.seek(1)
        for line in f:
            stats = line.split()
            if len(stats) == 15 and stats[0] != "S0C":
                self.ec.append(float(stats[4])/1024)
                self.eu.append(float(stats[5])/1024)
                self.oc.append(float(stats[6])/1024)
                self.ou.append(float(stats[7])/1024)
                self.pc.append(float(stats[8])/1024)
                self.pu.append(float(stats[9])/1024)


