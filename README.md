# KiCad-Diff

This is a python program with a Tk interface for comparing KiCad PCB revisions.

The diffing strategy has been changed for this version and SVGs are generated directly rather than doing renderings in ImageMagick as in previous versions. This has made the rendering possible for all layers in a few seconds (compared to 20-60s+ depending on resolution and number of layers selected in previous version). The SVG images are layered together with a different feColorMatrix filter applied to each diff. This highlights areas where features have been added or removed.

The output is presented as a gallery of images of each layer. Each layer pair can be compared and the combined view highlights clearly where the layers differ from each other.

The diff output can be scrolled and zoomed in and out for closer inspection. The pair of 'before and after' views will also pan and zoom together. I have looked at linking all three windows together but this makes for a very confusing and unsatisfactory effect.

## Instructions

### Dependencies

- Ensure that you have Python3 installed. Why? https://www.pythonclock.org
- Python Libraries from Kicad 5.*
- For python dependencies check the `requirements.txt`

To install KiCad-Diff dependencies:

```
cd KiCad-Diff
pip3 install -r requirements.txt
```

## Usage

Make sure you have SCMs (Git, Fossil and/or SVN) available throught the PATH variable.
Add the script path to your PATH too so the `kidiff` and `plotpcb` will be available.
This can be done easely with:

```
cd KiCad-Diff
source env.sh
```

The terminal should give you some useful information on progress. Please include a copy of the terminal output if you have any issues.

### Comandline help

```
➜ ./kidiff -h
usage: kidiff [-h] [-a COMMIT1] [-b COMMIT2] [-g] [-s SCM] [-d DISPLAY] [-p PORT] [-w] [-v] [PCB_PATH]

Kicad PCB visual diffs.

positional arguments:
  PCB_PATH              Kicad PCB path

optional arguments:
  -h, --help            show this help message and exit
  -a COMMIT1, --commit1 COMMIT1
                        Commit 1
  -b COMMIT2, --commit2 COMMIT2
                        Commit 2
  -g, --gui             Use gui
  -s SCM, --scm SCM     Select SCM (git, svn, fossil)
  -d DISPLAY, --display DISPLAY
                        Set DISPLAY value, default :1.0
  -p PORT, --port PORT  Set webserver port
  -w, --webserver-disable
                        Does not execute webserver (just generate images)
  -v, --verbose         Increase verbosity (-vvv)

```

### Usage example

```
# With a Git repo
kidiff led_test.kicad_pcb

# Forcing an specific SCM when more than one is available (Precedence: Git > Fossil > SVN)
kidiff led_test.kicad_pcb --scm fossil

# With a Git repo, passing Commit 1 and 2 on the command line
kidiff led_test.kicad_pcb -a r1 -b r3

```

## Debugging

There should be some output in the launch terminal. Please copy this and include it in any issues posted. If the program is not working, please check that you can run the `plotpcb` routine directly by invoking it from the command line and passing the name of the `*.kicad_pcb` file.

```
plotpcb board.kicad_pcb
```


# Screenshots

### GUI
<img src="/docs/gui.png" width="550" alt="gui">

### Main View
<img src="/docs/main1.png" width="820" alt="main1">
<img src="/docs/main2.png" width="820" alt="main2">

### Overlaped Diff
<img src="/docs/diff.png" width="300" alt="fab layer diff">

### Side-by-Side View
<img src="/docs/pair.png" width="600" alt="fab layer side by side">

### F_Cu Layer
<img src="/docs/cu.png" width="500" alt="Cu difference view">

### F_Cu Layer 3 Pane View
<img src="/docs/composite.png" width="500" alt="Cu layer - 3 pane view">

### Attributes Diff
<img src="/docs/text.png" width="850" alt="Text Diff">
