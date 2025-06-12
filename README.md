# UT Automatic Course Adder

A script that automatically monitors course availability at UT Austin and registers you for classes as soon as they open up. Based on [UT-Course-Availability-Tracker](https://github.com/christiandipert/UT-Course-Availability-Tracker).

## Features

- Monitors course availability in real-time
- Automatically registers when a class opens
- Joins waitlists and sets swap classes when needed
- Option to drop a class upon successful registration
- Handles UT EID login (Duo authentication necessary)

## Requirements

Install the required dependencies:

```bash
pip install selenium
```

## How to Use

### Basic Usage

Run the script and follow the interactive prompts:

```bash
python courseTrack.py
```

or

```bash
python3 courseTrack.py
```

The script will ask for:
- Whether to add a class (Add) or drop upon successful add (Drop)
- Unique ID of the class to add
- (If dropping) Unique ID of the class to drop
- Unique ID to swap if waitlisted (enter 0 if not applicable)
- Semester (fall or spring) and year
- Whether to show the browser window

### Advanced Usage with Command-Line Flags

For simpler execution, use the `-a` or `--advanced` flag to provide all parameters at once:

```bash
python courseTrack.py -a "Drop 12345 12346 0 fall 2025 Y"
```

Format for advanced mode:
`[Add/Drop] [ID to Add] [ID to Drop] [ID to Swap for WL] [Season] [Year] [Display Y/N]`

Where:
- First parameter: "Add" or "Drop" (whether to drop a class upon successful add)
- ID to Add: Unique number of the class you want to add
- ID to Drop: Unique number of the class you want to drop (only if first parameter is "Drop")
- ID to Swap for WL: Unique number to swap if waitlisted (enter 0 if not applicable)
- Season: "fall" or "spring"
- Year: Four-digit year (e.g., 2025)
- Display: "Y" to show browser window, "N" to minimize

### Authentication

Once the initial setup with classes to add/drop is completed, the window will open, but the terminal will have an important designation.

The script will ask if you want it to handle your credentials:
- If you select "Y", you'll need to enter your UT EID and password into the terminal
- You'll still need to complete Duo authentication manually
- If you select "N", you'll handle the entire login process manually, which will also mean that logout timeouts will practically end the script.

## Example

To add course 12345 for Fall 2025 without dropping any current classes or conditional waitlist dropping using advanced format:

```bash
python courseTrack.py -a "Add 12345 0 fall 2025 Y"
```

To add course 12345 and drop course 67890 for Spring 2026:

```bash
python courseTrack.py -a "Drop 12345 67890 0 spring 2026 Y"
```

## Help

For help with available options:

```bash
python courseTrack.py --help
```