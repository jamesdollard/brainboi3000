
import numpy as np
from scipy import integrate, signal
from mne.time_frequency import psd_array_multitaper
from brainflow import DataFilter, FilterTypes


# Stores bandpower processing hyper-parameters and processes bandpowers for a state
class BandpowerProcessing:

    def __init__(self):

        # Data processing variables
        self.filter_sixty_hz = False
        self.filter_zero_to_five_hz = False
        self.include_all_frequencies = True
        self.custom_low_frequency = 0
        self.custom_high_frequency = 50

        self.bp_methods = ["Welch's", "Multitaper", "FFT"]
        self.selected_bp_method = self.bp_methods[0]
        self.welch_window_length_fraction_of_total = 0.1

        self.include_all_electrodes = True
        self.custom_electrode_selection = []
        self.num_electrodes = 8
        self.sampling_rate = 250

        self.relative = False

        self.eeg_bands = [
            [0, 4],  # Delta
            [4, 7],  # Theta
            [7, 12],  # Alpha
            [12, 30],  # Beta
            [30, 50]  # Gamma
        ]

    # Processes the bandpower for a state, s
    def process_state(self, s_data):

        s_frequencies = []
        s_processed_channel_holder = []
        s_total_power = 0
        uncut_s_frequencies = []
        uncut_s_bandpowers = []

        for i in range(0, self.num_electrodes):
            if self.include_all_electrodes or (i+1) in self.custom_electrode_selection:
                s_channel = s_data[i] - np.mean(s_data[i])

                if self.filter_sixty_hz:
                    DataFilter.perform_bandstop(s_channel, self.sampling_rate, 60, 4,
                                                2, FilterTypes.BUTTERWORTH.value, 0.0)

                if self.filter_zero_to_five_hz:
                    band_pass_min = 5
                    band_pass_max = 125
                    center_freq = (band_pass_min + band_pass_max) / 2.0
                    band_width = band_pass_max - band_pass_min
                    DataFilter.perform_bandpass(s_channel, self.sampling_rate, center_freq, band_width, 2,
                                                FilterTypes.BUTTERWORTH.value, 0.0)

                if self.selected_bp_method == "Welch's":
                    s_welch_window_length = int(self.welch_window_length_fraction_of_total * len(s_channel))
                    s_frequencies, s_power_spectral_density = \
                        signal.welch(s_channel, fs=self.sampling_rate, nperseg=s_welch_window_length)
                elif self.selected_bp_method == "Multitaper":
                    s_power_spectral_density, s_frequencies = \
                        psd_array_multitaper(s_channel, self.sampling_rate,
                                             adaptive=True, normalization='full', verbose=0)
                elif self.selected_bp_method == "FFT":
                    s_fft = np.fft.rfft(s_channel)
                    s_power_spectral_density = np.multiply(s_fft, np.conjugate(s_fft)).real
                    s_frequencies = np.fft.rfftfreq(len(s_channel), 1/self.sampling_rate)
                else:
                    print('ERROR: Bandpower method is not implemented')
                    return

                uncut_s_frequencies = s_frequencies.copy()
                uncut_s_bandpowers = s_power_spectral_density.copy()

                if self.include_all_frequencies:
                    s_total_power = integrate.simps(s_power_spectral_density)
                else:
                    s_band_idx = np.logical_and(s_frequencies >= self.custom_low_frequency,
                                                s_frequencies <= self.custom_high_frequency)
                    s_frequencies = s_frequencies[s_band_idx]
                    s_power_spectral_density = s_power_spectral_density[s_band_idx]
                    s_total_power = integrate.simps(s_power_spectral_density)

                # Get relevant band powers
                s_band_powers = []
                for j in range(len(s_frequencies)):
                    bin = s_frequencies[j]
                    band_power = s_power_spectral_density[j]
                    if self.relative:
                        band_power = band_power / s_total_power
                    s_band_powers.append(band_power)

                s_processed_channel_holder.append(s_band_powers)

        s_processed_bp = np.mean(s_processed_channel_holder, axis=0)

        # Get Standard Band Power Ratios #

        s_standard_band_values = [0, 0, 0, 0, 0]

        if len(s_frequencies) > 0:
            for i in range(len(uncut_s_frequencies)):
                if uncut_s_frequencies[i] not in s_frequencies:
                    uncut_s_frequencies[i] = 0
                    uncut_s_bandpowers[i] = 0

            for i in range(len(self.eeg_bands)):
                start_freq = self.eeg_bands[i][0]
                end_freq = self.eeg_bands[i][1]

                uncut_s_band_idx = np.logical_and(uncut_s_frequencies >= start_freq,
                                                  uncut_s_frequencies <= end_freq)
                s_band_psd = uncut_s_bandpowers[uncut_s_band_idx]
                if len(s_band_psd) > 1:
                    s_band_power = integrate.simps(s_band_psd)
                else:
                    s_band_power = 0
                s_standard_band_values[i] = s_band_power / s_total_power

        return np.array(s_frequencies), np.array(s_processed_bp), np.array(s_standard_band_values)
