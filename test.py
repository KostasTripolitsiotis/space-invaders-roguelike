

['arial', 'arialblack', 'bahnschrift', 'calibri', 'cambria', 'cambriamath', 'candara', 'comicsansms', 
 'consolas', 'constantia', 'corbel', 'couriernew', 'ebrima', 'franklingothicmedium', 'gabriola', 'gadugi', 
 'georgia', 'impact', 'inkfree', 'javanesetext', 'leelawadeeui', 'leelawadeeuisemilight', 'lucidaconsole', 
 'lucidasans', 'malgungothic', 'malgungothicsemilight', 'microsofthimalaya', 'microsoftjhenghei', 'microsoftjhengheiui', 
 'microsoftnewtailue', 'microsoftphagspa', 'microsoftsansserif', 'microsofttaile', 'microsoftyahei', 'microsoftyaheiui', 
 'microsoftyibaiti', 'mingliuextb', 'pmingliuextb', 'mingliuhkscsextb', 'mongolianbaiti', 'msgothic', 'msuigothic', 'mspgothic', 
 'mvboli', 'myanmartext', 'nirmalaui', 'nirmalauisemilight', 'palatinolinotype', 'segoemdl2assets', 'segoeprint', 'segoescript', 
 'segoeui', 'segoeuiblack', 'segoeuiemoji', 'segoeuihistoric', 'segoeuisemibold', 'segoeuisemilight', 'segoeuisymbol', 'simsun', 
 'nsimsun', 'simsunextb', 'sitkasmall', 'sitkatext', 'sitkasubheading', 'sitkaheading', 'sitkadisplay', 'sitkabanner', 'sylfaen', 
 'symbol', 'tahoma', 'timesnewroman', 'trebuchetms', 'verdana', 'webdings', 'wingdings', 'yugothic', 'yugothicuisemibold', 'yugothicui', 
 'yugothicmedium', 'yugothicuiregular', 'yugothicregular', 'yugothicuisemilight', 'holomdl2assets', 'cascadiacoderegular', 'cascadiamonoregular']

# bahnschrift
# impact
# lucidaconsole
# 
# 
import pygame
def draw_border_new(point1:tuple[int, int], point2:tuple[int, int], thicness:int, color:tuple[int, int, int]):
    """point1: x, y of top left corner
       point2: x, y of bottom right corner"""
    print(color, (point1[0], point1[1], (point2[0]-point1[0]), thicness))
    print((255, 0, 0), (point1[0]-thicness, point1[0], thicness, point2[1]-point1[1]))
    print((0, 255, 255), (point1[0], point2[1]-thicness, (point2[0]-point1[0]), thicness))
    print((100, 0, 255), (point1[0], point1[1], thicness,(point2[0]-point1[0])))
    
draw_border_new([864, 486], [1056, 540], 2, (255, 255, 255))