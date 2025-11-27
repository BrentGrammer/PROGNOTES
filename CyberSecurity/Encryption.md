# Encryption

## Symmetric Encryption

- uses a secret key that it used to encrypt a token with AES (Advanced Encrytion Standard)
- The same key is used to both encrypt and decrypt a token
  - Normally used on server that both encrypts/decrypts JWT tokens for example.
- Faster than asymmetric encryption
- Uses only one key and that key must be shared between the two parties (client and server for ex.)
  - This is vulnerable to HTTP Man in the Middle attacks because the server must share the key over the wire with the client.

```javascript
const aes256 = require("aes256");

const key = "special-key-1";
const otherKey = "special-key-2";

const plaintext = "My unencrypted text";

const encrypted = aes256.encrypt(key, plaintext);
console.log("Encrypted: ", encrypted);

const decrypted = aes256.decrypt(key, encrypted);
console.log("Decrypted: ", decrypted);

// uses another key so decrypted does not produce original text
const failedDecrypted = aes256.decrypt(otherKey, encrypted);
console.log("Failed decrypted: ", failedDecrypted);
```

## Asymmetric Encryption (Public key Encryption)

- A public key is distributed and used to encrypt data, that data can only be decrypted using the public and private key (which only the owner possesses)
- Relies on two keys to encrypt and decrypt messages
  - a pair of keys - a Public Key and a Private Key
  - Keys are mathematically bound such that if you encrypt a message using the public key, that message can only be decrypted using the Private key.
  - Anyone can see the public key, but only the server has the private key associated with that public key
- Used when something needs to be encrypted on one machine (i.e. a server) and it needs to be decrypted on another (i.e. a client machine)
  - Private key stays on the server and the public key is used by client to decrypt the data.

## HTTPS

- Https is an extension of HTTP that runs on top of TLS (Transport Layer Security which is a security protocol)
  - Http traffic is encrypted using TLS
- SSL: Secure Sockets Layer
  - a precedent protocol prior to TLS

### Procedure

- Full walkthrough of process in [video](https://www.algoexpert.io/systems/fundamentals/security-and-https) at timestamp 33:34

- When client/server establishes a connection and a TLS handshake is initiated.
  - Client sends to the server a client hello (chello), a random string of bytes
  - Server responds to chello with a Server Hello (also a random string of bytes the server generates), and also sends it's SSL certificate (containing a public key).
    - In the SSL certificate is a public key coming from the public/private key pair that the server has.
- Client receives server hello and certificate and generates another random sequence of bytes called the pre-master secret. Client encrypts this premaster secret with the public key from the ssl cert and sends it to the server.
- The server decrypts the premaster secret from the client with the private key
  - normally the server is the only entity that has the private key associated with the public key sent.
- The client and server both have access to the client hello, the server hello and the premaster secret.
  - session keys are generated using these 3 things (usually 4 session keys).
  - This is effectively generating a logical symmetric encryption key. They key is only used during the session
    - The communication for the remainder of the session uses that symmetric key (the four session keys) which now only they have access to.
    - Once the session is over, the key is thrown away and not used again.
- There is a final "finished" message sent using the session keys sent at the end of the TLS handshake process. If everything is good with the keys then a secure session is established, otherwise the TLS handshake fails.

### SSL Certificates

- If the server sends the public key over the wire, a Man in the Middle attack could get the public key, use it to decrypt the premaster secret and use it to send back to the server.
- how can the client ensure that the public key sent from a server actually belongs to that server? That the server is actually who they claim they are?
- SSL Certs are granted by a trusted third party called a Certificate Authority
  - The community has agreed that this entity is trustworthy
  - They give out SSL Certs to parties that own servers
  - The cert is a digital item that a CA has signed with it's own private key and serves to assert that the server is who they say they are.
  - The cert contains the public key (and usually these public/private key pairs are given to the server by the Certificate Authority) and the name of the entity that owns the key pair (i.e. the entity that owns the server) and an assurance from the CA that the public key belongs to this server and the cert proves that the server is who they say they are.
  - The cert will be signed by a private key from the CA and the client will use the public key of the CA to verify the certificate.
- Because CAs are well known trusted entities, most browsers have the public keys of all the major Certificate Authorities stored in them so that it can easily verify all the SSL certs that will be received from various servers.

### What is a Digital Signature?

- A Digital Signature is an encrypted message digest (a hash like md5, sha1, etc.)
- `gpg` (GNU Privacy Guard) is industry standard and newer than `pgp`
- A private key is used to encrypt a digital signature and a public key can be used to verify the signature
  - Public keys for verifying digital signatures can be retrieved from well-reputed repositories such as mit.edu, for example
- The public key verification is the first step, but the key used should also be confirmed as belonging to a trusted entity. It should be matched to a list of trusted entities/keys provided by the service or software company you are verifying.
- see [Video](https://www.youtube.com/watch?v=rElJIPRw5iM) around timestamp 27:30

### Digitally Signing documents

- Bob produces a hash of some data (this does not involve a public or private key)
- Bob uses his private key to encrypt the hash (this is the signature)
- You use Bob's public key to decrypt the signature obtaining the original hash for the data
- You run the same hash function bob used over the data and verify that the hash output matches the decrypted hash obtained from the signature

So the reason this guarantees that Bob sent this data is that if you decrypt the hash with Bob's public key (which is linked/associated with his private key), then the hash you get from decryption is guaranteed to be the hash that Bob started with, encrypted and sent with the data as it's signature.

If the hash that you produce from the data does not match, then that means:
The data was altered by someone other than Bob - it is not the original data that was signed
