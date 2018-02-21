t = readtable("experiment_1.csv");
replications = 5;

threshold = t{:,{"system_cloudlet_threshold"}};
throughput = t{:,{"system_throughput"}};
responseTime = t{:,{"system_response_time_mean_"}};
utilization = t{:,{"system_utilization"}};

thresholdMean = mean(reshape(threshold, replications, []));
throughputMean = mean(reshape(throughput, replications, []));
responseMean = mean(reshape(responseTime, replications, []));
utilizationMean = mean(reshape(utilization, replications, []));

% PLOT: THROUGHPUT
figure(1);
plot(thresholdMean, throughputMean);
title("Throughput Analysis");
xlabel("Threshold (tasks)");
ylabel("Throughput (tasks/s)");

% PLOT: RESPONSE TIME
figure(2);
plot(thresholdMean, responseMean);
title("Response Time Analysis");
xlabel("Threshold (tasks)");
ylabel("Response Time (s)");

% PLOT: UTILIZATION
figure(3);
plot(thresholdMean, utilizationMean);
title("Utilization Analysis");
xlabel("Threshold (tasks)");
ylabel("Utilization");
