# COVID-19 Statistics for Italian Province/Regioni

Based on the data from [2], compute several statistics for different areas (Province, Regioni) in Italy.

**NOTE**: These statistics are based on 1) uncertain data, 2) possibly wrong! Always check and compare the official sources if in doubt.

For each day that has available data, the program outputs for each provincia/regione:
- `avg_N`: average of the number of new COVID cases in the last `W` days
- `lastW_pop`: total number of new cases in the last W days per `100000` inhabitants
- `lastW_area`: total number of new cases in the last W days per square Km
- `reff`: reproduction index
- `total`: total number of cases

The default value of `W` is 7 days, different values could be chosen with the `wsize` parameter.

For each provincia/regione, the program also computes the expected value day (see [4] for details), which gives a qualitative indication of how likely an outbreak is under control. The further away from the expected value day, the likelier an outbreak is under control.

## Details on the computed values

Let `N(t)` be the number of new cases at day `t`.
`avg_N(t)` on a window of size `W` is computed as:

- `avg_N(t)` = `(N(t) + N(t-1) + ... + N(t-W)) / W`

Averaging the number of new cases over a window of `W` days "smoothes" the uncertainty of the data. (Note that no "shifting"/"re-centering" on the day with statistically the highest number of submitted new cases is performed.)

The reproduction index `reff` is computed on the basis of `avg_N` values.

- `reff(t)` = `avg_N(t) / avg_N(t-W)`

With the default value of `W = 7` days, the assumption is that a new infection is visible in the statistics after `7` days.

Let `t` be a progressive day from the beginning of the available data (i.e., `t = 0` is day "one"), the expected value day is computed as (in pseudo latex notation):
```
exp_day = \sum_{t} (t * N(t)) / total_cases
```
The expected value day "looks" (hopefully back) from the most recent available data.

## Usage

```
mavg.py --help
```

The program uses input data from [1], [2], and [3]. The data from [1] and [3] has been consolidated into `data/regioni.csv` and `data/province.csv`.

Check the OFILE and IFILE dictionaries for the default locations of the input and output json/CSV files.

## Output

Two json files (one for the province, one for the regioni) reporting the statistics for each regione/provincia, and day.

### Example Output
```
avg_province.json
{
    "1": {
        "code": 1,
        "exp": [
            246.4967163445791,
            "2020-10-27T18:00:00",
            -108
        ],
        "name": "Torino",
        "stat": {
                ...
                "2020-03-11T17:00:00": {
                "avg_N": 21.428571428571427,
                "lastW_area": 0.02198781581832787,
                "lastW_pop": 6.648561893900477,
                "reff": 2.5,
                "tot": 159
            },
            ...
```

## Data Sources
- [1]: DEMO istat.it (November 2019 data) [ISTAT Italian Population](http://demo.istat.it/bilmens2019gen/index02.html). (Source data for the `tavola_bilancio_mensile_2019_*` files.)
- [2]: [COVID-19 Data](https://github.com/pcm-dpc/COVID-19/)
- [3]: Area of Italian Province. [Area](https://github.com/MatteoHenryChinaski/Comuni-Italiani-2018-Sql-Json-excel.git)
- [4]: Details on the statistics computed by "covid19 Germany districts visualization" [links](https://covh.github.io/cov19de/pages/about.html)

## License
- [Apache-2.0](LICENSE) or [https://www.apache.org/licenses/LICENSE-2.0]
