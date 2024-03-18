#!/bin/bash

forward_interrupt() {
    echo "Interrupt signal received. Forwarding to child processes..."
    kill -- -$$ 
}

trap forward_interrupt SIGINT

python3 server.py > dump/output1.log &

python3 server.py > dump/output2.log &

python3 server.py > dump/output3.log &

wait

echo "All processes completed."
