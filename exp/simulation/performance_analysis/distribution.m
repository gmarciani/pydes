% =========================================================================
% DISTRIBUTION ANALYSIS
% =========================================================================

% =========================================================================
% DATA
% =========================================================================
data       = readtable('out/result_5.csv');

measures = ["Response Time", "Throughput"];
entries  = ["response",      "throughput"];
units    = ["sec",           "tasks/sec"];

% =========================================================================
% PLOTS
% =========================================================================
for i = 1:length(measures)
    measure = measures(i);
    entry   = entries(i);
    unit    = units(i);
    
    values = data{:, {char(entry)}};    
    
    figure(i);
    cdfplot(values);
    title({'Distribution Analysis', measure});
    xlabel(sprintf('%s (%s)', measure, unit));
end