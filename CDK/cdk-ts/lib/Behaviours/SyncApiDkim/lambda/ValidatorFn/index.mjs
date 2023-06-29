//ValidatorFn

import * as crypto from 'crypto';

export const handler = (event) => {
    console.info("EVENT\n" + JSON.stringify(event, null, 2))

    const text = event['text']
    
    const publicKey2 = event['publicKey'] + '';
    if (!publicKey2.startswith('--')) {
        signature = 
            '-----BEGIN PUBLIC KEY-----\n' +
            publicKey2.toString( 'base64' ) +
            '\n-----END PUBLIC KEY-----'
    }
    
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
REQUEST: 
{
    "text": "{\"Header\":{\"Correlation\":\"b8535320-050b-45a1-8417-8e4ba4759091\",\"Timestamp\":\"2023-06-29T01:12:47.657234Z\",\"To\":\"38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org\",\"Subject\":\"AnyMethod\",\"Code\":\"dtfw.org/msg\",\"Version\":\"1\",\"From\":\"38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org\"},\"Body\":{}}",
    "publicKey": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAylaGuH5Mteyy/JMaQyEjBsoU6naz+pkWbNIetfJuP7FABfUl2RBwqN8IkeqAVv1j13YEvLmjBVbkDso1kXHH8y4X/AQts4PJZKKXjZMiAlzC+i6lPnszKx5+h2Od8Rm3066yNYEGfbJNRAwwqGDqwUjpPqrT,FBM+UnOBjeEC+/AO+O3n4OaJPPX8W69xqMmsUjfzr+DozylrlLIJsSLcIjNAVjeKKSzwFlimtYIQXaY3DWSt/uQ6jU978eRN9uuNfv4ZoZPZxvdRovEB8fGDx7GGGutMpcKYFx6FRxKDhrjLxU/MLWfPM7cMxA+hflnv/Sxp+qP/Gbst2f0zQ2P2YQIDAQAB",
    "signature": "gV+QmcHHINHjcloL3en1z1ttwDlqbAsmkk/Oo/2CAa0UNRsp4VCBJ09swU9jvoSu41kPtnPX8/6Mobnf5P9GHcebZiFMfzFVN6WPEFCXqpFMJeoqQe6BdCBY70AleD37wQHTkM0ia/+QXNo49OsllUZBLhNlDFGfNVefAmoObfWHj0Io4H3oR2ZqpNrmsw2FVANbtaAol+lDrWXCm5SJ2FVzWnoHFcnv3h/4HvL0kLbS8xAMV9xsgY4/TtVKzg/6wQgRJug8mrw7fVuut+YX+VwAxzY66CEgDB3DRXI/sU/oJt6bh4+Ucxkqcy2asigwn8nveDtDNFpK3CsV9Rczbg=="
}

RESPONSE: 
{
    "hash": "",
    "isVerified": True
}
*/