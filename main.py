from distutils.log import error
from fileinput import filename
from module.ZoomChat2Srt import ZoomChat2Txt
import argparse

parser = argparse.ArgumentParser(
  prog = "ZoomChat2Srt",
  description = "Convert Zoom chat text file into subtitle srt file",
  usage="python main.py \"meeting_saved_chat.txt\""
)

parser.add_argument(
  '-o',
  '--output-path',
  type= str,
  help= "Optional output file_path"
)

parser.add_argument(
  metavar="file_path",
  type=str,
  dest="file_path",
  help="location (file path) of the zoom chat txt file"
)

def split_filename_and_ext(file_path):
  *file_name, ext = file_path.split('.')
  file_name = '.'.join(file_name)
  
  return file_name, ext
  
if __name__ == "__main__":
  args = parser.parse_args()
  file_name, ext = split_filename_and_ext(args.file_path)
  if ext.lower() != 'txt':
    raise Exception("Sorry, this app supports txt file only. Please check your file extension")

  zchat2srt = ZoomChat2Txt(args.file_path)

  if args.output_path:
    file_name, ext = split_filename_and_ext(args.output_path)
    if ext.lower() != 'srt':
      raise Exception("Sorry, this app supports exporting srt file only. Please check your file extension")
  
  zchat2srt.save_srt(file_name + '.srt')

  



