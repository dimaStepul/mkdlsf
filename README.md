# Cypriot Censorship Checker

This project is designed to check various types of internet censorship, such as SNI blocking, DNS blocking, and HTTP blocking.

## Usage

You can use this tool via the command line as follows:

```bash
python3 -m venv env               # create virtual python environment;
source env/bin/activate           # activate virtual python environment;
pip3 install -r requirements.txt  # install dependencies;

python3 check.py                  # run the analysis (use statistics.db and timeout=30 seconds by default);

deactivate                        # deactivate python environment.
```


```bash
python main.py -s <site> -p <port> -f <file> -b <block>
```