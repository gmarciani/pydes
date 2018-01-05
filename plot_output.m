Array=csvread('results/simulation_cloud.csv', 1, 5);

threshold = Array(:, 17);
throughput = Array(:, 11);
response_time = Array(:, 12);

figure(1)
plot(threshold, throughput)
title("Throughput Analysis")
xlabel("Threshold (tasks)")
ylabel("Throughput (tasks/s)")

figure(2)
plot(threshold, response_time)
title("Response Time Analysis")
xlabel("Threshold (tasks)")
ylabel("Response Time (s)")

