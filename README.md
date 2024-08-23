# APEX Extension

This is an extension of the course project done in ECE 8803 Hardware Software Co-design for Machine Learning Systems offered at Georgia Institute of Technology during Spring 2024 semester.

## Abstract
Collective communication techniques have played a significant role in optimizing the performance and power of interconnection networks. In today’s world, where the need to support a large number of interconnected devices in a network arises, these techniques have been instrumental in enhancing network bandwidth, optimizing performance, and reducing power consumption. Research works such as ASTRASIM and TACOS, which simulate collective communication on large distributed networks, can provide valuable insights into the importance of collective communication techniques and facilitate the development of further optimizations. However, there exists a gap between TACOS and ASTRA-SIM, which could potentially hinder research on collective communications. Moreover, since TACOS can synthesize collectives for arbitrary network topologies, the engineering effort to characterize these topologies to the system layer of ASTRA-SIM is both cumbersome and error-prone. As such, the aim of this work is to bridge the gap between TACOS and ASTRA-SIM by automating the design and simulation of collectives for a 2D Mesh Topology. Moreover, this work seeks to characterize the logical topological structure through the use of Chakra ET’s to facilitate a more streamlined and error-free analysis. Utilizing the simulations from ASTRASIM, Design Space Exploration (DSE) has been performed to explore the possible configurations of collectives that optimize for network performance. Additionally, extensive statistical analysis of the DSE results has been presented, providing insights into the effect of parameters such as bandwidth, mesh size, chunks per collective and chunk size on network performance.

## Flow
1. Create TACOSGreedy objects for all the configurations specified in the YAML file, and relay this information - (no. of objects created, (events and "UNIQUE IDENTIFIERS" to identify these events)) to the APEX backend.

2. This information is used to instantiate the pipelines at build time.

3. Add a logger mechanism to keep track of the status of transactions taking place between TACOS and APEX.

![TACOS to APEX flow](https://github.com/davendramaharaj1/apex_tacos/blob/apex_extension/TACOS_APEX_Flow.png)
