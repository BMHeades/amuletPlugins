# A simple random arc function by @bmheades
# You may not use it commerically

import amulet
from amulet.api.selection import SelectionGroup
from amulet.api.data_types import Dimension
from amulet.api.level import BaseLevel
from amulet.api.level import World
from amulet.api.block import Block 
from amulet_nbt import (
    TAG_String,
    TAG_Int,
    TAG_Byte,
)  
import random
import math


# function to calculate the average
def midpoint(p1, p2): 
        return round((p1+p2)/2)


def colorful_arcs(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):

    
    print("Colorful Arcs Started...")

    block_platform = "bedrock"  # the platform the blocks below are defined in
    block_version = (1, 17, 0)  # the version the blocks below are defined in

    
    # Add your blocks here
    blockPalette = [
         Block("minecraft", "wool", {"color": TAG_String("white")}), 
         Block("minecraft", "wool", {"color": TAG_String("orange")}),
         Block("minecraft", "wool", {"color": TAG_String("light blue")}),
         Block("minecraft", "wool", {"color": TAG_String("yellow")}),
         Block("minecraft", "wool", {"color": TAG_String("pink")}),
         Block("minecraft", "wool", {"color": TAG_String("cyan")}),
         Block("minecraft", "wool", {"color": TAG_String("blue")}),
         Block("minecraft", "wool", {"color": TAG_String("black")})
    ]

    # Test blocks
    air = Block("minecraft", "air")
    stone = Block("minecraft", "stone", {})

    # Finding the center and size of the selection 
    for box in selection:

        selectionCenterX = midpoint(box.max_x, box.min_x)
        selectionCenterY = midpoint(box.max_y, box.min_y)
        selectionCenterZ = midpoint(box.max_z, box.min_z)

        selectionSizeX = box.max_x - box.min_x
        selectionSizeY = box.max_y - box.min_y
        selectionSizeZ = box.max_z - box.min_z

    # P5.js inspired Arc Function
    def arc(x1, y1, z1, r, angleStart, angleEnd, block): 
        while(angleStart < angleEnd):
            pointX = round(x1 + r * math.cos(angleStart * 3.142 / 180))
            pointZ = round(z1 + r * math.sin(angleStart * 3.142 / 180))
            world.set_version_block(
                                pointX, y1, pointZ, dimension, (block_platform, block_version), block
                            )
            angleStart += 1

    # Deciding how big the arcs should be depending on the selection size
    arcsSize = round(midpoint(selectionSizeX, selectionSizeZ) / 2.5)

    # Arcs density and inner radius
    density = options["Arcs Density"]
    if density > 10: # Primitive fail safe
        density = 10

    innerRadius = options["Inner Radius"]

    # Here come the crammed randoms
    for i in range(arcsSize):
        block1 = random.choice(blockPalette)
        for z in range(density):
            angleStart = random.randint(-180, 180)
            angleEnd = angleStart + random.randint(45 - (i*2), 90)
            arc(selectionCenterX, selectionCenterY, selectionCenterZ, innerRadius + i, angleStart, angleEnd, block1)
        

    print("Colorful Arcs Ended...")

operation_options = {
    "Arcs Density": [
        "int",
        2,
    ],
    "Inner Radius": [
        "int",
        8,
    ]
}

export = {
    "name": "Colorful Arcs",
    "operation": colorful_arcs,
    "options": operation_options,
}
