OpenTUMflex
=======

An open-source python-based flexibility model to quantify and price the flexibility of household devices.

[![DOI](https://zenodo.org/badge/212816117.svg)](https://zenodo.org/badge/latestdoi/212816117) [![Documentation Status](https://readthedocs.org/projects/opentumflex/badge/?version=latest)](https://opentumflex.readthedocs.io/en/latest/?badge=latest)


## Description

The increasing share of renewable energy requires alternative methods to provide power system ancillary services to ensure a stable operation of the electricity grids. Recent research has inclined their interests towards the aggregation of small-scale system flexibility potentials to accommodate grid variations. The advancements towards local flexibility markets (LFMs) allow prosumers participation in solving grid congestion problems. In order to allow prosumers to interact with the LFMs and submit their bids, a flexibility model is required. This research proposes an open-source flexibility estimation model that quantifies all possible flexibilities from the available prosumer devices and prices them.

#### Flexibility
Within this open-source model, flexibility is defined as the deviation of a device operation from its optimal schedule. Flexibility can be both negative and positive. Negative flexibility refers to the delay of grid feed-in or the consumption of unscheduled energy. Positive flexibility is the delay of grid energy consumption or the unscheduled grid feed-in.  


## Features
OpenTUMFlex...
* uses mixed-integer linear programming (MILP) to obtain cost-optimal operational schedules for household devices. 
* calculates the flexibility potential and flexibility prices based on price, weather, generation and load forecasts of household devices.
* supports the following devices: PV, battery storage systems (BSS), electric vehicles (EV), heat pumps (HP), combined heat and power (CHP) units.
* outputs flexibility offers for each household device in formats that can be used in flexibility markets (e.g. comax by Tennet or ALF by FfE e.V.)


## Installation

### Clone repository
You can download or clone the repository to a local directory of your choice. You can use version control tools such as GitHub Desktop, Sourcetree, GitKraken or pure Git. The link for pure Git is: 

`git clone https://github.com/tum-ewk/OpenTUMFlex.git`

### Create an environment and install required packages
The easiest way to install an IDE, create a virtual environment and install all required packages via Anaconda. 
1. Install Anaconda or Miniconda.
2. Shift to the local directory: `cd "Path to OpenTUMFlex local directory"`
3. Configure an IDE.

### Configure an IDE
**Pycharm**:
1. Create the virtual environment: open "Anaconda Prompt" -> type `conda env create -f environment_v1.0.yml`
2. Activate the virtual environment:
	- In the command prompt type `conda activate OpenTUMFlex`
	- Go to `File->Settings->Project->Python Interpreter->Show all->Add->Conda Environment->Existing environment->Select folder->OK` 

**Spyder**:
Since Spyder at the moment doesn't support Python 3.9 which is originally used in our enviroment file, we have added an additional enviroment file to support Python 3.7 for Spyder IDE.
1. Create the virtual environment: open "Anaconda Prompt" -> type `conda env create -f environment_v1.0_py37.yml`
2. Activate the virtual environment :
	- In the command prompt type `conda activate OpenTUMFlex_py37`
	- A new Spyder IDE application will be installed and can be found in the start menu.  


### Test your installation
Run the [example.py](https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/example.py) file to test if the OpenTUMFlex model is correctly installed. If the installation was succesful, you will see the following results:

<p align="center">
<img src = "https://user-images.githubusercontent.com/40628466/98377223-d6e30800-2044-11eb-8348-8fe4eefb0b5d.png" width=600/>
</p>	
	
	
<p align="center">
<img src = "https://user-images.githubusercontent.com/40628466/98377226-d77b9e80-2044-11eb-8602-fd678da44c9f.png" width="400"/>
<img src = "https://user-images.githubusercontent.com/40628466/98377228-d8143500-2044-11eb-8cb9-83d0ef9d8a95.png" width="400"/>
</p>




## Getting started
A scenario-based approach is incorporated in the OpenTUMFlex design. Here, a scenario refers to the device configurations installed in a household. For example, a scenario can refer to just a household with PV, BSS and EV. 

* **Change your scenario**
   Once you have successfully installed OpenTUMFlex, you can choose to change your scenario by replacing the desired name in line 12 in [example.py](https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/example.py). To give an idea, we have already created 10 sample scenarios inside [scenario.py](https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/opentumflex/scenarios/scenarios.py). 
   
  *For example the following scenarios portray the devices installed at the prosumers premises*
   * `scenario_hp`: Heat storage, boiler and HP
   * `scenario_simple_house`: PV, BSS, heat storage and boiler
   * `scenario_apartment`: PV, BSS, heat storage, boiler, CHP, HP and EV
  
  *Change the arguments to enable/disable each plot:*
   * `show_opt_res`: plot the optimization results (energy balance and device SoCs)
   * `save_opt_res`: save the optimization results in a spreedsheet 
   * `show_flex_res`: plot the flexibility results of all available devices individually (power, energy and price)
   * `show_aggregated_flex`: plot the cumulative flexibility power and price of all the available devices

* **Create your own scenario:** 
   * Refer our [documentation](https://github.com/tum-ewk/OpenTUMFlex/wiki/Create-your-scenario).
   
* **Analysis Toolbox:**
   * [EV Case Study - Quantifying the Flexibility of Electric Vehicles](analysis/)


<!---
## Conflict of Interest: 

The authors declare no conflict of interest. All authors have equally contributed to the development of this software. 
--->

## References

<sub>[Zade, M., You, Z., Kumaran Nalini, B., Tzscheutschler, P., & Wagner, U. (2020). Quantifying the Flexibility of Electric Vehicles in Germany and California—A Case Study. Energies, 13(21), 5617. doi:10.3390/en13215617](https://www.mdpi.com/1996-1073/13/21/5617)

<sub>[Z. You, B. K. Nalini, M. Zade, P. Tzscheutschler and U. Wagner, "Flexibility quantification and pricing of household heat pump and combined heat and power unit," 2019 IEEE PES Innovative Smart Grid Technologies Europe (ISGT-Europe), Bucharest, Romania, 2019, pp. 1-5, doi: 10.1109/ISGTEurope.2019.8905594.](http://dx.doi.org/10.1109/isgteurope.2019.8905594)<sub>

<sub>[B. K. Nalini, M. Eldakadosi, Z. You, M. Zade, P. Tzscheutschler and U. Wagner, "Towards Prosumer Flexibility Markets: A Photovoltaic and Battery Storage Model," 2019 IEEE PES Innovative Smart Grid Technologies Europe (ISGT-Europe), Bucharest, Romania, 2019, pp. 1-5, doi: 10.1109/ISGTEurope.2019.8905622.](http://dx.doi.org/10.1109/isgteurope.2019.8905622)<sub>

<sub>[M. Zade, Y. Incedag, W. El-Baz, P. Tzscheutschler and U. Wagner, "Prosumer Integration in Flexibility Markets: A Bid Development and Pricing Model," 2018 2nd IEEE Conference on Energy Internet and Energy System Integration (EI2), Beijing, 2018, pp. 1-9, doi: 10.1109/EI2.2018.8582022.](http://dx.doi.org/10.1109/EI2.2018.8582022)<sub>


## License

OpenTUMFlex can be used to optimize and calculate a household flexibility potential and price it. 
Copyright (C) 2020 TUM-EWK 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
