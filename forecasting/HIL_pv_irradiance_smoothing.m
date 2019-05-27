%% Conversion from GHI data to smoothed plane-of-array (POA) irradiance

% Requires the wavelet variability model and PV_LIB:
% https://pvpmc.sandia.gov/applications/wavelet-variability-model/wavelet-variability-model-download/
% https://github.com/sandialabs/MATLAB_PV_LIB

clear
close all
clc

%% Import irradiance data
ghi_data=xlsread('Solar Data.xlsx');  % excel time, GHI1, GHI2, ... GHI11
% ghi_data=xlsread('EnvSIM6.xlsx');  % excel time, GHI1, GHI2, ... GHI11

%% use dates from the solstice 
dt = 180+ghi_data(:,1)-floor(ghi_data(1,1))-4/24;

%%
% plant_sizes_MW = [0.258; 10; 1];  % PNM

% plant_sizes_MW = [684000;93353;5393.75;2242.35;44555.7;152388;  % NG
%     22180.9;18413.3;121307;54932.6;27494.8;29935.9;59594.4;57685.9;
%     280784;129058;58194.7;13166.9;52328.8;34853.4;22675.2;9156.04;1012210;
%     1028690;993513;373251;334862;344033;27142.1;23568.6;684]/1e6;

plant_sizes_MW = [46642.6,56383.2,62561.9,10094.1, 8563.54,47777.4,45748.4,40293.1, ...
    32855,40131.6,34901.1,45592.3,90011.8,130828,83720.2,42086.2, ...
    11855.6,8535.55,75925.2, 98560.8,181621,91243.4,2680.4,101459, ...
    90762.4,112622,14368.7,27842.8,4881.60, 11807.9,91918.9,129003,66882.9,11319.9, ...
    3936.36,83961.5,62044.2,51741.2,4698.41, ...
    283670,10696.7,174466,23443.3,103084,105539,63827.9,225660, ...
    14601.4,149936,6710.09,11785.8,76734.5,81629, ...
    105224,107985,177482,71814.5,4410.76,11893.7,61088.4, ...
    2674.83,6700.11,1260.61,11095.7]/1e6;

endcol = 4*length(plant_sizes_MW)-1;
col_idx = 3:4:endcol;
smooth_irradiance = zeros(length(ghi_data),length(col_idx));

%% Calculate the irradiance profiles
for i = 1:length(plant_sizes_MW)  % i = irradiance data set
    
    % Configure the irradiance sensor parameters
    irr_sensor.irr = ghi_data(:,col_idx(i)); %measured irradiance
    irr_sensor.time = dt; %timestamps
    irr_sensor.Lat = 32.7765; %sensor latitude
    irr_sensor.Lon = -79.9311; %sensor longitude
    irr_sensor.alt = 200; %sensor altitude (in meters)
    irr_sensor.tilt = 0; %tilt = 0 for GHI sensor
    irr_sensor.azimuth = 180; % azimuth = 0 for GHI sensor
    irr_sensor.UTCoffset = -4; %sensor UTC offset

    plantinfo.tilt = 0; 
    plantinfo.azimuth = 180; %assume modules facing south
    plantinfo.type = 'square'; %assume a square-shaped PV plant
    plantinfo.MW = plant_sizes_MW(i); 
    plantinfo.PVdensity = 41; %41 W/m2 = 1MW per 6 acres, which is a standard rule of thumb

    cloud_speed=10; %assume cloud speed of 10 m/s

    [smooth_irradiance(:,i),other_outputs]=pvl_WVM(irr_sensor,plantinfo,cloud_speed);

end

%%
% figure
% plot(datetime(datevec(irr_sensor.time)), other_outputs.clear_sky_index)
% plot(datetime(datevec(irr_sensor.time)), other_outputs.clear_sky_irr_POA)

%% Save the data in new excel sheet
updated_inputs = ghi_data;
for i = 1:length(plant_sizes_MW)
    updated_inputs(:,col_idx(i)) = smooth_irradiance(:,i);
end
xlswrite(sprintf('Solar Data - smoothed - %i plants.xlsx', length(plant_sizes_MW)), updated_inputs(:, 1:endcol))

%% Plot new irradiance profiles 
h_inv = figure('Position', get(0,'Screensize'));
set(gcf, 'Position', get(0,'Screensize')); % Mostly maximize figure.
set(gcf,'PaperPositionMode','auto')
plot(irr_sensor.time, irr_sensor.irr,'b', ...
    irr_sensor.time,smooth_irradiance(:,1),'r', ...
    irr_sensor.time,smooth_irradiance(:,2),'k', ...
    irr_sensor.time,smooth_irradiance(:,3),'g','linewidth',2);
l = legend('Measured GHI','WVM smoothed POA (258 kW)', 'WVM smoothed POA (10 MW)', 'WVM smoothed POA (1 MW)');
set(l, 'location', 'Northwest');
set(gca,'xtick',floor(nanmean(irr_sensor.time)):1/24:ceil(nanmean(irr_sensor.time)));
datetick('x','HH','keepticks','keeplimits');
xlabel('time of day [HH]');
ylabel('Irradiance [W m^{-2}]');
axis tight
title('Smoothed Irradiance Inputs for PNM Model')
set(gca, 'FontSize', 35)
set(l, 'FontSize', 30);
saveas(h_inv,sprintf('Smoothed PV Irradiance for Simulations for %i plants.jpg', length(plant_sizes_MW)),'jpg')

%% Create data for the comparison plots
smooth_irradiance_plot = zeros(length(ghi_data),length(col_idx));
for i = 1:length(plant_sizes_MW) % size(ghi_data,2)  % i = irradiance data set
    % Configure the irradiance sensor parameters
    irr_sensor.irr = ghi_data(:,col_idx(1)); %measured irradiance
    plantinfo.MW = plant_sizes_MW(i); 
    [smooth_irradiance_plot(:,i),other_outputs]=pvl_WVM(irr_sensor,plantinfo,cloud_speed);
end

%% Plot of the PV plant size vs smoothed POA irradiance
h_inv = figure('Position', get(0,'Screensize'));
set(gcf, 'Position', get(0,'Screensize')); % Mostly maximize figure.
set(gcf,'PaperPositionMode','auto')
plot(irr_sensor.time,irr_sensor.irr,'b',irr_sensor.time,smooth_irradiance_plot(:,1),'r', ...
irr_sensor.time,smooth_irradiance_plot(:,2),'k', irr_sensor.time,smooth_irradiance_plot(:,3),'g','linewidth',2);
l = legend('Measured GHI','WVM smoothed POA (258 kW)', 'WVM smoothed POA (10 MW)', 'WVM smoothed POA (1 MW)');
set(l, 'location', 'Northwest');
set(gca,'xtick',floor(nanmean(irr_sensor.time)):1/24:ceil(nanmean(irr_sensor.time)));
datetick('x','HH','keepticks','keeplimits');
xlabel('time of day [HH]');
ylabel('Irradiance [W m^{-2}]');
axis tight
title('Smoothed Irradiance Inputs for PNM Model')
set(gca, 'FontSize', 35)
set(l, 'FontSize', 30);
saveas(h_inv,sprintf('Smoothed PV Irradiance for %i plants.jpg', length(plant_sizes_MW)),'jpg')

%% Zoomed in plot of the irradiance smoothing effect
h_inv = figure('Position', get(0,'Screensize'));
set(gcf, 'Position', [1, 1, 2560*.95, 1600*.95]); % Mostly maximize figure.
set(gcf,'PaperPositionMode','auto')
plot(irr_sensor.time,irr_sensor.irr,'b',irr_sensor.time,smooth_irradiance_plot(:,1),'r', ...
irr_sensor.time,smooth_irradiance_plot(:,2),'k', irr_sensor.time,smooth_irradiance_plot(:,3),'g','linewidth',3);
l = legend('Measured GHI','WVM smoothed POA (258 kW)', 'WVM smoothed POA (10 MW)', 'WVM smoothed POA (1 MW)');
set(l, 'location', 'Northwest');
set(gca,'xtick',floor(nanmean(irr_sensor.time)):1/24:ceil(nanmean(irr_sensor.time)));
datetick('x','HH','keepticks','keeplimits');
xlabel('time of day [HH]');
plt_x_start = floor(length(irr_sensor.time)/2);
xlim([irr_sensor.time(plt_x_start) irr_sensor.time(plt_x_start+500)])
ylabel('Irradiance [W m^{-2}]');
title('Smoothed Irradiance Inputs for PNM Model')
set(gca, 'FontSize', 35)
set(l, 'FontSize', 30);
saveas(h_inv,sprintf('Smoothed PV Irradiance for %i plants (Zoom).jpg', length(plant_sizes_MW)),'jpg')

%% Plot new irradiance profiles for the larger datasets
h_inv = figure('Position', get(0,'Screensize'));
set(gcf, 'Position', get(0,'Screensize')); % Mostly maximize figure.
set(gcf,'PaperPositionMode','auto')
plot(irr_sensor.time, irr_sensor.irr,'b', irr_sensor.time,smooth_irradiance_plot,'r');
set(gca,'xtick',floor(nanmean(irr_sensor.time)):1/24:ceil(nanmean(irr_sensor.time)));
datetick('x','HH','keepticks','keeplimits');
xlabel('time of day [HH]');
ylabel('Irradiance [W m^{-2}]');
axis tight
title('Smoothed Irradiance Inputs for PNM Model')
set(gca, 'FontSize', 35)
set(l, 'FontSize', 30);
saveas(h_inv,sprintf('Smoothed PV Irradiance for Simulations for %i plants.jpg', length(plant_sizes_MW)),'jpg')

%%

% Livermore=load('example_data\Livermore_Sample_GHI.mat')
% 
% irr_sensor.irr=Livermore.GHI; %measured irradiance
% irr_sensor.time=Livermore.dt; %timestamps
% irr_sensor.Lat=37.676208; %sensor latitude
% irr_sensor.Lon=-121.703118; %sensor longitude
% irr_sensor.alt=200; %sensor altitude (in meters)
% irr_sensor.tilt=0; %tilt = 0 for GHI sensor
% irr_sensor.azimuth=0; % azimuth = 0 for GHI sensor
% irr_sensor.UTCoffset=-8; %sensor UTC offset
% 
% plantinfo.tilt=37; %assume modules tilted 37 degrees (approximately latitude tilt)
% plantinfo.azimuth=180; %assume modules facing south
% plantinfo.type='square'; %assume a square-shaped PV plant
% plantinfo.MW=30; %assume a 30MW plant
% plantinfo.PVdensity=41; %41 W/m2 = 1MW per 6 acres, which is a standard rule of thumb
% 
% cloud_speed=10; %assume cloud speed of 10 m/s
% 
% [smooth_irradiance,other_outputs]=pvl_WVM(irr_sensor,plantinfo,cloud_speed);
% 
% plot(irr_sensor.time,irr_sensor.irr,'b',irr_sensor.time,smooth_irradiance,'r');
% legend('measured GHI','WVM smoothed POA');
% set(gca,'xtick',floor(nanmean(irr_sensor.time)):1/24:ceil(nanmean(irr_sensor.time)));
% datetick('x','HH','keepticks','keeplimits');
% xlabel('time of day [HH]');
% ylabel('Irradiance [W m^{-2}]');
% axis tight
% title(datestr(nanmean(irr_sensor.time),'mmm-dd-yyyy'))
% 
% figure;
% plot(irr_sensor.time,irr_sensor.irr,'b',irr_sensor.time,smooth_irradiance,'r');
% legend('measured GHI','WVM smoothed POA');
% set(gca,'xtick',floor(nanmean(irr_sensor.time)):1/(24*12):ceil(nanmean(irr_sensor.time)));
% datetick('x','HH:MM','keepticks','keeplimits');
% xlabel('time of day [HH:MM]');
% ylabel('Irradiance [W m^{-2}]');
% xlim([floor(nanmean(irr_sensor.time))+10.75/24 floor(nanmean(irr_sensor.time))+11.25/24])
% title(datestr(nanmean(irr_sensor.time),'mmm-dd-yyyy'))