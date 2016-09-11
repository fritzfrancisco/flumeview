# FlumeView
Application for analysing and tracking fish in classical fluming tests.

FlumeView is divided up into a command line interface (cli) which manages the external commands, the analyser which analyses the tracking data and the stats file which manages all calculations.

|Argument       | Use           |Default |
|:-------------: |:-------------| :-----|
|- a | minimum area size of tracked blob|100 |
|- c |definition of center by clicking on first frame displayed in window | False|
|- r | refresh every n frames|1 |
| - s| show frame| False|
|- t |define timelimit | sys.maxint|
| - w |seconds waited,before initiation |1 |
| - x |relative x coordinate of center|0.5 |
| - y |relative y coordinate of center| 0.5|

## Example:

```bash
python2 FlumeView_cli.py -v D.rerio_test_wf1.dvd -s True -c True -r 100
```
## Information:

The software is created to facilitate laboratory use and ease the evaluation of video material, especially in combination with preference flumes.

This software should be used critically and when quoted in publications or similar form the author should be explicitly mentioned. If this helps, you have comments about the software or you have further requests please feel free to email me.
