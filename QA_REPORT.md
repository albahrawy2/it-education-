# IT Education — QA Report

## Fix applied in this revision
- Fixed the JavaScript-to-Android bridge call to pass both required arguments: Python source and the optional stdin text. This was a confirmed integration bug affecting execution, and particularly `input()`.
- Connected the example editor's input area (`#pyInput`) to the offline Python runner.

## Local tests performed
- JavaScript syntax check (`node --check`): passed.
- Python runner: `print(1+2)` returned `3`.
- Python stdin: `int(input())` with input `21` returned `42` after doubling.
- Runtime error: `1/0` reported `ZeroDivisionError`.
- Loop output: `for i in range(3)` returned lines `0`, `1`, `2`.
- Infinite loop guard: `while True: pass` stopped with the configured iteration-limit error.

## Not yet verified
- Android Gradle build and APK generation were not run in this environment.
- No installation/device tests were performed on a physical Android phone.
- This report does not guarantee zero defects. Please build and test on Android Studio before distribution.
