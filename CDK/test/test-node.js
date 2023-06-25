// Importing Required Modules
import * as crypto from 'crypto';
import * as buffer from 'buffer';
import * as fs from 'fs';

const create = () => {
    // Creating a private key
    const { privateKey, publicKey } = 
        crypto.generateKeyPairSync('rsa', { 
            modulusLength: 2048,
            publicKeyEncoding: {
                type: "pkcs1",
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


const load = () => {
    return {
        "privateKey": "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA85hH88OB1zSosW6DDdHD3xQKzwfUrFUIGy7ZwfC5VexfVlux\nv6zbu5E5cSoZP/dAyVVzR/ERlBCGZJ3zMoltIcP8wfdekxHFm7dIetptbLJNTpwA\nTueNQfVPgvnP5P4GM6lhp44y8nx/K55xJ0wW+4K3MlbNybotsUK5EAYmPVaI5DHC\nulHZRDFbofvNOiQpL74we361i27N7ZvHaWpRWEDjxRAyuB7s9TUE1omua6AMWZTl\nMU90LwHQsm8/evW7TyNlQe4VZHzFiO6cM8WN8n+wXB7nvxk1cZAnSkfNmTM2gb31\nxwI5/kUIvo0bPT07ExAYDl5mfp/o1GjHQtSclQIDAQABAoIBABwm3znmwFy0s0I+\nOVshgPeJA27Fwuhfs14g3f2x6llpxeLfGf3C5moY8ICJkv13f79E5tvLmnJ4Lm/2\naSLQCxK56b4o7n8ksKe8WN4J3FeRi6moEckMraCPzy6d3E7kpKbXzndk0bKAfNn3\np7AY9RcAFlf0/DdyEtHHmkelzkmMOu5K8oOlFJcQ0c4AkWvMQsIDBgnnAscMlg+w\nI2b7tfb7cym1N3wZcjMWN7Um8lDPd+jGDK9671hsyocKCftVzhw0qddwD5dTTgwJ\nP28joGr7EmmqCOAs32wJYs/aqL51I2ivlNF+NUBGsTR+oK045JTzFgQautIelF5C\n796p/EkCgYEA9KW3fDL3JbRNDd6++a/g/7wPSST5jQl0xWDyzvJoxhmcy/ddnEkZ\n1+GK29QCRh8zROFITRA0ptYprhvFR6t/baUmJ1wvTPd8JfBjvjjChCTn2sXm1Dq8\nyuphaF3eBxf+C2qMJdI7aVMQAOhxJ+K1Us8kCKEtbUTu8kU+Z6hCbC8CgYEA/uYP\ntgxWKg8ztDdLLUzTMrQuQn+nI0zutOtcRpJ7Qkf9UdUe6NxdW39njDMtuHrfigN9\nA4+knCf3EEZWHCHw4V50SIHWEe1pW0ZddUFqNduJL4l+xGsWVDB+FEKNlUEgjg/+\n2+KOv/SOAmNl7sMN9s34zdCJog+Hgg56rWys/nsCgYEAvv5RDOlNAWaNcXKgbZXd\ndkl/NX9kQ7NKMn3Jkb62BVIhkyr/Le/z+RHfslcFn3DkObYXF/K66DTyPTb5AUbm\nKNdxvfC+DLx5c7UEaZEuarPVPnqaBr4EffYVLcF6gNc+QfNgjnZeY4+xQsQ08wqO\nvKNyYjpSmKfkU8ezPIGjuYkCgYEAqKPPGzOYQiVioMXAYA0m4bHhtS89hhZdC6d3\nml1JXTXBvEVTON6qiWGGQXSOuDHa+TWLnTKIxqOOSt8uE1jFRGW4a0wzNBMtlCy+\nolgQC+feIGxISW1MDZEzqPXLNEctYa/lftaqeQc0eRIIG2pDL9lf1dM1a9n4Xix0\nL47p+UcCgYBRcuSscDR2xLuIvxw0kcZlKkQ4v2F5CO/eAbDI4cPAyG3ni8sXJDsT\ndw3FEDHD3WphBOUJE98PDt+ks81lAvsem51nhmBURMawEH9XyYHPn7GDFYWgcIu5\nGjTermRZnH19TpgmoP9ELTgcAToAuHR7MTH5nwr48YgXlxGUdDJE7A==\n-----END RSA PRIVATE KEY-----",
        "publicKey": "-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEA85hH88OB1zSosW6DDdHD3xQKzwfUrFUIGy7ZwfC5VexfVluxv6zb\nu5E5cSoZP/dAyVVzR/ERlBCGZJ3zMoltIcP8wfdekxHFm7dIetptbLJNTpwATueN\nQfVPgvnP5P4GM6lhp44y8nx/K55xJ0wW+4K3MlbNybotsUK5EAYmPVaI5DHCulHZ\nRDFbofvNOiQpL74we361i27N7ZvHaWpRWEDjxRAyuB7s9TUE1omua6AMWZTlMU90\nLwHQsm8/evW7TyNlQe4VZHzFiO6cM8WN8n+wXB7nvxk1cZAnSkfNmTM2gb31xwI5\n/kUIvo0bPT07ExAYDl5mfp/o1GjHQtSclQIDAQAB\n-----END RSA PUBLIC KEY-----"
    }
}

export const handler = (event) => {
        
    //const keys = create();    
    const keys = load();
    const privateKey2 = keys['privateKey'];
    const publicKey2 = keys['publicKey'];
    
    
    // Using Hashing Algorithm
    const algorithm = "SHA256";
     
    // Converting string to buffer
    //let text = '{"Header":{"Correlation":"bb37d258-015c-497e-8a67-50bf244a9299","Timestamp":"2023-06-24T23:08:24.550719Z","To":"105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org","Subject":"AnyMethod","Code":"dtfw.org/msg","Version":"1","From":"105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org"},"Body":{}}'
    let text = 'bacon';
    let data = Buffer.from(text);
         
    // Sign the data and returned signature in buffer
    let signature = crypto.sign(algorithm, data, privateKey2);

    // Verifying signature using crypto.verify() function
    let isVerified = crypto.verify(algorithm, data, publicKey2, signature);

    // Printing the result
    return {
        // openssl dgst -sha512  -verify public.pem  -signature sha256.sign myfile.txt
        isVerified,
        algorithm,
        hash1: crypto.createHash('sha256').update(text).digest('base64'),
        hash2: Buffer.from(crypto.createHash('sha256').update(text).digest('hex')).toString('base64'),
        // openssl dgst -sha256 myfile.txt
        hash3: crypto.createHash('sha256').update(text).digest('hex'),
        // openssl dgst -sha256 -sign private.pem -out sha256.bin  myfile.txt && openssl base64 -in sha256.bin -out sha256.sign
        signature: signature.toString("base64"),
        privateKey: privateKey2,
        publicKey: publicKey2,
    };


};

let ret = handler({});
console.log(ret);
console.log(ret['privateKey']);

fs.writeFileSync('private.pem', ret['privateKey']);