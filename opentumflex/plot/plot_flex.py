"""
The "plot_flex.py" can visualize the results of OpenTUMFlex/opentumflex
"""

__author__ = "Babu Kumaran Nalini"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Babu Kumaran Nalini"
__email__ = "babu.kumaran-nalini@tum.de"
__status__ = "Development"


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec


def plot_flex(my_ems, device):
    """
    

    Parameters
    ----------
    my_ems : Dictionary
        Dictionary of the opentumflex model with flex offer dataframe.
    device : String,  e.g. 'ev'/'pv'
        Device whose offers need to be plotted.

    Returns
    -------
    None.

    """
    if not np.count_nonzero(
        my_ems['flexopts'][device]['Pos_P']
    ) and not np.count_nonzero(my_ems['flexopts'][device]['Neg_P']):
        return
    # time data            
    timesteps = np.arange(my_ems['time_data']['isteps'], my_ems['time_data']['nsteps'])
    N = len(timesteps)
    isteps = my_ems['time_data']['isteps']
    nsteps = my_ems['time_data']['nsteps']
    ntsteps = my_ems['time_data']['ntsteps']
    dat1 = pd.DataFrame.from_dict(my_ems['flexopts'][device])
    ts_raw = my_ems['time_data']['time_slots'][isteps:nsteps]
    ts_hr = pd.to_datetime(ts_raw).strftime('%H:%M').to_list()
    ts_date = pd.to_datetime(ts_raw).strftime('%d %b %Y')

    # Initialize    
    neg_leg = 0
    pos_leg = 0
    font_size = 18
    fig = plt.figure(constrained_layout=True, figsize=(16, 12), dpi=80)
    spec = gridspec.GridSpec(ncols=1, nrows=4, figure=fig)
    plt_prc = fig.add_subplot(spec[3, 0])
    plt_pow = fig.add_subplot(spec[2, 0], sharex=plt_prc)
    plt_cum = fig.add_subplot(spec[0:2, 0], sharex=plt_prc)
    ts = my_ems['time_data']['time_slots']

    # Plotting cummulative energy exchange
    theta = 0
    cum_data = pd.DataFrame(
             index=my_ems['time_data']['time_slots'], columns={'cumm'})
    cum_data.iloc[0, 0] = 0
    for i in range(nsteps - 1):
        cum_data.iloc[i + 1, 0] = theta + dat1['Sch_P'][i]/ntsteps
        theta = cum_data.iloc[i + 1, 0]
    p1 = plt_cum.plot(cum_data.iloc[:, 0], linewidth=3, color='k')

    for x in range(nsteps):
        # Negative flexibility plots
        if dat1['Neg_E'][x] < 0:
            neg_leg = 1
            theta = cum_data.iloc[x, 0]
            slots = int(round(ntsteps * dat1['Neg_E'][x] / dat1['Neg_P'][x]))
            slots_lim = slots
            if x + slots >= nsteps:
                slots_lim = nsteps-x-1
            slot_flex = dat1['Neg_E'][x] / slots
            for y in range(1, slots_lim + 1):
                p2 = plt_cum.plot([ts[x + y - 1], ts[x + y]], [theta, cum_data.iloc[x + y, 0] + (slot_flex * y)],
                                  color='tab:blue')
                theta = cum_data.iloc[x + y, 0] + (slot_flex * y)
        p4 = plt_pow.bar(ts[x], dat1['Neg_P'][x], color='tab:blue', width=1.0, align='edge', edgecolor='k', zorder=3)
        p6 = plt_prc.bar(ts[x], dat1['Neg_Pr'][x], color='tab:blue', width=1.0, align='edge', edgecolor='k', zorder=3)

        # Positive flexibility plots
        if dat1['Pos_E'][x] > 0:
            pos_leg = 1
            theta = cum_data.iloc[x, 0]
            slots = int(round(ntsteps * dat1['Pos_E'][x] / dat1['Pos_P'][x]))
            slots_lim = slots
            if x + slots >= nsteps:
                slots_lim = nsteps-x-1
            slot_flex = dat1['Pos_E'][x] / slots
            for y in range(1, slots_lim + 1):
                p3 = plt_cum.plot([ts[x + y - 1], ts[x + y]], [theta, cum_data.iloc[x + y, 0] + (slot_flex * y)],
                                  color='darkred')
                theta = cum_data.iloc[x + y, 0] + (slot_flex * y)
            p5 = plt_pow.bar(ts[x], dat1['Pos_P'][x], color='darkred', width=1.0, align='edge', edgecolor='k', zorder=3)
            p7 = plt_prc.bar(ts[x], dat1['Pos_Pr'][x], color='darkred', width=1.0, align='edge', edgecolor='k', zorder=3)

    # Legend
    if neg_leg == 1 and pos_leg == 1:
        plt_cum.legend((p1[0], p2[0], p3[0]), ('Cummulative', 'Neg_flex', 'Pos_flex'),
                       prop={'size': font_size}, bbox_to_anchor=(1.01, 0), loc="lower left", frameon=False)
        plt_pow.legend((p4, p5), ('$P_{Neg\_flex}}$', '$P_{Pos\_flex}}$'),
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left", frameon=False)
        plt_prc.legend((p6, p7), ('$C_{Neg\_flex}}$', '$C_{Pos\_flex}}$'),
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left", frameon=False)
    elif neg_leg == 1:
        plt_cum.legend((p1[0], p2[0]), ('Cummulative', 'Neg_flex'),
                       prop={'size': font_size}, bbox_to_anchor=(1.01, 0), loc="lower left", frameon=False)
        plt_pow.legend(p4, ['$P_{Neg\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left", frameon=False)
        plt_prc.legend(p6, ['$C_{Neg\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left", frameon=False)
    elif pos_leg == 1:
        plt_cum.legend((p1[0], p3[0]), ('Cummulative', 'Pos_flex'),
                       prop={'size': font_size}, bbox_to_anchor=(1.01, 0), loc="lower left", frameon=False)
        plt_pow.legend((p5), ['$P_{Pos\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left", frameon=False)
        plt_prc.legend((p7), ['$C_{Pos\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left", frameon=False)
    else:
        plt_cum.legend(['Cummulative'], prop={'size': font_size+2}, frameon=False)

    # Labels            
    plt_cum.set_title('Flexibility plots' + ' - ' + device.upper(), fontsize=font_size, pad=20)
    plt_cum.set_ylabel('$CE\ [kWh]$', fontsize=font_size+2)
    plt_cum.tick_params(axis="x", labelsize=font_size, labelbottom=False, pad=20)
    plt_cum.tick_params(axis="y", labelsize=font_size)
    plt_cum.grid(color='lightgrey', linewidth=0.75)
    plt_pow.set_ylabel('$Power\ [kW]$', fontsize=font_size+2)
    plt_pow.tick_params(axis="x", labelsize=font_size, labelbottom=False)
    plt_pow.tick_params(axis="y", labelsize=font_size)
    plt_pow.grid(color='lightgrey', linewidth=0.75, zorder=0)
    # plt_prc.set_xlabel('Time', fontsize=font_size, labelpad=3)
    plt_prc.set_ylabel('$Price\ [€/kWh]$', fontsize=font_size+2)
    plt_prc.tick_params(axis="x", labelsize=font_size, pad=5)
    plt_prc.tick_params(axis="y", labelsize=font_size)
    plt_prc.grid(color='lightgrey', linewidth=0.75, zorder=0)
    fig.align_labels()

    # limits
    lim_a = abs(1.5 * dat1['Neg_P'].min())
    lim_b = abs(1.5 * dat1['Pos_P'].max())
    lim_ends = max(lim_a, lim_b)
    if lim_ends != 0:
        plt_pow.set_ylim(-lim_ends, lim_ends)
    lim_a = abs(1.5 * dat1['Neg_Pr'].min())
    lim_b = abs(1.5 * dat1['Pos_Pr'].max())
    lim_ends = max(lim_a, lim_b)
    if lim_ends != 0:
        plt_prc.set_ylim(-lim_ends, lim_ends)
    #    plt_prc.set_xlim(0, nsteps+1)

    # Horizontal line - bar plot
    plt_pow.axhline(y=0, linewidth=2, color='k')
    plt_prc.axhline(y=0, linewidth=2, color='k')

    # Change xtick intervals    
    req_ticks = 12   # ticks needed
    if nsteps > req_ticks:
        plt_prc.set_xticks(plt_prc.get_xticks()[::int(round(nsteps/req_ticks))])
        plt_prc.set_xticklabels(ts_hr[::int(round(nsteps/req_ticks))])
    else:
        plt_prc.set_xticks(plt_prc.get_xticks())
        plt_prc.set_xticklabels(ts_hr)        

    # Get Y limits
    ymin, ymax = plt_prc.get_ylim()
    ylim = max(abs(ymin), abs(ymax))

    # Get dates
    date_index, N_dates = find_date_index(ts_date, N)
    for i in np.arange(N_dates):
        if device!='pv': plt_prc.text(date_index[i], -ylim*1.5, ts_date[int(date_index[i])], size=font_size-2)
        else: plt_prc.text(date_index[i], -0.03, ts_date[int(date_index[i])], size=font_size-2)

    # Settings
    plt.rc('font', family='serif')
    plt.margins(x=0)
    plt.show()
    return 

# Get text from dates
def find_date_index(date_series, N):
    date_list = date_series.values.tolist()
    date_list_offset = iter(date_list[1:])
    date_change_index = [i for i, j in enumerate(date_list[:-1], 1) if j != next(date_list_offset)]
    date_change_index_total = [0] + date_change_index + [N-1]
    _N_index = len(date_change_index_total) - 1
    _date_index = np.zeros(_N_index)
    for _i in np.arange(_N_index):
        _date_index[_i] = (date_change_index_total[_i] + date_change_index_total[_i+1]) / 2
    return _date_index, _N_index

