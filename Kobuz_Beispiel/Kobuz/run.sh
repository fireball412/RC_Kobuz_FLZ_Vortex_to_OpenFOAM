#!/bin/bash
set -e
source /opt/openfoam14/etc/bashrc
cd "$(dirname "$0")"
trap 'echo "Failed: inspect the current log" > stage.txt' ERR
echo 'Building surrounding air domain' > stage.txt
blockMesh > log.blockMesh 2>&1
echo 'Extracting sharp surface edges' > stage.txt
surfaceFeatures > log.surfaceFeatures 2>&1
echo 'Refining and snapping the airflow mesh; adding boundary layers' > stage.txt
snappyHexMesh -overwrite > log.snappyHexMesh 2>&1
echo 'Checking mesh quality' > stage.txt
checkMesh -allTopology -meshQuality > log.checkMesh 2>&1
if ! grep -q 'Mesh OK' log.checkMesh; then echo 'Mesh quality needs review; solver not started' > stage.txt; exit 2; fi
echo 'Preparing calculation on four CPU workers' > stage.txt
decomposePar -force > log.decomposePar 2>&1
echo 'Calculating flow: up to 400 steady iterations' > stage.txt
mpirun -np 4 foamRun -parallel > log.foamRun 2>&1
echo 'Combining results for viewing' > stage.txt
reconstructPar -latestTime > log.reconstructPar 2>&1
echo 'First calculation finished; results need convergence review' > stage.txt
