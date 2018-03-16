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
notables = ["min",                      "max"];

% =========================================================================
% PLOTS
% =========================================================================
one = ones(size(threshold));
for i = 1:length(measures)
    measure = measures(i);
    ventry  = ventries(i);
    eentry  = eentries(i);
    unit    = units(i);
    notable = notables(i);
    
    values = data{:, {char(ventry)}};
    errors = data{:, {char(eentry)}};
    
    if strcmp(notable, "min") == 1
        criticalName = "Minimum";
        critical = min(values);
    elseif strcmp(notable, "max") == 1
        criticalName = "Maximum";
        critical = max(values);
    else
        raise 
    end
    
    figure(i);
    errorbar(threshold, values, errors, 'DisplayName', 'Average');
    title({'Performance Analysis', measure});
    xlabel('Cloudlet Threshold (task)');
    ylabel(sprintf('%s (%s)', measure, unit));
    
    yl = ylim;
    
    yyaxis right
    plot(threshold, ones(size(threshold)) * critical, '--r', 'DisplayName', criticalName);
    ylim(yl);
    set(gca,'ytick', (critical));
    
    lgd = legend('show');
    set(lgd, 'Location', 'northwest');
    set(lgd, 'Orientation', 'vertical');
end