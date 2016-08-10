import pandas as pd
import numpy as np
import glob


files_li = glob.glob("*.csv")#update path here
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

	csv_input.to_csv(x[:x.find('.csv')]+'_updated.csv', index=False)