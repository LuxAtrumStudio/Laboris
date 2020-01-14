# Available Commands

* create <task> [parents...] [tags...] [dueDate]
  * create Foo +ParentTask @TaskTag due:Friday
* start <task> [startTime]
  * start Foo -15m
* stop <task> [stopTime]
  * stop Foo +1h
* close <task>
  * close Foo
* open <task>
  * open Foo
* list FILTER_PARAMS
  * list +ParentTask @TaskTag duel:friday

# Filter Params

* task: Task reference, either uuid, or title
* parents: Task parents, tasks must have these parents
* children: Task children, tasks must have these children
* tag: Task tags, tasks must have these tags
* priority: Task must have this priority
* priorityG: Taks must have priority greather than this
* priorityL: task must have priority less than this
* parentCount: Task must have this number of parents
* parentCountG: Task must have more than this number of parents
* parentCountL: Task must have less than this number of parents
* childCount: Task must have this number of children
* childCountG: Task must have more than this number of children
* childCountL: Task must have less than this number of children
* tagCount: Task must have this number of tags
* tagCountG: Task must have more than this number of tags
* tagCountL: Task must have less than this number of tags
* due: Task must be due on this date
* dueBefore: Task must be due before this time
* dueAfter: Task must be due after this time
* entry: Task must have been entered on this date
* entryBefore: Task must have been entered before this time
* entryAfter: Task must have been entered after this time
* done: Task must be done on this date
* doneBefore: Task must be done before this time
* doneAfter: Task must be done after this time
* modified: Task must be modified on this date
* modifiedBefore: Task must be modified before this time
* modifiedAfter: Task must be modified after this time
* hidden: Task must be hidden
* no-hidden: Task must not be hidden [default]
* all-hidden: All tasks
* open: Tasks must be open[default]
* closed: tasks must be closed
* all: all tasks
