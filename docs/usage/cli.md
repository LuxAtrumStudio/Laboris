# Laboris

## Name ##

Laboris - manual page for Laboris 2.0

## Description

```
usage: laboris [-h] [--version]
               {add,done,undone,start,stop,delete,modify,list,report} ...
```

Task priority tracker, and manager. All actions preformed are part of a sub
process found below.

### Add ###

---

```
usage: laboris add [-h] [--priority PRIORITY] [--due [DUE]]
                   [--tag [TAG [TAG ...]]] [--project [PROJECT [PROJECT ...]]]
                   description [description ...]
```

#### Positional Arguments: ####

`description`

:   Task description

#### Optional Arguments: ####

`-h`, `--help`

:   Show the help message and exit

`--priority PRIORITY`, `-p PRIORITY`

:   Sets the tasks priority

`--due [DUE]`, `-d [DUE]`

:   Date/Time that the task is due

`--tag [TAG [TAG ...]]`, `-t [TAG [TAG ...]]`

:   The tasks tags

`--project [PROJECT [PROJECT ...]]`, `-pr [PROJECT [PROJECT ...]]`

:   The projects that the task belongs to

### Done ###

---

```
usage: laboris done [-h] task
```

#### Positional Arguments: ####

`task`

:   Task to complete

#### Optional Arguments: ####

`-h`, `--help`

:   Show the help message and exit


### Undone ###

---

```
usage: laboris undone [-h] task
```

#### Opsitional Arguments: ####

`task`

: Task to un-complete

#### Optional Arguments: ####

`-h`, `--help`

: Show the help message and exit

### Start ###

---

```
usage: laboris start [-h] task [time]
```

#### Positional Arugments: ####

`task`

:   Task to start work on

`time`

:   Date/Time work started on task

#### Optional Arugments: ####

`-h`, `--help`

:   Show the help message and exit

### Stop ###

---

```
usage: laboris stop [-h] task [time]
```

#### Positional Arugments: ####

`task`

:   Task to stop work on

`time`

:   Date/Time work stoped on task

#### Optional Arugments: ####

`-h`, `--help`

:   Show the help message and exit


### Delete ###

---

```
usage: laboris delete [-h] task
```

#### Positional Arguments: ####

`task`

:   Task to delete

#### Optional Arguments: ####

`-h`, `--help`

:   Show the help message and exit

### Modify ###

---

```
usage: laboris modify [-h] [--priority [PRIORITY]] [--due [DUE]]
                      [--tag [TAG [TAG ...]]]
                      [--project [PROJECT [PROJECT ...]]]
                      task [description [description ...]]
```

#### Positional Arguments: ####

`task`

:   Task to modify

`description`

:   Task description

#### Optional Arguments: ####

`-h`, `--help`

:   Show the help message and exit

`--priority PRIORITY`, `-p PRIORITY`

:   Sets the tasks priority

`--due [DUE]`, `-d [DUE]`

:   Date/Time that the task is due

`--tag [TAG [TAG ...]]`, `-t [TAG [TAG ...]]`

:   The tasks tags

`--project [PROJECT [PROJECT ...]]`, `-pr [PROJECT [PROJECT ...]]`

:   The projects that the task belongs to

### List ###

---

```
usage: laboris list [-h] [--sort [{urgency,description,due,entry,done,id,uuid,
                                   project,tag,status,times,priority}]]
                    [-group [{all,pending,completed}]] [--format [FORMAT]]
                    [task]
```

#### Positional Arguments: ####

`task`

:   Task search string

#### Optional Arguments: ####

`-h`, `--help`

:   Show the help message and exit

```
--sort [{urgency,description,due,entry,done,id,uuid,project,tag,status,times,
          priority}]
```

:   Object to sort list by

`--group [{all,pending,completed}]`

:   Shows group of tasks

`--format [FORMAT]`

:   Format of task table

### Report ###

---

#### Summary ####

#### Active ####

#### Times ####

#### Burndown ####

#### Graph ####

