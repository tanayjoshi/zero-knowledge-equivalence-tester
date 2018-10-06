Zero-Knowledge Equality Tester

How to Use: Run the server side script on one terminal, and run two client side scripts on two other terminals. If both the clients run the same code (i.e. with the same values, [5 here]), the server window will show Equal, and return the encrypted version of the same to the clients. Use different values for the clients, and the server will show Not Equal.

Scenario: Suppose two parties need to check/compare their values (e.g. comparing each other's net worth) without letting the other party know about it. Thus, the only answers they need to know are whether their values are equal or not without them (or anyone else) actually knowing what their values are.

Approach: We use a server that creates its RSA keypair and publishes its public key for the clients to use. The idea is that the clients will hash and then encrypt their values and send it over to the server that will decrypt and check for equality. However, we don't want the server to know their values (hence, zero-knowledge). So, the server creates a pair of nonce, and sends one to each client. The client hashes and then encrypts their values with the nonce, the server decrypts that, and then multiplies that value with the opposite nonce. If the values are equal (V(a) == V(b)), we get V(a)*non(a)*non(b) for both clients, and the server outputs YES, else NO.

Improvements: We can add an extra layer of security for nonces by introducing client RSA keypairs as well. But for simplicity, we have skipped that here.

Alternatives: We can use homomorphic encryption instead. That is a much easier approach, since the server just has to perform a subtraction operation on both the encrypted client values (since the encryption scheme is homomorphic), and if the decryption of the result is 0, the values are equal. However, the Paillier Homomorphic Cryptosystem doesn't support negative values, which is why this approach won't always work currently. However, once negative values are supported, this should be the go-to method.
