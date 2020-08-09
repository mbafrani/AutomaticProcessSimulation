# PMSIM: Automatic Discrete Event Simulation of Processes Using Event Logs
This project provides an open-source tool that allows the user to generate an event log by simulating the discovered process model from an original event log recorded from a process aware information system. This tool is completely written in [Python](https://www.python.org/), using the [pm4py](http://pm4py.org/) library for process model generation and the [SimPy](https://pypi.org/project/simpy/) library for discrete event simulation. The tool mainly comprises three modules:
* Process Mining
  - In this module, the process model is discovered in the form of a Petri net by applying process mining techniques on the original event log. This Petri net presents the possible flow of activities for the cases. Furthermore, feature extraction is performed in the subsequent performance analyses step, resulting in the calculation of _arrival rate of cases_ and _activity duration_. These extracted features are subsequently used in the discrete event simulation module.
* Discrete Event Simulation
  - In this module, new cases are generated based on the features extracted from the process mining module. Users are also provided with the option to interact with the tool by providing as input, the number of cases to be generated. This input also acts as an endpoint for the simulation process. Additionally, users can modify the arrival rate of cases as well as the activity duration for particular activities.
 * Generating the Simulated Event Logs
   - In this module, the simulated events for the generated cases are transformed into an event log. This event log is saved in the form of a ```.csv``` file. Moreover, the discrete event simulation clock is converted into a real timestamp and records each activity for the cases accordingly.

  ### Features 
  * In the process discovery step, the presence of loops in the Petri net is handled with _maximum trace length_ which limits the execution of unrealistic loops for the simulated cases.
  * The _arrival rate of cases_ is calculated by considering the _business hours_, which results in a more accurate value.
  * The tool provides users the option to modify the features _case arrival time_ and _activity time_.
  * The tool supports both ```.xes``` and ```.csv``` event log formats as input.
  * The tool is capable of handling event logs with single as well as two timestamps i.e. when the start and complete timestamps are given in the event log, then the value of the average duration of each activity is calculated.
  
  ### Screencast
  In [this](https://drive.google.com/file/d/1y319vHoL89Ue2_qiB4Yw-SshJkaozTjX/view) video, you can watch a screencast of the tool which demonstrates the main functionalities of our Python-based tool for automatic discrete event simulation of processes using event logs. Please note that you may need to download the video file to watch. 
 
  ### Requirements
  This open-source tool is OS-independent, and you only need to install the Python packages specified in the [requirements](https://github.com/mbafrani/AutomaticProcessSimulation/blob/master/requirements) file.
  
  ### Usage
  As a preceeding step, install the mentioned python packages using the following commands:
  
  ```shell
  pip install pm4py
  pip install simpy
  ```
  
  Then, navigate to the directory where the original event log (_running-example.xes_ in our case) is stored and run the _simulation_activity.py_ file using the following command:
  
  ```shell
  python simulation_activity.py running-example.xes
  ```

  Therewith, the simulation models of the discovered process model (including all the performance information) are produced and stored in the newly generated _methods.py_ file.
  
  Now, run the _simulation.py_ file which performs the actual simulation process (optionally with custom inputs provided by users) using the following command:
  
  ```shell
  python simulation.py running-example.xes
  ```