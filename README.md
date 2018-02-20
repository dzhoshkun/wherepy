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
| Device [✓] | Signal [====>     ] 54 % | Error  1.54 mm  | info message here.       |
```

* Device connected, but low-quality signal, no tracking error reported:

```
| Device [✓] | Signal [          ]  0 % | Error     ~     |
```

* Device not connected, tracking error not applicable:

```
| Device [✗] | Signal [          ]  0 % | Error    NA     |
```

#### Tracking data acquisition

Under construction.

## Licensing and Copyright

Copyright 2018 WherePy contributors.
WherePy is released under the Apache License, Version 2.0.
Please see the LICENSE file for details.
