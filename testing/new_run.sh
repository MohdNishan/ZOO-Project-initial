#!/bin/bash
#
# Author : Gérald FENOY
#
# Copyright 2011-2014 GeoLabs SARL. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

Usage=$(cat <<EOF
Please use the following syntaxe:

  ./run.sh <WPSInstance> <ServiceName> <Request>

where <WPSInstance> should be the url to a WPS Server, <ServiceName> should 
be the service name you want to run tests with (you can use multiple service 
names, use quote and seperate them using space), <Request> should contain the 
requests you want to use (you can use more than one at a time).

For instance to test the Buffer service on a localhost WPS server, use the 
following command:

  ./run.sh http://localhost/cgi-bin/zoo_loader.cgi Buffer "GetCapabilities DescribeProcess Execute"

EOF
)

echo "Starting script..."
echo "WPSInstance: $1"
echo "ServiceName: $2"
echo "Requests: $3"
echo "WPSVersion: $4"


if [ -z "$4" ]; then
    WPSVersion="1.0.0"
else
    WPSVersion=$4
fi


WPSInstance=$1
ServiceName=$2
NBRequests=1000
NBConcurrents=50
pstat=0

iter=0

function testPostRequests {
#
# Tests for Execute using POST requests
#
    for i in $1; 
    do
	cat requests/${i}.xml | sed "s:ServiceName:${ServiceName}:g;s:InputName:$(cat tmp/inputName.txt):g" > tmp/${i}1.xml
	if [ -z "$(echo $i | grep async)" ]; then
	    postRequest "${WPSInstance}" "tmp/outputE${i}.xml" "Execute" "tmp/${i}1.xml"
	else
	    postRequest "${WPSInstance}" "tmp/outputE${i}.xml" "Execute" "tmp/${i}1.xml" "async"
	fi
	echo ""
    done
}

function plotStat {
    echo " **"
    echo " * Plot statistics ..."
    echo " **"
    cp run.tsv tmp/run$1.tsv
    sed "s:\[image\]:$2:g;s:\[file\]:$3:g" -i tmp/run$1.tsv
    gnuplot tmp/run$1.tsv
    cp run1.tsv tmp/run1$1.tsv
    sed "s:\[image\]:$(echo $2 | sed "s:.jpg:1.jpg:g"):g;s:\[file\]:$3:g" -i tmp/run1$1.tsv
    gnuplot tmp/run1$1.tsv
}


function kvpRequest {
    echo " **"
    echo " <h1> Simple KVP request start on $(date) </h1>"
    echo " <a href='$1&VERSION=${WPSVersion}'>$1&VERSION=${WPSVersion}</a>"

    RESP=$(curl -v -o "$2" "$1&VERSION=${WPSVersion}" 2> testing/tmp/temp.log; grep "< HTTP" testing/tmp/temp.log | cut -d' ' -f3)

    if [ "${WPSVersion}" == "2.0.0" ]; then
        echo " * Checking for ${3} response XML validity..."
        xmllint --noout --schema http://schemas.opengis.net/wps/2.0/wps${3}_response.xsd "$2"
    else
        echo " * Checking for ${3} response XML validity..."
        xmllint --noout --schema http://schemas.opengis.net/wps/1.0.0/wps${3}_response.xsd "$2"
    fi
}



function postRequest {
    echo " **"
    echo " * Simple POST request started on $(date)"
    echo " **"
    echo " * Checking for ${3} request XML validity..."
    xmllint --noout --schema http://schemas.opengis.net/wps/${WPSVersion}/wps${3}_request.xsd "$4" 

    curl -H "Content-type: text/xml" -d@"$4" -o "$2" "$1"

    echo " * Checking for ${3} response XML validity on $(date) ..."
    xmllint --noout --schema http://schemas.opengis.net/wps/${WPSVersion}/wps${3}_response.xsd "$2"

    ab -g tmp/stat${3}${iter}.plot -e tmp/stat${3}${iter}.txt -T "text/xml" -p "$4" -n "$NBRequests" -c "$NBConcurrents" "$1"
}


function kvpRequestWrite {
    suffix=""
    cnt=0
    cnt0=0
    for i in $2; do
	if [ ! $1 -eq $cnt0 ]; then
	    if [ $cnt -gt 0 ]; then
		suffix="$suffix&$(echo $i | sed 's:\"::g')"
	    else
		suffix="$(echo $i | sed 's:\"::g')"
	    fi
	    cnt=$(expr $cnt + 1)
	fi
	cnt0=$(expr $cnt0 + 1)
    done
    echo $suffix
}

function kvpWrongRequestWrite {
    suffix=""
    cnt=0
    cnt0=0
    for i in $2; do
	if [ ! $1 -eq $cnt0 ]; then
	    if [ $cnt -gt 0 ]; then
		suffix="$suffix&$(echo $i | sed 's:\"::g')"
	    else
		suffix="$(echo $i | sed 's:\"::g')"
	    fi
	    cnt=$(expr $cnt + 1)
	else
	    cnt1=0
	    for j in $3; do 
		if [ $cnt1 -eq $1 ]; then
		    suffix="$suffix&$(echo $j | sed 's:\"::g')"
		fi
		cnt1=$(expr $cnt1 + 1)
	    done
	fi
	cnt0=$(expr $cnt0 + 1)
    done
    echo $suffix
}

for i in $3; do
    if [ "$i" == "GetCapabilities" ]; then
        kvpRequest "${WPSInstance}?REQUEST=GetCapabilities&SERVICE=WPS&VERSION=${WPSVersion}" "tmp/outputGC.xml" "GetCapabilities"
    fi

    if [ "$i" == "DescribeProcess" ]; then
        kvpRequest "${WPSInstance}?request=DescribeProcess&service=WPS&version=${WPSVersion}&Identifier=${ServiceName}" "tmp/outputDP.xml" "DescribeProcess"
    fi

    if [ "$i" == "Execute" ]; then
    for req in ijson_o igml_o ir_o ir_or irb_o irb_or ir_o_async ir_or_async irb_o_async irb_or_async; do
        if [ ! -f "requests/${req}.xml" ]; then
            echo "Error: requests/${req}.xml not found!" >&2
            exit 1
        fi
    done

    testPostRequests "ijson_o igml_o ir_o ir_or irb_o irb_or ir_o_async ir_or_async irb_o_async irb_or_async"
fi

done    