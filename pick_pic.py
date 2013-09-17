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
def getvalue(result,key='Make'):
    '''
    Image Description 图像描述、来源. 指生成图像的工具
    Artist作者 有些相机可以输入使用者的名字
    Make 生产者 指产品生产厂家
    Model 型号 指设备型号
    Orientation方向 有的相机支持，有的不支持
    XResolution/YResolution X/Y方向分辨率 本栏目已有专门条目解释此问题。
    ResolutionUnit分辨率单位 一般为PPI
    Software软件 显示固件Firmware版本
    DateTime日期和时间
    YCbCrPositioning 色相定位
    ExifOffsetExif信息位置，定义Exif在信息在文件中的写入，有些软件不显示。
    ExposureTime 曝光时间 即快门速度
    FNumber光圈系数
    ExposureProgram曝光程序 指程序式自动曝光的设置，各相机不同,可能是Sutter Priority（快门优先）、Aperture Priority（快门优先）等等。
    ISO speed ratings感光度
    ExifVersionExif版本
    DateTimeOriginal创建时间
    DateTimeDigitized数字化时间
    ComponentsConfiguration图像构造（多指色彩组合方案）
    CompressedBitsPerPixel(BPP)压缩时每像素色彩位 指压缩程度
    ExposureBiasValue曝光补偿。
    MaxApertureValue最大光圈
    MeteringMode测光方式， 平均式测光、中央重点测光、点测光等。
    Lightsource光源 指白平衡设置
    Flash是否使用闪光灯。
    FocalLength焦距，一般显示镜头物理焦距，有些软件可以定义一个系数，从而显示相当于35mm相机的焦距
    MakerNote(User Comment)作者标记、说明、记录
    FlashPixVersionFlashPix版本 （个别机型支持）
    ColorSpace色域、色彩空间
    ExifImageWidth(Pixel X Dimension)图像宽度 指横向像素数
    ExifImageLength(Pixel Y Dimension)图像高度 指纵向像素数
    Interoperability IFD通用性扩展项定义指针 和TIFF文件相关，具体含义不详
    FileSource源文件 Compression压缩比。
    '''
    keys=result.keys()
    if key not in keys:
        return False
    return result[key]

def getkeys(result):
    return result.keys()

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
