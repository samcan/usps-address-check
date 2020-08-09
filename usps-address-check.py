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
	# TODO replace spaces with + symbols
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

	try:
		r = requests.post(USPS_URL, headers=HEADERS, data=payload, timeout=timeout)
		print(r.json())
	except requests.exceptions.ReadTimeout as e:
		print('Timeout contacting usps.com')
	


def setup_argument_parser():
	parser = argparse.ArgumentParser(description='Lookup a US address at USPS.com')
	parser.add_argument('--company', type=str)
	parser.add_argument('--address1', type=str, required=True)
	parser.add_argument('--address2', type=str)
	parser.add_argument('--city', type=str)
	parser.add_argument('--state', type=str)
	parser.add_argument('--urbanCode', type=str)
	parser.add_argument('--zip', type=str)
	parser.add_argument('--timeout', type=float, help='Timeout (default of ' + str(TIMEOUT) + ' secs)')
	return parser

if __name__ == '__main__':
	parser = setup_argument_parser()
	args = parser.parse_args()
	main(args)