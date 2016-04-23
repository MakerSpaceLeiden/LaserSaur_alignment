# LaserSaur_alignment
Alignment tool for LaserSaur
Both python lib and cli for manipulation of lasersaur. 
With some preprogrammed movement patterns which come in handy while 
aligning
## Python interactive example

```python
import lsxs

instance = lsxs.Lsxs()
instance.reset()
instance.command = "G0 X100 Y100"
```
or

```python
instance.movetoxy(100, 100)
```

###flash, move, flash

```python
instance.leftvertical()
```
or

```python
instance.lowerhorizontal()
```

###coordsys

![crdsys](./artwork/drawing.svg)

## Disclaimer
work in progress etc..
