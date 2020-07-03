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

As of July 1, 2020, in our African region of interest there are `1,589,247` scenes in the Sinergise listing and `1,452,822` in
the Element84 listing.

There are `125` scenes in the Element 84 list that are not in the Sinergise list.
This due to some scenes that cover the 0 and 60 UTM zones slipping in to the list due to issues relating
to the antimeridian and reprojection to WGS84.

There are `136,838` scenes in the Sinergise list that are not in the Element 84 list. Reason for these missing
scenes are explored below. Of these, `56,240` have known reasons for not being in the Element 84 listing as follows:

* `5,663` have no `tileDataGeometry` field.
* `31,242` have `0.0` values for cloud in both level-2 and level-1 metadata
* `20,777` have `0.0` values for cloud in level-2 and have no level-1 metadata.

This leaves ~`80,000` scenes that don't have a clear reason for not being included.


### Known issues

Scenes with known issues are listed in the file [data/sinergise-qa-output.json](data/sinergise-qa-output.json).

#### 5 example scenes with no tileDataGeometry

These are scenes that are missing the field `tileDataGeometry` in the `tileInfo.json` document.

* `tiles/39/P/WL/2017/10/29/0` - 5% valid data. Scene looks fine.
* `tiles/39/P/WN/2019/11/18/0` - 5% valid data. Nearly all cloud.
* `tiles/34/R/ER/2019/7/5/0`   - 20% valid data. Scene looks fine.
* `tiles/34/S/BA/2019/6/13/1`  - 40% valid data. Over water, scene looks fine.
* `tiles/40/M/BV/2019/5/30/0`  - 5% valid data. Scene looks fine.

These scenes tend to have a lot of water or other less-valuable data in them. Still, they
can be included by failing over to `tileGeometry` when `tileDataGeometry` isn't present.

#### 5 example scenes with zeros in cloud cover

These are scenes that have `0.0` in cloud cover in both level-2 and level-1 `tileInfo.json` documents.

* `tiles/40/M/DU/2019/2/9/0`  - 5% valid data. Scene is over water. No cloud!
* `tiles/33/N/YG/2019/4/3/0`  - 40% valid data. No visible cloud. Some thin cloud in SCL.
* `tiles/33/P/WK/2017/12/5/1` - 50% valid data. No visible cloud.
* `tiles/35/Q/KF/2018/9/12/0` - 100% valid data. No visible cloud.
* `tiles/32/N/MN/2020/1/20/0` - 100% valid data. No visible cloud. Some thin cloud in SCL.

Almost all sampled scenes have valuable data, and usually heaps of it. It's very important to include these.

#### Example scenes with both no tileDataGeometry and zero cloud cover

These have both the cases above. I examined two just to see what's going on.

* `tiles/32/N/NG/2020/6/23/0` - Tiny little sliver of valid data.
* `tiles/32/P/MU/2020/6/8/0`  - 40% valid data, no cloud.

#### Scenes with no level-1 equivalent on the Sinergise API

A number of scenes have `0.0` in the metadata in the `tileInfo.json` document and do not
have a matching document in the level-1 archive on Sinergise's side. These were not
examined.

### Other QA scenes (todo)

Those listed in [data/sinergise-qa-todo.json](data/sinergise-qa-todo.json). 

#### No georeferencing information

Some scenes, such as `tiles/27/R/ZJ/2017/8/29/0`, do not have georeferencing information
in the JP2000 files. These were not listed out due to the requirement to retrieve
that information over the network.

#### Other scenes with no clear QA

These are scenes that are not in the Element84 inventory but that are in the Sinergise inventory
and the reasons for their exclusion are unknown.

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
