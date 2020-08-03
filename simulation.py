from datetime import datetime, timedelta
import simulation_activity
from pm4py.algo.discovery.inductive import factory as inductive_miner
import warnings
import pandas as pd
import csv
from copy import copy
from random import shuffle
from pm4py.util import constants
import random
import simpy
import pm4py.objects.log.log as log_instance
from pm4py.objects.petri import semantics
from pm4py.util import xes_constants
import sys, importlib
import methods
from pm4py.statistics.traces.log.case_arrival import get_case_arrival_avg
from pm4py.util.business_hours import BusinessHours

importlib.reload(sys.modules['methods'])
case_id_key = xes_constants.DEFAULT_TRACEID_KEY
activity_key = xes_constants.DEFAULT_NAME_KEY
timestamp_key = datetime.now()
results = []

warnings.filterwarnings('ignore')


def discover_process_model():
    """
                This function is responsible for mining the process model and in turn calling other functions to
                continue the simulation and provide additional functionality.

                Returns
                --------------
               net
                    The petri net generated from the event logs
                initial_marking
                    The initial marking of the petri net generated from the event logs
                final_marking
                    The final marking of the petri net generated from the event logs
                """
    log = simulation_activity.verify_extension_and_import()
    parameters1 = {constants.PARAMETER_CONSTANT_CASEID_KEY: "concept:name",
                   constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name",
                   constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "time:timestamp"}
    print("Beginning Petri net mining. Please wait...")
    net, initial_marking, final_marking = inductive_miner.apply(log, parameters=parameters1)
    print("Petri Net creation successful")
    relevant_info_generator(net, initial_marking, final_marking, log)
    return net, initial_marking, final_marking


def relevant_info_generator(net, initial_marking, final_marking, log):
    """
               
                Parameters
                --------------
                net
                    The petri net generated from the event logs
                initial_marking
                    The initial marking of the petri net generated from the event logs
                final_marking
                    The final marking of the petri net generated from the event logs
                log
                    The input events in the form of a log

                """
       
    simulation_of_events(log, net, initial_marking)


def simulation_of_events(log, net, initial_marking):
    """
    This method is called to begin the process of simulation

    Input:
    :param log: The input events in the form of a log
    :param net: The petrinet representing the process model
    :param initial_marking: The initial marking of the activities of the model
    """
    print("Simulation's result will be stored in simulated-logs.csv file")
    random.seed(41)  # This helps reproducing the results

    # Create an environment and start the setup process
    env = simpy.Environment()    

    print("Please enter no of cases to be generated")
    no_traces = int(input())

    env.process(setup(log, env, no_traces, net, initial_marking))

    # Execute!
    env.run()


def setup(log, env, no_traces, net, initial_marking):
    """

    :param log: The input events in the form of a log
    :param env: The simulation environment
    :param no_traces: Number of traces that needs to be generated, given by the user
    :param net: The petrinet representing the process model
    :param initial_marking: The initial marking of the activities of the model
    """
    user_yn = input("Do you want to configure the average arrival rate of the cases? Enter y or n ")
    if user_yn.lower() == "y":
        case_arrival_time = float(input("Enter in seconds the case arrival time "))

    else:
        case_arrival_time = get_case_arrival_avg(log)


    casegen = methods.Trace(env)

    # Create more cases while the simulation is running
    for i in range(1, no_traces+1):        
        yield env.timeout(case_arrival_time)
        env.process(simulation(env, 'Case %d' % i, casegen, net, initial_marking, no_traces))


def simulation(env, case_num, case, net, initial_marking, no_traces):
    """
    :param env:  The simulation environment
    :param case_num: Case ID
    :param case: The activity name to call the relevant method
    :param net: The petrinet representing the process model
    :param initial_marking: The initial marking of the activities of the model
    :param no_traces: Number of traces that needs to be generated, given by the user
    """
    max_trace_length = 1000  # Only traces with length lesser than 1000 are created
    f = open('simulated-logs.csv', 'w', newline='')
    thewriter = csv.writer(f)
    thewriter.writerow(['case_id', 'activity', 'timestamp'])
    curr_timestamp = datetime.now()
    log = log_instance.EventLog()    
    trace = log_instance.Trace()
    trace.attributes[case_id_key] = str(case_num.replace('Case', ''))
    marking = copy(initial_marking)
    while True:
        if not semantics.enabled_transitions(net, marking):
            break
        all_enabled_trans = semantics.enabled_transitions(net, marking)
        all_enabled_trans = list(all_enabled_trans)
        shuffle(all_enabled_trans)
        trans = all_enabled_trans[0]
        if trans.label is not None:
            event = log_instance.Event()
            event[activity_key] = trans.label
            results.append([case_num, event[activity_key], datetime.now() + timedelta(seconds=env.now)])
            yield env.process(getattr(case, str(trans.label).replace(" ", ""))())
            event[timestamp_key] = curr_timestamp
            trace.append(event)
        marking = semantics.execute(trans, net, marking)
        if len(trace) > max_trace_length:
            break
    if len(trace) > 0:
        log.append(trace)

        results.append([case_num, "case end", datetime.now() + timedelta(seconds=env.now)])

    for row in results:
        thewriter.writerow(row)

    f.close()
    return log


if __name__ == '__main__':
    discover_process_model()
