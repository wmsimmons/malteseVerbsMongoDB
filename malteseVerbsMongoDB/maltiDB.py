#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import pymongo
from pymongo import MongoClient

# coding= utf8


#connect to pymongo
client = MongoClient("localhost", 27017)
db = client.maltiVerbConjugator

def connect_maltidb():
    """connects to the maltiVerbConjugator database"""
    connection = MongoClient()
    db = connection.maltiVerbConjugator
    maltiverb_db = db.maltiVerbConjugator
    return maltiverb_db

"""Feed the root of the verb, and function will ask you for each form of the verb
from the first person singular and plurals to imperative forms and inserts the results
as a document in the database"""

def vinsert(root):
    #present forms
    first_sing_present = input("Type the first person singular form: ")
    second_sing_present = input("Type the second person singular form: ")
    third_sing_he_present = input("Type the third person singular form for 'he': ")
    third_sing_she_present = input("Type the third person singular form for 'she': ")

    first_plural_present = input("Type the first person plural present form: ")
    second_plural_present = input("Type the second person plural present form: ")
    third_plural_present = input("Type the third person plural present form: ")

    #past forms
    first_sing_past = input("Type the first person singular past form: ")
    second_sing_past = input("Type the second person singular past form: ")
    third_sing_he_past = input("Type the third person singular past form for 'he': ")
    third_sing_she_past = input("Type the third person singular past form for 'she': ")

    first_plural_past = input("Type the first person plural past form: ")
    second_plural_past = input("Type the second person plural past form: ")
    third_plural_past = input("Type the third person plural past form: ")

    #imperative command forms
    imperative_sing = input("Type the imperative singular form: ")
    imperative_plural = input("Type the imperative plural form: ")
    
    #how to structure mongo collection to work with verb tenses,
    #pronouns and verb roots
    verb_conj = {
    "_id":  root, 
    "verbRoot": root,
    "verbForms":{
    "presentFutureForms": {
        "singularForms": {
            "jiena":  first_sing_present,
            "int": second_sing_present,
            "hu_huwa":  third_sing_he_present,
            "hi_hija":  third_sing_she_present 
    },
        "pluralForms": {
            "aħna": first_plural_present,
            "intom": second_plural_present,
            "huma": third_plural_present
        }},
    "pastTenseForms": {
    
        "singularForms": {
            "jiena": first_sing_past,
            "int": second_sing_past,
            "hu_huwa": third_sing_he_past,
            "hi_hija": third_sing_she_past 
        },
            "pluralForms": {
            "aħna": first_plural_past,
            "intom": second_plural_past,
            "huma": third_plural_past
        }},
    "imperativeForms": {
            "singular": imperative_sing,
            "plural": imperative_plural 
            } 
           }};

    #logic that inserts "null" in an entry if the input entered is blank
    
    print(verb_conj)
    confirmation = input("Are you sure this verb" + ' + root + ' +  "is conjugated correctly? Write 'yes' or 'y' to confirm. ")
    if confirmation == 'yes' or 'y':
        #inserts the document and prints the result
        maltidb = connect_maltidb()
        inserted_entry = maltidb.insert_one(verb_conj)
        return inserted_entry
    elif confirmation == 'n' or 'no':
        pass
    
def vdel(root):
    """deletes the verb based off root from db"""
    maltidb = connect_maltidb()
    findEntry = maltidb.find({"_id": root})
    entry = {"_id": root}
    for rootForm in findEntry:
        print(rootForm)

        confirmation = input("Are you sure that you want to delete this document? Type 'yes' or 'no' to confirm: ")
        if confirmation == 'yes' or 'y':
            #removes entry from db and returns what was deleted
            delResult = maltidb.delete_one(entry)
            print(delResult.deleted_count)
            return delResult
        elif confirmation == 'no' or 'n':
            pass
            
def vfind():
  """finds a specific verb based on root fed to the input"""
  maltidb = connect_maltidb()
  root = input("Which verb are you looking for? Ikteb il-feghel hawn: ")
  entry = {"_id": root}
  findEntry = maltidb.find_one(entry)

  print(findEntry)

def vedit(root):
    #ex: ("rikeb", {'presentTenseForm.singularForms.hu_huwa':'jirkeb', 'pastTenseForms.pluralForms.aħna':'rkibna'})
    maltidb = connect_maltidb()
    entry = {"_id": root}
    findEntry = maltidb.find_one(root)
    for rootForm in findEntry:
        print(rootForm)

    confirmation = input("Are you sure that you want to edit this verb? " + root + ": ")
    if confirmation == 'yes' or 'y':
        updatedVForm = input("X'trid tbiddel din il-feghel? Please use {'presentTenseForm.singularForms.hu_huwa':'syntax'}: ")
        for form in updatedVForm:
            result = maltidb.update_one(entry, {"$set": updatedVForm}, upsert=False)
        print(result.modified_count)
    else:
        pass
    return result
    
