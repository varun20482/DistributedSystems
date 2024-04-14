# MAP REDUCE using gRPC

## Overview
This project implements a MapReduce system using gRPC. It comprises three main components: `master.py`, `mapper.py`, and `reducer.py`. The system operates by distributing tasks to multiple mapper and reducer nodes for parallel processing of data.

## Components
1. **master.py**: Acts as the central coordinator of the MapReduce process. It assigns tasks to mapper and reducer nodes, coordinates data transfer, and manages the overall workflow.

2. **mapper.py**: Receives data chunks from the master, performs mapping operations, and sends intermediate results to the reducer nodes.

3. **reducer.py**: Receives intermediate results from mapper nodes, performs reduction operations, and generates final output.

## Configuration
The project is configured using the `common.py` file. Key parameters include:
- Number of mappers (`MAPPERS`)
- Number of reducers (`REDUCERS`)
- Number of centroids (`CENTROIDS`)
- Number of iterations (`ITERATIONS`)
- Number of data points (`num_data_points`)
- Coordinate range (`coordinates_from` and `coordinates_to`)

## Usage
1. **Generate Data**: Before running the MapReduce process, generate input data by navigating to `data/input` directory and executing `generate.py`.
   ```
   cd data/input
   python generate.py
   ```

2. **Run Mappers and Reducers**: Start the mapper and reducer nodes by executing `mapper.py` and `reducer.py` with the desired IDs.
   ```
   python mapper.py <id>
   python reducer.py <id>
   ```

3. **Run Master**: Execute `master.py` to initiate the MapReduce process.
   ```
   python master.py
   ```

4. **View Logs**: Logs for the MapReduce process are available in the `data/dump` directory.

5. **Debugging Mode**: To run the master in debugging mode, provide the debug flag along with the master ID.
   ```
   python master.py 1 
   ```

## Notes
- Ensure that all nodes (master, mappers, reducers) are running and properly configured before starting the MapReduce process.
- Adjust the configuration parameters in `common.py` as needed based on the requirements of the dataset and processing tasks.

## GRPC Proto Compiling Command
python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. kmeans.proto