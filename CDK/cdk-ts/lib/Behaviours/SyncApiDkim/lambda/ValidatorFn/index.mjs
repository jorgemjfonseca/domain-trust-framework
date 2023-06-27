//ValidatorFn

import * as crypto from 'crypto';

export const handler = (event) => {
    console.info("EVENT\n" + JSON.stringify(event, null, 2))

    const text = event['text']
    
    const publicKey2 = event['publicKey'] + '';
    
    const signature = event['signature'];
    const loadedSign = Buffer.from(signature, 'base64');
    
    // Using Hashing Algorithm
    const algorithm = "SHA256";
    
    // Verifying signature using crypto.verify() function
    let isVerified = crypto.verify(algorithm, Buffer.from(text), publicKey2 + '', loadedSign);

    // Printing the result
    return {
        hash: crypto.createHash('sha256').update(text).digest('hex'),
        isVerified
    };

};

/* 
REQUEST: {
    "text": "",
    "publicKey": "",
    "signature": ""
}
RESPONSE: {
    "hash": "",
    "isVerified": True
}
*/