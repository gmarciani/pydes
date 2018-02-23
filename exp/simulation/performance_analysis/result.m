% =========================================================================
% PERFORMANCE ANALYSIS
% =========================================================================

% =========================================================================
% DATA
% =========================================================================
data = readtable('result.csv');

threshold  = data{:,{'system_cloudlet_threshold'}};
response   = data{:,{'system_statistics_t_response_mean'}};
throughput = data{:,{'system_statistics_throughput_mean'}};

one = ones(size(threshold));

minResponse = min(response);
maxResponse = max(response);
avgResponse = mean(response);

minThroughput = min(throughput);
maxThroughput = max(throughput);
avgThroughput = mean(throughput);

% =========================================================================
% SETTINGS
% =========================================================================
scaleMax = 1.025;
scaleMin = 0.975;

% =========================================================================
% PLOT: PERFORMANCE ANALYSIS, RESPONSE TIME
% =========================================================================
figure(1);
plot(threshold, response);
title('Response Time Analysis');
xlabel('Threshold (tasks)');
ylabel('Response Time (s)');
ylim([minResponse*scaleMin maxResponse*scaleMax]);

yyaxis right
plot(threshold, one * minResponse, '--r')
hold on
plot(threshold, one * maxResponse, '--r')
plot(threshold, one * avgResponse, '--r')
ylim([minResponse*scaleMin maxResponse*scaleMax]);
set(gca,'ytick',[minResponse avgResponse maxResponse])
hold off

% =========================================================================
% PLOT: PERFORMANCE ANALYSIS, THROUGHPUT
% =========================================================================
figure(2);
plot(threshold, throughput);
title('Throughput Analysis');
xlabel('Threshold (tasks)');
ylabel('Throughput (tasks/s)');
ylim([minThroughput*scaleMin maxThroughput*scaleMax]);

yyaxis right
plot(threshold, one * minThroughput, '--r')
hold on
plot(threshold, one * maxThroughput, '--r')
plot(threshold, one * avgThroughput, '--r')
ylim([minThroughput*scaleMin maxThroughput*scaleMax]);
set(gca,'ytick',[minThroughput avgThroughput maxThroughput])
hold off