# FlumeView
Application for analysing and tracking fish in classical choice fluming tests.

![alt text](http://www.pnas.org/content/suppl/2007/01/02/0606777104.DC1/06777Fig3.jpg "Gerlach et al. 10.1073/pnas.0606777104.")

Image 1.: Choice flume with channel (2 -3) and area (3-4) positions (A & B) and arrows showing the flow orientation (Gerlach et al. 10.1073/pnas.0606777104.; <http://www.pnas.org/content/104/3/858/suppl/DC1>)

The flume is set up in four compartments between which the fish can freely move and choose. Each channel can be filled with different odors or stimulants.

FlumeView is divided up into a command line interface which manages the external commands, the analyser which analyses the tracking data and the stats file which manages all calculations.

|Argument       | Use           |Default |
|:-------------: |:-------------| :-----|
|-a | minimum area size of tracked blob|100 |
|-c |definition of center of four test chambers by clicking on first frame displayed in a separate window | False|
|-p| print data to file| on|
|-r | refresh plot every n frames|1 |
| -s| show frame| False|
|-t |define timelimit | sys.maxint|
|-v|define videofile path for capture|default camera|
| -w |seconds waited,before initiating tracking |1 |
| -x |relative x coordinate of center point|0.5 |
| -y |relative y coordinate of center point| 0.5|


## Commandline Example:

```bash
python2 FlumeView_cli.py -v D.rerio_test_wf1.dvd -s True -c True -r 100
```

## Data Output

The data is emitted as ```.csv ``` file in the folder in which the  ```FlumeView_cli.py ``` file is located in the following format:

|File|Total Time [s]|Channel_A [s]|Channel_B [s]|Area_A [s]|Area_B [s]|
|:---|:---|:---|:---|:---|:---|
|D.rerio_test_wf1.dvd|22.17|0.00|11.38|0.10|10.71|
|D.rerio_test_wf1.dvd|22.17|0.00|11.31|0.10|10.78|


## Information:

The software is created to facilitate laboratory use and ease the evaluation of video material, especially in combination with preference flumes.

This software should be used critically and when quoted in publications or similar form the author should be explicitly mentioned. If this helps, you have comments about the software or you have further requests please feel free to email me.
