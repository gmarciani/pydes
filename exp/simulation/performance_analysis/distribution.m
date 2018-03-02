% =========================================================================
% DISTRIBUTION ANALYSIS
% =========================================================================

% =========================================================================
% SETTINGS
% =========================================================================
threshold = 20;
distName = 'Weibull';
binMethod = 'fd';

% =========================================================================
% DATA
% =========================================================================
data     = readtable(sprintf('out/%d/result.sampling.csv', threshold));

measures = ["Response Time"];
entries  = ["response"];
units    = ["sec"];

% =========================================================================
% PLOTS: distribution fitting histogram
% =========================================================================
for i = 1:length(measures)
    measure = measures(i);
    entry   = entries(i);
    unit    = units(i);
    
    values = data{:, {char(entry)}};
    
    bins = size(histcounts(values, 'BinMethod', binMethod), 2);
    dparams = fitdist(values, distName);
    
    figure(i);
    histfit(values, bins, distName);
    title({'Distribution Analysis', measure});
    xlabel(sprintf('%s (%s)', measure, unit));
    ylabel('Frequency');
    
    lgd = legend('Empirical',sprintf('%s(%.3f,%.3f)', distName, dparams.A, dparams.B));
    set(lgd, 'Location', 'northwest');
    set(lgd, 'Orientation', 'vertical');
end
