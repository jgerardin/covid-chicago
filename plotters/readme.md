
### Plotters  - Visualization and analysis of model outcomes and input data


#### Compare simulations to data 
- [data_comparison.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/data_comparison.py) 
compares the predicted number of new detected hospitalized cases, cumulative detections of hospitalized cases, total number of case hospitalizations and number of critical cases to hospital data and case reports for specified EMS region as included in exp_name (using base or age emodl)

- [data_comparison_spatial.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/data_comparison_spatial.py) 
compares the predicted number of new detected hospitalized cases, cumulative detections of hospitalized cases, total number of case hospitalizations and number of critical cases to hospital data and case reports for all EMS regions (using locale emodl) 

#### Comparison multiple simulation experiments 
- [plot_split_by_param](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/plot_split_by_param.py)
Takes two experiment simulations and compares generates a plot comparing the trajectories of both

- [plot_by_param_ICU_nonICU](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/plot_by_param_ICU_nonICU.py)
Plots the most recent trend in EMresource data for ICU and non-ICU and compares the next 2-3 weeks forward predictions, either with one or two exp_names

- [plot_split_by_channel](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/plot_split_by_channel.py)
Comparison plotter for 2 channels in one panel (i.e. all vs detected for infected, symptomatic, hospitalized ...)

- [plot_split_by_param_trajectories](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/plot_split_by_param_trajectories.py)
Simple plot per outcome channel for one experiment, instead of aggregating trajectories, show single trajectories

- [scenario_comparison.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/scenario_comparison.py)
Similar to [plot_split_by_param](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/plot_split_by_param.py), but takes multiple scenarios from a subfolder.
Can be modified with improved analysis and comparison of varing scenarios (per EMS or combined). 

- [combine_csv.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/combine_csv.py)
Reads in trajectoriesDat from several simulation experiments and appends the dataframe without aggregating them. 



#### Stacked and grouped timeline plots
- [EMS_combo_plotter.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/EMS_combo_plotter.py)
Generates a plot showing the trajectories for all EMS together.

- [locale_age_postprocessing.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/locale_age_postprocessing.py)
Generates a plot showing the trajectories for any group, either EMS or Age, separate plots per group and stacked plot. 

#### Generate "process-for-civis-like" timelines for selected channels
-  [process_for_civis.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/process_for_civis.py)
The stem argument allows to process only experiments that contain this string in the name.
`python plotters/process_for_civis.py --stem 'test'`


#### Process-for-civis scripts that generate custom outputs in the format requested by civis (not used)
- [combine_process_for_civis_csv.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/combine_process_for_civis_csv.py)
Reads in several EMS specific simulation experiments and sums the trajectores to be representative for the total area.

- [add_ems_to_IL.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/add_ems_to_IL.py)


#### Process-for-civis scripts
- [process_for_civis_EMSgrp.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/process_for_civis_EMSgrp.py)
(1) Generate aggregated csv file in specified format
- [overflow_probabilities.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/overflow_probabilities.py)
(2) Calculate overflow probabilities for ICU and non ICU capacity
- [get_Rt_forCivisOutputs.R](https://github.com/numalariamodeling/covid-chicago/blob/master/Rfiles/estimate_Rt/get_Rt_forCivisOutputs.R) (Rscript in Rfiles folder!)
(3) Estimate Rt from aggregated csv file (new_cases)
- [NUcivis_filecopy.py](https://github.com/numalariamodeling/covid-chicago/blob/master/plotters/NUcivis_filecopy.py)
(4) Generate output folder and copy required files and create changelog

#### Further scripts 
- trim_trajectoriesDat.py
- county_estimation.py
- generate_trajectories_for_dash.py
- Ki_map.py and  ki_red_map.py
- scenario_sets.py and mixed_reopening_scenarios.py
- safegrafe_awaytime_map.py



