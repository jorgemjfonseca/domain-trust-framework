import * as crypto from 'crypto';

const create = () => {
    // Creating a private key
    const { privateKey, publicKey } = 
        crypto.generateKeyPairSync('rsa', { 
            modulusLength: 2048,
            publicKeyEncoding: {
                type: "spki",
                format: "pem",
            },
            privateKeyEncoding: {
                type: "pkcs1",
                format: "pem",
            }
        });
        
        
    return {
        privateKey,
        publicKey
    }
}


export const handler = async(event) => {
    return create();    
};