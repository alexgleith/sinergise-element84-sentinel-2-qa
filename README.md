# Workspace for comparing differences between Sinergise and Element 84 Sentinel-2 buckets for DE Africa

## Enviroment notes

* Sinergise bucket: `sentinel-s2-l2a`
* Sinergise inventory bucket: `sentinel-inventory`
* Element 84 bucket: `sentinel-cogs`
* Element 84 inventory bucket: `sentinel-cogs-inventory`

## Process steps

1. Run the [0-parse-inventory-sinergise.py](0-parse-inventory-sinergise.py) and [0-parse-inventory-element84.py](0-parse-inventory-element84.py)
scripts, which will dump out inventories from the Sinergise and Element 84 buckets.
2. Use the notebook [1-sinergise-element84-differences.ipynb](1-sinergise-element84-differences.ipynb) to load the inventories and run
a quick comparison of the two lists. This will result in [data/sinergise-only.txt](data/sinergise-only.txt) and
[data/element84-only.txt](data/element84-only.txt) files. (The E84 one should only have the UTM 0 and 60 zoned scenes
that _are_ in the Sinergise bucket, but which I'm not listing.)
3. The notebook [2-do-qa-inventories.ipynb](2-do-qa-inventories.ipynb) will check for known flaws and check metadata
and such from the Sinergise API. The result is [data/sinergise-qa-output.json](data/sinergise-qa-output.json) and
[data/sinergise-qa-todo.json](data/sinergise-qa-todo.json).

## Brief QA Findings

### 5 scenes with no tileDataGeometry

* `tiles/39/P/WL/2017/10/29/0` - 5% valid data. Scene looks fine.
* `tiles/39/P/WN/2019/11/18/0` - 5% valid data. Nearly all cloud.
* `tiles/34/R/ER/2019/7/5/0`   - 20% valid data. Scene looks fine.
* `tiles/34/S/BA/2019/6/13/1`  - 40% valid data. Over water, scene looks fine.
* `tiles/40/M/BV/2019/5/30/0`  - 5% valid data. Scene looks fine.

These scenes tend to have a lot of water or other less-valuable data in them. Still, they
can be included by failing over to `tileGeometry` when `tileDataGeometry` isn't present.

### 5 scenes with zeros in cloud cover

* `tiles/40/M/DU/2019/2/9/0`  - 5% valid data. Scene is over water. No cloud!
* `tiles/33/N/YG/2019/4/3/0`  - 40% valid data. No visible cloud. Some thin cloud in SCL.
* `tiles/33/P/WK/2017/12/5/1` - 50% valid data. No visible cloud.
* `tiles/35/Q/KF/2018/9/12/0` - 100% valid data. No visible cloud.
* `tiles/32/N/MN/2020/1/20/0` - 100% valid data. No visible cloud. Some thin cloud in SCL.

Almost all sampled scenes have valuable data, and usually heaps of it. It's very important to include these.

### Scenes with bothe no tileDataGeometry and zero cloud cover

* `tiles/32/N/NG/2020/6/23/0` - Tiny little sliver of valid data.
* `tiles/32/P/MU/2020/6/8/0`  - 40% valid data, no cloud.

### Other QA scenes

* `tiles/36/G/XP/2017/10/21/0` - Over water, some cloud and 5% valid data.
* `tiles/30/Q/WM/2019/3/19/0`  - Scene looks totally fine. Clear, full, georeferenced, in the middle of Africa.
* `tiles/33/Q/TV/2018/10/19/0` - Scene looks fine. 90% valid data.
* `tiles/32/N/QH/2018/3/15/0`  - Mostly cloud, 20% valid data.
* `tiles/38/P/QV/2019/7/9/0`   - Almost all water, some cloud.
* `tiles/35/R/LP/2018/12/31/0` - Scene looks fine, 50% valid data.
* `tiles/27/R/ZJ/2017/8/29/0`  - This scene has no georeferencing.
* `tiles/36/G/XN/2019/4/14/0`  - Scene is around 1% data and all cloud.

While some of these scenes have invalid spatial extents, most of them do not. It's unclear why they are not included
and they should be.
