# reverse video search

RVSearch is a tool to do a reverse video search on YouTube.

The comparison is done using pHash and Linear search algorithm, 
thus it is fast and precise to find **exact** similar frames between any videos,
 but not smart enough to find **some what** similar frames when the video is distorted, swinged, transitioned and overall,
 changed, enough
 to escape YouTube own copyright detection algorithm.

Finding similarity between **distorted** and **changed** images can be done using basic object detection algorithms, but when importing them
to compare videos it will be unbearably slow. 

Requirements
------------
- Python 3 or greater

For other missing packages first you need to install them using `pip`:
```
python3 pip install pandas youtube_dl opencv-python numpy setuptools scikit-video PyQt5 Pillow pip pytz scipy python-dateutil six
```

Installation:
------------
```
python3 pip install rvsearch
```


Usage:
------
You can work directly with RVSearch's command line interface:
```
rvsearch input.csv
```

Input:
-----

For input you only need to provide the URLs for source and target videos in
 a `.csv` format file, under columns `Compilation` and `Source`.

For example:

```bash
i |         Compilation        |          Source          |
----------------------------------------------------------
0 |  https://you.tube/video    |   https://you.tube/video |
----------------------------------------------------------
1 |                            |   https://you.tube/video |
----------------------------------------------------------
2 |                            |   https://you.tube/video |
```
**Note**: Only **ONE** compilation per file is supported for now.

If you want to give multiple inputs, you can.

for example:

```
rvsearch input1.csv input2.csv input3.csv
```
But note that output file name will be redundant. If you want to manually specify the output file's name, see Advance Usage.

Output:
------

The output will be saved as a `.csv` file on current working directory. To see where a similarity
 between two videos happened, checkout the timestamp of both videos.

Below you can see an example of output format:

```
|    Cmpl_url   |  Cmp_name | Cmp_chnl |   Source_url  | Source_name | Source_chnl | Cmp_TimeStamp | Source_TimeStamp |
-----------------------------------------------------------------------------------------------------------------------
|  https://...  |    Name   |   Name   |  https://...  |    Name     |    Name     |     12:34     |      1:23        |
```
- `Cmpl_url`: Web URL for the compilation video
- `Cmp_name`: Title of the compilation video
- `Cmp_chnl`: Channel name (uploader) of the compilation video
- `Source_url`: Web URL for the Source video
- `Source_name`: Title of the Source video
- `Source_chnl`: Channel name (uploader) of the Source video
- `Cmp_TimeStamp`: The timestamp on compilation video where similarity found
- `Source_TimeStamp`: The timestamp on source video where similarity found

Advance Usage:
-------------
| Argument | Explanation |
| -------- | ----------- |
| ```-h``` | Displays help message listing all command-line arguments |
| ```-q``` | Be quiet. Doesn't show anything about what you do|
| ```-v``` | Be verbose. Output everything, used mostly for debugging the program.|
| ```-o``` | Specifies the name for output file|

For example:
```
rvsearch input1.csv input2.csv -o results.csv -q
```

## License

Copyright (c) 2021 by [sadiqush](https://github.com/sadiqush). All rights reserved.<br>
[RVSearch](https://github.com/sadiqush/rvsearch) is licensed under the GLPv3 License as stated in the [LICENSE file](LICENSE).
