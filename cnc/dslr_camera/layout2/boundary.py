from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

feedrate = 150.0
fileName = 'layout2.dxf'
depth = 0.30
startZ = 0.0
safeZ = 0.5
maxCutDepth = 0.08
toolDiam = 0.25 
direction = 'ccw'
startDwell = 1.0
startCond = 'minX'


prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))
prog.add(gcode_cmd.PathBlendMode(p=0.02,q=0.01))

if True:
    param = {
            'fileName'    : fileName,
            'dxfTypes'    : ['LINE', 'ARC', 'CIRCLE'],
            'layers'      : ['camera_hole'],
            'depth'       : depth,
            'startZ'      : startZ,
            'safeZ'       : safeZ,
            'toolDiam'    : toolDiam,
            'direction'   : direction,
            'cutterComp'  : 'inside',
            'maxCutDepth' : maxCutDepth,
            'startDwell'  : startDwell, 
            }
    circle = cnc_dxf.DxfCircBoundary(param)
    prog.add(circle)

if True:
    param = {
            'fileName'    : fileName,
            'dxfTypes'    : ['LINE', 'ARC', 'CIRCLE'],
            'layers'      : ['boundary'],
            'depth'       : depth,
            'startZ'      : startZ,
            'safeZ'       : safeZ,
            'toolDiam'    : toolDiam,
            'direction'   : direction,
            'cutterComp'  : 'outside',
            'maxCutDepth' : maxCutDepth,
            'startDwell'  : startDwell, 
            'startCond'   : startCond,
            }
    boundary = cnc_dxf.DxfBoundary(param)
    prog.add(boundary)

prog.add(gcode_cmd.ExactPathMode())

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}.ngc'.format(baseName)
print('generating: {0}'.format(fileName))
prog.write(fileName)
