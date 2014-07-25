'''
Created on Jul 17, 2014

@author: qurban.ali
'''

#import pymel.core as pc
#import maya.cmds as cmds
import os.path as osp
import os
import subprocess
import multiprocessing as mp
user = osp.expanduser('~')

def find_live_nodes():
    '''returns the list of all connected computers in a LAN'''
    os.system('net view > conn.tmp')
    f = open('conn.tmp', 'r')
    f.readline();f.readline();f.readline()
    
    conn = []
    host = f.readline()
    while host[0] == '\\':
        conn.append(host[2:host.find(' ')])
        host = f.readline()
    f.close()
    return conn

def submit_job(command):
    subprocess.call(command)

def ai_render(file_path=None):
    '''renders the scene in chuncks by sending each chunck
    to a sepearate computer using psexec.exe'''

    nodes = ['\\\\ice-089', '\\\\ice-088', '\\\\ice-067']

    #res = pc.ls(type='resolution')[0]
    width = 500 #res.width.get()
    height = 500 #res.height.get()

    numNodes = len(nodes)
    quotient = height/numNodes
    remender = height%numNodes

    if file_path == None:
        file_path = r"\\ice-089\public\maya\scenes\cylinder.ma"
        
    lastPixel = -1
    yEnd = quotient - 1
    count = 1
    commands = []
    for node in nodes:
        name = osp.splitext(osp.basename(file_path))[0] +"_"+ str(count).zfill(3)
        command = "render.exe -proj \\\\ice-089\\public\\maya -r arnold -im "+ name+ " -reg %s %s %s %s %s"%(0, width-1, lastPixel+1, yEnd, file_path)
        commands.append(command)
        lastPixel = yEnd
        yEnd += quotient
        if yEnd > height:
            if remender > 0:
                count += 1
                name = osp.splitext(osp.basename(file_path))[0] +"_"+ str(count)
                command = "render.exe -proj \\\\ice-089\\public\\maya -r arnold -im "+ name+ " -reg %s %s %s %s %s"%(0, width-1, lastPixel+1, lastPixel+remender, file_path)
                commands.append(command)
        count += 1
    nodeCount = 0
    if len(commands) > len(nodes):
        nodes.append(nodes[-1])
    for cmd in commands:
        fileName = 'ai_render_'+ str(nodeCount) + '.bat'
        fullFileName = osp.join(user, fileName)
        f = open(fullFileName, 'w+')
        f.write("call \\\\nas\\storage\\scripts\\mount.bat"+
                "\nset MAYA_RENDER_DESC_PATH=C:\\solidangle\\mtoadeploy\\2013"+
                "\nset PATH=C:\\solidangle\\mtoadeploy\\2013\\bin;%path%"+
                "\nset MAYA_MODULE_PATH=C:\\solidangle\\mtoadeploy\\2013"+
                "\nset MAYA_PLUG_IN_PATH=C:\\solidangle\\mtoadeploy\\2013\\plug-ins"+
                "\nset PATH=C:\\Program Files\\Autodesk\Maya2013\\bin;%path%\n" + cmd)
        f.close()
        psexec = r"psexec -d "+ nodes[nodeCount] +" -u ICEANIMATIONS\qurban.ali -p 13490 -c -f "+ fullFileName
        os.system(psexec)
        nodeCount += 1