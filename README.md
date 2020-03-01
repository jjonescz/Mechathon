# Mechathon

This repository contains source code of Sprinteři27's robot for [Mechathon
2020](https://www.mechathon.cz/).

## Installation

```cmd
py -3 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Authors

- [Jan Joneš](https://github.com/jjonescz)
- [Jana Řežábková](https://github.com/janarez)
- [Martin Vejbora](https://github.com/vejbomar)
- [Adéla Čekalová](https://github.com/cekalovaadela)

## Third-party libraries

To avoid connecting our EV3 brick to the Internet and installing 3rd party
libraries from there, we include library
[simple_pid](https://pypi.org/project/simple-pid/) directly in the source code.
