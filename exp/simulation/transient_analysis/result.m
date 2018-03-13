% =========================================================================
% TRANSIENT ANALYSIS
% =========================================================================

% =========================================================================
% DATA
% =========================================================================
measures = ["Response Time",   "Throughput"];
entries  = ["response_global", "throughput_global"];
units    = ["sec/task",        "task/sec"];

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
ratioForMean = 0.5;

% =========================================================================
% PLOTS
% =========================================================================

for i = 1:length(measures)
    measure = measures(i);
    entry   = entries(i);
    unit    = units(i);
    
    valuesForMean = [];
    
    figure(i);
    title({'Transient Analysis', measure});
    xlabel('Time (sec)');
    ylabel(sprintf('%s (%s)', measure, unit));
    
    for seed = seeds
        data = readtable(sprintf('out/%s/result.sampling.csv', seed{:}));
        time = data{:, {'time'}};
        values = data{:, {char(entry)}};
        
        nValues = size(time, 1);
        valuesForMean = cat(1, valuesForMean, values(floor(ratioForMean*nValues):1:end));        
        samplePace = floor(nValues/samplePoints);
    
        hold on
        scatter(time(1:samplePace:end), values(1:samplePace:end), 10, 'LineWidth', 0.1, 'DisplayName', char(seed));  
        hold off
    end
    
    yl = ylim;
    
    avg = mean(valuesForMean);
    
    yyaxis right
    plot(time, ones(size(time)) * avg, '--r', 'DisplayName', 'Average');
    ylim(yl);
    set(gca,'ytick', (avg))
    
    lgd = legend('show');
    set(lgd, 'Location', 'southeast');
    set(lgd, 'Orientation', 'vertical');
end

