import os,sys,shutil,glob
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(fname):
    """Get embedded EXIF data from image file."""
    ret = {}
    try:
        img = Image.open(fname)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        print 'IOERROR ' + fname
    return ret

def parserdate(date):    
    return date[0:4],date[5:7],date[8:10]

def parserpic(pathfrom,pathto,k='copy'):
    i=0
    result={}
    for root,dirs,files in os.walk(pathfrom):
        for file in files:
            file=os.path.join(root,file)
            try:
                year,month,day=parserdate(get_exif_data(file)['DateTimeOriginal'])
                path0=pathto
                path1=path0+year
                path1=path1.strip()
                path2=path1+'/'+year+'-'+month
                path2=path2.strip()
                path3=path2+'/'+year+'-'+month+'-'+day
                path3=path3.strip()

                if os.path.isdir(path0)==False:os.mkdir(path0)
                if os.path.isdir(path1)==False:os.mkdir(path1)
                if os.path.isdir(path2)==False:os.mkdir(path2)
                if os.path.isdir(path3)==False:os.mkdir(path3)

                i+=1
                if k.lower().strip()=='copy':
                    print 'copy',i,':',file
                    shutil.copy(file,path3)
                if k.lower().strip()=='move':
                    print 'move',i,':',file
                    shutil.move(file,path3)
                    
                key=year+'-'+month+'-'+day
                if result.has_key(key):
                    result[key]+=1
                else:
                    result[key]=1
            except:
                print file,'is except'
    print
    return result

def ansysispic(path):
    result={}
    for root,dirs,files in os.walk(path):
        for file in files:
            file=os.path.join(root,file)
            try:
                c= get_exif_data(file)['DateTimeOriginal']
                key= c[0:10]
                if result.has_key(key):
                    result[key]+=1
                    print key,result[key]
                else:
                    result[key]=1
                    print key,result[key]
            except:
                print file,'is except'
    print 
    return result

def writelog(result,logfile='./log.log'):
    FILE=open(logfile,'a')
    for key in result.keys():
        s='%s|%s' % (key,result[key])
        FILE.write(s+'\n')
    FILE.close()
                
if __name__=='__main__':
    commands=['copy','move','analysis','exit','help']
    while(1):
        #exit
        cmds=raw_input('>>>').lower().strip().split(' ')
        cmd=cmds[0]
        
        if cmd not in commands:
            print cmd,'is not a command.'
            continue
        
        if len(cmds)==1:
            #输入一个参数
            if cmd=='exit':break
            if cmd=='help':
                print '1. copy/move path1 path2(from path1 to path2)'
                print '2. analysis path logfile(analysis path, put result to logfile)'
                print '3. exit'
                print '4. help'
                continue
        if len(cmds)==3:
            #输入三个参数
            cmd,pfrom,pto=cmds[0],cmds[1],cmds[2]
            if cmd=='copy' or cmd=='move':
                #copy/move from path1 to path2
                #>>>copy/move path1 path2

                if pfrom[-1:]!='/' or pfrom[-1:]!='\\':pfrom+='/'
                if pto[-1:]!='/' or pto[-1:]!='\\':pto+='/'

                if os.path.isdir(pfrom)==False:
                    print 'path from is except.'
                    continue
                if os.path.isdir(pto)==False:os.mkdir(pto)

                result=parserpic(pfrom,pto,cmd)

                print 'write log...'
                writelog(result,pto+'log.log')
                print 'log write ok...'
                
            if cmd=='analysis':
                #analysis path to logfile
                #>>>analysis path logfile
                print 'analysis...'

                if pfrom[-1:]!='/' or pfrom[-1:]!='\\':pfrom+='/'
                if os.path.isdir(pfrom)==False:
                    print 'path from is except.'
                    continue               
                
                result=ansysispic(pfrom)
                print 'OK!'
                print 'write log...'
                writelog(result,pto)
                print 'ok!'
                
    sys.exit(0)
