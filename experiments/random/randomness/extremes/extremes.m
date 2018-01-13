% %
% EXTREMES TEST OF RANDOMNESS
% %

% VARIABLES
modulus = 2147483647;
multiplier = 50812;
%multiplier = 48271;
%multiplier = 16807;
streams = 256;
samsize = 10000;
d = 5;

% DATASET
filenameData = sprintf('out/mod%d_mul%d_str%d/extremes_sms%d_d%d.csv', modulus, multiplier, streams, samsize, d);

data = readtable(filenameData);

x = data{:,1:1};
y = data{:,2:2};

% REPORT
filenameReport = sprintf('out/mod%d_mul%d_str%d/extremes_sms%d_d%d_report.csv', modulus, multiplier, streams, samsize, d);

report = readtable(filenameReport);

criticalLower = report{:,11};
criticalUpper = report{:,12};

offset = 25;
xLim = [ -offset streams-1+offset ];

% PLOT
figure(1);
scatter(x, y);
hold on
plot([-offset streams-1+offset], [1 1] * criticalLower, '--r')
plot([-offset streams-1+offset], [1 1] * criticalUpper, '--r')
hold off
title({'Extremes Test';sprintf('Modulus: %d | Multiplier: %d', modulus, multiplier)});
xlabel('Stream Number');
ylabel('Chi-Square Statistic');
xlim(xLim)
%ylim([0 30])
set(gca,'xtick',[0 streams-1])
set(gca,'ytick',[criticalLower criticalUpper])
yticklabels({'min', 'max'})