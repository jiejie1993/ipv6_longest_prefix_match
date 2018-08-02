# -*- coding: utf-8 -*-

class trieNode(object):
    def __init__(self):
        #initialize the trieNode 
        self.data = {}
        self.isWord = False
        
class trie(object):
    """
    creat a trie for each index in TCAM mem
    put the tire in a TCAM mem list,which 
    contains the trie and the ip_table_index 
    """
    def __init__(self):
        self.root = trieNode()
       
        
    def insert(self, word):
        """
        insert word into the trie
        type word: str
        return type: void 
        """
        if len(word) == 0:
            return
        node = self.root
        for letter in word:
            child = node.data.get(letter)
            if not child:
                node.data[letter] = trieNode()
            node = node.data[letter]
        node.isWord = True
        
    def search(self,word):
        """
        search the word in the trie 
        type word: str
        return type: str
        """
        res = ''
        temp_res = ''
        node = self.root
        for letter in word:
            child = node.data.get(letter)
            if child:
                temp_res += letter
                if child.isWord:
                    res = temp_res
                node = child
            else:
                break
        return res