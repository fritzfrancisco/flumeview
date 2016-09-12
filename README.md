# FlumeView
Application for analysing and tracking fish in classical choice fluming tests.

![alt text](http://www.pnas.org/content/suppl/2007/01/02/0606777104.DC1/06777Fig3.jpg "Gerlach et al. 10.1073/pnas.0606777104.")

Image 1.: Choice flume with channel (2 -3) and area (3-4) positions (A & B) and arrows showing the flow orientation (Gerlach et al. 10.1073/pnas.0606777104.; <http://www.pnas.org/content/104/3/858/suppl/DC1>)

The flume is set up in four compartments between which the fish can freely move and choose. Each channel can be filled with different odors or stimulants.

<img src="https://github.com/fritzfrancisco/flumeview/blob/master/screenshot_live.png " width="400">

Image 2.: Screenshot: Live View

<img src="https://github.com/fritzfrancisco/flumeview/blob/master/screenshot_plot.png " width="400">

Image 3.: Screenshot: Plot

FlumeView is divided up into a command line interface which manages the external commands, the analyser which analyses the tracking data and the stats file which manages all calculations.

|Argument       | Use           |Default |
|:-------------: |:-------------| :-----|
|-a | minimum area size of tracked blob|100 |
|-c |definition of center of four test chambers by clicking on first frame displayed in a separate window | False|
|-d|save frame number, x- and y-coordinates to given file |no default|
|-i|save live view tracking image to given file|no default|
|-p| save combined data to given file| no default|
|-r | refresh plot every n frames|1 |
| -s| show frame| False|
|-t |define timelimit | sys.maxint|
|-v|define videofile path for capture|default camera|
| -w |seconds waited,before initiating tracking |1 |
| -x |relative x coordinate of center point|0.5 |
| -y |relative y coordinate of center point| 0.5|


## Commandline Example:

```bash
python2 FlumeView_cli.py -v D.rerio_test_wf1.dvd -s True -c True -r 100 -w 5 -t 10 -d D_test_data
```

## Data Input
The library used in this application is based on the open source project OpenCv  (<http://opencv.org/>) which is a powerful video and image computation platform. Therefore, FlumeView directly supports most common video extensions.


## Data Output

When saving data to a file the expressions ```-d``` ,```-p``` or ```-i``` can be utilized.

* ```-d```: dump

File name, frame count, and (relative) fish x- and y-coordinates for each frame are stored as row in a single ```.csv ``` file with the given name. However, the file is overwritten if the exact file already exists. This can be changed by exchanging the ```'w'``` for an ```'a'``` (append) in ```with open(args["dump"],'w') as csvfile:``` of the ```FlumeView_cli.py``` script. However, additional changes may be needed to ensure that the file is recognized if already present.

The data when using the ```-d``` command is emitted as ```.csv ``` file in the folder in which the  ```FlumeView_cli.py ``` file is located, and stored in the following format:

|File|x_Coord|Y_Coord|Frame_number|
|:---|:---|:---|:---|
|D.rerio_test_wf1.dvd|0.61|0.6636636636636637|90|
|D.rerio_test_wf1.dvd|0.61|0.6606606606606606|91|
|D.rerio_test_wf1.dvd|0.612|0.6636636636636637|92|
|D.rerio_test_wf1.dvd|0.612|0.6636636636636637|93|
|D.rerio_test_wf1.dvd|0.612|0.6636636636636637|94|

* ```-i``` : image

The ```FlumeView - Live``` output, with marking is saved to a image file after tracking is completed. The file extension can freely be chosen between ```.jpg```,```.jpeg```,```.png``` and ```.tiff``` and should be added as file name extension. Files with the same name and extension within the folder in which the  ```FlumeView_cli.py ``` file is located are overwritten.

* ```-p``` : print

File name, total time, channel A, channel B, area A and area B is saved to the given file as ```.csv ``` row after tracking is complete. If the given file name already exists, the new data is appended to this file as new row as well and the file is not replaced. This can be altered by exchanging the ```'a'``` for ```'w'``` in ```with open(args["print"],'a') as csvfile:``` of the ```FlumeView_cli.py``` script. However, additional changes may be needed to ensure that the file is recognized if already present.

The data when using the ```-p``` command is emitted as ```.csv ``` file in the folder in which the  ```FlumeView_cli.py ``` file is located in the following format:

|File|Total Time [s]|Channel_A [s]|Channel_B [s]|Area_A [s]|Area_B [s]|
|:---|:---|:---|:---|:---|:---|
|D.rerio_test_wf1.dvd|22.17|0.00|11.38|0.10|10.71|
|D.rerio_test_wf1.dvd|22.17|0.00|11.31|0.10|10.78|


## Information:

The software is created to facilitate laboratory use and ease the evaluation of video material, especially in combination with preference flumes.

This software should be used critically and when quoted in publications or similar form the author should be explicitly mentioned. If this helps, you have comments about the software or you have further requests please feel free to email me.
