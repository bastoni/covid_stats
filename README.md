# Moving Average COVID-19 Data for Italian Province/Regioni

Computes the moving average for the new COVID cases (new cases `x` days/population * 100000) of Italian Province and Regioni using official ISTAT population data and PCM-DPC COVID-19 data.
For the regioni, also compute the moving average of the number of active cases (this number is not available on a provincia-basis).

Optionally compute moving average of the COVID cases over the area of a provincia.

By default, the average is computed on `x = 7` days

The moving average is based on uncertain data. Please read it as such.

## Usage

```
mavg.py --help
```

The program uses input data from [1], [2], and optionally [3]. Check the OFILE and IFILE dictionaries for the default locations of the input and output json/CSV files.

## Output

Two json files (one for the province, one for the regioni) reporting for each analyzed range:
- new cases `x` days/population * 100000
- Regioni only: active cases `x` days/population * 100000
- total cases / population * 100000
- total cases

e.g.,:
```
{
    "Abruzzo": {
        "avg_pop": {
            "2020-02-24T18:00:00 - 2020-03-01T17:00:00": [
                0.054722670431294536,
                0.09850080677633016,
                0.3830586930190618,
                5
            ],
```

For the province, if the `--area` option is specified, the number of cases `x` days/population * 100000 is also reported.

e.g.,:
```
    "AG": {
        "area": 3044.85,
        "avg_area": {
            "2020-02-24T18:00:00 - 2020-03-01T17:00:00": 0.0,
```

## Data Sources
- [1]: DEMO istat.it (November 2019 data) [ISTAT Italian Population](http://demo.istat.it/bilmens2019gen/index02.html). (Source data for the `tavola_bilancio_mensile_2019_*` files.)
- [2]: [COVID-19 Data](https://github.com/pcm-dpc/COVID-19/)
- [3]: Optional: area of Italian Province. The `load_area.py` module parses the input coming from [Area](https://github.com/MatteoHenryChinaski/Comuni-Italiani-2018-Sql-Json-excel.git)

## License
- [Apache-2.0](LICENSE) or [https://www.apache.org/licenses/LICENSE-2.0]
