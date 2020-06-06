# Moving Average COVID-19 Data for Italian Province/Regioni

Computes the moving average for the COVID cases (cases `x` days/population * 100000) of Italian Province and Regioni using official ISTAT population data and PCM-DPC COVID-19 data.

Optionally compute moving average of the COVID cases over the area of a provincia.

By default, the average is computed on `x = 7` days

The moving average is based on uncertain data. Please read it as such.

## Usage

```
mavg.py --help
```

The program uses input data from [1], [2], and optionally [3]. Check the OFILE and IFILE dictionaries for the default locations of the input and output json/CSV files.

## Data Sources
- [1]: DEMO istat.it (November 2019 data) [ISTAT Italian Population](http://demo.istat.it/bilmens2019gen/index02.html)
- [2]: [COVID-19 Data](https://github.com/pcm-dpc/COVID-19/)
- [3]: Optional: area of Italian Province. The `load_area.py` module parses the input coming from [Area](https://github.com/MatteoHenryChinaski/Comuni-Italiani-2018-Sql-Json-excel.git)

## License
- [Apache-2.0](LICENSE) or [https://www.apache.org/licenses/LICENSE-2.0]
