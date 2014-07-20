#!/usr/bin/env python
import libvirt
import argparse
import sys
from xml.etree import ElementTree as ET


parser = argparse.ArgumentParser()
group1 = parser.add_argument_group('VM Control')
group1.add_argument('name', type=str, nargs="?", help="name of the virtual machine")
group1.add_argument('--start', '-s', default=False, action="store_true", help="power on a virtual machine")
group1.add_argument('--poweroff', '-p', default=False, action="store_true", help="power off a virtual machine")
group1.add_argument('--restart', '-r', default=False, action="store_true",help="power off a virtual machine")
group2 = parser.add_argument_group('Display Options')
group2.add_argument("-l", "--list", action="store_true", help="list all virtual machines with stats")
group3 = parser.add_argument_group('Snapstop Options')
group3.add_argument('desc', type=str, nargs="?", help="description of the snapshot")
group3.add_argument('--snapshot', default=False, action="store_true",help="create a online virtual machine snapshot")
args = parser.parse_args()


def connect():
  conn = libvirt.open("qemu:///system")
  return conn 


def find_element(name):
  dom = connect().lookupByName(name)
  dom_info = ET.fromstring(dom.xmlDesr)
  disks = xml_disks = dom_info.findall('.//disk')
  
  for disk in disks:
    oldpath = disk.find('source').get('file')
    dev = disk.find('target').get('dev')
  return oldpath, dev 


#def create_snap_xml(desc, oldpath, newpath, dev):
#  templatexml = \
#  '''<domainsnapshot>
#  <description>{desc}</description>
#  <disks>
#    <disk name='{oldpath}'>
#      <source file='{newpath}{snapshot}'/>
#    </disk>
#    <disk name='{dev}' snapshot='yes'/>
#  </disks>
#</domainsnapshot>
#'''
#  snapshotxml = templatexml.dormat(desc=desc, oldpath=oldpath, newpath=newpath, dev=dev)
#return snapshotxml


#def create_snapshot(name, desc):
#  dom = conn.lookupByName(name)
#  for xmlinfo in find_element(name):
#    snapxml += create_snap_xml(desc, newpath, xmlinfo)
#  return snapxml#

#  dom.snapshotCreateXML(snapxml)


def listvms():
  onlinedomid = ([connect().lookupByID(id) for id in connect().listDomainsID()])
  offlinedomid = ([connect().lookupByName(domname) for domname in connect().listDefinedDomains()])

  print 'Online VMS'
  print ''
  for dom in onlinedomid:
    infos = dom.info()
    print 'Name =  %s' % dom.name()
    print 'Max Memory = %d' % infos[1]
    print 'Number of virt CPUs = %d' % infos[3]
    print 'CPU Time (in ns) = %d' % infos[2]
    print ''
  return


  print 'Offline VMs'
  print ''
  for dom in offlinedomid:
    infos = dom.info()
    print 'Name =  %s' % dom.name()
    print 'Max Memory = %d' % infos[1]
    print 'Number of virt CPUs = %d' % infos[3]
    print 'CPU Time (in ns) = %d' % infos[2]
    print ''
  return


def start(name):
  try:
    dom = connect().lookupByName(name)
  except:
    print 'Could not find the VM named %s' % name
    sys.exit(1)

  dom.create()
  print 'Virtual machine %s has been started' % dom.name()


def stop(name):
  try:
    dom = connect().lookupByName(name)
  except:
    print 'Could not find the VM named %s' % name
    sys.exit(1)

  dom.destroy()


#def snapshot(name, decription):
#  try:
#    dom = connect().lookupByName(name)
#  except:
#    print 'Could not find the VM named %s' % name
#    sys.exit(1)


def reset(name):
  from time import sleep

  try:
    dom = connect().lookupByName(name)
  except:
    print 'Could not find the VM named %s' % name
    sys.exit(1)

  dom.reset()
  sleep(2)
  print 'Virtual Machine %s has been reset' % dom.name()


if args.list and args.name == None:
    listvms()


if args.name != None:
    print ("preforming action on " + args.name)
if args.start == True:
    start(args.name)
elif args.poweroff == True:
    stop(args.name)
elif args.restart == True:
    reset()



