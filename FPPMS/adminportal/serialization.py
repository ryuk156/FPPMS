from django.db.models import fields
from rest_framework import serializers
from FPPMS.models import Proposalmodel

class AdminSerializationClass(serializers.ModelSerializer):
    assignedTo = serializers.SerializerMethodField()

    class Meta:
        model = Proposalmodel
        fields = '__all__'

    def get_assignedTo(self, obj):
        if obj.assignedTo:
            return obj.assignedTo.username
        else:
            return None
        
