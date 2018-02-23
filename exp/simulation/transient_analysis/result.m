% =========================================================================
% TRANSIENT ANALYSIS
% =========================================================================

% =========================================================================
% DATA
% =========================================================================
data = readtable('result.csv');

batch      = data{:,{'batch'}};
response   = data{:,{'t_response'}};
throughput = data{:,{'throughput'}};

one = ones(size(batch));

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
% PLOT: TRANSIENT ANALYSIS, RESPONSE TIME
% =========================================================================
figure(1);
plot(batch, response);
title('Transient Analysis, Response Time');
xlabel('Batch Number');
ylabel('Mean Response Time (s)');
ylim([minResponse*scaleMin maxResponse*scaleMax]);

yyaxis right
plot(batch, one * minResponse, '--r')
hold on
plot(batch, one * maxResponse, '--r')
plot(batch, one * avgResponse, '--r')
ylim([minResponse*scaleMin maxResponse*scaleMax]);
set(gca,'ytick',[minResponse avgResponse maxResponse])
hold off

% =========================================================================
% PLOT: TRANSIENT ANALYSIS, THROUGHPUT
% =========================================================================
figure(2);
plot(batch, throughput);
title('Transient Analysis, Throughput');
xlabel('Batch Number');
ylabel('Mean Throughput (tasks/s)');
ylim([minThroughput*scaleMin maxThroughput*scaleMax]);

yyaxis right
plot(batch, one * minThroughput, '--r')
hold on
plot(batch, one * maxThroughput, '--r')
plot(batch, one * avgThroughput, '--r')
ylim([minThroughput*scaleMin maxThroughput*scaleMax]);
set(gca,'ytick',[minThroughput avgThroughput maxThroughput])
hold off