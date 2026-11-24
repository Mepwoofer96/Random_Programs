close all; clear; clc

%  PART 1: NORMAL (BASEBAND) WAVES - three sine tones, no modulation

% --- Parameters ---
A   = 4.5;  f0 = 3;      % tone 1: 4.5 V at 3 Hz
A2  = 3;    f2 = 5;      % tone 2: 3 V at 5 Hz
A3  = 1;    f3 = 100;    % tone 3 (carrier): 1 V at 100 Hz
phi = 0;
w0 = 2*pi*f0;
w2 = 2*pi*f2;
w3 = 2*pi*f3;

% --- Time vector ---
Fs = 1000;
t  = 0:1/Fs:3-1/Fs;
N  = length(t);

% --- Signals ---
x = (A*sin(w0*t - phi) + A2*sin(w2*t - phi)) .* (A3*sin(w3*t - phi));  % DSB-SC: (3+5 Hz message) x 100 Hz carrier

x2 = A3*sin(w3*t - phi);                                           % NORMAL single wave (10 Hz only)

% --- FFT (single-sided amplitude) of the NORMAL composite wave ---
X  = fft(x);
P2 = abs(X/N);
P1 = P2(1:N/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f  = Fs*(0:N/2)/N;

% --- Figure 1: NORMAL composite wave + its spectrum ---
figure('Color','w')

subplot(2,1,1)
plot(t, x, 'LineWidth', 1.5, 'Color', 'b')
grid on; box on
xlim([0 2])
xlabel('Time (s)'); ylabel('Voltage (V)')
title('NORMAL wave: x(t) = A_1 sin(\omega_0 t - \phi) + A_2 sin(\omega_2 t - \phi) + A_3 sin(\omega_3 t - \phi)')
yline(0, 'k-', 'LineWidth', 0.5)

subplot(2,1,2)
stem(f, P1, 'LineWidth', 1.8, 'Color', 'r', 'Marker', 'o')
grid on; box on
xlabel('Frequency (Hz)'); ylabel('Amplitude (V)')
title('NORMAL wave: Single-Sided Amplitude Spectrum')


% --- Build the FM signal (self-contained) ---
Fs  = 1000;  t = 0:1/Fs:3-1/Fs;  N = numel(t);
s   = (3*sin(2*pi*5*t) + 4.5*sin(2*pi*3*t)) / 7.5;   % message, normalized to +/-1
fc  = 100;  kf = 20;
xfm = sin(2*pi*fc*t + 2*pi*kf*cumsum(s)/Fs);          % FM signal

% --- FFT (single-sided amplitude) of the FM signal ---
Xf  = fft(xfm);
Pf2 = abs(Xf/N);
Pf1 = Pf2(1:N/2+1);
Pf1(2:end-1) = 2*Pf1(2:end-1);
ff  = Fs*(0:N/2)/N;

% --- Figure: FM signal + its spectrum ---
figure('Color','w')

subplot(2,1,1)
plot(t, xfm, 'LineWidth', 1.2, 'Color', 'b')
grid on; box on
xlim([0 1])
ylim([-1.2 1.2])
xlabel('Time (s)'); ylabel('Voltage (V)')
title('FM signal: x(t) = sin(2\pi f_c t + 2\pi k_f \int s(\tau)d\tau)')
yline(0, 'k-', 'LineWidth', 0.5)

subplot(2,1,2)
stem(ff, Pf1, 'LineWidth', 1.5, 'Color', 'r', 'Marker', 'o', 'MarkerSize', 4)
grid on; box on
xlim([60 140]); xticks(60:10:140)
xlabel('Frequency (Hz)'); ylabel('Amplitude (V)')
title('FM signal: Single-Sided Amplitude Spectrum')

% --- Figure 2: NORMAL third component alone ---
figure('Color','w')
plot(t, x2, 'LineWidth', 1.8, 'Color', 'g')
grid on; box on
xlim([0 2])
ylim([-A3*1.2 A3*1.2])
xlabel('Time (s)'); ylabel('Voltage (V)')
title('NORMAL wave: x_3(t) = A_3 sin(\omega_3 t - \phi)')

% --- Figure 3: spectrogram (frequency vs time) ---
L    = 1500;                              % window length (samples) = 1.5 s at Fs = 1000
hop  = 100;                               % step between windows
nfft = 4096;                              % zero-pad for a smoother image
w = 0.5*(1 - cos(2*pi*(0:L-1)/(L-1)));    % Hann window
starts = 1:hop:(N - L + 1);
nSeg   = numel(starts);
Amp    = zeros(nfft/2 + 1, nSeg);
for k = 1:nSeg
    seg = x(starts(k) : starts(k)+L-1) .* w;
    X   = fft(seg, nfft);
    Amp(:,k) = 2*abs(X(1:nfft/2+1)) / sum(w);
end
fS = Fs*(0:nfft/2)/nfft;                  % frequency axis (Hz)
tS = (starts - 1 + L/2) / Fs;             % time at the center of each window (s)

figure('Color','w')
imagesc(tS, fS, Amp)
axis xy
ylim([90 110])
yticks(90:2:110)                          % ticks land on 95, 97, 103, 105
xlabel('Time (s)'); ylabel('Frequency (Hz)')
title('Spectrogram: Frequency vs Time')
cb = colorbar; cb.Label.String = 'Amplitude (V)';
colormap turbo


%  PART 2: AM (AMPLITUDE MODULATION) - and the FM signal is generated here

fs = 5000;  t = 0:1/fs:3;

x1 = 3*sin(2*pi*5*t);          % NORMAL message tone 1 (5 Hz)
x2 = 4.5*sin(2*pi*3*t);        % NORMAL message tone 2 (3 Hz)
s  = (x1 + x2) / 7.5;          % NORMAL message (baseband), normalized to +/-1

fc = 100;  m = 1;              % carrier >> message frequencies
carrier = sin(2*pi*fc*t);      % NORMAL carrier wave (100 Hz)

am = (1 + m*s) .* carrier;     % *** AM signal ***

% FM version (computed here, but not plotted in this section)
kf = 20;                       % Hz deviation per unit of s
fm = sin(2*pi*fc*t + 2*pi*kf*cumsum(s)/fs);   % *** FM signal (time domain) ***

% AM plot: blue = AM signal, red = envelope (+/-(1 + m*s), i.e. the message riding on the carrier)
figure('Color','w')
plot(t, am); hold on
plot(t, 1 + m*s, 'r', t, -(1 + m*s), 'r')
grid on; box on
xlabel('Time (s)'); ylabel('Amplitude')
title('AM signal (blue) with message envelope (red)')
legend('AM signal', 'Envelope +(1+ms)', 'Envelope -(1+ms)')


%  PART 3: FM (FREQUENCY MODULATION) - spectrogram

% --- Build the FM signal ---
Fs = 1000;  t = 0:1/Fs:3-1/Fs;  N = numel(t);
x1 = 3*sin(2*pi*5*t);                     % NORMAL message tone 1 (5 Hz)
x2 = 4.5*sin(2*pi*3*t);                   % NORMAL message tone 2 (3 Hz)
s  = (x1 + x2) / 7.5;                     % NORMAL message (baseband), normalized to +/-1
fc = 100;  kf = 20;
x  = sin(2*pi*fc*t + 2*pi*kf*cumsum(s)/Fs);   % *** FM signal ***

% --- Figure: FM spectrogram (frequency vs time, base MATLAB) ---
L    = 150;                               % window length (samples) = 0.15 s at Fs = 1000
hop  = 10;                                % step between windows
nfft = 4096;
w = (1 - cos(2*pi*(0:L-1)/(L-1)));    % Hann window
starts = 1:hop:(N - L + 1);
nSeg   = numel(starts);
Amp    = zeros(nfft/2 + 1, nSeg);
for k = 1:nSeg
    seg = x(starts(k) : starts(k)+L-1) .* w;
    X   = fft(seg, nfft);
    Amp(:,k) = 2*abs(X(1:nfft/2+1)) / sum(w);
end
fS = Fs*(0:nfft/2)/nfft;
tS = (starts - 1 + L/2) / Fs;
figure('Color','w')
imagesc(tS, fS, Amp)
axis xy
ylim([60 140])                            % FM lives around fc = 100 Hz
xlabel('Time (s)'); ylabel('Frequency (Hz)')
title('FM signal: Spectrogram, Frequency vs Time')
cb = colorbar; cb.Label.String = 'Amplitude (V)';
colormap turbo
yticks(60:10:140)
hold on
plot(t, fc + kf*s, 'w--')                 % ideal instantaneous frequency of the FM signal (NORMAL message shifted to fc)
legend('Ideal instantaneous frequency')



% --- Figure: AM spectrogram (frequency vs time) ---
La    = 10000;                            % window length (samples) = 2 s at fs = 5000
hopA  = 500;                              % step between windows
nfftA = 16384;                            % zero-pad for a smoother image
wA    = 0.5*(1 - cos(2*pi*(0:La-1)/(La-1)));   % Hann window
Na      = numel(am);
startsA = 1:hopA:(Na - La + 1);
nSegA   = numel(startsA);
AmpA    = zeros(nfftA/2 + 1, nSegA);
for k = 1:nSegA
    seg = am(startsA(k) : startsA(k)+La-1) .* wA;
    X   = fft(seg, nfftA);
    AmpA(:,k) = 2*abs(X(1:nfftA/2+1)) / sum(wA);
end
fSA = fs*(0:nfftA/2)/nfftA;               % frequency axis (Hz)
tSA = (startsA - 1 + La/2) / fs;          % time at the center of each window (s)

figure('Color','w')
imagesc(tSA, fSA, AmpA)
axis xy
ylim([90 110])
yticks(90:2:110)
xlabel('Time (s)'); ylabel('Frequency (Hz)')
title('AM signal: Spectrogram, Frequency vs Time')
cb = colorbar; cb.Label.String = 'Amplitude (V)';
colormap turbo