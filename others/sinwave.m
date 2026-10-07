close all; clear; clc

% --- Parameters ---
A   = 4.5;  f0 = 3;
A2  = 3;    f2 = 5;
A3  = 1;    f3 = 10;
phi = 0;

w0 = 2*pi*f0;
w2 = 2*pi*f2;
w3 = 2*pi*f3;

% --- Time vector ---
Fs = 1000;
t  = 0:1/Fs:3-1/Fs;
N  = length(t);

% --- Signals ---
x  = A*sin(w0*t - phi) + A2*sin(w2*t - phi) + A3*sin(w3*t - phi);
x2 = A3*sin(w3*t - phi);

% --- FFT (single-sided amplitude) ---
X  = fft(x);
P2 = abs(X/N);
P1 = P2(1:N/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f  = Fs*(0:N/2)/N;

% --- Figure 1: composite signal + spectrum ---
figure('Color','w')

subplot(2,1,1)
plot(t, x, 'LineWidth', 1.5, 'Color', 'b')
grid on; box on
xlim([0 2])
xlabel('Time (s)'); ylabel('Voltage (V)')
title('x(t) = A_1 sin(\omega_0 t - \phi) + A_2 sin(\omega_2 t - \phi) + A_3 sin(\omega_3 t - \phi)')
yline(0, 'k-', 'LineWidth', 0.5)

subplot(2,1,2)
stem(f, P1, 'LineWidth', 1.8, 'Color', 'r', 'Marker', 'o')
grid on; box on
xlim([0 15]); xticks(0:1:15)
xlabel('Frequency (Hz)'); ylabel('Amplitude (V)')
title('Single-Sided Amplitude Spectrum')

% --- Figure 2: third component alone ---
figure('Color','w')
plot(t, x2, 'LineWidth', 1.8, 'Color', 'g')
grid on; box on
xlim([0 2])
ylim([-A3*1.2 A3*1.2])
xlabel('Time (s)'); ylabel('Voltage (V)')
title('x_3(t) = A_3 sin(\omega_3 t - \phi)')