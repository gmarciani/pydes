echo "Launching performance analysis for Algorithm 1"
python3 pydes.py simulate-performance \
--config config/performance_analysis_1.yaml

echo "Launching analytical solver for Algorithm 1"
python3 pydes.py solve-cloud-cloulet \
--config config/analytical_solution_1.yaml

THRESHOLDS=(1 5 15 20)
for threshold in ${THRESHOLDS}; do
  echo "Launching performance analysis for Algorithm 2 (threshold: ${threshold}"
  python3 pydes.py simulate-performance \
  --config config/performance_analysis_2.yaml \
  --parameters "{'system': {'cloudlet': {'threshold': ${threshold}}}"

  echo "Launching analytical solver for Algorithm 2 (threshold: ${threshold})"
  python3 pydes.py solve-cloud-cloulet \
  --config config/analytical_solution_2.yaml \
  --parameters "{'system': {'cloudlet': {'threshold': ${threshold}}}"
done