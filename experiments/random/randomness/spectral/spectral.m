% %
% SPECTRAL TEST
% %

% VARIABLES
modulus = 2147483647;
multiplier = 16807;
%multiplier = 48271;
%multiplier = 50812;
samsize = modulus-1;
a = 0.0;
b = 0.001;

% DATASET
filename = sprintf("out/mod%d_mul%d/spectral_%d.csv", modulus, multiplier, samsize);

t = readtable(filename);

x = t{:,1:1};
y = t{:,2:2};

% PLOT
figure(1);
scatter(x, y);
xlim([a b])
ylim([a b])
title({"Spectral Test";sprintf("Modulus: %d | Multiplier: %d", modulus, multiplier)});
xlabel("Random Number");
ylabel("Random Number");
