import folium
import xlrd
import time
import clize
import os
import urllib.parse

# http://www.findlatitudeandlongitude.com/batch-geocode/
# python test_carte.py Cartographie\ des\ réseaux\ de\ chaleur\ au\ bois\ en\ 2014.xlsx -c "#ff4c00" -f "0.4" -l "" -o fdc2.html -r

@clize.clize(
    alias = {
        'output': ('o',),
        'default_color': ('c',),
        'fill_opacity': ('f',),
        'line_color': ('l',),
        'render': ('r',),
        'sheet': ('s',),
        },
    )
def __main__(xlsx, output:str=None, default_color='#3186cc', fill_opacity:float=1, line_color='', render=False, sheet:str=''):
    """
    carte.py

    xlsx: xlsx data file
    output: output html filename
    default_color: default color
    fill_opacity : fill opacity
    render : render to file
    sheet : select sheet by name

    Example:
    python carte.py

    Written by : Alexandre Norman <norman at xael.org>
    """

    if output is None:
        output = '.'.join(xlsx.split('.')[:-1]) + '.html'

    output_png = '.'.join(output.split('.')[:-1]) + '.png'
        
    book = xlrd.open_workbook(xlsx, 'r')
    if sheet == '':
        mysheet = book.sheet_by_index(0)
    else:
        mysheet = book.sheet_by_name(sheet)
        
    row = mysheet.row(0)  # 1st row
    
    keys = [mysheet.cell(0, col_index).value for col_index in range(mysheet.ncols)]
    
    carte = []
    for row_index in range(1, mysheet.nrows):
        d = {keys[col_index]: mysheet.cell(row_index, col_index).value 
             for col_index in range(mysheet.ncols)}
        
        carte.append(d)
    
    
    
    # Get a basic world map.
    #carte_map = folium.Map(location=[47, 4], zoom_start=6, tiles='Stamen Toner')
    carte_map = folium.Map(location=[47, 4], zoom_start=6, tiles='Mapbox Bright')
    #carte_map = folium.Map(location=[47, 4], zoom_start=6)
    
    # Draw markers on the map.
    for row in carte:
        nom = row["Nom"]
        lat, lon = row["Latitude"], row["Longitude"]
        print(nom, lat, lon)
        try:
            radius = row["Taille"]
        except KeyError:
            radius = 12000
        try:
            couleur = row["Couleur"]
            # vert : #009d48
            # bleu : #0074b1
            # orange : #e8843d
            if couleur == "vert":
                couleur = "#009d48"
            elif couleur == "bleu":
                couleur = "#0074b1"
            elif couleur == "orange":
                couleur = "#e8843d"
    
        except KeyError:
            couleur = default_color
            
        carte_map.circle_marker(location=[lat, lon],
                                popup=nom,
                                radius=radius,
                                fill_color=couleur,
                                fill_opacity=fill_opacity,
                                line_color=line_color,
        )
    
    # Create and show the map.
    carte_map.create_map(output)
    carte_map

    #import pdb; pdb.set_trace()
    if render:
        from selenium import webdriver
        browser = webdriver.Firefox()
        browser.maximize_window()
        browser.get('file://'+urllib.parse.quote(os.path.realpath(output)))
        time.sleep(5)
        print('Save as :', output_png)
        browser.save_screenshot(output_png)
        browser.quit()
    

    
    return

############################################################################



# MAIN -------------------
if __name__ == '__main__':

    clize.run(__main__)
    sys.exit(0)


#<EOF>######################################################################
