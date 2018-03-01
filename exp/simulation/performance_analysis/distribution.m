% =========================================================================
% DISTRIBUTION ANALYSIS
% =========================================================================

% =========================================================================
% DATA
% =========================================================================
data     = readtable('out/20/result.transient.csv');

measures = ["Response Time", "Throughput"];
entries  = ["response", "throughput"];
units    = ["sec", "task/sec"];

% =========================================================================
% SETTINGS
% =========================================================================
scalemn = [0.98, 0.98];
scalemx = [1.02, 1.02];

% =========================================================================
% PLOTS: histogram
% =========================================================================
bins = 10;
for i = 1:length(measures)
    measure = measures(i);
    entry   = entries(i);
    unit    = units(i);
    
    values = data{:, {char(entry)}};
    
    mn = min(values);
    mx = max(values);
    avg = mean(values);
    sdev = std(values) / sqrt(length(values));
    
    x = linspace(avg-3*sdev, avg+3*sdev);
    norm = normpdf(x, avg, sdev);
    
    figure(i);
    histogram(values, 'Normalization','probability');
    title({'Distribution Analysis', measure});
    xlabel(sprintf('%s (%s)', measure, unit));
    ylabel('PDF');
    
end
