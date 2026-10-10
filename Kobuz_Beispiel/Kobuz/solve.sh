#!/bin/bash
set -e
source /opt/openfoam14/etc/bashrc
cd "$(dirname "$0")"
trap 'echo "Calculation stopped: inspect current log" > stage.txt' ERR
echo 'Preparing four calculation workers' > stage.txt
decomposePar -force > log.decomposePar 2>&1
echo 'Calculating flow: up to 400 steady iterations' > stage.txt
mpirun -np 4 foamRun -parallel > log.foamRun 2>&1
echo 'Combining results for viewing' > stage.txt
reconstructPar -latestTime > log.reconstructPar 2>&1
echo 'First calculation finished; results need convergence review' > stage.txt
