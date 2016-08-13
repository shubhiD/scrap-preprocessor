import pandas as pd
import glob

'''
define similarly
'''

def listing_banner_street_view(lat, lng):
	return "a:5:{s:8:\"latitude\";s:9:\""+str(lat)+"\";s:9:\"longitude\";s:19:\""+str(lng)+"\";s:4:\"zoom\";s:1:\"1\";s:7:\"heading\";s:3:\"-18\";s:5:\"pitch\";s:2:\"25\";}"

def listing_street_view_location(lat, lng):
	return "a:5:{s:8:\"latitude\";s:9:\""+str(lat)+"\";s:9:\"longitude\";s:19:\""+str(lng)+"\";s:4:\"zoom\";s:1:\"1\";s:7:\"heading\";s:3:\"-18\";s:5:\"pitch\";s:2:\"25\";}"


files_li = glob.glob("*_updated.csv")#update path here
fields = ['lat', 'lng']

for file in files_li:
	##################################################
	# create lists here same no. as cols to be added #
	##################################################
	li1 = []; li2 = []

	print file + ' -> ' + file[:file.find('_updated.csv')]+'_filled.csv'
	csv_input = pd.read_csv(file)
	#print csv_input.keys()
	for x in range(len(csv_input.lat)):

		####################
		# create col here  #
		####################
		csv_input['listing_banner_street_view'] = ''
		csv_input['listing_street_view_location'] = ''

		#############################
		# call functions from here  #
		#############################
		li1.append(listing_banner_street_view(csv_input.lat[x], csv_input.lng[x]))
		li2.append(listing_banner_street_view(csv_input.lat[x], csv_input.lng[x]))
		#csv_input.loc[ x ,'listing_banner_street_view'] = listing_banner_street_view(csv_input.lat[x], csv_input.lng[x])
	
	#######################
	# finally change here #
	#######################
	for x in range(len(li1)):
		csv_input.loc[ x ,'listing_banner_street_view'] = li1[x]
		csv_input.loc[ x ,'listing_street_view_location'] = li2[x]

	'''
	# check values of col using this
	for y in csv_input.listing_banner_street_view:
		print y
		print '\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
	'''
	
	
	
	csv_input.to_csv(file[:file.find('_updated.csv')]+'_filled.csv', index=False)




















