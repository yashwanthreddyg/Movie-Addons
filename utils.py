import os,hashlib
mediaExtensions = \
    ['264', '3G2', '3GP', '3GP2', '3GPP', '3GPP2', '3MM', '3P2',
    '60D', '787', '890', 'AAF', 'AEC', 'AEP', 'AEPX', 'AET',
    'AETX', 'AJP', 'ALE', 'AM', 'AMC', 'AMV', 'AMX', 'ANIM', 
    'ANX', 'AQT', 'ARCUT', 'ARF', 'ASF', 'ASX', 'AVB', 'AVC',
    'AVCHD', 'AVD', 'AVI', 'AVM', 'AVP', 'AVS', 'AVS', 'AVV', 
    'AWLIVE', 'AXM', 'AXV', 'BDM', 'BDMV', 'BDT2', 'BDT3', 'BIK',
    'BIN', 'BIX', 'BMC', 'BMK', 'BNP', 'BOX', 'BS4', 'BSF', 
    'BU', 'BVR', 'BYU', 'CAMPROJ', 'CAMREC', 'CAMV', 'CED', 'CEL',
    'CINE', 'CIP', 'CLK', 'CLPI', 'CMMP', 'CMMTPL', 'CMPROJ', 'CMREC',
    'CMV', 'CPI', 'CPVC', 'CST', 'CVC', 'CX3', 'D2V', 'D3V',
    'DASH', 'DAT', 'DAV', 'DB2', 'DCE', 'DCK', 'DCR', 'DCR',
    'DDAT', 'DIF', 'DIR', 'DIVX', 'DLX', 'DMB', 'DMSD', 'DMSD3D',
    'DMSM', 'DMSM3D', 'DMSS', 'DMX', 'DNC', 'DPA', 'DPG', 'DREAM',
    'DSY', 'DV', 'DV-AVI', 'DV4', 'DVDMEDIA', 'DVR', 'DVR-MS', 'DVX',
    'DXR', 'DZM', 'DZP', 'DZT', 'EDL', 'EVO', 'EVO', 'EXO',
    'EYE', 'EYETV', 'EZT', 'F4F', 'F4P', 'F4V', 'FBR', 'FBR',
    'FBZ', 'FCARCH', 'FCP', 'FCPROJECT', 'FFD', 'FFM', 'FLC', 'FLH',
    'FLI', 'FLV', 'FLX', 'FPDX', 'FTC', 'G64', 'GCS', 'GFP',
    'GIFV', 'GL', 'GOM', 'GRASP', 'GTS', 'GVI', 'GVP', 'GXF',
    'H264', 'HDMOV', 'HDV', 'HKM', 'IFO', 'IMOVIELIBRARY', 'IMOVIEMOBILE', 'IMOVIEPROJ',
    'IMOVIEPROJECT', 'INP', 'INT', 'IRCP', 'IRF', 'ISM', 'ISMC',
    'ISMCLIP', 'ISMV', 'IVA', 'IVF', 'IVR', 'IVS', 'IZZ', 'IZZY',
    'JMV', 'JSS', 'JTS', 'JTV', 'K3G', 'KDENLIVE', 'KMV', 'KTN',
    'LREC', 'LRV', 'LSF', 'LSX', 'LVIX', 'M15', 'M1PG', 'M1V',
    'M21', 'M21', 'M2A', 'M2P', 'M2T', 'M2TS', 'M2V', 'M4E',
    'M4U', 'M4V', 'M75', 'MANI', 'META', 'MGV', 'MJ2', 'MJP',
    'MJPEG', 'MJPG', 'MK3D', 'MKV', 'MMV', 'MNV', 'MOB', 'MOD',
    'MODD', 'MOFF', 'MOI', 'MOOV', 'MOV', 'MOVIE', 'MP21', 'MP21',
    'MP2V', 'MP4', 'MP4.INFOVID', 'MP4V', 'MPE', 'MPEG', 'MPEG1',
    'MPEG2', 'MPEG4', 'MPF', 'MPG', 'MPG2', 'MPG4', 'MPGINDEX', 'MPL',
    'MPL', 'MPLS', 'MPROJ', 'MPSUB', 'MPV', 'MPV2', 'MQV', 'MSDVD',
    'MSE', 'MSH', 'MSWMM', 'MT2S', 'MTS', 'MTV', 'MVB', 'MVC',
    'MVD', 'MVE', 'MVEX', 'MVP', 'MVP', 'MVY', 'MXF', 'MXV',
    'MYS', 'NCOR', 'NSV', 'NTP', 'NUT', 'NUV', 'NVC', 'OGM',
    'OGV', 'OGX', 'ORV', 'OSP', 'OTRKEY', 'PAC', 'PAR', 'PDS',
    'PGI', 'PHOTOSHOW', 'PIV', 'PJS', 'PLAYLIST', 'PLPROJ', 'PMF', 'PMV',
    'PNS', 'PPJ', 'PREL', 'PRO', 'PRO4DVD', 'PRO5DVD', 'PROQC', 'PRPROJ',
    'PRTL', 'PSB', 'PSH', 'PSSD', 'PVA', 'PVR', 'PXV', 'QT',
    'QTCH', 'QTINDEX', 'QTL', 'QTM', 'QTZ', 'R3D', 'RCD', 'RCPROJECT',
    'RCREC', 'RCUT', 'RDB', 'REC', 'RM', 'RMD', 'RMD', 'RMP',
    'RMS', 'RMV', 'RMVB', 'ROQ', 'RP', 'RSX', 'RTS', 'RTS',
    'RUM', 'RV', 'RVID', 'RVL', 'SAN', 'SBK', 'SBT', 'SBZ',
    'SCC', 'SCM', 'SCM', 'SCN', 'SCREENFLOW', 'SDV', 'SEC', 'SEC',
    'SEDPRJ', 'SEQ', 'SFD', 'SFERA', 'SFVIDCAP', 'SIV', 'SMI', 'SMI',
    'SMIL', 'SMK', 'SML', 'SMV', 'SNAGPROJ', 'SPL', 'SQZ',
    'SSF', 'SSM', 'STL', 'STR', 'STX', 'SVI', 'SWF', 'SWI',
    'SWT', 'TDA3MT', 'TDT', 'TDX', 'THEATER', 'THP', 'TID',
    'TIVO', 'TIX', 'TOD', 'TP', 'TP0', 'TPD', 'TPR', 'TREC',
    'TRP', 'TS', 'TSP', 'TTXT', 'TVLAYER', 'TVRECORDING', 'TVS', 'TVSHOW',
    'USF', 'USM', 'VBC', 'VC1', 'VCPF', 'VCR', 'VCV', 'VDO',
    'VDR', 'VDX', 'VEG', 'VEM', 'VEP', 'VF', 'VFT', 'VFW',
    'VFZ', 'VGZ', 'VID', 'VIDEO', 'VIEWLET', 'VIV', 'VIVO', 'VIX',
    'VLAB', 'VMLF', 'VMLT', 'VOB', 'VP3', 'VP6', 'VP7', 'VPJ',
    'VRO', 'VS4', 'VSE', 'VSP', 'VTT', 'W32', 'WCP', 'WEBM',
    'WFSP', 'WGI', 'WLMP', 'WM', 'WMD', 'WMMP', 'WMV', 'WMX',
    'WOT','WP3', 'WPL', 'WSVE', 'WTV', 'WVE', 'WVX', 'WXP',
    'XEJ', 'XEL', 'XESC', 'XFL', 'XLMV', 'XMV', 'XVID',
    'Y4M', 'YOG', 'YUV', 'ZEG', 'ZM1', 'ZM2', 'ZM3', 'ZMV']

def getAllFileNames(folderPath,recursive = False):
    if recursive:
        return getFileNamesRecursive(folderPath)
    else:
        return getFileNames(folderPath)
def getFileNames(folderPath):
    if not os.path.isdir(folderPath):
        return None
    entries = os.listdir(folderPath)
    files = []
    for entry in entries:
        absPath = os.path.abspath(os.path.join(folderPath,entry))
        if os.path.isfile(absPath) and not os.path.islink(absPath):
            files.append((entry,absPath))
    return files
def getFileNamesRecursive(folderPath):
    if not os.path.isdir(folderPath):
        return None
    files = []
    for entry in os.listdir(folderPath):
        absPath = os.path.abspath(os.path.join(folderPath,entry))
        if entry in [".",".."] or os.path.islink(absPath):
            continue
        if os.path.isdir(absPath):
            files.extend(getFileNamesRecursive(absPath))
        else:
             files.append((entry,absPath))
    return files
def isMediaFileName(fileName):
    if not '.' in fileName:
        return False
    fileExtension = fileName.split('.')[-1:][0]
    if fileExtension.upper() in mediaExtensions:
        return True
    return False



def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()