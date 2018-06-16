# worldcup
[![Build Status](https://travis-ci.org/tadeoos/worldcup.svg?branch=master)](https://travis-ci.org/tadeoos/worldcup)

A simple CLI to stay up to date with 2018 World Cup

## demo

```
$ worldcup/worldcup.py next
Match #5: 🇫🇷  France vs Australia 🇦🇺
When: Saturday, 16. June 2018 12:00PM
Where: Kazan

$ worldcup/worldcup.py groups a
GROUP A                    MP GF GA PTS
---------------------------------------
Russia                      1  5  0  3
Uruguay                     1  1  0  3
Egypt                       1  0  1  0
Saudi Arabia                1  0  5  0

$ worldcup/worldcup.py --help
Usage: worldcup.py [OPTIONS] COMMAND [ARGS]...

  CLI tool for being up to date with 2018 World Cup

Options:
  --help  Show this message and exit.

Commands:
  groups  Show group info
  next    Show nearest match info
```

## developement

## acknowledgments

World Cup data available thanks to json file from [lsv fifa-worldcup-2018](https://github.com/lsv/fifa-worldcup-2018)

Inspired by: [SkullCarverCoder](https://github.com/SkullCarverCoder/wc18-cli)
