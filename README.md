# WherePy

[![Build Status](https://travis-ci.org/dzhoshkun/wherepy.svg?branch=master)](https://travis-ci.org/dzhoshkun/wherepy)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/dzhoshkun/wherepy/blob/master/LICENSE)

Sample application to demonstrate real-time tool tracking.

## Getting Started

### Requirements

* [Python 2.7][python-27]
* [ndicapi Python interface][ndicapi-py]
* [PyYAML][pyyaml]

[python-27]: https://www.python.org/
[ndicapi-py]: https://github.com/PlusToolkit/ndicapi#python
[pyyaml]: https://github.com/yaml/pyyaml

### Installation

`pip install git+git://github.com/dzhoshkun/wherepy`

### Usage

#### Supported tracking systems

Currently [NDI Aurora][ndi-aurora] only.

[ndi-aurora]: https://www.ndigital.com/medical/products/aurora/

#### Tracking quality indicator

Run: `wherepy-indicator-cli`.
This will display a live tracking quality indicator like the following samples:

* Device connected, signal quality 54 %, tracking error 1.54 mm, and an info message:

```
|  Device  |       Signal      |   Error   |           Info           |
-----------------------------------------------------------------------
    LIVE     [====>     ] 54 %    1.54 mm        info message here
```

* Device connected, but low-quality signal, no tracking error reported:

```
|  Device  |       Signal      |   Error   |           Info           |
-----------------------------------------------------------------------
    LIVE     [          ]  0 %       ~
```

* Device not connected, tracking error not applicable:

```
|  Device  |       Signal      |   Error   |           Info           |
-----------------------------------------------------------------------
  OFFLINE    [          ]  0 %       NA
```

Running `wherepy-indicator-cli` with the `--pretty` option displays a nicer output, but may not be supported on all 
platforms.

#### Tracking data collection

Run `wherepy-collector-cli --help` to see the tracking data collection options.
For instance `wherepy-collector-cli --num-poses 5 --output-file tool-poses.yml` to capture the tracking tool's 
poses at 5 points in time into the file `tool-poses.yml`.

## Licensing and Copyright

Copyright 2018 WherePy contributors.
WherePy is released under the Apache License, Version 2.0.
Please see the LICENSE file for details.
