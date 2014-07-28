'''
Created on Jul 28, 2014

@author: Qurban Ali
'''
import os.path as osp
import maya.cmds as cmds

user = osp.expanduser("~")
info_file = osp.join(user, 'ai_batch_render_info.txt')

def check_info(version = 2014):
    info = {}
    if osp.exists("\"C:/Program Files/Autodesk/Maya"+version+"/bin/mayapy.exe\""):
        info['maya'] = True
    else: info['maya'] = False
    
    if osp.exists("C:/solidangle/mtoadeploy/"+version+"/plug-ins/mtoa.mll"):
        info['arnold'] = True
    else: info['arnold'] = False
    
    f = open(info_file)
    f.write(str(info))
    f.close()