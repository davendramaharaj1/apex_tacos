# APEX Extension
This is an extension of the course project done in ECE 8803 Hardware Software Co-design for Machine Learning Systems offered at Georgia Institute of Technology during Spring 2024 semester.

## Flow
1. Create TACOSGreedy objects for all the configurations specified in the YAML file, and relay this information - (no. of objects created, (events and "UNIQUE IDENTIFIERS" to identify these events)) to the APEX backend.

2. This information is used to instantiate the pipelines at build time.

3. Add a logger mechanism to keep track of the status of transactions taking place between TACOS and APEX.
    Record the following events using a logger:
    - Print message for each TACOS object created
    - Print message for each Pipeline created for the corresponding TACOS object.
    - Displaying contents of the communication.
    - XML generated message.

![TACOS to APEX flow](https://github.com/davendramaharaj1/apex_tacos/blob/apex_extension/TACOS_APEX_Flow.png)