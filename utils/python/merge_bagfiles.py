#!/usr/bin/python
import sys
import logging
import rosbag
import argparse
  
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(name)s: %(message)s', datefmt='%I:%M:%S %p')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def MergeBagfiles(bagfiles_list, merged_bagfile):
  logger.info( "bagfiles:\n\t* " + "\n\t* ".join(bagfiles_list) )
  with rosbag.Bag(merged_bagfile, 'w') as outbag:
    for input_bagfile in bagfiles_list:
      for topic, msg, t in rosbag.Bag(input_bagfile, 'r').read_messages():
        outbag.write(topic, msg, t)
  logger.info('finished merging to ' + merged_bagfile)

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='merge two or more ROS bagfiles sequentially')
  parser.add_argument('--bagfiles', metavar='BAGFILES', type=str, nargs='+', help='list of bagfiles to merge (in order)', required=True)
  parser.add_argument('--out', metavar='OUTFILE', type=str, help='output bag file', default='merged.bag')
  
  args = parser.parse_args()
  
  if len(args.bagfiles) < 2:
    logger.warn('less than 2 bagfiles specified. aborting...')
  else:
    MergeBagfiles(args.bagfiles, args.out)
