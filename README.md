# PMSIM: Automatic Discrete Event Simulation Using Event Logs
This project provides a open-source tool that automatically generates a discrete event logs from event logs. This tool is written in [Python](https://www.python.org/), where we have used [pm4py](http://pm4py.org/) and [SimPy](https://pypi.org/project/simpy/) for process model generation and discrete event simulation. This tool mainly consist of three modules:
* Process Mining
  - In this module, the process model is discovered in the form of petri net which presents the possible flow of activities for the cases by applying process mining techniques on the original event log. furthermore, the feature extration is done with the help of performance analyses which is helpful in discrete event simulation.
* Discrete Event Simulation
  - This module mainly generates the new cases based on the feature extracted from the previous module. It also provide user option to interact with the tool where user can enter the number of cases to be generated which also acts as a end point for the simulation process. user can also modify the arrival rate of the cases and activity duration for particular activities.
 * Generating the Simulated Logs
   - This modules transform the simulated events for the generated cases into the event logs and stores it in csv file. here, the discrete event simulation clock is converted into real timestamp and records the activity for the cases.
   
  ### Features 
  * Every module in this tool is implemented in Python.
  * In process discovery step, presence of the loops in the process model (Petri net) is handled with _maximum trace length_ which limits the execution of unrealistic loops for the simulated cases.
  * _arrival rate of cases_ are calculated by considering the _business hours_, which results in more accurate value.
  * This tool provide an user option to modify the _case arrival time_ and _activity time_.
  
  ### Screencast
  In [this](https://link.com) video, you can watch a screencast of the tool which demonstrates the main functionalities of our Python-based tool for automatic discrete event simulated using event logs.
 
  ### Requirements
  The tool is OS-independent, and you only need to install Python packages specified in the [requirements](https://github.com/mbafrani/AutomaticProcessSimulation/blob/master/requirements) file.
  
  ### Usage
  To simply the usage, please use the following commands to install python packages:
  
  ```shell
  pip install pm4py
  pip install simpy
  ```
  
  After installing python packages, navigate to the directory where the original event log is stored and run the _simulation_activity.py_ file:
  
  ```shell
  python simulation_activity.py test-logs.xes
  ```
  now run the _simulation.py_ file:
  ```shell
  python simulation.py
  ```
  
  
  
