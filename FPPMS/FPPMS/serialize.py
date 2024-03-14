from django.db.models import fields
from rest_framework import serializers
from FPPMS.models import Proposalmodel

class Proposalserialize(serializers.ModelSerializer):
    class Meta:
        model=Proposalmodel
        fields="__all__"