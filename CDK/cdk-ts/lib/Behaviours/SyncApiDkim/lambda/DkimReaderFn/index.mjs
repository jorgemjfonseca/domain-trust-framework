// DkimReaderFn


import * as dns from 'dns';
const dnsPromise = dns.promises;

// 👉 https://github.com/enbits/nodejs-dkim-dns-validator/blob/master/dkimValidator.js
// parses TXT record into an array
var buildItemsArray = (item) => {
  var splittedItem = item.trim().split('=');
  var itemKey = splittedItem[0];
  var itemValue = splittedItem[1];
  return { 
      'key': itemKey,
      'value': itemValue 
  };
};



export const handler = async(event) => {
    // 👉 https://nodejs.org/api/dns.html
    const hostname = event['hostname']
    return dnsPromise
        .resolveTxt(hostname)
        .then((txt) => {
            var dkimData = txt.join().split(';');
            var itemsArray = dkimData.map(buildItemsArray);
            
            let ret = 'NOT FOUND!'
            itemsArray.forEach((x) => { 
                if (x['key'] == 'p') {
                    ret = x['value'].replace(',', '');
                }
            });
            return ret;
        });
    
};

/*
{
    "hostname": "dtfw._domainkey.38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
}
*/