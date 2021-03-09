-------------------------------------------------------------
# pc_status
Displays information and your computer status

Fernando Mendiburu - 2021
-------------------------------------------------------------

# Table of Contents

- [Foundations](#Foundations)
- [Installation](#installation)
- [Dependences](#Dependences)
- [Cron](#Cron)
- [Alias](#Alias)
- [User Guide](#User-Guide)
- [TODO](#TODO)



## Foundations

If you have a outdated hardware, or you love living dangerously, like this:

```
Memory: 90.7% (swap: 23.1%)
CPU: 81.6%, Core0: 82.3%, Core1: 84.3%
CPU: 93.0º, Core0: 87.0º, Core1: 86.0º
Battery percentage: 2.19%
```

<p align="center">
  <img src=".//gif/explosion.gif" alt="Size Limit CLI" width="200">
</p>


Yes, clearly your PC is living on the edge!

Using `pc_status.py`, you will live dangerously, but with safety XD

You can monitor variables and information from your CPU, memories, like usage, temperature, among others.

There are some notifications implemented, when reaching certain values of temperature, memory and CPU usage, and battery discharging.

## Installation

Download from [here](https://github.com/fermendi/pc_status/archive/main.zip) or using git clone:

```
$ git clone https://github.com/fermendi/pc_status.git
```

Install Python 3.6.9 (Jan 26 2021) or later (In Linux is already installed in /usr/bin/python3 or /usr/bin/python3.6).


## Dependences

#### psutil

Module to retrieving information on running processes. More information [here](https://pypi.org/project/psutil/).

```
$ pip install psutil
```

#### notify-py

Module for sending native cross-platform notifications. More information [here](https://pypi.org/project/notify-py/).

```
pip install notify-py
```

## Cron

(Optional) If you want to schedule this program to be executed automatically, you can use Cron. Information can be found [here](https://www.adminschoice.com/crontab-quick-reference). 

Open the file (or create one) to store the cron jobs (preferibly use nano):

```
$ crontab -e
```

and copy the folowing line on the file:

```
0-59 * * * * /bin/sh -c '~/pc_status/config/pc_status.sh' > /dev/null 2>&1
```

This line will execute the program each 1 minute.


## Alias

(Optional) To execute this program easily, create an alias:

```
$ sudo nano ~/.bashrc
```

Copy this line at the end of this file:

```
alias pc_status='~/bash_files/sh/pc_status.sh'
```

Save the changes (`ctrl+x`, `y` and `enter`).

So, next time you can open the program simply typing 'pc_status':

```
$ pc_status 
```

## User Guide

The command to execute the program has the following form:

```
$ pc_status.py --info INFO --loop LOOP --notifications NOTIF --sound SOUND
```

or:

```
$ pc_status --info INFO --loop LOOP --notifications NOTIF --sound SOUND
```

If you did the above 'alias' step.

`INFO`: can be {full,status}, it displays almost all the information available from your PC (full) or only the status: it displays a summarize version of the usage of CPU, memories, temperature and battery status (battery status if you have a notebook).

`LOOP`: can be {y,n}, if 'y', it repeats the measures.

`NOTIF`: can be {y,n}, pop-up all the notifications if measures are above the threshold.

`SOUND`: can be {y,n}, if notifications are enabled, they will warn you.

There are other constants to set in the file 'config.txt':

`PATH_NOTIF_ICON`: path to the icon that appears in the notification.

`PATH_NOTIF_SOUND`: path to the sound of notification.

`HIGH_USAGE_CPU`: CPU percentage (0-100%) that triggers the notification of high CPU usage.

`HIGH_USAGE_MEM`: Memory percentage (0-100%) that triggers the notification of high memory usage.

`DISCHARGING_BATTERY`: Battery percentage (0-100%) that triggers the notification of battery discharging.


Setting the `NOTIF` parameter to 'yes' you allow/ deny ALL the notifications (CPU, memory and battery), but you can desactivate / activate in isolation:

`NOTIFICATION_BATTERY`: Ativate (yes) or deactivate (no) the battery notification.

`NOTIFICATION_MEMORY`: Ativate (yes) or deactivate (no) the high memory usage notification.

`NOTIFICATION_CPU`: Ativate (yes) or deactivate (no) the high CPU usage notification.

`NOTIFICATION_TEMPERATURE`: Ativate (yes) or deactivate (no) the high temperature notification.

## TODO

Using this base program it is possible to add some functionalities to avoid overheating, hanging and/or freezing. For example, achieving a certain threshold we can close stuff to save memory, rebooting our system, etc.


