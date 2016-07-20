function resampled_signal = resample_signal(signal, time, resample_time)

signal_timeseries = timeseries(signal, time);
resampled_signal_timeseries = resample(signal_timeseries, resample_time, 'zoh');
resampled_signal = squeeze(resampled_signal_timeseries.Data)';