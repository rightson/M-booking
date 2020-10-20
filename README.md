# Booking Robot

## Requirements

### 1. Python3
### 2. ChromeDriver
### 3. Tesseract

- Purpose: Parse validation image
- Must install to your OS
- https://digi.bib.uni-mannheim.de/tesseract/
	- Version 4.x works fine

### 4. Install pip packages

- Command
    ```
	pip install -r requirements.txt
    ```

- For insecure ssl environment
    ```
	pip-install.bat -r requirements.txt
    ```

# Booking Flow

### Treadmill

```
python booking.py --treadmill --row 1 --column 1
```

### Massage

```
python booking.py --massage --row 1 --column 1
```

# Auto Run

- See https://www.thewindowsclub.com/how-to-schedule-batch-file-run-automatically-windows-7

