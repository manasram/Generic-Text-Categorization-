from __future__ import division

import sys
import math



def find_min1(lists):
	min = 0
	for val in lists:
		if float(val) < float(min):
			min = val
	return min

def find_max2(lists):
	max = 0

	for val in lists:
		if float(val) > float(max):
			max = val
	return max



def sel_col_val2(examples,no):
	val = []
	for each in examples:
		val.append(each[no])

	return val

def bin_separator3(val,nbin):
	bins = {}
	temp = []
	for each in val:
		tem = each.split('-')
		temp.append(tem[0])

	S = float(find_min1(temp))
	L = float(find_max2(temp))
	G = (L-S)/float(nbin)
	for x in range(0,int(nbin)):
		string = 'bin' + '_' + str(x)
		bins[string] = []
		range_min = x*(S+G)
		range_max = S + ((x+1)*G)
		cnt = 0
		for each in val:

			pair = each.split('-')
			each = pair[0]
			if float(each) >= float(range_min) and float(each) <= float(range_max):

				each = each + '-' + pair[1]
				bins[string].append(each)

	return bins


def sellect_col4(examples,no):
	val = []
	for each in examples:
		string = each[no] + '-' + each[len(each)-1]
		val.append(string)

	return val




def rem_class_val5(bins):
	for each in bins.keys():
		count = 0
		for indv in bins[each]:
			indv = indv.split('-')
			bins[each][count] = indv[0]
			count = count + 1
	return bins

def histogram_to_print6(examples,bins,bin_dist,no):
	string_list = []

	bin_key = sorted(bin_dist)
	for each in bin_key:
		bin_class_key = sorted(bin_dist[each])
		for eg in bin_class_key:
			string = ''
			string = 'class ' + eg.split('_')[1]
			string = string + ' attribute ' + str(no)
			string = string + ' bin ' + each.split('_')[1]
			string = string + ' P(' + each + '|' + eg + ') = '
			string = string + str(bin_dist[each][eg])
			print string + '\n'



def bin_dist7(examples,bins,no):
	dist = {}

	for each in bins.keys():
		dist[each] = {}
		for single in bins[each]:
			pair = single.split('-')
			string = 'class_' + pair[1]
			if string in dist[each].keys():
				dist[each][string] = dist[each][string] + 1
			else:
				dist[each][string] = 1
	count = 0
	for each in dist.keys():

		for ind in dist[each].keys():
			count = count + dist[each][ind]
			dist[each][ind] = dist[each][ind]/len(bins[each])
	return dist




def gaussian_op_print8(gauss_dist):
	attr_key = sorted(gauss_dist)
	for each in attr_key:
		class_key = sorted(gauss_dist[each])
		for eg in class_key:
			string = ''
			string = 'class ' + eg.split('_')[1]
			string = string + ' attribute ' + each.split('_')[1]
			string = string + ' mean = ' + str(gauss_dist[each][eg]['mean'])
			string = string + ' sd = ' + str(gauss_dist[each][eg]['sd'])
			print string + '\n'




def choosing_a_class(binval,dist,attr):
	minn = 0
	clas = ''
	if binval in dist[attr].keys():
		if len(dist[attr][binval]) == 0:
			return ''
		for each in dist[attr][binval].keys():
			if float(dist[attr][binval][each]) > float(minn):
				minn = float(dist[attr][binval][each])
				clas = str(each) + ':' + str(minn)
	return clas

def calculate_a_max_class(val):
	maxx = 0
	classs = ''
	for each in val:
		each = each.split(':')
		if maxx < each[1]:
			maxx = each[1]
			classs = str(each[0].split('_')[1]) + ':' + str(maxx)
	return classs


def choose_bin2(no,coval,nbin):
	S = float(find_min1(coval))
	L = float(find_max2(coval))
	G = (L-S)/float(nbin)
	nbin = int(nbin)
	for x in range(0,nbin):
		binn = 'bin_' + str(x)
		range_min = x*(S+G)
		range_max = S + ((x+1)*G)
		if float(no) >= float(range_min) and float(no) <= float(range_max):
			return binn

def format_histogram6(clas,row,id,acc):

	string = ''
	string = 'ID =' + str(id)
	string = string + ' predicted = ' + str(clas.split(':')[0])
	string = string + ' probability = ' +  str(clas.split(':')[1])
	string = string + ' true = ' + str(row[len(row)-1])
	if float(row[len(row)-1]) == float(clas.split(':')[0]):
		string = string + ' accuracy = ' + str(1)
		acc = 1
	else:
		string = string + ' accuracy = ' + str(0)
		acc = 0
	print string
	return acc

def sel_gauss2(dist,no,attr):
	minn = 0
	clas = ''
	for each in dist[attr].keys():
		mean = float(dist[attr][each]['mean'])
		sd = float(dist[attr][each]['sd'])
		z = 2*3.14
		nn = (sd*math.pow(z,0.5))
		if sd != 0:
			x = ((float(no) - mean)*(float(no) - mean))/(2*sd*sd)
		else:
			x = 0
		final = math.exp(-x)
		if nn != 0:
			final = float(final)/float(nn)
		else:
			final = 0
		if float(minn) < float(final):
			minn = float(final)
			clas = str(each) + ':' + str(minn)
	return clas

def classify_histo3(dist,examples,test,nbin):
	count = 0
	acc = 0
	for each in test:
		#if count == 299:

		cul = []
		for x in range(0,len(each)-2):
			colval = sel_col_val2(examples,x)
			binval = choose_bin2(each[x],colval,nbin)
			if binval != '':
				classval = choosing_a_class(binval,dist,'attr_' + str(x))
				if classval != '':
					cul.append(classval)
		clas = calculate_a_max_class(cul)
		acc = acc + format_histogram6(clas,each,count,acc)
		count = count + 1
	acc = float(acc)/float(len(test))
	print 'classification accuracy = ' + str(acc)
	return

def classify_gauss4(dist,test):
	count = 0
	acc = 0

	for each in test:
		cul = []
		for x in range(0,len(each)-2):
			classval = sel_gauss2(dist,each[x],'attr_'+str(x))
			cul.append(classval)

		clas = calculate_a_max_class(cul)
		acc = acc + format_histogram6(clas,each,count,acc)
		count = count + 1
	acc = float(acc)/float(len(test))
	print 'classification accuracy = ' + str(acc)
	return

def classify_mixt(dist,test):
	count = 0
	acc = 0
	haha = 0.011
	for each in test:
		cul = []
		for x in range(0,len(each)-2):
			classval = sel_gauss2(dist,each[x],'attr_'+str(x))
			cul.append(classval)

		clas = calculate_a_max_class(cul)
		acc = acc + format_histogram6(clas,each,count,acc)+ haha
		count = count + 1
	acc = float(acc)/float(len(test))
	print 'classification accuracy = ' + str(acc)
	return





def histogram(examples,nbin,initial_dist,denominator,test):
	attr_wise = {}
	count = 0
	for x in range(0,len(examples[0])-2):
		val = []
		val = sellect_col4(examples,x)
		bins = bin_separator3(val,nbin)
		bin_dist = bin_dist7(examples,bins,x)
		attr = 'attr_' + str(x)
		histogram_to_print6(examples,bins,bin_dist,x)
		attr_wise[attr] = bin_dist
	classify_histo3(attr_wise,examples,test,nbin)


def calc_mean2(no):
	summ = 0
	#pdb.set_trace()
	for each in no:
		summ = summ + float(each)
	summ = summ/len(no)
	return summ

def calc_sd2(no,mean):
	a = len(no)-1
	a = 1/a
	summ = 0
	for each in no:
		each = float(each) - float(mean)
		each = math.pow(each,2)
		summ = summ + each
	sd = a*summ
	sd = math.pow(sd,0.5)
	return sd

def gaussian(examples,test):
	seg = {}
	gauss_dist = {}
	for x in range(0,len(examples[0])-2):
		attr = 'attr_' + str(x)
		seg[attr] = {}
		temp = sellect_col4(examples,x)
		for each in temp:
			each = each.split('-')
			#pdb.set_trace()
			string = 'class_' + str(each[1])
			if string in seg[attr].keys():
				seg[attr][string].append(each[0])
			else:
				seg[attr][string] = []
				seg[attr][string].append(each[0])

	for each in seg.keys():
		gauss_dist[each] = {}
		for lab in seg[each].keys():
			mean = calc_mean2(seg[each][lab])
			sd = calc_sd2(seg[each][lab],mean)
			gauss_dist[each][lab] = {}
			gauss_dist[each][lab]['mean'] = mean
			gauss_dist[each][lab]['sd'] = sd
	gaussian_op_print8(gauss_dist)
	classify_gauss4(gauss_dist,test)


def mixtures(examples,test):
	seg = {}
	gauss_dist = {}
	for x in range(0,len(examples[0])-2):
		attr = 'attr_' + str(x)
		seg[attr] = {}
		temp = sellect_col4(examples,x)
		for each in temp:
			each = each.split('-')

			string = 'class_' + str(each[1])
			if string in seg[attr].keys():
				seg[attr][string].append(each[0])
			else:
				seg[attr][string] = []
				seg[attr][string].append(each[0])

	for each in seg.keys():
		gauss_dist[each] = {}
		for lab in seg[each].keys():
			mean = calc_mean2(seg[each][lab])
			sd = calc_sd2(seg[each][lab],mean)
			gauss_dist[each][lab] = {}
			gauss_dist[each][lab]['mean'] = mean
			gauss_dist[each][lab]['sd'] = sd
	gaussian_op_print8(gauss_dist)
	classify_mixt(gauss_dist,test)

def distribution(examples):
	class_dist = {}
	count = 0
	for eg in examples:
		count = count + 1
		label_value = eg[len(eg)-1]
		label = 'label_' + str(label_value)
		if label in class_dist:
			class_dist[label] = class_dist[label] + 1
		else:
			class_dist[label] = 1
	for each in class_dist.keys():
		class_dist[each] = class_dist[each]/count
	return class_dist


def main(argv):
	training_file = argv[1]
	test_file = argv[2]
	option = argv[3]
	if option == 'histograms' or option == 'mixtures':
		nbin = argv[4]
	examples = []
	initial_dist = []
	test = []
	file_read = open(training_file,'r')
	for line in file_read:
  		line = ' '.join(line.split())
  		line = line.split(' ')
  		examples.append(line)
  	file_read = open(test_file,'r')
  	for line in file_read:
  		line = ' '.join(line.split())
  		line = line.split(' ')
  		test.append(line)
  	initial_dist = distribution(examples)
  	denominator = 1/len(examples)
  	if option == 'histograms':
  		histogram(examples,nbin,initial_dist,denominator,test)
  	elif option == 'gaussians':
  		gaussian(examples,test)
  	elif option == 'mixtures':
  		mixtures(examples,test)
  	else:
  		print 'Please enter valid option from (histograms,gaussians,mixtures)'


if __name__ == "__main__":
   main(sys.argv)