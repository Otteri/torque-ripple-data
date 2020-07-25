% Entry function, call this! E.g. plot_data('line_chart', args)
% Check the required args from function definitions below.
% This function is needed because Matlab doesn't allow direct function calls...
% And no, I'm not going to make a file for each ugly plot-function.
function plotdata(plot_type, args)
    num_of_args = size(args, 2);
    if strcmp(plot_type, 'linechart') && (num_of_args == 3)
        linechart(args{1}, args{2}, args{3})
    elseif strcmp(plot_type, 'linechart') && (num_of_args == 4)
        linechart(args{1}, args{2}, args{3}, args{4})
    elseif strcmp(plot_type, 'linechart2')
        double_linechart(args{1}, args{2}, args{3}, args{4})
    elseif strcmp(plot_type, 'amplitude_spectrum')
        amplitude_spectrum(args{1}, args{2}, args{3})
    end
end

% Creates a regular plot.
% time and torque parameters are required, while
% T_nom is optional. If it is given, then additional
% mean, min and max lines are drawn to the plot.
function linechart(filename, time, torque, T_nom)
    figure('Name', filename, 'NumberTitle', 'off')
    plot(time, torque);
    title('Torque signal waveform')
    xlabel('t (s)')
    ylabel('T (Nm)')
    legend('torque');
    if exist('T_nom','var') 
        show_ripple(time, torque, T_nom) 
    end
end

% Line chart with y-axises on the left and right
function double_linechart(filename, time, signal1, signal2)
    figure('Name', filename, 'NumberTitle', 'off')
    yyaxis left
    plot(time, signal1);
    ylabel('Torque [Nm]')
    yyaxis right
    plot(time, signal2);
    xlabel('t [s]')
    ylabel('Speed [rpm]')
end

% Inserts three lines to an already existing plot.
% First line shows the torque mean. Two other lines show
% symmetrical ripple boundary with respect to nominal torque.
function show_ripple(time, torq, T_nom)
    orange = [1 0.5 0];
    red = [1 0.2 0.2];

    % Select the one that is further away from average
    if(abs(mean(torq) - max(torq)) > abs(mean(torq) - min(torq)))
      limit = max(torq);
    else
      limit = min(torq);
    end

    % Match percent to the limit
    syms x;
    eqn = abs(mean(torq) + x * T_nom) == limit;
    S = abs(solve(eqn, x));

    % get mean, min and max values
    torque_mean = mean(torq);
    lower = torque_mean - S * T_nom;
    upper = torque_mean + S * T_nom;
    
    % Lines for mean, min and max
    line([0,time(end)], [lower, lower], 'Color',orange,'LineStyle','--');
    line([0,time(end)], [torque_mean, torque_mean], 'Color',red,'LineStyle',':');    
    line([0,time(end)], [upper, upper], 'Color',orange,'LineStyle','--');
    legend('Torque', 'boundary', 'Torque mean') 
end

% Does a FFT and then creates a plot
function amplitude_spectrum(filename, time, signal)
    sample_time = time(2)-time(1);
    sample_length = time(end) - time(1);

    Y = fft(signal);              % Fourier transform
    Fs = (1 / sample_time);       % Frequency from sample time
    L = Fs * sample_length;       % Length of the signal

    P2 = abs(Y/L);                % Two-sided spectrum
    P1 = P2(1:L/2+1);             % Single-sided spectrum
    P1(2:end-1) = 2*P1(2:end-1);
    f = Fs*(0:(L/2))/L;           % frequency domain
    
    figure('Name', filename, 'NumberTitle', 'off')
    plot(f,P1)
    %xlim([0 100])  % if automatic axle-limits are bad,
    %ylim([0 10])   % then uncomment and give limits yourself
    title('Torque signal harmonics')
    xlabel('f (Hz)')
    ylabel('Amplitude (Nm)')
end
