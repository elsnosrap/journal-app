# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A simple Python CLI application for collecting personal health metrics (daily rating and sleep score). Uses only Python standard library with no external dependencies.

## Running the Application

```bash
python3 rating_cli.py
```

## Architecture

Single-file application (`rating_cli.py`) with:
- **Input collection**: `get_rating()` and `get_sleep_score()` functions prompt for 1-10 values, accept 0 to skip
- **Data persistence**: Saves to `.data/` directory with timestamped filenames (`rating_{timestamp}.txt`, `sleep_score_{timestamp}.txt`)
- **Main flow**: Greeting → optional rating → optional sleep score → confirmation

Both inputs are optional (user can skip by entering 0). Data files use `YYYY-MM-DD-HH-MM` timestamp format.

## Python Version

Requires Python 3.10+ (uses `int | None` union type syntax).
