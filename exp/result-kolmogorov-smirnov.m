% %
% KOLMOGOROV-SMIRNOV ANALYSIS
% %

% VARIABLES
modulus = 2147483647;
multiplier = 50812;
%multiplier = 48271;
%multiplier = 16807;
streams = 256;
samsize = 10000;
d = 5;
bins = 1000;
testName = 'extremes';

% DATASET
filenameData = sprintf('out/mod%d_mul%d_str%d/ks_%s_chi.csv', modulus, multiplier, streams, testName);
data = readtable(filenameData);

dataEmpirical = sort(data{:,2:2});
dataTheoretical = chi2cdf(dataEmpirical, bins - 1);

% REPORT
filenameReport = sprintf('out/mod%d_mul%d_str%d/ks_%s_report.csv', modulus, multiplier, streams, testName);

report = readtable(filenameReport);

criticalPoint = report{:,13};

% PLOT
figure(1);
cdfplot(dataEmpirical)
hold on
plot(dataEmpirical, dataTheoretical)
plot([1 1] * criticalPoint, [0.0 1.0], '--r')
hold off

title({'Kolmogorov-Smirnov Test (Extremes)';sprintf('Modulus: %d | Multiplier: %d | Streams: %d', modulus, multiplier, streams)});
xlabel('x');
ylabel('CDF');

set(gca,'ytick',[0.0 1.0])

legend('Empirical','Theoretical','Location','NW')