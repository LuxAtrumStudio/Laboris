# Date Time Reference #

A valid date time reference argument must have one of the following forms:

### Replacements ###

* `/` is replaced by `-`
* `T` is replaced by `@`

## Day Month Year ##

* `dd-mm-yyy`
* `dd-mm-yy`
* `mm-dd-yyyy`
* `mm-dd-yy`
* `yyyy-mm-dd`
* `yy-mm-dd`

## Day Month Year Hour Minute ##

* `dd-mm-yyyy@HH:MM`
* `dd-mm-yy@HH:MM`
* `mm-dd-yyyy@HH:MM`
* `mm-dd-yy@HH:MM`
* `yyyy-mm-dd@HH:MM`
* `yy-mm-dd@HH:MM`

## Day ##

* `Weekday`
* `Day`

## Day Hour Minute ##

* `Weekday@HH:MM`
* `Day@HH:MM`

## Day Month ##

* `dd-mm`
* `mm-dd`

## Hour Minute Second ##

* `HH:MM`
* `HH.MM`
* `HH:MM:SS`
* `HH.MM.SS`

## Relative ##

* `yesterday`, `Yesterday`
* `today`, `Today`
* `tomorrow`, `Tomorrow`
* `day` → `today`
* `week` → Start of current week
* `lastweek` → Start of last week
* `all` → `01/01/0001`
* `month` → Start of current month
* `lastmonth` → Start of last month
* `year` → Start of current year
* `lastyear` → Start of last year
