import argparse
import os
from pathlib import Path
from datetime import datetime, timedelta
import statistics
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as conversion_factory
import math
import warnings
from pm4py.util import xes_constants
from pm4py.util import constants
import pandas as pd
import matplotlib.pyplot as plt

case_id_key = xes_constants.DEFAULT_TRACEID_KEY
activity_key = xes_constants.DEFAULT_NAME_KEY
timestamp_key = datetime.now()
results = []

warnings.filterwarnings('ignore')


def read_input_file_path():
    """
        Reads the input file path from the Command Line Interface and verifies if the file exists

        Returns
        --------------
        file.file_path
                The file path of the input event log file
    """    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path)
    file = parser.parse_args()
    print("File received: ", file.file_path)
    if file.file_path.exists():
        print("File exists")
    else:
        print("File does not exist. Please input correct file")
        exit()
        
    return str(file.file_path)
    """
    file = 'running-example.xes'
    return file


def import_xes(file_path):
    """
        Imports logs from the input xes file
        Parameters
        --------------
        file_path
            Path of the input event log file

        Returns
        --------------
        xes_log
            The input event logs in the form of a log
        """
    xes_log = xes_import_factory.apply(file_path)
    print("Import of xes successful,with {0} traces in total".format(len(xes_log)))
    return xes_log


def import_csv(file_path):
    """
            Imports logs from the input csv file
            Parameters
            --------------
            :param file_path:
                The path to the csv log file

            Returns
            --------------
            csv_log
                The input event logs in the form of a log

            """
    data_frame = csv_import_adapter.import_dataframe_from_path(
        os.path.join(file_path), sep=";")
    data_frame["time:timestamp"] = data_frame["time:timestamp"].apply(lambda x:
                                                                      datetime.strptime(x, '%d-%m-%Y:%H.%M'))
    if 'time:complete' in data_frame.columns:
        data_frame["time:complete"] = pd.to_datetime(data_frame["time:complete"], format='%d-%m-%Y:%H.%M')
    data_frame["Activity"] = data_frame["concept:name"]
    parameters = {constants.PARAMETER_CONSTANT_CASEID_KEY: "concept:name",
                  constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "activity",
                  constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "time:timestamp"}
    csv_log = conversion_factory.apply(data_frame, parameters=parameters)
    print("Import of csv successful,with {0} traces in total".format(len(csv_log)))
    return csv_log


def verify_extension_and_import():
    """
            This function verifies that the extension of the event log file is .xes or .csv and imports the
            logs from those files
            Returns
            --------------
            log
                The input event logs in the form of a log
            """

    file_path = read_input_file_path()
    """
    file_name, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.replace("'))", "")
    print("File Extension: ", file_extension)
    if file_extension == ".xes":
        log = import_xes(file_path)
        return log
    elif file_extension == ".csv":
        log = import_csv(file_path)
        return log
    else:
        print("Unsupported extension. Supported file extensions are .xes and .csv ONLY")
        exit()
"""
    log = import_xes(file_path)
    return log

def remove_outliers(dataset, attribute):
    
    Q1 = dataset[attribute].quantile(0.25)
    Q3 = dataset[attribute].quantile(0.75)
    IQR = Q3 - Q1
    
    UpperWhisker = Q3 + 1.5 *IQR
    LowerWhisker = Q1 - 1.5 *IQR
    
    filter = (dataset[attribute] > LowerWhisker) | (dataset[attribute] < UpperWhisker)
    
    result = dataset.loc[filter]   

    return result
    
    
def create_methods():
    """
                This function calculates the average time taken for each activity and writes methods to method.py file
                to be used for simulation

                """
    log = verify_extension_and_import()
    timetaken = {}
    for trace in log:
        length = len(trace)
        for index, event in enumerate(trace):
            if index < (length - 1):
                next_event = trace[index + 1]
                if "concept:name" in event:
                    attribute = event["concept:name"]
                    if "time:complete" in event:
                        if attribute not in timetaken:
                            timetaken[attribute] = [(event["time:complete"] - event["time:timestamp"]).total_seconds()]
                        else:
                            timetaken[attribute].append(
                                (event["time:complete"] - event["time:timestamp"]).total_seconds())
                    else:
                        if "time:timestamp" in event:
                            time = event["time:timestamp"]
                        if "time:timestamp" in next_event:
                            next_time = next_event["time:timestamp"]
                        if attribute not in timetaken:
                            timetaken[attribute] = [(next_time - time).total_seconds()]
                        else:
                            timetaken[attribute].append((next_time - time).total_seconds())
            else:
                mean = statistics.mean(timetaken[attribute])
                if "concept:name" in event:
                    attribute = event["concept:name"]
                if attribute not in timetaken:
                    timetaken[attribute] = [mean]
                else:
                    timetaken[attribute].append(mean)

    dfn = pd.DataFrame.from_dict(timetaken, orient='index')
    dfr = dfn.transpose()
          
    
    for col in dfr.columns:         
        cleaned = remove_outliers(dfr, col)

    cleaned.dropna(inplace = True) 
    new_timetaken = cleaned.to_dict('list')
    
    for attribute in new_timetaken:
        new_timetaken[attribute] = statistics.mean(new_timetaken[attribute])
    user_req = "y"
    user_input = input("Do you want to modify the average time for any activity? Enter y to modify or press any key to "
                       "continue ")
    if user_input.lower() == "y":
        while user_req.lower() == "y":
            print("Average time taken for each activity in seconds: ", new_timetaken)
            user_activity = input("Enter the activity you want to configure the average time taken ")
            if user_activity not in new_timetaken:
                print("No such activity found")
            else:
                print("Activity Found, Average time taken is ", new_timetaken[user_activity])
                user_time = input("Enter the average time (in seconds) ")
                new_timetaken[user_activity] = float(user_time)
            user_req = input("Do you want to configure more activities? Enter y to configure or press any key to "
                             "continue ")

    attributes = {}
    for trace in log:
        for event in trace:
            if "concept:name" in event:
                attribute = event["concept:name"]
                if attribute not in attributes:
                    attributes[attribute] = math.ceil(new_timetaken[attribute])
                # attributes[attribute] = attributes[attribute] + 1
    print(attributes)

    f = open("methods.py", "w")
    f.write('''\
class Trace(object):

    def __init__(self,env):
        self.env = env       
    ''')
    for attribute in attributes:
        f.write('''\

    def %s(self):
        yield self.env.timeout(%d)       
    ''' % (str(attribute).replace(" ", ""), attributes[attribute]))
    f.close()


if __name__ == '__main__':
    create_methods()
