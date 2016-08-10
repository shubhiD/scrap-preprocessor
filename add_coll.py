import pandas as pd
import glob


files_li = glob.glob("processed_*.csv")#update path here
count = 1
for x in files_li:

	#x='input.csv'
	csv_input = pd.read_csv(x)

	###adding cols
	csv_input['listing_banner_map_marker'] = 'on'
	csv_input['listing_banner_map_type'] = 'ROADMAP'
	csv_input['listing_banner_map_zoom'] = '16'
	csv_input['listing_inside_view_location'] = ''
	csv_input['listing_inside_view_location_latitude'] = ''
	csv_input['listing_inside_view_location_longitude'] = ''
	csv_input['listing_inside_view_location_zoom'] = '16'
	csv_input['listing_google_street_view_latitude'] = ''
	csv_input['listing_google_street_view_longitude'] = ''
	csv_input['listing_google_street_view_zoom'] = '16'
	csv_input['listing_banner_street_view_latitude'] = ''
	csv_input['listing_banner_street_view_longitude'] = ''
	csv_input['listing_banner_street_view_zoom'] = '16'
	csv_input['claim_name'] = csv_input['Name']	# TO assign values of 1 col to new col
	#csv_input['claim_phone']
	#csv_input['listing_description] = csv_input['About']
	#csv_input['listing_address'] = csv_input['Address']
	#csv_input['listing_email'] = csv_input['Mail']
	#csv_input['listing_gallery'] = csv_input['Images URL']
	#csv_input['listing_google_address']
	#csv_input['listing_google_map'] = csv_input['Address']
	#csv_input['listing_phone'] 
	#csv_input['listing_inside_view_location']
	#csv_input['listing_map_location'] = csv_input['Address']
	#csv_input['listing_street_view_location']

	#csv_input['post_category'] = csv_input['Services Offered']
	#csv_input['post_tag'] = csv_input['Services Offered']
	#csv_input['categories'] = csv_input['Services Offered']

	###renaming 
	csv_input.rename( columns = {
									'Name'   :  'post_title',
									'About'  :  'post_content',
									'Mail'   :  'claim_email',
									'listing_name' : 'claim_name'
									###phone
									###listing_description
									#'Address'

								}, inplace = True )
	
	print(count)
	count+=1

	csv_input.to_csv(x[:x.find('.csv')]+'_updated.csv', index=False)
