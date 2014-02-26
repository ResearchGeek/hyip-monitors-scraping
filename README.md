hyip-monitors-scraping
======================

Downloads data about running HYIP programs from webmonitors like GoldPoll or PopularHYIP.com

GoldPoll is a popular website which aggregates everyday working HYIP online establishment and verifies their status (paying / not paying) basing on the user experience. This monitor gives also clear information about time of existence of a particular HYIP in days (although the credibility of this may be bias) and range of percentage payed per day/week/month.

**Output:**

CSV with data parsed from the monitor(s). CSV file is named hyip-date.csv, where the date is the today date of the program execution. CSV file is seperated with commas and encoded in Unicode.

**Usage instruction:**

Tested on Python 2.7. Basic usage:

```
python aurum.py
```

```
python aurum.py --method=native --verbose
```

Check file usage.txt for more optional parameters.

**License**

Providen in the LICENSE file. No civil rights claimed whats so ever. Program provided "as it is" and we are not responsible for the data or action which may be connected with the program or deriven results.

**To do list:**

- Ask Google about real time-of-existence variable
- Implement scrapping more websites
