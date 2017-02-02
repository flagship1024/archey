# -*- encoding:utf-8 -*-
import os, sys, subprocess, optparse, re, linecache
from subprocess import Popen, PIPE
from optparse import OptionParser
from getpass import getuser
from time import ctime, sleep

# Display [Comment/Uncomment to Enable/Disable information.]
display = [
 'user', # Display Username
 'hostname', # Display Machine Hostname
 'distro', # Display Distribution
 'kernel',  # Display Kernel Version
 'uptime',  # Display System Uptime
 'wm',  # Display Window Manager
 'de', # Display Desktop Environment
 'sh', # Display Current Shell
 'term', # Display Current Terminal
 'packages', # Display Number of Packages Installed
 'cpu', # Display CPU Model
 'ram', # Display RAM Usage
 'disk' # Display Disk Usage
 ]

 
# Array containing Values
result = []

# Options

if __name__=='__main__':
    parser = OptionParser(usage='%prog [-s, --screenshot]', description='Archey is a system information tool written in Python.', version="%prog 0.2.8")
    parser.add_option('-s', '--screenshot',action='store_true', dest='screenshot', help='take a screenshot')
    (options, args) = parser.parse_args()

# Define Colour Scheme
'''
格式: echo "\033[字背景颜色;字体颜色m字符串\033[0m" 
           \x1b[1;31mUser:\x1b[0m root

'''
clear = '\x1b[0m'
blackB = '\x1b[0;30m'
blackB = '\x1b[1;30m'
redN = '\x1b[0;31m'
redB = '\x1b[1;31m'
greenN = '\x1b[0;32m'
greenB = '\x1b[1;32m'
yellowN = '\x1b[0;33m'
yellowB = '\x1b[1;33m'
blueN = '\x1b[0;34m'
blueB = '\x1b[1;34m'
magentaN = '\x1b[0;35m'
magentaB = '\x1b[1;35m'
cyanN = '\x1b[0;36m'
cyanB = '\x1b[1;36m'
whiteN = '\x1b[0;37m'
whiteB = '\x1b[1;37m'

wm_dict = {
 'awesome': 'Awesome',
 'beryl': 'Beryl',
 'blackbox': 'Blackbox',
 'compiz': 'Compiz',
 'dwm': 'DWM',
 'enlightenment': 'Enlightenment',
 'fluxbox': 'Fluxbox',
 'fvwm': 'FVWM',
 'i3': 'i3',
 'icewm': 'IceWM',
 'kwin': 'KWin',
 'metacity': 'Metacity',
 'musca': 'Musca',
 'openbox': 'Openbox',
 'pekwm': 'PekWM',
 'ratpoison': 'ratpoison',
 'scrotwm': 'ScrotWM',
 'wmaker': 'Window Maker',
 'wmfs': 'Wmfs',
 'wmii': 'wmii',
 'xfwm4': 'Xfwm',
 'xmonad': 'xmonad'}

sh_dict = {
 'zsh': 'Zsh',
 'bash': 'Bash',
 'dash': 'Dash',
 'fish': 'Fish',
 'ksh': 'Ksh',
 'csh': 'Csh',
 'jsh': 'Jsh',
 'tcsh': 'Tcsh'}

de_dict = {
 'gnome-session': 'GNOME',
 'ksmserver': 'KDE',
 'xfce4-session': 'Xfce'}
# Find Distro.
DetectDistro = Popen(['lsb_release', '-i'], stdout=PIPE).communicate()[0].split(':')[1].lstrip('\t').rstrip('\n')

def xmonadfix(str):
    if re.compile("xmonad").match(str): return "xmonad"
    return str
p1 = Popen(['ps', '-u', getuser()], stdout=PIPE).communicate()[0].split('\n')
processes = map(xmonadfix, [process.split()[3] for process in p1 if process])
p1 = None
# Print coloured key with normal value.
def output(key, value):
    if DetectDistro == 'Ubuntu':
        output ='%s%s:%s %s' % (redB, key, clear, value)
    result.append(output)

# RAM Function.
def ram_display():
    raminfo = Popen(['free', '-m'], stdout=PIPE).communicate()[0].split('\n')
    ram = ''.join(filter(re.compile('M').search, raminfo)).split()
    used = int(ram[2]) - int(ram[5]) - int(ram[6])
    usedpercent = ((float(used) / float(ram[1])) * 100)
    if usedpercent <= 33:
        ramdisplay = '%s%s MB %s/ %s MB' % (greenB, used, clear, ram[1])
        output('RAM', ramdisplay)
    if usedpercent > 33 and usedpercent < 67:
        ramdisplay = '%s%s MB %s/ %s MB' % (yellowB, used, clear, ram[1])
        output('RAM', ramdisplay)
    if usedpercent >= 67:
        ramdisplay = '%s%s MB %s/ %s MB' % (redB, used, clear, ram[1])
        output('RAM', ramdisplay)

# Screenshot Function.
screen = '%s' % options.screenshot
def screenshot():
    print ('Taking shot in')
    list = range(1,6)
    list.reverse()
    for x in list:
        print("%s.."%x)
        sys.stdout.flush()
        sleep(1)
    print ('Say Cheeze!')
    subprocess.check_call(['scrot'])

# Operating System Function.
def distro_display(): 
    arch = Popen(['uname', '-m'], stdout=PIPE).communicate()[0].rstrip('\n')
    if DetectDistro == 'Ubuntu' or DetectDistro == 'elementary OS':
        release = Popen(['lsb_release', '-r'], stdout=PIPE).communicate()[0].split(':')[1].lstrip('\t').rstrip('\n')
        distro = '%s %s %s' % (DetectDistro, release, arch)
    output('OS', distro)

# Kernel Function.
def kernel_display():
    kernel = Popen(['uname', '-r'], stdout=PIPE).communicate()[0].rstrip('\n')
    output ('Kernel', kernel)

def user_display():
    username= os.getenv('USER')
    output ('User', username)

# Hostname Function.
def hostname_display():
    hostname = Popen(['uname', '-n'], stdout=PIPE).communicate()[0].rstrip('\n')
    output('Hostname', hostname)

# CPU Function.
def cpu_display():
    file = open('/proc/cpuinfo').readlines()
    cpuinfo = re.sub('  +', ' ', file[4].replace('model name\t: ', '').rstrip('\n'))
    output ('CPU', cpuinfo) 

# Uptime Function.
def uptime_display():
    fuptime = int(open('/proc/uptime').read().split('.')[0])
    day = int(fuptime / 86400)
    fuptime = fuptime % 86400
    hour = int(fuptime / 3600)
    fuptime = fuptime % 3600
    minute = int(fuptime / 60)
    uptime = ''
    if day == 1:
        uptime += '%d day, ' % day
    if day > 1:
        uptime += '%d days, ' % day
    uptime += '%d:%02d' % (hour, minute)
    output('Uptime', uptime)

# Desktop Environment Function.
def de_display():
    for key in de_dict.keys():
        if key in processes:
            de = de_dict[key]
            output ('Desktop Environment', de)

# Window Manager Function.
def wm_display():
    for key in wm_dict.keys():
        if key in processes:
            wm = wm_dict[key]
            output ('Window Manager', wm)

# Shell Function.
def sh_display():
    sh = os.getenv("SHELL").split('/')[-1].capitalize()
    output ('Shell', sh)

# Terminal Function.
def term_display():
    term = os.getenv("TERM").split('/')[-1].capitalize()
    output ('Terminal', term)

# Packages Function.
def packages_display():
    if DetectDistro == 'Ubuntu' or DetectDistro == 'elementary OS':
        p1 = Popen(['dpkg', '--get-selections'], stdout=PIPE)
        p2 = Popen(['grep', '-v', 'deinstall'], stdin=p1.stdout, stdout=PIPE)
        p3 = Popen(['wc', '-l'], stdin=p2.stdout, stdout=PIPE)
        packages = p3.communicate()[0].rstrip('\n')
        output ('Packages', packages)

def disk_display():
    p1 = Popen(['df', '-Tlh', '--total', '-t', 'ext4', '-t', 'ext3', '-t', 'ext2', '-t', 'reiserfs', '-t', 'jfs', '-t', 'ntfs', '-t', 'fat32', '-t', 'btrfs', '-t', 'fuseblk'], stdout=PIPE).communicate()[0]
    total = p1.splitlines()[-1]
    used = total.split()[3]
    size = total.split()[2]
    usedpercent = float(re.sub("[A-Z]", "", used)) / float(re.sub("[A-Z]", "", size)) * 100
    if usedpercent <= 33:
        fs = '%s%s %s/ %s' % (greenB, used, clear, size)  
        output ('Disk', fs) 
    if usedpercent > 33 and usedpercent < 67:
        fs = '%s%s %s/ %s' % (yellowB, used, clear, size)  
        output ('Disk', fs) 
    if usedpercent >= 67:
        fs = '%s%s %s/ %s' % (redB, used, clear, size)  
        output ('Disk', fs) 

# Print the locals() content
'''
local = open('local.txt','w')
temp = locals()
print(temp)
local.write(str(temp))
local.close()
'''
# Run functions found in 'display' array.
for x in display:
    funcname=x+'_display'
    func=locals()[funcname]
    func()

# Array containing values.
result.extend(['']*(20 - len(display)))
#print(result)
'''
['\x1b[1;31mUser:\x1b[0m root', 
'\x1b[1;31mHostname:\x1b[0m flagship-1005PX', 
'\x1b[1;31mOS:\x1b[0m Ubuntu 16.04 x86_64', 
'\x1b[1;31mKernel:\x1b[0m 4.4.0-42-generic', 
'\x1b[1;31mUptime:\x1b[0m 1 day, 22:17', 
'\x1b[1;31mShell:\x1b[0m Bash', 
'\x1b[1;31mTerminal:\x1b[0m Xterm-256color', 
'\x1b[1;31mPackages:\x1b[0m 1854', 
'\x1b[1;31mCPU:\x1b[0m Intel(R) Atom(TM) CPU N450 @ 1.66GHz', 
'\x1b[1;31mRAM:\x1b[0m \x1b[1;32m2 MB \x1b[0m/ 982 MB', 
'\x1b[1;31mDisk:\x1b[0m \x1b[1;32m4.8G \x1b[0m/ 229G', '', '', '', '', '', '', '']

'''

# Result.
if DetectDistro == 'Ubuntu':
    print ("""
    %s                          .oyhhs:   %s
    %s                 ..--.., %sshhhhhh-   %s
    %s               -+++++++++`:%syyhhyo`  %s
    %s          .--  %s-++++++++/-.-%s::-`    %s
    %s        .::::-   %s:-----:/+++/++/.   %s
    %s       -:::::-.          %s.:++++++:  %s
    %s  ,,, %s.:::::-`             %s.++++++- %s
    %s./+++/-%s`-::-                %s./////: %s
    %s+++++++ %s.::-                        %s
    %s./+++/-`%s-::-                %s:yyyyyo %s
    %s  ``` `%s-::::-`             %s:yhhhhh: %s
    %s       -:::::-.         %s`-ohhhhhh+  %s
    %s        .::::-` %s-o+///+oyhhyyyhy:   %s
    %s         `.--  %s/yhhhhhhhy+%s,....     %s
    %s               /hhhhhhhhh%s-.-:::;    %s
    %s               `.:://::- %s-:::::;    %s
    %s                         `.-:-'     %s
    %s                                    %s
    %s""") % ( redN, result[0], redB, redN, result[1], redB, redN, result[2], yellowB, redB, redN, result[3], yellowB, redB, result[4], yellowB, redB, result[5], redB, yellowB, redB, result[6], redB, yellowB, redB, result[7], redB, yellowB, result[8], redB, yellowB, redN, result[9], redB, yellowB, redN, result[10], yellowB, redN, result[11], yellowB, redN, result[12], yellowB, redN, yellowB, result[13], redN, yellowB, result[14], redN, yellowB, result[15], yellowB, result[16], yellowB, result[17], clear )

if screen == 'True':
    screenshot()

