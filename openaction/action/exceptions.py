# -*- coding: utf-8 -*-

from django.core import exceptions
from action import const as action_const

class ParanoidException(exceptions.PermissionDenied):
    
    def __unicode__(self):
        return u"Oops, qualcosa è andato storto, l'operazione che si sta provando a eseguire non è consentita."

class ActionInvalidStatusException(exceptions.PermissionDenied):
    
    def __init__(self, status):
        if status == action_const.ACTION_STATUS_DRAFT:
            self._status = u"in stato bozza"
        elif status == action_const.ACTION_STATUS_DELETED:
            self._status = u"stata cancellata"
        elif status == action_const.ACTION_STATUS_CLOSED:
            self._status = u"stata chiusa"
        elif status == action_const.ACTION_STATUS_ACTIVE:
            self._status = u"già attiva"
        elif status == action_const.ACTION_STATUS_READY:
            self._status = u"già pronta per essere votata"

class VoteActionInvalidStatusException(ActionInvalidStatusException):
    
    def __unicode__(self):
        return u"L'azione non può essere votata perchè è %s." % self._status

class CommentActionInvalidStatusException(ActionInvalidStatusException):
    
    def __unicode__(self):
        return u"L'azione non può essere commentata perchè è %s." % self._status

class EditActionInvalidStatusException(ActionInvalidStatusException):
    
    def __unicode__(self):
        return u"L'azione non può essere modificata perchè è %s." % self._status

class FollowActionInvalidStatusException(ActionInvalidStatusException):
    
    def __unicode__(self):
        return u"L'azione non può essere seguita perchè è %s." % self._status

class BlogpostActionInvalidStatusException(ActionInvalidStatusException):
    
    def __unicode__(self):
        return u"Non è possibile aggiungere un articolo al blog dell'azione perchè questa è %s." % self._status

class InvalidReferralError(exceptions.PermissionDenied):
    
    def __unicode__(self):
        return u"Un utente non può avere se stesso come referente del voto."

class InvalidReferralTokenException(exceptions.PermissionDenied):
    
    def __unicode__(self):
        return u"All'utente non risulta associato nessun referente per il voto."

class UserCannotVoteTwice(exceptions.PermissionDenied):
   
    def __init__(self, user, post):
        self.user = user
        if post.post_type == 'question':
            self._post_type = "questa azione"
        elif post.post_type == 'answer':
            self._post_type = "questa risposta"
        elif post.post_type == 'comment':
            self._post_type = "questo commento"

    def __unicode__(self):
        return u"L'utente %s ha già votato %s." % (self.user,
            self._post_type)
        
class UserCannotVote(UserCannotVoteTwice):

    def __unicode__(self):
        return u"L'utente %s non può votare %s." % (self.user,
            self._post_type)

class VoteOnUnauthorizedCommentException(exceptions.PermissionDenied):
    
    def __unicode__(self):
        return u"L'utente sta tentando di votare un commento non autorizzato" 

class UserIsNotActionOwnerException(exceptions.PermissionDenied):

    def __init__(self, user, action):
        self.user = user
        self.action = action

    def __unicode__(self):
        return u"L'utente %s non può modificare il contenuto dell'azione %s poichè non ne è l'autore." % (self.user, self.action)
 
class UserIsNotActionReferralException(UserIsNotActionOwnerException):

    def __unicode__(self):
        return u"L'utente %s non può aggiungere un articolo nel blog dell'azione %s poichè non ne è né autore né moderatore." % (self.user, self.action)

class UserCannotRemoveActionModeratorException(exceptions.PermissionDenied):

    def __init__(self, user, moderator, action):
        self.user = user
        self.moderator = moderator
        sefl.action = action

    def __unicode__(self):
        return u"L'utente %s non può rimuovere il moderatore %s dall'azione %s perchè non ne è il proprietrario." % (self.user, self.moderator, self.action)

class ThresholdNotComputableException(exceptions.PermissionDenied):

    def __init__(self, action):
        self.action = action

    def __unicode__(self):
        return u"Non è possibile calcolare la soglia di adesioni oltre la quale l'azione %s diviene attiva" % self.action

#class InvalidPoliticianListError(exceptions.ValidationError):
#
#    def __init__(self, politicians):
#        self.politicians = politicians
#
#    def __unicode__(self):
#        return u"Non tutti i politici sono stati recuperati. Sono rimasti fuori i politici con id: %s" % self.politicians
#
#class InvalidGeonameListError(exceptions.ValidationError):
#
#    def __init__(self, geonames):
#        self.geonames = geonames
#
#    def __unicode__(self):
#        return u"Non tutti i luoghi sono stati recuperati. Sono rimasti fuori i luoghi con id: %s" % self.geonames
