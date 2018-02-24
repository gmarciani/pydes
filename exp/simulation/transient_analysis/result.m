% =========================================================================
% TRANSIENT ANALYSIS
% =========================================================================

% =========================================================================
% DATA
% =========================================================================
data     = readtable('out/result.csv');
batch    = data{:, {'batch'}};

%measures = ["Arrived",   "Completed", "Service Time", "N",     "Response Time", "Throughput"];
%entries  = ["arrived",   "completed", "service",      "n",     "response",      "throughput"];
%units    = ["tasks",     "tasks",     "sec",          "tasks", "sec",           "tasks/sec"];

measures = ["Completed", "Service Time", "Response Time", "Throughput"];
entries  = ["completed", "service",      "response",      "throughput"];
units    = ["tasks",     "sec",          "sec",           "tasks/sec"];

% =========================================================================
% SETTINGS
% =========================================================================
%scalemn = [0.975, 0.975, 0.975, 0.975, 0.975, 0.975];
%scalemx = [1.025, 1.025, 1.025, 1.025, 1.025, 1.025];

scalemn = [0.975, 0.975, 0.975, 0.975];
scalemx = [1.025, 1.025, 1.025, 1.025];

% =========================================================================
% PLOTS
% =========================================================================
one = ones(size(batch));
for i = 1:length(measures)
    measure = measures(i);
    entry   = entries(i);
    unit    = units(i);
    
    values = data{:, {char(entry)}};    
    
    mn  = min(values);
    mx  = max(values);
    avg = mean(values);
    
    figure(i);
    scatter(batch, values);
    title({'Transient Analysis', measure});
    xlabel('Batch (id)');
    ylabel(sprintf('%s (%s)', measure, unit));
    ylim([mn*scalemn(i) mx*scalemx(i)]);

    yyaxis right
    plot(batch, one * mn,'--r')
    hold on
    plot(batch, one * mx, '--r')
    plot(batch, one * avg, '--r')
    ylim([mn*scalemn(i) mx*scalemx(i)]);
    set(gca,'ytick', [mn avg mx])
    hold off
end