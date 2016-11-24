# Knogget

Knogget will records any piece of knowledge inputed in text form and do interesting things with them (hopefully)

At the moment, this is just a draft / study.  
This repo will focus on the backend work.  
Ultimatly, I would like it to be a good example of service based application developed in Python. So,I welcome any feedback.


## Description
A knogget is a piece of text (probably in markdown format)  
Following some conventions or using small Domain-Specific Languages the user can describe different types of "objects"  
The front end will be able to switch between text and graphical representation of those objects.  
The backend will extract objects that it regnonize and index / store them for later use.

Example of object type : recipe  
It will be extracted from MD code syntax
```
```recipe

<recipe description using DSL>

``` .
```


From the recipe, the BE will be
* indexing ingredients and actions used by a recipe
* store ingredient/actions descriptions / comments

it can be used for autocompletion, recipe specific search query, requesting definition of culinary terms

It can then be linked to other services (e.g. ingredient cost scrapper/api)
