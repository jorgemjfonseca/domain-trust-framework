
openssl enc -d -A -base64 -in signature.txt -out signature.sha1 
openssl dgst -sha256 -verify public.pem -signature signature.sha1 myfile.txt
rm via-openssl/signature.sha1