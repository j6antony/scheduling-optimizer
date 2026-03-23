# Scheduling Optimizer

Scheduling Optimizer is a small Python and Pygame project for creating tasks, saving them to JSON, and viewing a calendar-style schedule interface.

## Features

- Create task cards with a name, due date, duration, and availability
- Save task data into `tasks.json`
- View a read-only calendar layout
- Run basic scheduling logic from the Python codebase

## Project Files

- `menu.py`: main task entry UI
- `task.py`: task card component and task data conversion
- `button.py`: reusable button component
- `calender.py`: calendar view
- `algorithim.py`: scheduling logic
- `tasks.json`: saved task data

## Requirements

- Python 3
- `pygame`
- `make`

## Installation

Install dependencies with:

```bash
make install
```

Or manually:

```bash
python3 -m pip install pygame
```

## Usage

Run the main planner UI:

```bash
make run
```

Run the calendar view:

```bash
make run-calendar
```

Check that the Python files compile:

```bash
make check
```

Clean cache files:

```bash
make clean
```

## Notes

- The project uses Pygame for the interface, so it should be run in a local desktop environment.
- Task data is written to `tasks.json`.
- The current scheduling logic lives in `algorithim.py` and is still fairly simple.
