# pylint-checkbranch #
Run Pylint against every file changed on this branch!

This script automatically runs Pylint against any files that have been changed
in the current working branch.  The scores are collected and output in a fancy
table suitable for use on GitHub or other sites that use GitHub-flavored
Markdown.

## Features ##
* Outputs a GitHub-flavored Markdown table
* Escapes underscores in filenames to avoid embarrassing italics
* Indicates some file status options (added, changed, deleted)
* Emojis supplement score quality for quick reference
* Automatically uses the `.pylintrc` file in the repo root

## Caveats ##
I made this on my lunch break, so it's not very well tested.  There are a
number of current shortcomings.  In no particular order:

* Filename sorting may be case-sensitive
* Can only find `.pylintrc` in the repository root
* Absent `.pylintrc` file may cause errors
* Assumes that `pylint` and `git` commands are available
* Developed and used in a wholly Unix-like environment (not tested in Windows)

## Example ##
Invoking the script:
```
./pylint-checkbranch.py
```

Here's an example of the output:
```
| Status  | File Name                             | Pylint Score   |
| ------- | ------------------------------------- | -------------- |
| NEW     | lib/BluetoothSupport.py               | 9.79/10 :star: |
| changed | lib/ConfigReader.py                   | 7.98/10        |
| changed | StationConfig/conf\_example.py        | -50.00/10 :x:  |
| NEW     | Test/BluetoothTests/\_\_init\_\_.py   | N/A            |
| NEW     | Test/BluetoothTests/test\_bt\_sink.py | 7.76/10        |
```

And here's the table it produces on GitHub:

| Status  | File Name                             | Pylint Score   |
| ------- | ------------------------------------- | -------------- |
| NEW     | lib/BluetoothSupport.py               | 9.79/10 :star: |
| changed | lib/ConfigReader.py                   | 7.98/10        |
| changed | StationConfig/conf\_example.py        | -50.00/10 :x:  |
| NEW     | Test/BluetoothTests/\_\_init\_\_.py   | N/A            |
| NEW     | Test/BluetoothTests/test\_bt\_sink.py | 7.76/10        |

## Contact ##
You can reach me at fspreen@logikos.com or Fred\_Spreen@bose.com and I'll put
you right on the bottom of my TODO list!  (Hey, I _did_ mention it was a
lunch-break project...)
