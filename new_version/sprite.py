# in this file , we convert the pixels to sprite

def raster_to_sprite(mask):
    rows = []
    n = len(mask[0])
    for row in mask:
        bits = 0
        for i,v in enumerate(row):
            if v :
                bits |= (1 << (n-1-i))
        #if bits > 0:
        rows.append(bits)
    
    
    return (rows,n,len(mask))

        