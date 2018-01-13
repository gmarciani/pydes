modulus = 2147483647;
%multiplier = 16807;
%multiplier = 48271;
%multiplier = 50812;
multiplier = 1234;

streams = 5;

samsize = 10000;
d = 5;

filenameData = sprintf('out/mod%d_mul%d_str%d/extremes_sms%d_d%d.csv', modulus, multiplier, streams, samsize, d);

data = readtable(filenameData);

x = data{:,1:1};
y = data{:,2:2};

filenameReport = sprintf('out/mod%d_mul%d_str%d/extremes_sms%d_d%d_report.csv', modulus, multiplier, streams, samsize, d);

report = readtable(filenameReport);

%mn = report{:,{"critical_bounds.lower_bound"}};
%mx = report{:,{"critical_bounds.upper_bound"}};
mn = 10.0;
mx = 20.0;

% PLOT: THROUGHPUT
figure(1);
scatter(x, y);
hold on
plot([0 streams-1], [1 1] * mn, '--r')
plot([0 streams-1], [1 1] * mx, '--r')
hold off
title({'Extremes Test';sprintf('Modulus: %d | Multiplier: %d', modulus, multiplier)});
xlabel('Stream Number');
ylabel('Chi-Square Statistic');
xlim([0 streams-1])
ylim([0 30])
set(gca,'xtick',0:10)
set(gca,'ytick',[mn mx])
yticklabels({'min', 'max'})