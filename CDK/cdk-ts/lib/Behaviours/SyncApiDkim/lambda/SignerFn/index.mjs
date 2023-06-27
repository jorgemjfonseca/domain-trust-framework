//SignerFn

import * as crypto from 'crypto';

export const handler = async(event) => {

    const privateKey2 = event['privateKey'] + '';
    const publicKey2 = event['publicKey'] + '';
    
    // Using Hashing Algorithm
    const algorithm = "SHA256";
     
    // Converting string to buffer
    let text = event['text']
         
    // Sign the data and returned signature in buffer
    let originalSign = crypto.sign(algorithm, Buffer.from(text), privateKey2 + '');
    let signature = originalSign.toString("base64") + '';
    let loadedSign = Buffer.from(signature, 'base64');

    // Verifying signature using crypto.verify() function
    let isVerified = crypto.verify(algorithm, Buffer.from(text), publicKey2 + '', loadedSign);

    // Printing the result
    return {
        hash: crypto.createHash('sha256').update(text).digest('hex'),
        signature: signature,
        isVerified
    };

};

/* REQUEST
{
    "privateKey": "...",
    "publicKey": "...",
    "text": "bla"
}
*/

/* RESPONSE
{
    "hash": "...",
    "signature": "...",
    "isVerified": true
}
*/