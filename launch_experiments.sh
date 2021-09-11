#!/usr/bin/env bash

echo "Launching performance analysis for Algorithm 1"
python3 pydes.py simulate-performance \
--config "config/performance_analysis_1.yaml" \
--outdir "out/performance_analysis/algorithm_1"

echo "Launching analytical solver for Algorithm 1"
python3 pydes.py solve-cloud-cloudlet \
--config config/analytical_solution_1.yaml \
--outdir "out/analytical_solution/algorithm_1"

for threshold in 5 20
do
  echo "Launching performance analysis for Algorithm 2 (threshold: ${threshold})"
  python3 pydes.py simulate-performance \
  --config config/performance_analysis_2.yaml \
  --parameters "{\"system\": {\"cloudlet\": {\"threshold\": ${threshold}}}}" \
  --outdir "out/performance_analysis/algorithm_2/threshold_${threshold}"

  echo "Launching analytical solver for Algorithm 2 (threshold: ${threshold})"
  python3 pydes.py solve-cloud-cloudlet \
  --config config/analytical_solution_2.yaml \
  --parameters "{\"system\": {\"cloudlet\": {\"threshold\": ${threshold}}}}" \
  --outdir "out/analytical_solution/algorithm_2/threshold_${threshold}"
done
