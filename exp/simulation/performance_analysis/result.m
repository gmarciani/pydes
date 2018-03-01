% =========================================================================
% PERFORMANCE ANALYSIS
% =========================================================================

% =========================================================================
% DATA
% =========================================================================
data       = readtable('out/result.csv');
threshold  = data{:, {'system_cloudlet_threshold'}};

measures = ["Response Time",            "Throughput"];
ventries = ["statistics_response_mean", "statistics_throughput_mean"];
eentries = ["statistics_response_cint", "statistics_throughput_cint"];
units    = ["sec/task",                 "task/sec"];

% =========================================================================
% SETTINGS
% =========================================================================
scalemn = [0.975, 0.9999];
scalemx = [1.025, 1.0001];

% =========================================================================
% PLOTS
% =========================================================================
one = ones(size(threshold));
for i = 1:length(measures)
    measure = measures(i);
    ventry  = ventries(i);
    eentry  = eentries(i);
    unit    = units(i);
    
    values = data{:, {char(ventry)}};
    errors = data{:, {char(eentry)}};
    
    mn  = min(values);
    mx  = max(values);
    avg = mean(values);
    
    figure(i);
    errorbar(threshold, values, errors);
    title({'Performance Analysis', measure});
    xlabel('Cloudlet Threshold (tasks)');
    ylabel(sprintf('%s (%s)', measure, unit));
    %ylim([mn*scalemn(i) mx*scalemx(i)]);

    yyaxis right
    plot(threshold, one * mn, '--r')
    hold on
    plot(threshold, one * mx, '--r')
    plot(threshold, one * avg, '--r')
    %ylim([mn*scalemn(i) mx*scalemx(i)]);
    set(gca,'ytick', [mn avg mx])
    hold off
end