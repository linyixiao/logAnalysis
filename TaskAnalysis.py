# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import numpy as np

class taskAnalysis:

    def __init__(self, filenames):
        self.filenames = filenames

    def get_json(self, line):
        # Need to first strip the trailing newline, and then escape newlines (which can appear
        # in the middle of some of the JSON) so that JSON library doesn't barf.
        return json.loads(line.strip("\n").replace("\n", "\\n"))#transfer to str


    def analysis(self):

        f = open(self.filenames, "r")
        test_line = f.readline()

        try:
            self.get_json(test_line)
            is_json = True
            print ("Parsing file %s as JSON" % self.filenames)
        except:
            is_json = False
            print ("Parsing file %s as JobLogger output" % self.filenames)
        f.seek(0)

        taskIDs = []
        taskRuntimes = []
        execTimes = []
        gcTimes = []
        execTimeRatio = []
        gcTimeRatio = []

        for line in f:
            if is_json:
                json_data = self.get_json(line)
                event_type = json_data["Event"]

                if event_type == "SparkListenerTaskEnd":
                    #print("Event type:%s" % event_type)

                    task_info = json_data["Task Info"]
                    taskIDs.append(task_info["Task ID"])

                    taskRuntime = int(task_info["Finish Time"]-task_info["Launch Time"])
                    taskRuntimes.append(taskRuntime)
                    print taskRuntime

                    task_metrics=json_data["Task Metrics"]
                    execTimes.append(task_metrics["Executor Run Time"])
                    gcTimes.append(task_metrics["JVM GC Time"])

                    execTimeRatio.append(float(100*task_metrics["Executor Run Time"]/taskRuntime))
                    gcTimeRatio.append(float(1000*task_metrics["JVM GC Time"]/taskRuntime))

        gcTimeRatios = dict(zip(taskIDs[::-1],gcTimeRatio)).values()
        execTimeRatios = dict(zip(taskIDs,execTimeRatio)).values()
        #print gcTimeRatios
        #print execTimeRatios
        print len(taskIDs)
        timeArray = sorted(taskIDs)

        plt.rc('font', family='SimHei', size=13)
        num = np.array(execTimeRatios[0:50])
        print gcTimeRatios
        width = 0.5
        idx = np.arange(len(timeArray[0:50]))
        plt.bar(idx, num,  width, color='g', label='execTime ratio')
        #plt.bar(idx, ratio, width, bottom=num, color='yellow', label='mv')
        plt.xlabel("Task ID",fontsize=14)
        plt.ylabel("Executor Run Time Ratio",fontsize=14)
        plt.ylim(0, 100)
        plt.xticks(idx+width/2, timeArray[0:50], rotation=40)
        plt.legend()
        plt.show()


