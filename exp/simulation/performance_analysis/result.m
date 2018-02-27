% =========================================================================
% PERFORMANCE ANALYSIS
% =========================================================================

% =========================================================================
% DATA
% =========================================================================
data       = readtable('out/result.csv');
threshold  = data{:, {'system_cloudlet_threshold'}};

measures = ["Response Time",            "Throughput"];
entries  = ["statistics_response_mean", "statistics_throughput_mean"];
units    = ["sec",                      "tasks/sec"];

% =========================================================================
% SETTINGS
% =========================================================================
scalemn = [0.975, 0.99999];
scalemx = [1.025, 1.00001];

% =========================================================================
% PLOTS
% =========================================================================
one = ones(size(threshold));
for i = 1:length(measures)
    measure = measures(i);
    entry   = entries(i);
    unit    = units(i);
    
    values = data{:, {char(entry)}};    
    
    mn  = min(values);
    mx  = max(values);
    avg = mean(values);
    
    figure(i);
    plot(threshold, values);
    title({'Performance Analysis', measure});
    xlabel('Cloudlet Threshold (tasks)');
    ylabel(sprintf('%s (%s)', measure, unit));
    ylim([mn*scalemn(i) mx*scalemx(i)]);

    yyaxis right
    plot(threshold, one * mn, '--r')
    hold on
    plot(threshold, one * mx, '--r')
    plot(threshold, one * avg, '--r')
    ylim([mn*scalemn(i) mx*scalemx(i)]);
    set(gca,'ytick', [mn avg mx])
    hold off
end