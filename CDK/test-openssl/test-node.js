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


const load = () => {
    return {
        "privateKey": "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA85hH88OB1zSosW6DDdHD3xQKzwfUrFUIGy7ZwfC5VexfVlux\nv6zbu5E5cSoZP/dAyVVzR/ERlBCGZJ3zMoltIcP8wfdekxHFm7dIetptbLJNTpwA\nTueNQfVPgvnP5P4GM6lhp44y8nx/K55xJ0wW+4K3MlbNybotsUK5EAYmPVaI5DHC\nulHZRDFbofvNOiQpL74we361i27N7ZvHaWpRWEDjxRAyuB7s9TUE1omua6AMWZTl\nMU90LwHQsm8/evW7TyNlQe4VZHzFiO6cM8WN8n+wXB7nvxk1cZAnSkfNmTM2gb31\nxwI5/kUIvo0bPT07ExAYDl5mfp/o1GjHQtSclQIDAQABAoIBABwm3znmwFy0s0I+\nOVshgPeJA27Fwuhfs14g3f2x6llpxeLfGf3C5moY8ICJkv13f79E5tvLmnJ4Lm/2\naSLQCxK56b4o7n8ksKe8WN4J3FeRi6moEckMraCPzy6d3E7kpKbXzndk0bKAfNn3\np7AY9RcAFlf0/DdyEtHHmkelzkmMOu5K8oOlFJcQ0c4AkWvMQsIDBgnnAscMlg+w\nI2b7tfb7cym1N3wZcjMWN7Um8lDPd+jGDK9671hsyocKCftVzhw0qddwD5dTTgwJ\nP28joGr7EmmqCOAs32wJYs/aqL51I2ivlNF+NUBGsTR+oK045JTzFgQautIelF5C\n796p/EkCgYEA9KW3fDL3JbRNDd6++a/g/7wPSST5jQl0xWDyzvJoxhmcy/ddnEkZ\n1+GK29QCRh8zROFITRA0ptYprhvFR6t/baUmJ1wvTPd8JfBjvjjChCTn2sXm1Dq8\nyuphaF3eBxf+C2qMJdI7aVMQAOhxJ+K1Us8kCKEtbUTu8kU+Z6hCbC8CgYEA/uYP\ntgxWKg8ztDdLLUzTMrQuQn+nI0zutOtcRpJ7Qkf9UdUe6NxdW39njDMtuHrfigN9\nA4+knCf3EEZWHCHw4V50SIHWEe1pW0ZddUFqNduJL4l+xGsWVDB+FEKNlUEgjg/+\n2+KOv/SOAmNl7sMN9s34zdCJog+Hgg56rWys/nsCgYEAvv5RDOlNAWaNcXKgbZXd\ndkl/NX9kQ7NKMn3Jkb62BVIhkyr/Le/z+RHfslcFn3DkObYXF/K66DTyPTb5AUbm\nKNdxvfC+DLx5c7UEaZEuarPVPnqaBr4EffYVLcF6gNc+QfNgjnZeY4+xQsQ08wqO\nvKNyYjpSmKfkU8ezPIGjuYkCgYEAqKPPGzOYQiVioMXAYA0m4bHhtS89hhZdC6d3\nml1JXTXBvEVTON6qiWGGQXSOuDHa+TWLnTKIxqOOSt8uE1jFRGW4a0wzNBMtlCy+\nolgQC+feIGxISW1MDZEzqPXLNEctYa/lftaqeQc0eRIIG2pDL9lf1dM1a9n4Xix0\nL47p+UcCgYBRcuSscDR2xLuIvxw0kcZlKkQ4v2F5CO/eAbDI4cPAyG3ni8sXJDsT\ndw3FEDHD3WphBOUJE98PDt+ks81lAvsem51nhmBURMawEH9XyYHPn7GDFYWgcIu5\nGjTermRZnH19TpgmoP9ELTgcAToAuHR7MTH5nwr48YgXlxGUdDJE7A==\n-----END RSA PRIVATE KEY-----",
        "publicKey": "-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEA85hH88OB1zSosW6DDdHD3xQKzwfUrFUIGy7ZwfC5VexfVluxv6zb\nu5E5cSoZP/dAyVVzR/ERlBCGZJ3zMoltIcP8wfdekxHFm7dIetptbLJNTpwATueN\nQfVPgvnP5P4GM6lhp44y8nx/K55xJ0wW+4K3MlbNybotsUK5EAYmPVaI5DHCulHZ\nRDFbofvNOiQpL74we361i27N7ZvHaWpRWEDjxRAyuB7s9TUE1omua6AMWZTlMU90\nLwHQsm8/evW7TyNlQe4VZHzFiO6cM8WN8n+wXB7nvxk1cZAnSkfNmTM2gb31xwI5\n/kUIvo0bPT07ExAYDl5mfp/o1GjHQtSclQIDAQAB\n-----END RSA PUBLIC KEY-----"
    }
}

export const handler = (event) => {
        
    const keys = create();    
    //const keys = load();
    const privateKey2 = keys['privateKey'] + '';
    const publicKey2 = keys['publicKey'] + '';
    
    
    // Using Hashing Algorithm
    const algorithm = "SHA256";
     
    // Converting string to buffer
    let text = '{"Header":{"Correlation":"bb37d258-015c-497e-8a67-50bf244a9299","Timestamp":"2023-06-24T23:08:24.550719Z","To":"105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org","Subject":"AnyMethod","Code":"dtfw.org/msg","Version":"1","From":"105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org"},"Body":{}}'
    //let text = 'bacon';
         
    // Sign the data and returned signature in buffer
    let originalSign = crypto.sign(algorithm, Buffer.from(text), privateKey2 + '');
    let signature = originalSign.toString("base64") + '';
    let loadedSign = Buffer.from(signature, 'base64');

    // Verifying signature using crypto.verify() function
    let isVerified = crypto.verify(algorithm, Buffer.from(text), publicKey2 + '', loadedSign);

    // Printing the result
    return {
        text,
        algorithm,
        privateKey: privateKey2,
        publicKey: publicKey2,
        /*
        less myfile.txt | openssl dgst -sha256 >> hash.txt
        */
        hash: crypto.createHash('sha256').update(text).digest('hex'),
        /* 
        openssl dgst -sha256 -sign private.pem -out signature.sha1 myfile.txt && \
        openssl base64 -in signature.sha1 -out signature.txt
        */
        signature: signature,
        /*
        openssl enc -d -A -base64 -in signature.txt -out signature.sha1 && \
        openssl dgst -sha256 -verify public.pem -signature signature.sha1 myfile.txt
        */
        isVerified
    };


};

let ret = handler({});
console.log(ret);
//console.log(ret['privateKey']);

let f1 = 'via-node/';
fs.writeFileSync(f1+'node-logs.json', JSON.stringify(ret, null, 4));
fs.writeFileSync(f1+'private.pem', ret['privateKey']);
fs.writeFileSync(f1+'public.pem', ret['publicKey']);
fs.writeFileSync(f1+'signature.txt', ret['signature']);
fs.writeFileSync(f1+'hash.txt', ret['hash']);
fs.writeFileSync(f1+'myfile.txt', ret['text']);

let f2 = 'via-openssl/';
fs.writeFileSync(f1+'test.sh', `
echo == NEXT STEPS ========== 
mkdir via-openssl 
echo == VALIDATE THE SIGNATURE, EXPECT "Verified OK" ========== 
openssl enc -d -A -base64 -in ${f1}signature.txt -out ${f2}signature.sha1 
openssl dgst -sha256 -verify ${f1}public.pem -signature ${f2}signature.sha1 ${f1}myfile.txt
rm ${f2}signature.sha1
echo == CREATE THE SIGNATURE, EXPECT EMPTY DIFF ==========
openssl dgst -sha256 -sign ${f1}private.pem -out ${f2}signature.sha1 ${f1}myfile.txt
openssl base64 -A -in ${f2}signature.sha1 -out ${f2}signature.txt
rm ${f2}signature.sha1
diff ${f1}signature.txt ${f2}signature.txt
echo == CREATE THE HASH, EXPECT EMPTY DIFF ==========
cat ${f1}myfile.txt | openssl dgst -sha256 > ${f2}hash.txt 
truncate -s -1 ${f2}hash.txt 
diff ${f1}hash.txt ${f2}hash.txt
`);

console.log(`run 
chmod +x ${f1}test.sh && ./${f1}test.sh`);