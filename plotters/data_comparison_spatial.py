import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.path.append('../')
from load_paths import load_box_paths
import matplotlib as mpl
import matplotlib.dates as mdates
from datetime import date, timedelta, datetime
import seaborn as sns
from processing_helpers import *

mpl.rcParams['pdf.fonttype'] = 42
today = datetime.today()
datetoday = date(today.year, today.month, today.day)

def parse_args():

    description = "Simulation run for modeling Covid-19"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "-stem",
        "--stem",
        type=str,
        help="Name of simulation experiment"
    )
    parser.add_argument(
        "-loc",
        "--Location",
        type=str,
        help="Local or NUCLUSTER",
        default = "Local"
    )
    parser.add_argument(
        "-t", "--trajectoriesName",
        type=str,
        help="Name of trajectoriesDat file, could be trajectoriesDat.csv or trajectoriesDat_trim.csv",
        default='trajectoriesDat.csv',
    )
    return parser.parse_args()
    
def load_sim_data(exp_name, ems_nr,  input_wdir=None, fname= 'trajectoriesDat.csv', input_sim_output_path=None, column_list=None):

    input_wdir = input_wdir or wdir
    sim_output_path_base = os.path.join(input_wdir, 'simulation_output', exp_name)
    sim_output_path = input_sim_output_path or sim_output_path_base

    df = pd.read_csv(os.path.join(sim_output_path,fname), usecols=column_list)

    #df.columns = df.columns.str.replace('_All', '')
    df.columns = df.columns.str.replace('_EMS-' +str(ems_nr), '')
    df['infected_cumul'] = df['infected'] + df['recovered'] + df['deaths']
    df = calculate_incidence(df)

    return df


def plot_sim_and_ref(df, ems_nr, ref_df, channels, data_channel_names, titles, first_day=date(2020, 2, 22),
                     ymax=40, logscale=True):
    fig = plt.figure(figsize=(13, 6))
    palette = sns.color_palette('husl', 8)
    k = 0
    for c, channel in enumerate(channels):
        ax = fig.add_subplot(2, 3, c + 1)

        # for k, (ki, kdf) in enumerate(df.groupby('Ki')) :
        mdf = df.groupby('time')[channel].agg([np.mean, CI_5, CI_95, CI_25, CI_75]).reset_index()
        dates = [first_day + timedelta(days=int(x)) for x in mdf['time']]
        ax.plot(dates, mdf['mean'], color=palette[k])
        ax.fill_between(dates, mdf['CI_5'], mdf['CI_95'],
                        color=palette[k], linewidth=0, alpha=0.2)
        ax.fill_between(dates, mdf['CI_25'], mdf['CI_75'],
                        color=palette[k], linewidth=0, alpha=0.4)

        ax.set_title(titles[c], y=0.8, fontsize=12)
        # ax.legend()

        formatter = mdates.DateFormatter("%m-%d")
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.set_xlim(first_day, datetoday)
        ax.grid(b=True, which='major', color='#999999', linestyle='-', alpha=0.3)
        if logscale :
            ax.set_ylim(0.1, ymax)
            ax.set_yscale('log')

        ax.plot(ref_df['date'], ref_df[data_channel_names[c]], 'o', color='#303030', linewidth=0, ms=1)
        ax.plot(ref_df['date'], ref_df[data_channel_names[c]].rolling(window = 7, center=True).mean(), c='k', alpha=1.0)

    fig.suptitle(f'Covidregion {ems_nr}', y=1, fontsize=14)
    fig.tight_layout()
    fig.subplots_adjust(top=0.88)

    plot_name = 'compare_to_data_covidregion_' + str(ems_nr)
    if logscale == False :
        plot_name = plot_name + "_nolog"
    plt.savefig(os.path.join(wdir, 'simulation_output', exp_name,  plot_name + '.png'))
    plt.savefig(os.path.join(wdir, 'simulation_output', exp_name,  plot_name + '.pdf'), format='PDF')
    # return a

def load_ref_df(ems_nr):
    ref_df = pd.read_csv(os.path.join(datapath, 'covid_IDPH', 'Corona virus reports', 'emresource_by_region.csv'))

    if ems_nr > 0:
        ref_df = ref_df[ref_df['covid_region'] == ems_nr]
    else:
        ref_df = ref_df.groupby('date_of_extract').agg(np.sum).reset_index()
    ref_df['suspected_and_confirmed_covid_icu'] = ref_df['suspected_covid_icu'] + ref_df['confirmed_covid_icu']
    data_channel_names_emr = ['confirmed_covid_deaths_prev_24h', 'confirmed_covid_icu', 'covid_non_icu']
    ref_df = ref_df.groupby('date_of_extract')[data_channel_names_emr].agg(np.sum).reset_index()
    ref_df['date'] = pd.to_datetime(ref_df['date_of_extract'])
    ref_df_emr = ref_df

    LL_file_date = get_latest_LLfiledate(file_path=os.path.join(datapath, 'covid_IDPH', 'Cleaned Data'))
    ref_df_ll = pd.read_csv(os.path.join(datapath, 'covid_IDPH', 'Cleaned Data', f'{LL_file_date}_jg_aggregated_covidregion.csv'))

    ref_df_cli  = pd.read_csv(os.path.join(datapath, 'covid_IDPH', 'Corona virus reports','CLI_admissions_by_covidregion.csv'))

    if ems_nr > 0:
        ref_df_ll = ref_df_ll[ref_df_ll['covid_region'] == ems_nr]
    else:
        ref_df_ll = ref_df_ll.groupby('date').agg(np.sum).reset_index()
    ref_df_ll['date'] = pd.to_datetime(ref_df_ll['date'])
    ref_df_cli['date'] = pd.to_datetime(ref_df_cli['date'])

    if ems_nr > 0:
        ref_df_cli = ref_df_cli[ref_df_cli['covidregion'] == ems_nr]
    else:
        ref_df_cli = ref_df_cli.groupby('date').agg(np.sum).reset_index()

    ref_df = pd.merge(how='outer', left=ref_df_ll, left_on='date', right=ref_df_emr, right_on='date')
    ref_df = pd.merge(how='outer', left=ref_df, left_on='date', right=ref_df_cli, right_on='date')

    ref_df = ref_df.sort_values('date')

    return ref_df

def compare_ems(exp_name,fname, ems_nr=0):

    column_list = ['time', 'startdate', 'scen_num', 'sample_num','run_num']

    outcome_channels = ['susceptible', 'infected', 'recovered', 'infected_cumul', 'asymp_cumul', 'asymp_det_cumul', 'symp_mild_cumul', 'symp_severe_cumul', 'symp_mild_det_cumul',
        'symp_severe_det_cumul', 'hosp_det_cumul', 'hosp_cumul', 'detected_cumul', 'crit_cumul', 'crit_det_cumul', 'death_det_cumul',
        'deaths', 'crit_det',  'critical', 'hosp_det', 'hospitalized']

    for channel in outcome_channels:
        column_list.append(channel + "_EMS-" + str(ems_nr))

    df = load_sim_data(exp_name, ems_nr, fname=fname,column_list=column_list)
    first_day = datetime.strptime(df['startdate'].unique()[0],  '%Y-%m-%d')

    df['critical_with_suspected'] = df['critical']


    df['date'] = df['time'].apply(lambda x: first_day + timedelta(days=int(x)))
    df = df[df['date']  <=  datetime.today()]

    ref_df = load_ref_df(ems_nr)

    channels = ['new_detected_deaths', 'crit_det', 'hosp_det', 'new_deaths','new_detected_hospitalized',
                'new_detected_hospitalized']
    data_channel_names = ['confirmed_covid_deaths_prev_24h',
                          'confirmed_covid_icu', 'covid_non_icu', 'deaths','inpatient', 'admissions']
    titles = ['New Detected\nDeaths (EMR)', 'Critical Detected (EMR)', 'Inpatient non-ICU\nCensus (EMR)', 'New Detected\nDeaths (LL)',
              'Covid-like illness\nadmissions (IDPH)', 'New Detected\nHospitalizations (LL)']
    plot_path = os.path.join(wdir, 'simulation_output', exp_name, 'compare_to_data_combo')
    plot_sim_and_ref(df,ems_nr, ref_df, channels=channels, data_channel_names=data_channel_names, titles=titles, ymax=10000,
                      first_day=first_day)

    # return ref_df_emr, ref_df_ll


if __name__ == '__main__':

    args = parse_args()  
    trajectoriesName = args.trajectoriesName
    #Location = 'Local'
    datapath, projectpath, wdir, exe_dir, git_dir = load_box_paths(Location = args.Location)

    stem = args.stem
    exp_names = [x for x in os.listdir(os.path.join(wdir, 'simulation_output')) if stem in x]

    for exp_name in exp_names:
        for ems_nr in range(1,12):
            print("Start processing region " + str(ems_nr))
            compare_ems(exp_name,fname=trajectoriesName, ems_nr=int(ems_nr))
