#!/usr/bin/env python
""" public_key.py
        
    Paul A. Lambert 2015
"""
__all__ = ['PublicKey', 'PublicKeyPair']

class Eon: pass # serialization stubbed for now

class PublicKey( Eon ):
    """ Public keys are assoicated with a CipherSuite that determines
        the algorithms and encodings used with the key.
    """
    def __init__( self, cipherSuite, keyValue ):
        """ New public key from point or octetstring """
        self.cipherSuite = cipherSuite
        self.group = cipherSuite.Group()
        
        if keyValue.__class__ == 'Str':
            point = cipherSuite.pub_key_from_octets( keyValue )
        elif keyValue.__class__.__name__ == 'Point' :
            point = keyValue
        else:
            raise 'bad key type'
        
        #assert self.group.is_valid( point )
        assert self.group.on_curve( point )
        self.publicKeyValue = point   # keyValue is a Point for ECC
        self.uaid = cipherSuite.hashUaid( self )
    
    def validate( self, data, signature ):
        """ Validate a signature using this public key."""
        return self.cipherSuite.validate( self.publicKeyValue, data, signature )
    
    def decrypt( self, cipherText ):
        """ Decrypts the cipherText and returns a opaque octet string """
        plainText = self.cipherSuite.pubKeyDecrypt( self.publicKeyValue, cipherText )
        return plainText
    
   
class PublicKeyPair( PublicKey ):
    """ Public keys are created using the mechanisms defined by the Cipher Suite.
    """
    def __init__( self, cipherSuite ):
        """ Create a new random key pair based on the Cipher Suite """
        self.cipherSuite = cipherSuite
        self.group = cipherSuite.Group()
        self.__secret = self.group.newAsymSecret()
        self.publicKeyValue = self.group.make_PublicKey( self.__secret )
        #publicKeyOctets = ... serailize ...       
        #self.uaid = cipherSuite.HashUaid( publicKeyOctets )
        
    def sign( self, data ):
        """ Sign data using the private key. Result is an opaque octet string.
        """
        return self.cipherSuite.sign( self, data )

    def encrypt( self, plainText ):
        """ Encrypt the plainText and returns an opaque octet string
        """
        cipherText = self.cipherSuite.pubKeyDecrypt( self.__secret, plainText )
        return cipherText        
           
           







