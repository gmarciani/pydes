% =========================================================================
% TRANSIENT ANALYSIS
% =========================================================================

% =========================================================================
% DATA
% =========================================================================
measures = ["Response Time", "Throughput"];
entries  = ["response",      "throughput"];
units    = ["sec/task",      "task/sec"];

seeds = {};
ls = dir('out');
for i=1:size(ls,1)
    n = ls(i).name;
    if strcmp(n, '.') == 0 && strcmp(n, '..') == 0
        seeds = [seeds, n];
    end
end

% =========================================================================
% SETTINGS
% =========================================================================
samplePoints = 30;

% =========================================================================
% PLOTS
% =========================================================================
for i = 1:length(measures)
    measure = measures(i);
    entry   = entries(i);
    unit    = units(i);
    
    figure(i);
    title({'Transient Analysis', measure});
    xlabel('Time (sec)');
    ylabel(sprintf('%s (%s)', measure, unit));
    
    for seed = seeds
        data = readtable(sprintf('out/%s/result.transient.csv', seed{:}));
        time = data{:, {'time'}};
        values = data{:, {char(entry)}};
        
        samplePace = floor(size(time,1)/samplePoints);
    
        hold on
        scatter(time(1:samplePace:end), values(1:samplePace:end), 'DisplayName', char(seed));  
        hold off
    end
    
    lgd = legend('show');
    title(lgd, 'Initial Seeds');
end
