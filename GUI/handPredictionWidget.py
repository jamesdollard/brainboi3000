import numpy as np
import keras
from keras import models
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from brainflow import DataFilter, FilterTypes
import matplotlib.pyplot as plt
from mne.time_frequency import psd_array_multitaper
from scipy import integrate

# Page to make live finger motion predictions using pre-trained ML model
class HandPredictionWidget(QWidget):
    def __init__(self, parentSelf):
        self.parentSelf = parentSelf
        self.update_speed_ms = 1000
        self.isCollecting = False
        self.isGraphing = False
        self.model = keras.models.load_model('/Users/jamesdollard/git/brainboi2000/GUI/rbmeotmd1.keras')
        self.counter = 0
        super().__init__()

        title = QLabel("Let's see if we can predict when you move your finger!")
        title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        title.setStyleSheet("""
            color: #fff;
            font-size: 30px;
        """)

        self.feedButton = QPushButton("Start Detection")
        self.feedButton.pressed.connect(self.togglePrediction)
        self.feedButton.setStyleSheet("""
            background-color: green;
            border-image: none !important;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            color: #fff;
            font: 14px;
            height: 1em;
            padding: 6px;
            margin: 1em 10em;
        """)

        subTitle = QLabel("Place your right hand on the table in front of you. When you are ready, lift your right index finger.")
        subTitle.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        subTitle.setStyleSheet("""
            color: #fff;
            font: 25px;
        """)

        self.statusTitle = QLabel("Status: ")
        self.statusTitle.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.statusTitle.setStyleSheet("""
            color: #fff;
            font: 20px
        """)
        self.status = QLabel("No Movement")
        self.status.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.status.setStyleSheet("""
            color: red;
            font: 20px;
        """)

        pageLayout = QVBoxLayout()
        self.title_layout = QHBoxLayout()
        self.subtitle_layout = QHBoxLayout()
        self.status_layout = QHBoxLayout()
        pageLayout.addLayout(self.title_layout)
        pageLayout.addLayout(self.subtitle_layout)
        pageLayout.addLayout(self.status_layout)
        self.title_layout.addWidget(title)
        self.title_layout.addWidget(self.feedButton)
        self.subtitle_layout.addWidget(subTitle)
        self.setLayout(pageLayout)
        #
        #
        #
        #
        #Put the 16 channels normalized in here
        self.train_normalized_numbers = [15.769502888754888, 30.692777518460847, 13.215505105014646, 16.52733368928467, 111.83829012305853, 13.484382641115294, 10.408530337495607, 23.397121381714626, 11.088439474934157, 12.8897989616352, 11.184752739484285, 9.751377190510011, 14.266627832874757, 17.8253244650739, 16.370117956978405, 27.770300778303998]



    # Toggle if data is being collected and fed into model
    def togglePrediction(self):
        self.status_layout.addWidget(self.statusTitle)
        self.status_layout.addWidget(self.status)
        self.time_period = 2.5
        self.num_points = self.time_period * self.parentSelf.sampling_rate
        self.num_points = 311
        self.parentSelf.timer.timeout.connect(self.predict)
        self.parentSelf.timer.start(self.update_speed_ms)

    # # Use to predict muscle movement from muscle data (for training)
    # def predict(self):
    #     data = self.parentSelf.board_shim.get_current_board_data(62)
    #     data = data[8]
    #     data -= np.mean(data)
    #     self.run_band_pass(data)
    #     # Predict muscle movement different way
    #     muscle_data = data
    #     muscle_data = np.square(muscle_data)
    #     threshold = 200
    #     moved = False
    #     for value in muscle_data:
    #         if value >= threshold:
    #             moved = True
    #             break
    #     if moved:
    #         self.status.setText("Finger moved!")
    #         self.status.setStyleSheet("""
    #                     color: green;
    #                     font: 20px;
    #                 """)
    #         self.counter = 0
    #         print("SUCCCCCCCCESSS")
    #     elif self.counter >= 5:
    #         self.status.setText("No Movement")
    #         self.status.setStyleSheet("""
    #                 color: red;
    #                 font: 20px;
    #             """)
    #         print("no_move")
    #     self.counter += 1

    # # Predict muscle movement using gamma spike in fourth electrode
    # def predict(self):
    #     # Process raw data
    #     data = self.parentSelf.board_shim.get_current_board_data(250)
    #     data = data[2]
    #     data_mean = np.mean(data)
    #     data -= data_mean
    #     reference = data[0:125]
    #     interest = data[125:250]
    #     reference_psd, frequencies = \
    #         psd_array_multitaper(reference, 250, adaptive=True, normalization='full', verbose=0)
    #     interest_psd, frequencies = \
    #         psd_array_multitaper(interest, 250, adaptive=True, normalization='full', verbose=0)
    #
    #     # Get relevant band powers
    #     reference_band_powers = []
    #     interest_band_powers = []
    #     band_idx = frequencies > 80
    #     for i in range(len(frequencies)):
    #         bin = frequencies[i]
    #         if bin > 80:
    #             reference_band_powers.append(reference_psd[band_idx])
    #             interest_band_powers.append(interest_psd[band_idx])
    #     reference_band_powers = np.array(reference_band_powers).transpose()
    #     interest_band_powers = np.array(interest_band_powers).transpose()
    #     total_reference_power = np.sum(integrate.simps(reference_band_powers))
    #     total_interest_power = np.sum(integrate.simps(interest_band_powers))
    #
    #     reference_multiplier = 2.4
    #     moved = False
    #     if total_interest_power > total_reference_power * reference_multiplier:
    #         moved = True
    #     if moved:
    #         self.status.setText("Finger moved!")
    #         self.status.setStyleSheet("""
    #                     color: green;
    #                     font: 20px;
    #                 """)
    #         self.counter = 0
    #         print("SUCCCCCCCCESSS")
    #     elif self.counter >= 5:
    #         self.status.setText("No Movement")
    #         self.status.setStyleSheet("""
    #                 color: red;
    #                 font: 20px;
    #             """)
    #         print("no_move")
    #     self.counter += 1

    # Predict muscle movement using a dense network and brain waves
    def predict(self):
        data = self.parentSelf.board_shim.get_current_board_data(350)

        # Process electrodes
        e3 = data[2]
        e3 -= np.mean(e3)
        e4 = data[3]
        e4 -= np.mean(e4)
        e7 = data[6]
        e7 -= np.mean(e7)

        # Remove interference from all electrodes
        band_stop_frequency = 60
        band_stop_width = 10.0
        band_pass_min = 2
        band_pass_max = 125
        center_freq = (band_pass_min + band_pass_max) / 2.0
        band_width = band_pass_max - band_pass_min

        # Filter
        DataFilter.perform_bandstop(e3, 250, band_stop_frequency,
                                    band_stop_width, 2, FilterTypes.BUTTERWORTH.value, 0.0)
        DataFilter.perform_bandpass(e3, 250, center_freq, band_width, 2,
                                    FilterTypes.BUTTERWORTH.value, 0.0)
        DataFilter.perform_bandstop(e4, 250, band_stop_frequency,
                                    band_stop_width, 2, FilterTypes.BUTTERWORTH.value, 0.0)
        DataFilter.perform_bandpass(e4, 250, center_freq, band_width, 2,
                                    FilterTypes.BUTTERWORTH.value, 0.0)
        DataFilter.perform_bandstop(e7, 250, band_stop_frequency,
                                    band_stop_width, 2, FilterTypes.BUTTERWORTH.value, 0.0)
        DataFilter.perform_bandpass(e7, 250, center_freq, band_width, 2,
                                    FilterTypes.BUTTERWORTH.value, 0.0)

        # Remove first hundred datapoints from all samples
        e3 = e3[100:]
        e4 = e4[100:]
        e7 = e7[100:]

        # Remove data if amplitude too high (hopefully gets muscle interference)
        bad_sample = False
        bad_samples_idx = []
        for sample in [e3, e4, e7]:
            if np.max(sample) > 100 or np.min(sample) < -100:
                print('HIGH AMPLITUDE SAMPLE')
                bad_sample = True

        # Get power bins
        e3_psd, self.frequencies = \
            psd_array_multitaper(e3, 250, adaptive=True, normalization='full', verbose=0)
        e3_total_band_power = integrate.simps(e3_psd)
        e3_relative_bands = e3_psd / e3_total_band_power

        e4_psd, self.frequencies = \
            psd_array_multitaper(e4, 250, adaptive=True, normalization='full', verbose=0)
        e4_total_band_power = integrate.simps(e4_psd)
        e4_relative_bands = e4_psd / e4_total_band_power

        e7_psd, self.frequencies = \
            psd_array_multitaper(e7, 250, adaptive=True, normalization='full', verbose=0)
        e7_total_band_power = integrate.simps(e7_psd)
        e7_relative_bands = e7_psd / e7_total_band_power

        sample = [[e3_relative_bands, e4_relative_bands, e7_relative_bands]]
        sample = np.swapaxes(sample, 1, 2)

        train_std = \
            [[0.01476474, 0.01631246, 0.01631718],
                [0.02620701, 0.02686283, 0.02804365],
                [0.02044909, 0.02105626, 0.02235255],
                [0.01677405, 0.01872686 ,0.01830245],
                [0.01685349, 0.01871326 ,0.0182856 ],
                [0.01664785, 0.01844743 ,0.01911868],
                [0.01438977, 0.01741451 ,0.01976959],
                [0.01315815, 0.01528999 ,0.02050752],
                [0.012611  , 0.0146526  ,0.02098592],
                [0.01177259, 0.01418756 ,0.02002651],
                [0.01091025, 0.01413216 ,0.0196515 ],
                [0.0100345 , 0.01353677 ,0.01824545],
                [0.00943196, 0.01278214 ,0.01666602],
                [0.00859619, 0.01121476 ,0.0129942 ],
                [0.00757761, 0.00923231 ,0.00877395],
                [0.00715873, 0.00733369 ,0.00720624],
                [0.00691866, 0.00679066 ,0.00654214],
                [0.0065439 , 0.00612532 ,0.00649415],
                [0.00617699, 0.00582739 ,0.00593671],
                [0.00606672, 0.00581866 ,0.00567298],
                [0.00580141, 0.00557059 ,0.00542462],
                [0.00550212, 0.00533288 ,0.00517623],
                [0.0055653 , 0.00513437 ,0.00505187],
                [0.00542666, 0.00495912 ,0.00507906],
                [0.00506654, 0.00478077 ,0.00490897],
                [0.00503117, 0.00470742 ,0.00479067],
                [0.00506894, 0.00454103 ,0.00472174],
                [0.004988  , 0.00468142 ,0.00487829],
                [0.00483885, 0.00466738 ,0.00468365],
                [0.00456471, 0.00463647 ,0.00465998],
                [0.0044456 , 0.00457108 ,0.00450727],
                [0.00443583, 0.00454569 ,0.00452091],
                [0.00422836, 0.00440366 ,0.00456744],
                [0.00424851, 0.00419822 ,0.00455142],
                [0.00398442, 0.00400003 ,0.00431252],
                [0.00395255, 0.00387852 ,0.00430317],
                [0.00386372, 0.00370908 ,0.00420777],
                [0.00376149, 0.00353131 ,0.00413788],
                [0.00349449, 0.00340614 ,0.00387468],
                [0.00348416, 0.00338079 ,0.00382123],
                [0.00341332, 0.00338862 ,0.00378832],
                [0.00328861, 0.00345155 ,0.00370163],
                [0.00322939, 0.00346962 ,0.00362286],
                [0.00304765, 0.00336139 ,0.0034354 ],
                [0.00302042, 0.00330749 ,0.0033357 ],
                [0.00282179, 0.00324208 ,0.00319523],
                [0.00282012, 0.00323532 ,0.0032489 ],
                [0.00258887, 0.0030305  ,0.00297817],
                [0.00260791, 0.00296263 ,0.00306391],
                [0.00250922, 0.00280417 ,0.00294357],
                [0.00242332, 0.00276005 ,0.00283524],
                [0.00235729, 0.00261534 ,0.0027464 ],
                [0.00217427, 0.00235471 ,0.00250529],
                [0.001888  , 0.00207419 ,0.00215566],
                [0.00157358, 0.00170387 ,0.00179604],
                [0.00133257, 0.00133964 ,0.00142254],
                [0.00114733, 0.00109454 ,0.00117748],
                [0.00087214, 0.00079859 ,0.00085146],
                [0.00054932, 0.00053114 ,0.00051695],
                [0.00027825, 0.00024193 ,0.00024499],
                [0.0001955 , 0.00013014 ,0.00015771],
                [0.00027986, 0.00019677 ,0.00021665],
                [0.00048702, 0.00037219 ,0.00039031],
                [0.00067456, 0.00052766 ,0.00057637],
                [0.00102222, 0.00071474 ,0.00086084],
                [0.00115356, 0.00090195 ,0.00104168],
                [0.00115935, 0.0010568  ,0.00116886],
                [0.00207372, 0.0014003  ,0.00151503],
                [0.0022074 , 0.00152946 ,0.00165126],
                [0.00226483, 0.00160395 ,0.00173882],
                [0.00233362, 0.00170726 ,0.00182778],
                [0.00235195, 0.00171512 ,0.00182902],
                [0.00235087, 0.00174036 ,0.0018829 ],
                [0.00224077, 0.00168372 ,0.0018542 ],
                [0.00193064, 0.00170197 ,0.00182041],
                [0.00161717, 0.00170774 ,0.00182212],
                [0.00152008, 0.00164595 ,0.00174044],
                [0.00155375, 0.00166774 ,0.00174443],
                [0.00160103, 0.00169811 ,0.00174424],
                [0.00155086, 0.00169602 ,0.0016872 ],
                [0.00155638, 0.00169796 ,0.00167004],
                [0.00156257, 0.00170149 ,0.00165233],
                [0.00147267, 0.00159182 ,0.00152674],
                [0.00140802, 0.00152442 ,0.00148874],
                [0.00132605, 0.00151323 ,0.00144341],
                [0.00134809, 0.00150129 ,0.0014931 ],
                [0.00131266, 0.00145235 ,0.00146463],
                [0.00126366, 0.00137945 ,0.00141568],
                [0.00119536, 0.00132739 ,0.001353  ],
                [0.00111695, 0.00120929 ,0.00129041],
                [0.00105399, 0.00111511 ,0.00122668],
                [0.00096263, 0.00103437 ,0.00116186],
                [0.00089893, 0.0009684  ,0.00106862],
                [0.00084244, 0.00090962 ,0.00100892],
                [0.00081701, 0.00087116 ,0.00096164],
                [0.00074428, 0.00079878 ,0.000885  ],
                [0.00070537, 0.0007724  ,0.00082168],
                [0.00064852, 0.00073278 ,0.00074008],
                [0.0006129 , 0.00070892 ,0.00070441],
                [0.00058877, 0.00068412 ,0.00068019],
                [0.00059084, 0.00066943 ,0.00066649],
                [0.00056798, 0.00063915 ,0.00065088],
                [0.00054041, 0.00063198 ,0.0006424 ],
                [0.00052098, 0.0006301  ,0.00063775],
                [0.00051996, 0.00064545 ,0.00065343],
                [0.0004894 , 0.00061979 ,0.00061901],
                [0.00048858, 0.00061096 ,0.00060581],
                [0.00047422, 0.00056547 ,0.00058244],
                [0.00046152, 0.00055193 ,0.00056345],
                [0.00046204, 0.00054823 ,0.00054971],
                [0.00046074, 0.00053461 ,0.00053619],
                [0.00046125, 0.00050899 ,0.00052091],
                [0.00044409, 0.00048805 ,0.00049713],
                [0.00042432, 0.00047766 ,0.00049429],
                [0.00041436, 0.0004812  ,0.00048796],
                [0.00042557, 0.00047934 ,0.00049906],
                [0.0004624 , 0.00048543 ,0.00051518],
                [0.00056137, 0.00051641 ,0.00057718],
                [0.00055948, 0.00050355 ,0.00057889],
                [0.00055622, 0.00049523 ,0.00057238],
                [0.00054586, 0.00047975 ,0.0005588 ],
                [0.00053044, 0.00046093 ,0.00055582],
                [0.00054408, 0.00047611 ,0.00055358],
                [0.0005475 , 0.00048938 ,0.00055586],
                [0.00044007, 0.00047332 ,0.00048086],
                [0.00023027, 0.00024807 ,0.00024619]
             ]

        sample /= train_std
        sample = np.array([sample])

        prediction = self.model.predict(sample)
        print(prediction)

        moved = False
        if prediction > .5:
            moved = True
        if moved and not bad_sample:
            self.status.setText("Finger moved!")
            self.status.setStyleSheet("""
                        color: green;
                        font: 20px;
                    """)
            self.counter = 0
            print("SUCCCCCCCCESSS")
        elif self.counter >= 5:
            self.status.setText("No Movement")
            self.status.setStyleSheet("""
                    color: red;
                    font: 20px;
                """)
            print("no_move")
        self.counter += 1

    # # Predict muscle movement using event related potential
    # def predict(self):
    #     data = self.parentSelf.board_shim.get_current_board_data(250)
    #     data -= np.mean(data, axis=0)
    #
    #     electrode_3_data = data[2] - np.mean(data[2])
    #     electrode_4_data = data[3] - np.mean(data[3])
    #     electrode_7_data = data[6] - np.mean(data[6])
    #
    #     # Filter unwanted frequencies
    #     band_stop_frequency = 60
    #     band_stop_width = 10.0
    #     DataFilter.perform_bandstop(electrode_3_data, 250, band_stop_frequency,
    #                                 band_stop_width, 2, FilterTypes.BUTTERWORTH.value, 0.0)
    #     DataFilter.perform_bandstop(electrode_4_data, 250, band_stop_frequency,
    #                                 band_stop_width, 2, FilterTypes.BUTTERWORTH.value, 0.0)
    #     DataFilter.perform_bandstop(electrode_7_data, 250, band_stop_frequency,
    #                                 band_stop_width, 2, FilterTypes.BUTTERWORTH.value, 0.0)
    #
    #     processed_data = np.array([electrode_3_data, electrode_4_data, electrode_7_data]).transpose()
    #
    #     sample = np.array([processed_data])
    #
    #     prediction = self.model.predict(sample)
    #     print(prediction)
    #     moved = False
    #     if prediction > .6:
    #         moved = True
    #     if moved:
    #         self.status.setText("Finger moved!")
    #         self.status.setStyleSheet("""
    #                     color: green;
    #                     font: 20px;
    #                 """)
    #         self.counter = 0
    #         print("SUCCCCCCCCESSS")
    #     elif self.counter >= 0:
    #         self.status.setText("No Movement")
    #         self.status.setStyleSheet("""
    #                 color: red;
    #                 font: 20px;
    #             """)
    #         print("no_move")

    def normalize(self, data):
        for i in range(16):
            channel = data[i]
            channel -= channel.mean(axis=0)
            # channel /= channel.std(axis=0)
            channel /= self.train_normalized_numbers[i]
            data[i] = channel
        return data

    def run_band_pass(self, data):
        band_stop_frequency = 60
        band_stop_width = 10.0
        band_pass_min = 25
        band_pass_max = 30
        center_freq = (band_pass_min + band_pass_max) / 2.0
        band_width = band_pass_max - band_pass_min
        sample_rate = 250

        DataFilter.perform_bandstop(data, sample_rate, band_stop_frequency,
                                    band_stop_width, 2, FilterTypes.BUTTERWORTH.value, 0.0)
        DataFilter.perform_bandstop(data, sample_rate, band_stop_frequency,
                                    band_stop_width, 2, FilterTypes.BUTTERWORTH.value, 0.0)
        DataFilter.perform_bandpass(data, sample_rate, center_freq, band_width, 2,
                                    FilterTypes.BUTTERWORTH.value, 0.0)
        DataFilter.perform_bandpass(data, sample_rate, center_freq, band_width, 2,
                                    FilterTypes.BUTTERWORTH.value, 0.0)
        DataFilter.perform_bandpass(data, sample_rate, center_freq, band_width, 2,
                                    FilterTypes.BUTTERWORTH.value, 0.0)
