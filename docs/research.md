# Research

A POST request is made to `https://tools.usps.com/tools/app/ziplookup/zipByAddress`. In
this request's headers are the address data, formatted as form parameters:

```
companyName=&address1=1600+Pennsylvania+Ave+NW&address2=&city=Washington&state=DC&urbanCode=&zip=20500
```

The `urbanCode` parameter isn't listed as an option in the standard form, but I think it shows up
when you specify Puerto Rico as the state (and perhaps some other "states.").

The response to the request is as follows:

```
{
    "resultStatus": "SUCCESS",
    "addressList": [{
        "addressLine1": "1600 PENNSYLVANIA AVE NW",
        "city": "WASHINGTON",
        "state": "DC",
        "zip5": "20500",
        "zip4": "0005",
        "carrierRoute": "C000",
        "countyName": "DISTRICT OF COLUMBIA",
        "deliveryPoint": "00",
        "checkDigit": "8",
        "cmar": "N",
        "elot": "0002",
        "elotIndicator": "A",
        "recordType": "S",
        "dpvConfirmation": "Y",
        "defaultFlag": "",
        "defaultInd": "E"
    }]
}
```

`resultStatus` can be one of a few values:

* `SUCCESS`
* `INVALID-ZIPCODE`. This means an invalid zip code was given and USPS didn't have enough data
to make an address match.
* `ADDRESS NOT FOUND`. USPS didn't have enough address data to make a match.
* `INVALID-CITY`. An invalid city was given and USPS didn't have enough data to make a match.

The API (at least, as exposed through the form) needs either city/state, state/zip, or city/zip
specified. If none of those combinations are specified, don't make the API call.