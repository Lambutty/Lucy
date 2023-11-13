## Quick Guide

Python Version 3.10.0 required

run:

With virtual environment. Dependencies are **not** installed globally
```shell
python -m venv .venv
Set-ExecutionPolicy Unrestricted -Scope Process
python .venv\Scripts\activate
pip install -r requirements.txt
```
For Global installation just this
```shell
pip install -r requirements.txt
```

Overall help: python main.py -h

To actually run it we need to get the id of your microphone

```shell
python main.py -l

# find you microphone device id
```

Then

```shell
python main.py -d YOUR_DEVICE_ID_HERE -m de 
```

Say
```
Sag Lucy, warte auf Antwort und dann frag nach Metten Bockwürtschen.
Wenn Lucy nicht mehr zuhören soll und sofort nach der Antwort suchen soll kannst du STOP am ende des satzes sagen
```

