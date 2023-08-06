#!/usr/bin/env python

import xml.dom.minidom
import requests
import argparse
import sys
import json

URL = "http://hargharbijli.bsphcl.co.in/WebService/WebServiceGIS.asmx?wsdl/"


def main():
    parser = argparse.ArgumentParser(description="Get smart meter balance")

    parser.add_argument(
        "con_num",
        metavar="Consumer-Number",
        type=int,
        help="enter your consumer number",
    )
    parser.add_argument(
        "-i", "--info", action="store_true", help="show other information"
    )

    args = parser.parse_args()

    con_num = args.con_num

    if len(str(con_num)) != 9:
        sys.exit("Invalid Consumer-Number!")

    data_bal = f"<v:Envelope xmlns:i='http://www.w3.org/2001/XMLSchema-instance' xmlns:d='http://www.w3.org/2001/XMLSchema' xmlns:c='http://schemas.xmlsoap.org/soap/encoding/' xmlns:v='http://schemas.xmlsoap.org/soap/envelope/'><v:Header /><v:Body><GetSMPaymentDetails xmlns='http://bsphcl.co.in/' id='o0' c:root='1'><StrCANumber i:type='d:string'>{con_num}</StrCANumber></GetSMPaymentDetails></v:Body></v:Envelope>"
    data_details = f"<v:Envelope xmlns:i='http://www.w3.org/2001/XMLSchema-instance' xmlns:d='http://www.w3.org/2001/XMLSchema' xmlns:c='http://schemas.xmlsoap.org/soap/encoding/' xmlns:v='http://schemas.xmlsoap.org/soap/envelope/'><v:Header /><v:Body><GetConsumerDtls xmlns='http://bsphcl.co.in/' id='o0' c:root='1'><ConId i:type='d:string'>{con_num}</ConId></GetConsumerDtls></v:Body></v:Envelope>"

    headers_bal = {
        "User-Agent": "ksoap2-android/2.6.0+",
        #"SOAPAction": "http://bsphcl.co.in/GetSMPaymentDetails",
        "Content-Type": "text/xml;charset=utf-8",
        #"Connection": "close",
        #"Accept-Encoding": "gzip",
        #"Host": "hargharbijli.bsphcl.co.in",
    }
    headers_details = {
        "User-Agent": "ksoap2-android/2.6.0+",
        #"SOAPAction": "http://bsphcl.co.in/GetConsumerDtls",
        "Content-Type": "text/xml;charset=utf-8",
        #"Connection": "close",
        #"Accept-Encoding": "gzip",
        #"Host": "hargharbijli.bsphcl.co.in",
    }

    if args.info:
        res_json = fetch(data_details, headers_details, "GetConsumerDtlsResult")
    else:
        res_json = fetch(data_bal, headers_bal, "GetSMPaymentDetailsResult")

    print(json.dumps(res_json, indent=2))


def fetch(data, headers, search):
    try:
        response = requests.post(
            URL,
            headers=headers,
            data=data,
        )
    except requests.RequestException as e:
        print("Error: {}".format(e))
        sys.exit()

    res_text = response.text
    # print(res_text)

    domtree = xml.dom.minidom.parseString(res_text)
    group = domtree.documentElement

    search = group.getElementsByTagName(search)[0].childNodes[0].nodeValue
    try:
        res_json = json.loads(search)
    except Exception as e:
        print("Server error!")
        sys.exit()


    return res_json


if __name__ == "__main__":
    main()
