# the "#!" is required to tell the system to run the code
#!/bin/bash
python3 src/main.py  # easy way to run our code
cd public && python3 -m http.server 8888  # generate simple web server after generate page