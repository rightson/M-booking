# Booking Robot

## Requirements

### 1. Python3
### 2. ChromeDriver
### 3. Tesseract

- Purpose: Parse validation image
- Must install to your OS
- https://digi.bib.uni-mannheim.de/tesseract/
	- Version 4.x works fine

### 4. Install dependencies

##### For standard python environment (from python.org)
1. create Virtualenv
```
python3 -m venv venv
```
2. activate venv
```
venv/Script/activate.bat
```
3. install dependency
```
pip install -r requirements.txt
```
3. install dependency (for insecure ssl environment)
```
pip-install.bat -r requirements.txt
```

##### For Anaconda
1. create a new conda env and install dependencies
```
conda create --name booking --file requirements.conda
```
2. install pytesseract
```
conda install -c conda-forge pytesseract
```

## Booking Resources (Dev mode)

Enter virtualenv first

### Treadmill

```
python booking.py --treadmill --row 1 --column 1
```

### Massage

```
python booking.py --massage --row 1 --column 1
```

## Build into a Binary


```
make	# if make for win32 installed
```
or

```
pyinstaller -F --add-binary "bin;." --onefile booking.py
```


## Auto Run

- See https://www.thewindowsclub.com/how-to-schedule-batch-file-run-automatically-windows-7

