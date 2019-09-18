#
#
red_clr = "\033[1;33;31m"     # red
green_clr = "\033[1;33;32m"   # green
yellow_clr = "\033[1;33;33m"  # yellow
blue_clr = "\033[1;33;34m"    # blue
pink_clr = "\033[1;33;35m"    # pink
cyan_clr = "\033[1;33;36m"    # cyan
d_color = "\033[0m"           # default
#
import sys, getopt

def help_text():
    print("\n")
    print("Format Example : check_log -h[--help] ")
    print("                 check_log -i[--filename] inputfilename")
    print("\n")

def title():
	print("   ===============================================")
	print("   ===              Checked Result            ====")
	print("   ===============================================")
	print("\n")	
	
	
def check_log(Fname):
    # read string from file 
	k_str = []                                                   # k_str : read from string.txt contains string what user want to check
	f = open("string.txt", "r", encoding="utf-8")                # string.txt : key in string by user
	str1 = f.readlines()
	f.close()
	
	for i in range(len(str1)):
		k_str.append(str1[i].strip().lower())                    # read file and assign to a list k_str /  str1.strip() : delete "\n"

	k_cnt = [ 0 for n in range(len(k_str)) ]                     # k_cnt : according to k_str to create the default veluae 0 for each string

	f = open(Fname, "r", encoding="utf-8")
	article = f.readlines()
	f.close()

	title()
	
	for context in article:
		for i in range(len(k_str)):
			if k_str[i] in context.lower():
				k_cnt[i] = k_cnt[i] + 1
	for i in range(len(k_str)):
		print("    [ "+ k_str[i] + " ] ..............." + str(k_cnt[i]))
	print("\n")

if __name__ == '__main__':	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "-h-v-i:", ["help","version",'filename='])
		for opt_name, opt_value in opts:
			if opt_name in("-h", "--help"):
				help_text()
				exit()
			if opt_name in("-v", "--version"):
				print("# version information")
				exit()
			if opt_name in ("-i", "--filename"):
				FileName = opt_value
				check_log(FileName)
				exit()
	except getopt.GetoptError:
		help_text()
