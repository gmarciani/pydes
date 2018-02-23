% DATA
t = readtable('result.csv');

threshold = t{:,{'system_cloudlet_threshold'}};
response = t{:,{'system_statistics_t_response_mean'}};
throughput = t{:,{'system_statistics_throughput_mean'}};

one = ones(size(threshold));

minResponse = min(response);
maxResponse = max(response);

minThroughput = min(throughput);
maxThroughput = max(throughput);

% SETTINGS
scaleMax = 1.025;
scaleMin = 0.975;


% PLOT: RESPONSE TIME
figure(2);
plot(threshold, response);
title('Response Time Analysis');
xlabel('Threshold (tasks)');
ylabel('Response Time (s)');
ylim([minResponse*scaleMin maxResponse*scaleMax]);

yyaxis right
plot(threshold, one * minResponse, '--r')
hold on
plot(threshold, one * maxResponse, '--r')
ylim([minResponse*scaleMin maxResponse*scaleMax]);
set(gca,'ytick',[minResponse maxResponse])
%yticklabels({'v_{min}', 'v_{max}'})
hold off

% PLOT: THROUGHPUT
figure(1);
plot(threshold, throughput);
title('Throughput Analysis');
xlabel('Threshold (tasks)');
ylabel('Throughput (tasks/s)');
ylim([minThroughput*scaleMin maxThroughput*scaleMax]);

yyaxis right
plot(threshold, one * minThroughput, '--r')
hold on
plot(threshold, one * maxThroughput, '--r')
ylim([minThroughput*scaleMin maxThroughput*scaleMax]);
set(gca,'ytick',[minThroughput maxThroughput])
hold off

