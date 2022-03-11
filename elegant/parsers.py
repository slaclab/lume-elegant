import numpy as np

import subprocess
import os


def parse_sdds_table(sddsfile, columns, sdds2plaindata_exe='sdds2plaindata'):
    """
    Get tabular data from SDDS file.
    
    Example:
        get_table('LCLS2scH.twi', ['s', 'betax', 'betay', 'etax'])
    """
    
    assert os.path.exists(sddsfile)
    
    outfile = sddsfile+'_table'
    cmd0 = [sdds2plaindata_exe, sddsfile, outfile, '-noRowCount', '-outputMode=ascii']
    
    cmd = cmd0 + [f'-col={c}' for c in columns] + ['-separator= ']

    output,error  = subprocess.Popen(
                    cmd, universal_newlines=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    assert os.path.exists(outfile), f'{outfile} does not exist'
    
    rdat = np.loadtxt(outfile)
    
    dat = {}
    for i, key in  enumerate(columns):
        dat[key] = rdat[:,i]
    
    os.remove(outfile)
    return dat