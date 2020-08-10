import requests
import argparse

# If we don't specify a user agent like this, the USPS website apparently sends
# us into endless redirects. Charming.
HEADERS = {
	'User-Agent':	'Mozilla/5.0'
}

USPS_URL = 'https://tools.usps.com/tools/app/ziplookup/zipByAddress'
TIMEOUT = 30

def main(args):
	# Note that we don't need to replace spaces with pluses in the data passed
	# in the URL. I tried converting the spaces, and the USPS website didn't
	# like that.
	payload = { 'companyName': args.company,
				'address1': args.address1,
				'address2': args.address2,
				'city': args.city,
				'state': args.state,
				'urbanCode': args.urbanCode,
				'zip': args.zip
				}

	# set default timeout if none is specified
	if args.timeout != None:
		timeout = args.timeout
	else:
		timeout = TIMEOUT

	# check that either city/state, state/zip, or city/zip are specified, else
	# don't check and return an error message
	if is_missing_city_state_zip(payload['city'], payload['state'], payload['zip']):
		print('ERROR: Please specify either city and state, state and zip, or city and zip.')
		return

	usps_response = lookup_address(payload, timeout)
	if usps_response != None:
		print(usps_response.json())

def lookup_address(address_dict, timeout):
	assert not is_missing_city_state_zip(address_dict['city'], address_dict['state'], address_dict['zip']), "Need city/state, state/zip, or city/zip specified!"
	try:
		r = requests.post(USPS_URL, headers=HEADERS, data=address_dict, timeout=timeout)
		return r
	except requests.exceptions.ReadTimeout as e:
		print('Timeout contacting usps.com')

def is_missing_city_state_zip(city, state, zip):
	# check that either city/state, state/zip, or city/zip are specified
	err_missing_value = False
	if city == None and not (state != None and zip != None):
		err_missing_value = True
	elif state == None and not (city != None and zip != None):
		err_missing_value = True
	elif zip == None and not (city != None and state != None):
		err_missing_value = True
	
	return err_missing_value

def setup_argument_parser():
	parser = argparse.ArgumentParser(description='Lookup a US address at USPS.com')
	parser.add_argument('--company', type=str)
	parser.add_argument('--address1', type=str, required=True)
	parser.add_argument('--address2', type=str)
	parser.add_argument('--city', type=str)
	parser.add_argument('--state', type=str)
	parser.add_argument('--urbanCode', type=str, help='Urbanization Code (only applies to Puerto Rico)')
	parser.add_argument('--zip', type=str)
	parser.add_argument('--timeout', type=float, help='Timeout (default of ' + str(TIMEOUT) + ' secs)')
	return parser

if __name__ == '__main__':
	parser = setup_argument_parser()
	args = parser.parse_args()
	main(args)