Sample Certificates
====================

A set of sample certificates uses for testing a self-signed PKI scheme with a root an intermediate authority.

The two chains are:

```
ca.crt -> ia.crt -> master.crt
ca.crt -> ia.crt -> outstation.crt
```

Thus each side (master and outstation), should be able to verify each other using only ca.crt, their own private key,
and the certificate chain presented by the other side.

The certificates and keys were generated using the guide [here](http://blog.didierstevens.com/2008/12/30/howto-make-your-own-cert-with-openssl/).

This [guide](http://developer-should-know.tumblr.com/post/127063737582/how-to-create-your-own-pki-with-openssl) includes the magic incantation necessary to get the proper v3 extensions into the intermediate certificate to give it authority priveledges.

Verifying Certificates
=======================

Certificate chains for the master and outstation were produced as follows:

```
> cat ia.crt outstation.crt > ia_outstation_chain.pem
> cat ia.crt master.crt > ia_master_chain.pem
```

They can be verified using openssl:

```
>openssl verify -CAfile ca.crt ia_outstation_chain.pem
ia_outstation_chain.pem: OK
```

These certificate chains are presented by one side to the other during the SSL handshake and are verified using only the CA root certificate.
